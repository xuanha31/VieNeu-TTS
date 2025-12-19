"""
FastAPI Server for VieNeu-TTS
Provides REST API endpoints for text-to-speech synthesis
"""
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import soundfile as sf
import tempfile
import torch
import os
import time
import numpy as np
import yaml
from vieneu_tts import VieNeuTTS
try:
    from vieneu_tts import FastVieNeuTTS
    LMDEPLOY_AVAILABLE = True
except ImportError:
    LMDEPLOY_AVAILABLE = False
    FastVieNeuTTS = None
from utils.core_utils import split_text_into_chunks
from functools import lru_cache
import gc
import base64

# Load config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    _config = yaml.safe_load(f) or {}

BACKBONE_CONFIGS = _config.get("backbone_configs", {})
CODEC_CONFIGS = _config.get("codec_configs", {})
VOICE_SAMPLES = _config.get("voice_samples", {})
_text_settings = _config.get("text_settings", {})
MAX_CHARS_PER_CHUNK = _text_settings.get("max_chars_per_chunk", 256)

# Initialize FastAPI
app = FastAPI(
    title="VieNeu-TTS API",
    description="Vietnamese Text-to-Speech API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
tts = None
current_config = {
    "backbone": None,
    "codec": None,
    "device": None,
    "loaded": False,
    "using_lmdeploy": False
}

# Pydantic models
class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to synthesize", max_length=10000)
    voice: str = Field(default="Vĩnh (nam miền Nam)", description="Voice sample name")
    use_batch: bool = Field(default=True, description="Use batch processing if available")

class TTSCustomRequest(BaseModel):
    text: str = Field(..., description="Text to synthesize", max_length=10000)
    ref_text: str = Field(..., description="Reference text for custom voice")
    use_batch: bool = Field(default=True, description="Use batch processing if available")

class ModelLoadRequest(BaseModel):
    backbone: str = Field(default="VieNeu-TTS (GPU)", description="Backbone model name")
    codec: str = Field(default="NeuCodec (Standard)", description="Codec model name")
    device: str = Field(default="Auto", description="Device: Auto, CPU, or CUDA")
    enable_triton: bool = Field(default=True, description="Enable Triton compilation")
    max_batch_size: int = Field(default=8, ge=1, le=16, description="Max batch size")

class StatusResponse(BaseModel):
    status: str
    model_loaded: bool
    backbone: Optional[str]
    codec: Optional[str]
    device: Optional[str]
    using_lmdeploy: bool
    available_voices: List[str]

@lru_cache(maxsize=32)
def get_ref_text_cached(text_path: str) -> str:
    """Cache reference text loading"""
    with open(text_path, "r", encoding="utf-8") as f:
        return f.read()

def cleanup_gpu_memory():
    """Cleanup GPU memory"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    gc.collect()

def should_use_lmdeploy(backbone_choice: str, device_choice: str) -> bool:
    """Determine if we should use LMDeploy backend"""
    if not LMDEPLOY_AVAILABLE:
        return False
    
    if "gguf" in backbone_choice.lower():
        return False
    
    if device_choice == "Auto":
        has_gpu = torch.cuda.is_available()
    elif device_choice == "CUDA":
        has_gpu = torch.cuda.is_available()
    else:
        has_gpu = False
    
    return has_gpu

@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "VieNeu-TTS API Server",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get server status and model information"""
    return StatusResponse(
        status="running",
        model_loaded=current_config["loaded"],
        backbone=current_config["backbone"],
        codec=current_config["codec"],
        device=current_config["device"],
        using_lmdeploy=current_config["using_lmdeploy"],
        available_voices=list(VOICE_SAMPLES.keys())
    )

@app.get("/voices", response_model=dict)
async def list_voices():
    """List available voice samples"""
    voices = {}
    for name, info in VOICE_SAMPLES.items():
        voices[name] = {
            "audio_path": info["audio"],
            "text_path": info["text"]
        }
    return {"voices": voices}

@app.post("/load_model", response_model=dict)
async def load_model(request: ModelLoadRequest):
    """Load TTS model with specified configuration"""
    global tts, current_config
    
    try:
        # Cleanup before loading new model
        if current_config["loaded"] and tts is not None:
            del tts
            cleanup_gpu_memory()
        
        if request.backbone not in BACKBONE_CONFIGS:
            raise HTTPException(status_code=400, detail=f"Invalid backbone: {request.backbone}")
        if request.codec not in CODEC_CONFIGS:
            raise HTTPException(status_code=400, detail=f"Invalid codec: {request.codec}")
        
        backbone_config = BACKBONE_CONFIGS[request.backbone]
        codec_config = CODEC_CONFIGS[request.codec]
        
        use_lmdeploy = should_use_lmdeploy(request.backbone, request.device)
        
        if use_lmdeploy:
            print(f"🚀 Using LMDeploy backend")
            backbone_device = "cuda"
            codec_device = "cpu" if "ONNX" in request.codec else "cuda"
            
            tts = FastVieNeuTTS(
                backbone_repo=backbone_config["repo"],
                backbone_device=backbone_device,
                codec_repo=codec_config["repo"],
                codec_device=codec_device,
                memory_util=0.3,
                tp=1,
                enable_prefix_caching=True,
                enable_triton=request.enable_triton,
                max_batch_size=request.max_batch_size,
            )
            
            # Pre-cache voice references
            print("📝 Pre-caching voice references...")
            for voice_name, voice_info in VOICE_SAMPLES.items():
                audio_path = voice_info["audio"]
                text_path = voice_info["text"]
                if os.path.exists(audio_path) and os.path.exists(text_path):
                    ref_text = get_ref_text_cached(text_path)
                    tts.get_cached_reference(voice_name, audio_path, ref_text)
            
            current_config["using_lmdeploy"] = True
        else:
            print(f"📦 Using standard backend")
            
            if request.device == "Auto":
                if "gguf" in request.backbone.lower():
                    backbone_device = "gpu" if torch.cuda.is_available() else "cpu"
                else:
                    backbone_device = "cuda" if torch.cuda.is_available() else "cpu"
                codec_device = "cpu" if "ONNX" in request.codec else backbone_device
            else:
                backbone_device = request.device.lower()
                codec_device = "cpu" if "ONNX" in request.codec else backbone_device
            
            if "gguf" in request.backbone.lower() and backbone_device == "cuda":
                backbone_device = "gpu"
            
            tts = VieNeuTTS(
                backbone_repo=backbone_config["repo"],
                backbone_device=backbone_device,
                codec_repo=codec_config["repo"],
                codec_device=codec_device
            )
            current_config["using_lmdeploy"] = False
        
        current_config.update({
            "backbone": request.backbone,
            "codec": request.codec,
            "device": request.device,
            "loaded": True
        })
        
        return {
            "status": "success",
            "message": "Model loaded successfully",
            "backend": "LMDeploy" if use_lmdeploy else "Standard",
            "config": current_config
        }
        
    except Exception as e:
        current_config["loaded"] = False
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")

@app.post("/synthesize", response_class=FileResponse)
async def synthesize(request: TTSRequest):
    """Synthesize speech from text using preset voice"""
    global tts, current_config
    
    if not current_config["loaded"] or tts is None:
        raise HTTPException(status_code=400, detail="Model not loaded. Call /load_model first")
    
    if not request.text or request.text.strip() == "":
        raise HTTPException(status_code=400, detail="Text is required")
    
    if request.voice not in VOICE_SAMPLES:
        raise HTTPException(status_code=400, detail=f"Invalid voice: {request.voice}")
    
    try:
        # Get reference
        voice_info = VOICE_SAMPLES[request.voice]
        ref_audio_path = voice_info["audio"]
        text_path = voice_info["text"]
        ref_codes_path = voice_info["codes"]
        
        ref_text_raw = get_ref_text_cached(text_path)
        
        # Encode reference
        codec_config = CODEC_CONFIGS[current_config["codec"]]
        if codec_config['use_preencoded'] and os.path.exists(ref_codes_path):
            ref_codes = torch.load(ref_codes_path, map_location="cpu", weights_only=True)
        else:
            if current_config["using_lmdeploy"] and hasattr(tts, 'get_cached_reference'):
                ref_codes = tts.get_cached_reference(request.voice, ref_audio_path, ref_text_raw)
            else:
                ref_codes = tts.encode_reference(ref_audio_path)
        
        if isinstance(ref_codes, torch.Tensor):
            ref_codes = ref_codes.cpu().numpy()
        
        # Split text into chunks
        text_chunks = split_text_into_chunks(request.text.strip(), max_chars=MAX_CHARS_PER_CHUNK)
        
        # Synthesize
        all_audio_segments = []
        sr = 24000
        silence_pad = np.zeros(int(sr * 0.15), dtype=np.float32)
        
        # Use batch processing if enabled and available
        if request.use_batch and current_config["using_lmdeploy"] and hasattr(tts, 'infer_batch') and len(text_chunks) > 1:
            chunk_wavs = tts.infer_batch(text_chunks, ref_codes, ref_text_raw)
            for i, chunk_wav in enumerate(chunk_wavs):
                if chunk_wav is not None and len(chunk_wav) > 0:
                    all_audio_segments.append(chunk_wav)
                    if i < len(text_chunks) - 1:
                        all_audio_segments.append(silence_pad)
        else:
            for i, chunk in enumerate(text_chunks):
                chunk_wav = tts.infer(chunk, ref_codes, ref_text_raw)
                if chunk_wav is not None and len(chunk_wav) > 0:
                    all_audio_segments.append(chunk_wav)
                    if i < len(text_chunks) - 1:
                        all_audio_segments.append(silence_pad)
        
        if not all_audio_segments:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
        
        # Concatenate and save
        final_wav = np.concatenate(all_audio_segments)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            sf.write(tmp.name, final_wav, sr)
            output_path = tmp.name
        
        # Cleanup memory
        if current_config["using_lmdeploy"] and hasattr(tts, 'cleanup_memory'):
            tts.cleanup_memory()
        cleanup_gpu_memory()
        
        return FileResponse(
            output_path,
            media_type="audio/wav",
            filename=f"tts_output_{int(time.time())}.wav",
            background=None
        )
        
    except Exception as e:
        cleanup_gpu_memory()
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")

@app.post("/synthesize_custom")
async def synthesize_custom(
    text: str = Form(...),
    ref_text: str = Form(...),
    ref_audio: UploadFile = File(...),
    use_batch: bool = Form(True)
):
    """Synthesize speech with custom reference audio"""
    global tts, current_config
    
    if not current_config["loaded"] or tts is None:
        raise HTTPException(status_code=400, detail="Model not loaded. Call /load_model first")
    
    if not text or text.strip() == "":
        raise HTTPException(status_code=400, detail="Text is required")
    
    try:
        # Save uploaded audio to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
            content = await ref_audio.read()
            tmp_audio.write(content)
            ref_audio_path = tmp_audio.name
        
        # Encode reference
        ref_codes = tts.encode_reference(ref_audio_path)
        if isinstance(ref_codes, torch.Tensor):
            ref_codes = ref_codes.cpu().numpy()
        
        # Split text into chunks
        text_chunks = split_text_into_chunks(text.strip(), max_chars=MAX_CHARS_PER_CHUNK)
        
        # Synthesize
        all_audio_segments = []
        sr = 24000
        silence_pad = np.zeros(int(sr * 0.15), dtype=np.float32)
        
        if use_batch and current_config["using_lmdeploy"] and hasattr(tts, 'infer_batch') and len(text_chunks) > 1:
            chunk_wavs = tts.infer_batch(text_chunks, ref_codes, ref_text)
            for i, chunk_wav in enumerate(chunk_wavs):
                if chunk_wav is not None and len(chunk_wav) > 0:
                    all_audio_segments.append(chunk_wav)
                    if i < len(text_chunks) - 1:
                        all_audio_segments.append(silence_pad)
        else:
            for i, chunk in enumerate(text_chunks):
                chunk_wav = tts.infer(chunk, ref_codes, ref_text)
                if chunk_wav is not None and len(chunk_wav) > 0:
                    all_audio_segments.append(chunk_wav)
                    if i < len(text_chunks) - 1:
                        all_audio_segments.append(silence_pad)
        
        if not all_audio_segments:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
        
        # Concatenate and save
        final_wav = np.concatenate(all_audio_segments)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            sf.write(tmp.name, final_wav, sr)
            output_path = tmp.name
        
        # Cleanup
        os.unlink(ref_audio_path)
        if current_config["using_lmdeploy"] and hasattr(tts, 'cleanup_memory'):
            tts.cleanup_memory()
        cleanup_gpu_memory()
        
        return FileResponse(
            output_path,
            media_type="audio/wav",
            filename=f"tts_custom_{int(time.time())}.wav",
            background=None
        )
        
    except Exception as e:
        cleanup_gpu_memory()
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")

@app.post("/synthesize_base64", response_model=dict)
async def synthesize_base64(request: TTSRequest):
    """Synthesize speech and return as base64 encoded audio"""
    global tts, current_config
    
    if not current_config["loaded"] or tts is None:
        raise HTTPException(status_code=400, detail="Model not loaded. Call /load_model first")
    
    if not request.text or request.text.strip() == "":
        raise HTTPException(status_code=400, detail="Text is required")
    
    if request.voice not in VOICE_SAMPLES:
        raise HTTPException(status_code=400, detail=f"Invalid voice: {request.voice}")
    
    try:
        # Get reference
        voice_info = VOICE_SAMPLES[request.voice]
        ref_audio_path = voice_info["audio"]
        text_path = voice_info["text"]
        ref_codes_path = voice_info["codes"]
        
        ref_text_raw = get_ref_text_cached(text_path)
        
        # Encode reference
        codec_config = CODEC_CONFIGS[current_config["codec"]]
        if codec_config['use_preencoded'] and os.path.exists(ref_codes_path):
            ref_codes = torch.load(ref_codes_path, map_location="cpu", weights_only=True)
        else:
            if current_config["using_lmdeploy"] and hasattr(tts, 'get_cached_reference'):
                ref_codes = tts.get_cached_reference(request.voice, ref_audio_path, ref_text_raw)
            else:
                ref_codes = tts.encode_reference(ref_audio_path)
        
        if isinstance(ref_codes, torch.Tensor):
            ref_codes = ref_codes.cpu().numpy()
        
        # Split text into chunks
        text_chunks = split_text_into_chunks(request.text.strip(), max_chars=MAX_CHARS_PER_CHUNK)
        
        # Synthesize
        all_audio_segments = []
        sr = 24000
        silence_pad = np.zeros(int(sr * 0.15), dtype=np.float32)
        
        if request.use_batch and current_config["using_lmdeploy"] and hasattr(tts, 'infer_batch') and len(text_chunks) > 1:
            chunk_wavs = tts.infer_batch(text_chunks, ref_codes, ref_text_raw)
            for i, chunk_wav in enumerate(chunk_wavs):
                if chunk_wav is not None and len(chunk_wav) > 0:
                    all_audio_segments.append(chunk_wav)
                    if i < len(text_chunks) - 1:
                        all_audio_segments.append(silence_pad)
        else:
            for i, chunk in enumerate(text_chunks):
                chunk_wav = tts.infer(chunk, ref_codes, ref_text_raw)
                if chunk_wav is not None and len(chunk_wav) > 0:
                    all_audio_segments.append(chunk_wav)
                    if i < len(text_chunks) - 1:
                        all_audio_segments.append(silence_pad)
        
        if not all_audio_segments:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
        
        # Concatenate and save to temp file
        final_wav = np.concatenate(all_audio_segments)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            sf.write(tmp.name, final_wav, sr)
            
            # Read and encode to base64
            with open(tmp.name, "rb") as f:
                audio_bytes = f.read()
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            os.unlink(tmp.name)
        
        # Cleanup memory
        if current_config["using_lmdeploy"] and hasattr(tts, 'cleanup_memory'):
            tts.cleanup_memory()
        cleanup_gpu_memory()
        
        return {
            "status": "success",
            "audio_base64": audio_base64,
            "sample_rate": sr,
            "duration": len(final_wav) / sr
        }
        
    except Exception as e:
        cleanup_gpu_memory()
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    import sys
    
    # Detect if running in Colab
    try:
        import google.colab
        IN_COLAB = True
    except ImportError:
        IN_COLAB = False
    
    # Get config from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    # Setup Ngrok if in Colab
    ngrok_url = None
    if IN_COLAB:
        try:
            from pyngrok import ngrok
            
            print("\n" + "="*60)
            print("🌐 Đang chạy trên Google Colab - Ngrok integration")
            print("="*60)
            
            # Prompt for Ngrok token
            ngrok_token = input("\n🔑 Nhập Ngrok Auth Token (lấy tại https://dashboard.ngrok.com/get-started/your-authtoken):\n> ").strip()
            
            if ngrok_token:
                # Set auth token
                ngrok.set_auth_token(ngrok_token)
                
                # Create tunnel
                print(f"\n⏳ Đang tạo Ngrok tunnel cho port {port}...")
                ngrok_url = ngrok.connect(port)
                
                print("\n" + "="*60)
                print("✅ Ngrok tunnel đã được tạo thành công!")
                print("="*60)
                print(f"\n🌐 Public URL: {ngrok_url}")
                print(f"📖 API Docs: {ngrok_url}/docs")
                print(f"\n💡 Sử dụng URL trên để gọi API từ bất kỳ đâu!")
                print("="*60 + "\n")
            else:
                print("\n⚠️ Không có Ngrok token - chỉ chạy local")
                print(f"📍 Local URL: http://localhost:{port}")
                
        except ImportError:
            print("\n⚠️ pyngrok chưa được cài đặt - chỉ chạy local")
            print("Cài đặt: pip install pyngrok")
        except Exception as e:
            print(f"\n❌ Lỗi khi setup Ngrok: {e}")
            print(f"📍 Chuyển sang chạy local: http://localhost:{port}")
    else:
        print(f"\n📍 Chạy local mode")
    
    print(f"\n🚀 Starting VieNeu-TTS API Server on {host}:{port}")
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    
    if ngrok_url:
        print(f"🌐 Ngrok Public URL: {ngrok_url}")
    
    print("\n⚠️ Nhấn CTRL+C để dừng server\n")
    
    try:
        uvicorn.run(app, host=host, port=port)
    except KeyboardInterrupt:
        print("\n\n🛑 Server đã dừng")
        if ngrok_url:
            print("🔌 Đóng Ngrok tunnel...")
            ngrok.disconnect(ngrok_url)

