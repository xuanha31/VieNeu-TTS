# API Integration

VieNeu-TTS giờ đây có REST API để bạn có thể gọi từ bất kỳ hệ thống nào!

## 🚀 Quick Start

### Option 1: Google Colab (Khuyến nghị - Có GPU miễn phí)

1. Upload `colab_notebook.ipynb` lên [Google Colab](https://colab.research.google.com)
2. Lấy Ngrok token tại [ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)
3. Chạy notebook và copy public URL
4. Gọi API từ bất kỳ đâu!

```python
import requests

API_URL = "https://xxxx.ngrok-free.app"  # URL từ Colab

# Load model
requests.post(f"{API_URL}/load_model", json={
    "backbone": "VieNeu-TTS (GPU)",
    "codec": "NeuCodec (Standard)",
    "device": "Auto",
    "max_batch_size": 8
})

# Synthesize
response = requests.post(f"{API_URL}/synthesize", json={
    "text": "Xin chào!",
    "voice": "Vĩnh (nam miền Nam)"
})

with open("output.wav", "wb") as f:
    f.write(response.content)
```

### Option 2: Local (macOS/Linux/Windows)

```bash
# Cài đặt
pip install -r requirements-api.txt

# Chạy API
python api_server.py

# API sẽ chạy tại: http://localhost:8000
```

## 📖 Documentation

- **Bắt đầu:** `START_HERE.md`
- **Test trên Colab:** `TEST_ON_COLAB.md`
- **Chạy trên macOS:** `QUICKSTART_MACOS.md`
- **API Endpoints:** `API_USAGE.md`
- **Fix lỗi:** `FIX_MACOS_INSTALL.md`

## 🎯 API Endpoints

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/` | GET | Health check |
| `/status` | GET | Trạng thái server |
| `/voices` | GET | Danh sách giọng |
| `/load_model` | POST | Load model |
| `/synthesize` | POST | TTS với preset voice |
| `/synthesize_base64` | POST | TTS trả về base64 |
| `/synthesize_custom` | POST | TTS với custom voice |

API Documentation: `http://localhost:8000/docs`

## 🧪 Test

```bash
python test_api.py
```

## 💡 Use Cases

- Web applications (React, Vue, Angular)
- Mobile apps (iOS, Android, Flutter)
- Desktop applications
- Chatbots và voice assistants
- E-learning platforms
- Accessibility tools

## 📱 Examples

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/synthesize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Xin chào!',
    voice: 'Vĩnh (nam miền Nam)'
  })
});

const blob = await response.blob();
const audio = new Audio(URL.createObjectURL(blob));
audio.play();
```

### cURL
```bash
curl -X POST "http://localhost:8000/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Xin chào!", "voice": "Vĩnh (nam miền Nam)"}' \
  --output output.wav
```

## 🚀 Performance

| Environment | Speed | Setup |
|-------------|-------|-------|
| Google Colab (GPU) | 5-10x realtime | 10 min |
| macOS (CPU) | 0.5-1x realtime | 5 min |
| Linux + GPU | 5-10x realtime | 15 min |

## 📦 Files

- `api_server.py` - FastAPI server
- `colab_notebook.ipynb` - Colab notebook với Ngrok
- `test_api.py` - Test suite
- `requirements-api.txt` - Dependencies cho CPU/macOS
- `START_HERE.md` - Hướng dẫn bắt đầu

---

**Bắt đầu ngay:** Đọc file `START_HERE.md` 🚀
