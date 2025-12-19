# VieNeu-TTS API

API REST để chuyển đổi văn bản tiếng Việt thành giọng nói (Text-to-Speech).

## 🚀 Quick Start

### 1. Cài đặt

#### Cách 1: Script tự động (Linux/macOS)

```bash
# Chạy script cài đặt
bash install_api.sh

# Activate virtual environment
source venv/bin/activate
```

#### Cách 2: Cài đặt thủ công

**Trên macOS/Windows (không có lmdeploy):**
```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# hoặc venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements-api.txt
```

**Trên Linux với GPU (có lmdeploy):**
```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate

# Cài đặt PyTorch với CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Cài đặt tất cả dependencies
pip install -r requirements.txt
```

### 2. Chạy API Server

```bash
python api_server.py
```

Server sẽ chạy tại: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

> **Lưu ý:** Nếu gặp lỗi "No module named 'vieneu_tts'", cài đặt package:
> ```bash
> pip install -e .
> ```

### 3. Chạy trên Google Colab với Ngrok

1. Upload file `colab_notebook.ipynb` lên Google Colab
2. Đăng ký tài khoản Ngrok tại: https://ngrok.com
3. Lấy auth token tại: https://dashboard.ngrok.com/get-started/your-authtoken
4. Mở notebook và chạy các cell theo thứ tự
5. Copy public URL để sử dụng từ bên ngoài

> **Colab có GPU miễn phí** nên sẽ chạy nhanh hơn nhiều so với CPU!

## 📖 API Endpoints

### Load Model (Bắt buộc gọi trước)

```bash
curl -X POST "http://localhost:8000/load_model" \
  -H "Content-Type: application/json" \
  -d '{
    "backbone": "VieNeu-TTS (GPU)",
    "codec": "NeuCodec (Standard)",
    "device": "Auto",
    "enable_triton": true,
    "max_batch_size": 8
  }'
```

### Synthesize Speech

```bash
curl -X POST "http://localhost:8000/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Xin chào, đây là hệ thống TTS tiếng Việt",
    "voice": "Vĩnh (nam miền Nam)",
    "use_batch": true
  }' \
  --output output.wav
```

### Synthesize với Base64 Response

```bash
curl -X POST "http://localhost:8000/synthesize_base64" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Xin chào!",
    "voice": "Ngọc (nữ miền Bắc)",
    "use_batch": true
  }'
```

### Synthesize với Custom Voice

```bash
curl -X POST "http://localhost:8000/synthesize_custom" \
  -F "text=Đây là giọng nói tùy chỉnh" \
  -F "ref_text=Xin chào, tôi là người mẫu" \
  -F "ref_audio=@my_voice.wav" \
  -F "use_batch=true" \
  --output output_custom.wav
```

## 🐍 Python Examples

### Basic Usage

```python
import requests

# 1. Load model
API_URL = "http://localhost:8000"

load_config = {
    "backbone": "VieNeu-TTS (GPU)",
    "codec": "NeuCodec (Standard)",
    "device": "Auto",
    "enable_triton": True,
    "max_batch_size": 8
}

response = requests.post(f"{API_URL}/load_model", json=load_config)
print(response.json())

# 2. Synthesize speech
tts_request = {
    "text": "Xin chào từ hệ thống TTS!",
    "voice": "Vĩnh (nam miền Nam)",
    "use_batch": True
}

response = requests.post(f"{API_URL}/synthesize", json=tts_request)

# Save audio
with open("output.wav", "wb") as f:
    f.write(response.content)

print("✅ Audio saved to output.wav")
```

### Get Base64 Audio

```python
import requests
import base64

response = requests.post(
    f"{API_URL}/synthesize_base64",
    json={
        "text": "Test base64 response",
        "voice": "Ngọc (nữ miền Bắc)",
        "use_batch": True
    }
)

result = response.json()
audio_bytes = base64.b64decode(result['audio_base64'])

with open("output.wav", "wb") as f:
    f.write(audio_bytes)

print(f"Duration: {result['duration']:.2f}s")
```

### Custom Voice

```python
import requests

with open("my_voice.wav", "rb") as audio_file:
    response = requests.post(
        f"{API_URL}/synthesize_custom",
        data={
            "text": "Đây là giọng nói tùy chỉnh của tôi",
            "ref_text": "Xin chào, tôi là người mẫu",
            "use_batch": True
        },
        files={
            "ref_audio": audio_file
        }
    )

with open("output_custom.wav", "wb") as f:
    f.write(response.content)
```

## 🧪 Testing

Chạy test suite:

```bash
# Test với local server
python test_api.py

# Test với Ngrok URL
python test_api.py https://xxxx-xx-xxx-xxx-xxx.ngrok-free.app
```

## 🎤 Available Voices

- **Nam miền Bắc**: Tuyên, Bình
- **Nam miền Nam**: Vĩnh, Nguyên, Sơn
- **Nữ miền Bắc**: Ngọc, Ly, Hương
- **Nữ miền Nam**: Đoan, Dung

Xem danh sách đầy đủ:
```bash
curl http://localhost:8000/voices
```

## ⚙️ Configuration

### GPU (Recommended)
```json
{
  "backbone": "VieNeu-TTS (GPU)",
  "codec": "NeuCodec (Standard)",
  "device": "Auto",
  "enable_triton": true,
  "max_batch_size": 8
}
```

### CPU
```json
{
  "backbone": "VieNeu-TTS-q4-gguf",
  "codec": "NeuCodec ONNX (Fast CPU)",
  "device": "CPU",
  "enable_triton": false,
  "max_batch_size": 2
}
```

## 🔧 Troubleshooting

### Out of Memory (OOM)
- Giảm `max_batch_size` xuống 4 hoặc 2
- Sử dụng model nhẹ hơn (q4-gguf)
- Giảm độ dài văn bản

### Slow Performance
- Sử dụng GPU nếu có
- Bật `use_batch=true`
- Bật `enable_triton=true` (GPU only)
- Tăng `max_batch_size` nếu có đủ VRAM

### Model Not Loaded
- Luôn gọi `/load_model` trước khi synthesize
- Kiểm tra response của `/status` để xác nhận model đã load

## 📚 Documentation

- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc`
- **Chi tiết API**: Xem file `API_USAGE.md`

## 🌐 Deploy to Production

### Docker

```bash
# Build
docker build -t vieneu-tts-api -f docker/Dockerfile.gpu .

# Run
docker run -p 8000:8000 --gpus all vieneu-tts-api
```

### Environment Variables

```bash
export API_HOST=0.0.0.0
export API_PORT=8000
python api_server.py
```

## 📝 Notes

- Model cần được load trước khi sử dụng (gọi `/load_model`)
- Batch processing chỉ hoạt động với GPU và LMDeploy backend
- Văn bản dài sẽ được tự động chia thành các đoạn nhỏ
- File audio output có sample rate 24kHz, format WAV

## 🤝 Integration Examples

### Node.js

```javascript
const axios = require('axios');
const fs = require('fs');

async function synthesize() {
  const response = await axios.post(
    'http://localhost:8000/synthesize',
    {
      text: 'Xin chào!',
      voice: 'Vĩnh (nam miền Nam)',
      use_batch: true
    },
    { responseType: 'arraybuffer' }
  );
  
  fs.writeFileSync('output.wav', response.data);
}
```

### PHP

```php
<?php
$ch = curl_init('http://localhost:8000/synthesize');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
    'text' => 'Xin chào!',
    'voice' => 'Vĩnh (nam miền Nam)',
    'use_batch' => true
]));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$audio = curl_exec($ch);
file_put_contents('output.wav', $audio);
curl_close($ch);
?>
```

## 📄 License

Xem file LICENSE trong repository.
