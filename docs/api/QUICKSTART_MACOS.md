# Quick Start cho macOS

Hướng dẫn nhanh để chạy VieNeu-TTS API trên macOS.

## Bước 1: Cài đặt

```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies (không bao gồm lmdeploy)
pip install -r requirements-api.txt
```

## Bước 2: Cài đặt VieNeuTTS package

Nếu gặp lỗi "No module named 'vieneu_tts'", bạn cần cài đặt package:

```bash
# Nếu có file setup.py
pip install -e .

# Hoặc cài từ GitHub
pip install git+https://github.com/pnnbao97/VieNeu-TTS.git
```

## Bước 3: Chạy API

```bash
python api_server.py
```

API sẽ chạy tại: http://localhost:8000

## Bước 4: Test API

Mở terminal mới và chạy:

```bash
# Test health check
curl http://localhost:8000/

# Load model (CPU-friendly)
curl -X POST "http://localhost:8000/load_model" \
  -H "Content-Type: application/json" \
  -d '{
    "backbone": "VieNeu-TTS-q4-gguf",
    "codec": "NeuCodec ONNX (Fast CPU)",
    "device": "CPU",
    "enable_triton": false,
    "max_batch_size": 2
  }'

# Synthesize speech
curl -X POST "http://localhost:8000/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Xin chào, đây là test TTS trên macOS",
    "voice": "Vĩnh (nam miền Nam)",
    "use_batch": false
  }' \
  --output test.wav

# Play audio
afplay test.wav
```

## Hoặc dùng Python

```python
import requests

API_URL = "http://localhost:8000"

# 1. Load model
print("Loading model...")
response = requests.post(
    f"{API_URL}/load_model",
    json={
        "backbone": "VieNeu-TTS-q4-gguf",
        "codec": "NeuCodec ONNX (Fast CPU)",
        "device": "CPU",
        "enable_triton": False,
        "max_batch_size": 2
    }
)
print(response.json())

# 2. Synthesize
print("\nSynthesizing...")
response = requests.post(
    f"{API_URL}/synthesize",
    json={
        "text": "Xin chào từ macOS!",
        "voice": "Vĩnh (nam miền Nam)",
        "use_batch": False
    }
)

# 3. Save audio
with open("output.wav", "wb") as f:
    f.write(response.content)

print("✅ Saved to output.wav")

# 4. Play audio (macOS)
import os
os.system("afplay output.wav")
```

## Chạy test suite

```bash
python test_api.py
```

## Lưu ý quan trọng

### ⚠️ Trên macOS không có lmdeploy
- API sẽ tự động sử dụng backend standard (không có lmdeploy)
- Tốc độ sẽ chậm hơn so với Linux + GPU + lmdeploy
- Khuyến nghị sử dụng model GGUF (q4 hoặc q8) để tối ưu tốc độ

### 💡 Cấu hình tốt nhất cho macOS
```json
{
  "backbone": "VieNeu-TTS-q4-gguf",
  "codec": "NeuCodec ONNX (Fast CPU)",
  "device": "CPU",
  "enable_triton": false,
  "max_batch_size": 1
}
```

### 🚀 Muốn tốc độ nhanh hơn?
Sử dụng Google Colab (có GPU miễn phí):
1. Upload `colab_notebook.ipynb` lên Colab
2. Chạy notebook
3. Lấy Ngrok URL
4. Gọi API từ máy Mac của bạn

## Troubleshooting

### Lỗi: "No module named 'vieneu_tts'"
```bash
pip install -e .
```

### Lỗi: "No matching distribution found for lmdeploy"
Đây là bình thường trên macOS. Sử dụng `requirements-api.txt`:
```bash
pip install -r requirements-api.txt
```

### API chạy chậm
- Sử dụng model q4-gguf (nhẹ nhất)
- Giảm `max_batch_size` xuống 1
- Giảm độ dài văn bản

### Port 8000 đã được sử dụng
```bash
# Chạy trên port khác
export API_PORT=8080
python api_server.py
```

## API Documentation

Khi server đang chạy, truy cập:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Files quan trọng

- `api_server.py` - API server
- `requirements-api.txt` - Dependencies cho macOS/CPU
- `test_api.py` - Test suite
- `API_USAGE.md` - Chi tiết API endpoints
- `colab_notebook.ipynb` - Chạy trên Colab với GPU

## Gọi API từ hệ thống khác

Sau khi API đang chạy trên macOS, bạn có thể gọi từ:
- Web app (JavaScript/React/Vue)
- Mobile app (iOS/Android)
- Desktop app
- Bất kỳ hệ thống nào có thể gọi HTTP

Ví dụ từ JavaScript:
```javascript
const response = await fetch('http://localhost:8000/synthesize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Xin chào!',
    voice: 'Vĩnh (nam miền Nam)',
    use_batch: false
  })
});

const blob = await response.blob();
const audio = new Audio(URL.createObjectURL(blob));
audio.play();
```
