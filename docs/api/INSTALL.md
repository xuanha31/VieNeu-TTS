# Hướng dẫn cài đặt VieNeu-TTS API

## Cài đặt cho macOS / Windows (CPU hoặc GPU không có lmdeploy)

### Bước 1: Cài đặt dependencies cơ bản

```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# hoặc
venv\Scripts\activate  # Windows

# Cài đặt dependencies cho API
pip install -r requirements-api.txt
```

### Bước 2: Cài đặt VieNeuTTS package

```bash
# Nếu có file setup.py hoặc pyproject.toml
pip install -e .

# Hoặc cài đặt trực tiếp từ source
pip install git+https://github.com/pnnbao97/VieNeu-TTS.git
```

### Bước 3: Chạy API

```bash
python api_server.py
```

API sẽ chạy tại: http://localhost:8000

---

## Cài đặt cho Linux với GPU (có lmdeploy - tốc độ nhanh hơn)

### Bước 1: Cài đặt CUDA

Đảm bảo bạn đã cài đặt CUDA Toolkit (11.8 hoặc 12.1)

```bash
nvidia-smi  # Kiểm tra GPU
```

### Bước 2: Cài đặt dependencies đầy đủ

```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate

# Cài đặt PyTorch với CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Cài đặt tất cả dependencies (bao gồm lmdeploy)
pip install -r requirements.txt
```

### Bước 3: Chạy API

```bash
python api_server.py
```

---

## Cài đặt cho Google Colab

### Cách 1: Sử dụng Notebook có sẵn

1. Upload file `colab_notebook.ipynb` lên Google Colab
2. Chạy các cell theo thứ tự
3. Lấy Ngrok auth token tại: https://dashboard.ngrok.com/get-started/your-authtoken

### Cách 2: Cài đặt thủ công

```python
# Clone repository
!git clone https://github.com/YOUR_USERNAME/VieNeu-TTS.git
%cd VieNeu-TTS

# Cài đặt dependencies
!pip install -r requirements.txt

# Cài đặt ngrok
!pip install pyngrok

# Setup ngrok
from pyngrok import ngrok
ngrok.set_auth_token("YOUR_NGROK_TOKEN")

# Chạy API trong background
import threading
import uvicorn
from api_server import app

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Tạo public URL
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")
```

---

## Kiểm tra cài đặt

### Test 1: Kiểm tra API server

```bash
# Trong terminal khác
curl http://localhost:8000/
```

Kết quả mong đợi:
```json
{
  "message": "VieNeu-TTS API Server",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### Test 2: Chạy test suite

```bash
python test_api.py
```

### Test 3: Load model và synthesize

```python
import requests

# Load model
response = requests.post(
    "http://localhost:8000/load_model",
    json={
        "backbone": "VieNeu-TTS-q4-gguf",  # Nhẹ nhất, phù hợp CPU
        "codec": "NeuCodec ONNX (Fast CPU)",
        "device": "CPU",
        "enable_triton": False,
        "max_batch_size": 2
    }
)
print(response.json())

# Synthesize
response = requests.post(
    "http://localhost:8000/synthesize",
    json={
        "text": "Xin chào!",
        "voice": "Vĩnh (nam miền Nam)",
        "use_batch": False
    }
)

with open("test.wav", "wb") as f:
    f.write(response.content)
print("✅ Saved to test.wav")
```

---

## Troubleshooting

### Lỗi: "No module named 'vieneu_tts'"

```bash
# Cài đặt package
pip install -e .
# hoặc
pip install git+https://github.com/pnnbao97/VieNeu-TTS.git
```

### Lỗi: "No matching distribution found for lmdeploy"

Đây là bình thường trên macOS/Windows. Sử dụng `requirements-api.txt` thay vì `requirements.txt`:

```bash
pip install -r requirements-api.txt
```

### Lỗi: "CUDA out of memory"

Giảm `max_batch_size` hoặc sử dụng model nhẹ hơn:

```json
{
  "backbone": "VieNeu-TTS-q4-gguf",
  "max_batch_size": 2
}
```

### Lỗi: "Model not loaded"

Luôn gọi `/load_model` trước khi synthesize:

```bash
curl -X POST "http://localhost:8000/load_model" \
  -H "Content-Type: application/json" \
  -d '{"backbone": "VieNeu-TTS-q4-gguf", "codec": "NeuCodec ONNX (Fast CPU)", "device": "CPU"}'
```

### API chạy chậm

**Trên CPU:**
- Sử dụng model GGUF (q4 hoặc q8)
- Sử dụng codec ONNX
- Giảm `max_batch_size` xuống 1-2

**Trên GPU:**
- Cài đặt lmdeploy (chỉ Linux)
- Bật `enable_triton=true`
- Tăng `max_batch_size` lên 8-12

---

## Cấu hình khuyến nghị

### Máy tính cá nhân (CPU)
```json
{
  "backbone": "VieNeu-TTS-q4-gguf",
  "codec": "NeuCodec ONNX (Fast CPU)",
  "device": "CPU",
  "enable_triton": false,
  "max_batch_size": 2
}
```

### Máy có GPU (NVIDIA)
```json
{
  "backbone": "VieNeu-TTS (GPU)",
  "codec": "NeuCodec (Standard)",
  "device": "Auto",
  "enable_triton": true,
  "max_batch_size": 8
}
```

### Google Colab (GPU T4)
```json
{
  "backbone": "VieNeu-TTS (GPU)",
  "codec": "NeuCodec (Standard)",
  "device": "Auto",
  "enable_triton": true,
  "max_batch_size": 6
}
```

---

## Environment Variables

```bash
# API configuration
export API_HOST=0.0.0.0
export API_PORT=8000

# Ngrok (cho Colab)
export NGROK_AUTH_TOKEN=your_token_here

# Chạy
python api_server.py
```

---

## Docker (Optional)

```bash
# Build
docker build -t vieneu-tts-api -f docker/Dockerfile.gpu .

# Run với GPU
docker run -p 8000:8000 --gpus all vieneu-tts-api

# Run với CPU
docker run -p 8000:8000 vieneu-tts-api
```

---

## Cập nhật

```bash
# Cập nhật code
git pull

# Cập nhật dependencies
pip install -r requirements-api.txt --upgrade

# Restart server
python api_server.py
```
