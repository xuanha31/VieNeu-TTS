# 🚀 VieNeu-TTS API - Bắt đầu từ đây

## 📋 Tổng quan

Bạn có 2 cách để chạy API:

1. **Google Colab** (Khuyến nghị để test) - Có GPU miễn phí, nhanh
2. **macOS Local** - Chạy trên máy của bạn, chậm hơn nhưng ổn định

---

## 🎯 Option 1: Test trên Google Colab (Khuyến nghị)

### Tại sao chọn Colab?
- ✅ GPU T4 miễn phí
- ✅ Nhanh hơn CPU 5-10 lần
- ✅ Không cần cài đặt gì trên máy
- ✅ Có lmdeploy (tối ưu tốc độ)
- ✅ Gọi từ bất kỳ đâu qua Ngrok

### Các bước:

#### 1. Upload notebook lên Colab
- Truy cập: https://colab.research.google.com
- File → Upload notebook
- Chọn file `colab_notebook.ipynb`

#### 2. Lấy Ngrok token
- Đăng ký miễn phí: https://ngrok.com
- Lấy token: https://dashboard.ngrok.com/get-started/your-authtoken

#### 3. Chạy notebook
- Runtime → Change runtime type → **GPU**
- Chạy các cell theo thứ tự
- Paste Ngrok token khi được hỏi
- Copy public URL (dạng: `https://xxxx.ngrok-free.app`)

#### 4. Test API
```bash
# Từ máy Mac của bạn
python test_api.py https://xxxx.ngrok-free.app
```

📖 **Chi tiết:** Đọc file `TEST_ON_COLAB.md`

---

## 💻 Option 2: Chạy trên macOS Local

### Tại sao chọn Local?
- ✅ Không cần internet
- ✅ Ổn định, không timeout
- ✅ Không giới hạn thời gian
- ⚠️ Chậm hơn (CPU only)
- ⚠️ Không có lmdeploy

### Các bước:

#### 1. Cài đặt
```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies (không có lmdeploy)
pip install -r requirements-api.txt
```

#### 2. Chạy API
```bash
python api_server.py
```

#### 3. Test
```bash
# Terminal mới
python test_api.py
```

📖 **Chi tiết:** Đọc file `QUICKSTART_MACOS.md`

---

## 🐛 Gặp lỗi?

### Lỗi: "No matching distribution found for lmdeploy"
➡️ Đọc file `FIX_MACOS_INSTALL.md`

**TL;DR:** Dùng `requirements-api.txt` thay vì `requirements.txt`

### Lỗi: "No module named 'vieneu_tts'"
```bash
pip install -e .
```

### API chạy chậm trên macOS
➡️ Đây là bình thường (CPU only). Dùng Colab để có tốc độ nhanh hơn.

---

## 📚 Tài liệu

| File | Mục đích |
|------|----------|
| `START_HERE.md` | **File này** - Bắt đầu từ đây |
| `TEST_ON_COLAB.md` | Hướng dẫn test trên Colab |
| `QUICKSTART_MACOS.md` | Hướng dẫn nhanh cho macOS |
| `FIX_MACOS_INSTALL.md` | Fix lỗi lmdeploy trên macOS |
| `API_USAGE.md` | Chi tiết tất cả API endpoints |
| `README_API.md` | Quick start và examples |
| `INSTALL.md` | Hướng dẫn cài đặt đầy đủ |
| `API_FILES_SUMMARY.md` | Tổng hợp tất cả files |

---

## 🎯 Workflow khuyến nghị

### Cho Development/Testing:
```
1. Test trên Colab (nhanh, có GPU)
   ↓
2. Gọi API từ máy Mac qua Ngrok
   ↓
3. Develop app của bạn
```

### Cho Production:
```
1. Deploy lên cloud server (AWS/GCP/Azure)
   ↓
2. Có GPU và lmdeploy
   ↓
3. Domain riêng (không dùng Ngrok)
```

---

## 🔥 Quick Commands

### Test trên Colab
```bash
# Sau khi có Ngrok URL
python test_api.py https://xxxx.ngrok-free.app
```

### Test trên macOS
```bash
# Terminal 1: Chạy API
python api_server.py

# Terminal 2: Test
python test_api.py
```

### Gọi API từ Python
```python
import requests

API_URL = "http://localhost:8000"  # Hoặc Ngrok URL

# Load model
requests.post(f"{API_URL}/load_model", json={
    "backbone": "VieNeu-TTS-q4-gguf",  # CPU
    # "backbone": "VieNeu-TTS (GPU)",  # GPU (Colab)
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

## 📊 So sánh

| | macOS Local | Google Colab |
|---|-------------|--------------|
| **Tốc độ** | 0.5-1x realtime | 5-10x realtime |
| **Setup** | 5 phút | 10 phút |
| **Chi phí** | Miễn phí | Miễn phí |
| **Ổn định** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ (timeout 12h) |
| **Internet** | Không cần | Cần |
| **lmdeploy** | ❌ | ✅ |
| **GPU** | ❌ | ✅ T4 |

---

## ✅ Checklist

### Để test trên Colab:
- [ ] Đã có tài khoản Google
- [ ] Đã đăng ký Ngrok
- [ ] Đã lấy Ngrok token
- [ ] Upload `colab_notebook.ipynb`
- [ ] Chọn GPU runtime
- [ ] Chạy các cell
- [ ] Copy Ngrok URL
- [ ] Test từ máy Mac

### Để chạy trên macOS:
- [ ] Đã cài Python 3.8+
- [ ] Tạo virtual environment
- [ ] Cài `requirements-api.txt`
- [ ] Chạy `python api_server.py`
- [ ] Test với `python test_api.py`

---

## 🎉 Kết luận

**Khuyến nghị:**
1. **Test trên Colab trước** - Nhanh, dễ, có GPU
2. **Sau đó chạy local** - Nếu cần ổn định hơn
3. **Deploy production** - Khi ready

**Bắt đầu ngay:**
- Colab: Mở file `colab_notebook.ipynb`
- macOS: Chạy `pip install -r requirements-api.txt`

**Cần giúp đỡ:**
- Colab: Đọc `TEST_ON_COLAB.md`
- macOS: Đọc `QUICKSTART_MACOS.md`
- Lỗi: Đọc `FIX_MACOS_INSTALL.md`

---

## 📞 Support Files

- `api_server.py` - API server code
- `colab_notebook.ipynb` - Colab notebook
- `test_api.py` - Test suite
- `requirements-api.txt` - Dependencies cho macOS
- `requirements.txt` - Dependencies đầy đủ (Colab)

---

**Chúc bạn thành công! 🚀**

Nếu gặp vấn đề, đọc các file hướng dẫn hoặc check logs của API server.
