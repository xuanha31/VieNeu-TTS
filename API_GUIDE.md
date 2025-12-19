# 🚀 VieNeu-TTS API

REST API để chuyển đổi văn bản tiếng Việt thành giọng nói.

## 📖 Documentation

**Tất cả tài liệu API:** [`docs/api/`](./docs/api/)

### Bắt đầu nhanh:
- 📘 **[START_HERE.md](./docs/api/START_HERE.md)** - Bắt đầu từ đây (5 phút)
- 📗 **[API_COMPLETE_GUIDE.md](./docs/api/API_COMPLETE_GUIDE.md)** - Tổng hợp tất cả (30-45 phút)

### Theo chủ đề:
- 🌐 **[TEST_ON_COLAB.md](./docs/api/TEST_ON_COLAB.md)** - Test trên Google Colab
- 💻 **[QUICKSTART_MACOS.md](./docs/api/QUICKSTART_MACOS.md)** - Chạy trên macOS
- 📚 **[API_USAGE.md](./docs/api/API_USAGE.md)** - Chi tiết API endpoints
- 🔧 **[FIX_MACOS_INSTALL.md](./docs/api/FIX_MACOS_INSTALL.md)** - Fix lỗi cài đặt

---

## 🚀 Quick Start

### Option 1: Google Colab (Khuyến nghị - GPU miễn phí)

```bash
# 1. Upload colab_notebook.ipynb lên Colab
# 2. Lấy Ngrok token tại: https://dashboard.ngrok.com
# 3. Chạy notebook và copy public URL
# 4. Test API
python test_api.py https://xxxx.ngrok-free.app
```

### Option 2: macOS/Linux Local

```bash
# Cài đặt
pip install -r requirements-api.txt

# Chạy API
python api_server.py

# Test
python test_api.py
```

---

## 🎯 API Endpoints

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/` | GET | Health check |
| `/status` | GET | Trạng thái server |
| `/voices` | GET | Danh sách giọng |
| `/load_model` | POST | Load model (bắt buộc) |
| `/synthesize` | POST | TTS với preset voice |
| `/synthesize_base64` | POST | TTS trả về base64 |
| `/synthesize_custom` | POST | TTS với custom voice |

**API Docs:** `http://localhost:8000/docs`

---

## 💻 Example

```python
import requests

API_URL = "http://localhost:8000"

# Load model
requests.post(f"{API_URL}/load_model", json={
    "backbone": "VieNeu-TTS-q4-gguf",
    "codec": "NeuCodec ONNX (Fast CPU)",
    "device": "CPU",
    "max_batch_size": 2
})

# Synthesize
response = requests.post(f"{API_URL}/synthesize", json={
    "text": "Xin chào!",
    "voice": "Vĩnh (nam miền Nam)"
})

with open("output.wav", "wb") as f:
    f.write(response.content)
```

---

## 📦 Files

- `api_server.py` - FastAPI server
- `colab_notebook.ipynb` - Colab notebook
- `test_api.py` - Test suite
- `requirements-api.txt` - Dependencies (macOS/CPU)
- `requirements.txt` - Dependencies đầy đủ (Linux/GPU)
- `docs/api/` - Tất cả tài liệu (17 files)

---

## 🔗 Links

- **Documentation:** [`docs/api/`](./docs/api/)
- **Bắt đầu:** [`docs/api/START_HERE.md`](./docs/api/START_HERE.md)
- **Tổng hợp:** [`docs/api/API_COMPLETE_GUIDE.md`](./docs/api/API_COMPLETE_GUIDE.md)

---

**Bắt đầu ngay:** Đọc [`docs/api/START_HERE.md`](./docs/api/START_HERE.md) 🚀
