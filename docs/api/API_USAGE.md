# VieNeu-TTS API Documentation

## Tổng quan

API này cung cấp các endpoint để chuyển đổi văn bản tiếng Việt thành giọng nói (Text-to-Speech).

## Base URL

- **Local**: `http://localhost:8000`
- **Colab + Ngrok**: `https://xxxx-xx-xxx-xxx-xxx.ngrok-free.app` (URL sẽ được tạo khi chạy trên Colab)

## API Endpoints

### 1. Health Check

**GET** `/`

Kiểm tra server có hoạt động không.

**Response:**
```json
{
  "message": "VieNeu-TTS API Server",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### 2. Get Status

**GET** `/status`

Lấy thông tin trạng thái server và model.

**Response:**
```json
{
  "status": "running",
  "model_loaded": true,
  "backbone": "VieNeu-TTS (GPU)",
  "codec": "NeuCodec (Standard)",
  "device": "Auto",
  "using_lmdeploy": true,
  "available_voices": [
    "Tuyên (nam miền Bắc)",
    "Vĩnh (nam miền Nam)",
    "Bình (nam miền Bắc)",
    "Nguyên (nam miền Nam)",
    "Sơn (nam miền Nam)",
    "Đoan (nữ miền Nam)",
    "Ngọc (nữ miền Bắc)",
    "Ly (nữ miền Bắc)",
    "Dung (nữ miền Nam)"
  ]
}
```

---

### 3. List Voices

**GET** `/voices`

Lấy danh sách các giọng mẫu có sẵn.

**Response:**
```json
{
  "voices": {
    "Vĩnh (nam miền Nam)": {
      "audio_path": "./sample/Vĩnh (nam miền Nam).wav",
      "text_path": "./sample/Vĩnh (nam miền Nam).txt"
    },
    "Ngọc (nữ miền Bắc)": {
      "audio_path": "./sample/Ngọc (nữ miền Bắc).wav",
      "text_path": "./sample/Ngọc (nữ miền Bắc).txt"
    }
  }
}
```

---

### 4. Load Model

**POST** `/load_model`

Load model TTS trước khi sử dụng.

**Request Body:**
```json
{
  "backbone": "VieNeu-TTS (GPU)",
  "codec": "NeuCodec (Standard)",
  "device": "Auto",
  "enable_triton": true,
  "max_batch_size": 8
}
```

**Parameters:**
- `backbone` (string): Tên backbone model
  - `"VieNeu-TTS (GPU)"` - Chất lượng cao nhất, yêu cầu GPU
  - `"VieNeu-TTS-q8-gguf"` - Cân bằng chất lượng và tốc độ
  - `"VieNeu-TTS-q4-gguf"` - Nhẹ nhất, phù hợp CPU
- `codec` (string): Tên codec
  - `"NeuCodec (Standard)"` - Codec chuẩn
  - `"NeuCodec ONNX (Fast CPU)"` - Tối ưu cho CPU
- `device` (string): Device để chạy model
  - `"Auto"` - Tự động chọn
  - `"CPU"` - Chạy trên CPU
  - `"CUDA"` - Chạy trên GPU
- `enable_triton` (boolean): Bật Triton compilation (chỉ với GPU)
- `max_batch_size` (integer): Số lượng đoạn văn bản xử lý cùng lúc (1-16)

**Response:**
```json
{
  "status": "success",
  "message": "Model loaded successfully",
  "backend": "LMDeploy",
  "config": {
    "backbone": "VieNeu-TTS (GPU)",
    "codec": "NeuCodec (Standard)",
    "device": "Auto",
    "loaded": true,
    "using_lmdeploy": true
  }
}
```

---

### 5. Synthesize Speech (Preset Voice)

**POST** `/synthesize`

Chuyển đổi văn bản thành giọng nói sử dụng giọng mẫu có sẵn.

**Request Body:**
```json
{
  "text": "Xin chào, đây là hệ thống chuyển đổi văn bản thành giọng nói tiếng Việt.",
  "voice": "Vĩnh (nam miền Nam)",
  "use_batch": true
}
```

**Parameters:**
- `text` (string, required): Văn bản cần chuyển đổi (tối đa 10,000 ký tự)
- `voice` (string): Tên giọng mẫu (xem danh sách tại `/voices`)
- `use_batch` (boolean): Sử dụng batch processing (nhanh hơn với GPU)

**Response:**
- Content-Type: `audio/wav`
- File WAV audio

**Example (Python):**
```python
import requests

response = requests.post(
    "http://localhost:8000/synthesize",
    json={
        "text": "Xin chào!",
        "voice": "Vĩnh (nam miền Nam)",
        "use_batch": True
    }
)

with open("output.wav", "wb") as f:
    f.write(response.content)
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Xin chào!",
    "voice": "Vĩnh (nam miền Nam)",
    "use_batch": true
  }' \
  --output output.wav
```

---

### 6. Synthesize Speech (Base64)

**POST** `/synthesize_base64`

Chuyển đổi văn bản thành giọng nói và trả về dưới dạng base64.

**Request Body:**
```json
{
  "text": "Xin chào!",
  "voice": "Ngọc (nữ miền Bắc)",
  "use_batch": true
}
```

**Response:**
```json
{
  "status": "success",
  "audio_base64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEA...",
  "sample_rate": 24000,
  "duration": 2.5
}
```

**Example (Python):**
```python
import requests
import base64

response = requests.post(
    "http://localhost:8000/synthesize_base64",
    json={
        "text": "Xin chào!",
        "voice": "Ngọc (nữ miền Bắc)",
        "use_batch": True
    }
)

result = response.json()
audio_bytes = base64.b64decode(result['audio_base64'])

with open("output.wav", "wb") as f:
    f.write(audio_bytes)
```

---

### 7. Synthesize Speech (Custom Voice)

**POST** `/synthesize_custom`

Chuyển đổi văn bản thành giọng nói sử dụng giọng mẫu tùy chỉnh.

**Request (multipart/form-data):**
- `text` (string, required): Văn bản cần chuyển đổi
- `ref_text` (string, required): Lời thoại của file audio mẫu
- `ref_audio` (file, required): File audio mẫu (.wav)
- `use_batch` (boolean): Sử dụng batch processing

**Response:**
- Content-Type: `audio/wav`
- File WAV audio

**Example (Python):**
```python
import requests

with open("my_voice.wav", "rb") as audio_file:
    response = requests.post(
        "http://localhost:8000/synthesize_custom",
        data={
            "text": "Đây là giọng nói tùy chỉnh của tôi.",
            "ref_text": "Xin chào, tôi là người mẫu.",
            "use_batch": True
        },
        files={
            "ref_audio": audio_file
        }
    )

with open("output_custom.wav", "wb") as f:
    f.write(response.content)
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/synthesize_custom" \
  -F "text=Đây là giọng nói tùy chỉnh" \
  -F "ref_text=Xin chào, tôi là người mẫu" \
  -F "ref_audio=@my_voice.wav" \
  -F "use_batch=true" \
  --output output_custom.wav
```

---

## Chạy API Server

### Local

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy server
python api_server.py

# Hoặc với uvicorn
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build image
docker build -t vieneu-tts-api -f docker/Dockerfile.gpu .

# Run container
docker run -p 8000:8000 --gpus all vieneu-tts-api
```

### Google Colab + Ngrok

1. Upload `colab_notebook.ipynb` lên Google Colab
2. Lấy Ngrok auth token tại: https://dashboard.ngrok.com/get-started/your-authtoken
3. Chạy các cell theo thứ tự trong notebook
4. Copy public URL để sử dụng

---

## Error Codes

- `400` - Bad Request (thiếu parameters hoặc sai format)
- `500` - Internal Server Error (lỗi khi xử lý)

**Example Error Response:**
```json
{
  "detail": "Model not loaded. Call /load_model first"
}
```

---

## Best Practices

1. **Load model trước**: Luôn gọi `/load_model` trước khi synthesize
2. **Batch processing**: Bật `use_batch=true` khi có GPU để tăng tốc độ
3. **Giới hạn text**: Không nên gửi văn bản quá dài (> 3000 ký tự) trong 1 request
4. **Reuse connection**: Sử dụng session để tái sử dụng connection
5. **Error handling**: Luôn kiểm tra status code và xử lý lỗi

---

## Performance Tips

### GPU (Recommended)
- Backbone: `VieNeu-TTS (GPU)`
- Codec: `NeuCodec (Standard)`
- Device: `Auto` hoặc `CUDA`
- Enable Triton: `true`
- Max Batch Size: `8-12` (tùy VRAM)

### CPU
- Backbone: `VieNeu-TTS-q4-gguf`
- Codec: `NeuCodec ONNX (Fast CPU)`
- Device: `CPU`
- Max Batch Size: `2-4`

---

## Interactive API Documentation

Khi server đang chạy, truy cập:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Support

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra logs của server
2. Đảm bảo đã load model trước khi synthesize
3. Kiểm tra VRAM nếu dùng GPU (giảm `max_batch_size` nếu OOM)
