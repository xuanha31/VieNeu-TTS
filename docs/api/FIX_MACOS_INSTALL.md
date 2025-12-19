# Fix lỗi cài đặt trên macOS

## Vấn đề bạn đang gặp

```
ERROR: Could not find a version that satisfies the requirement lmdeploy==0.11.0
ERROR: No matching distribution found for lmdeploy==0.11.0
```

## Nguyên nhân

`lmdeploy` chỉ hỗ trợ Linux với CUDA. Package này **không có** trên macOS.

## ✅ Giải pháp

### Cách 1: Sử dụng requirements-api.txt (Khuyến nghị cho macOS)

```bash
# Xóa virtual environment cũ nếu có
rm -rf venv

# Tạo virtual environment mới
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies KHÔNG có lmdeploy
pip install -r requirements-api.txt

# Cài đặt VieNeuTTS package (nếu cần)
pip install -e .
```

### Cách 2: Chỉnh sửa requirements.txt gốc

Nếu bạn muốn dùng `requirements.txt` gốc, comment dòng lmdeploy:

```bash
# Mở file requirements.txt và comment dòng này:
# lmdeploy==0.11.0

# Hoặc dùng command:
sed -i.bak '/lmdeploy/d' requirements.txt

# Sau đó cài đặt:
pip install -r requirements.txt
```

## 🚀 Hướng dẫn cài đặt đầy đủ cho macOS

```bash
# 1. Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Upgrade pip
pip install --upgrade pip

# 3. Cài đặt dependencies (không có lmdeploy)
pip install -r requirements-api.txt

# 4. Kiểm tra cài đặt
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"

# 5. Chạy API server
python api_server.py
```

## 🧪 Test cài đặt

Mở terminal mới và chạy:

```bash
# Test 1: Health check
curl http://localhost:8000/

# Test 2: Load model (CPU-friendly)
curl -X POST "http://localhost:8000/load_model" \
  -H "Content-Type: application/json" \
  -d '{
    "backbone": "VieNeu-TTS-q4-gguf",
    "codec": "NeuCodec ONNX (Fast CPU)",
    "device": "CPU",
    "enable_triton": false,
    "max_batch_size": 2
  }'

# Test 3: Synthesize
curl -X POST "http://localhost:8000/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Xin chào từ macOS",
    "voice": "Vĩnh (nam miền Nam)",
    "use_batch": false
  }' \
  --output test.wav

# Test 4: Play audio
afplay test.wav
```

## 📦 requirements-api.txt vs requirements.txt

| File | Mục đích | Có lmdeploy? | Dùng cho |
|------|----------|--------------|----------|
| `requirements-api.txt` | API cơ bản | ❌ Không | macOS, Windows, Linux CPU |
| `requirements.txt` | Full features | ✅ Có | Linux với GPU |

## ⚠️ Lưu ý quan trọng

### API vẫn hoạt động bình thường trên macOS!

- ✅ Tất cả endpoints hoạt động
- ✅ Tất cả giọng nói có sẵn
- ✅ Có thể gọi từ hệ thống thứ 3
- ⚠️ Chỉ chậm hơn so với Linux + GPU + lmdeploy

### Code đã được update

File `api_server.py` đã được cập nhật để:
- Tự động detect có lmdeploy hay không
- Fallback về backend standard nếu không có lmdeploy
- Không báo lỗi khi chạy trên macOS

```python
# Code trong api_server.py
try:
    from vieneu_tts import FastVieNeuTTS
    LMDEPLOY_AVAILABLE = True
except ImportError:
    LMDEPLOY_AVAILABLE = False
    FastVieNeuTTS = None
```

## 🚀 Muốn tốc độ nhanh hơn?

### Option 1: Sử dụng Google Colab (Khuyến nghị)

Colab có GPU miễn phí, nhanh hơn macOS CPU rất nhiều:

1. Upload `colab_notebook.ipynb` lên Colab
2. Lấy Ngrok token: https://dashboard.ngrok.com/get-started/your-authtoken
3. Chạy notebook
4. Gọi API từ macOS qua Ngrok URL

### Option 2: Sử dụng Cloud GPU

- AWS EC2 với GPU
- Google Cloud với GPU
- Azure với GPU
- RunPod, Vast.ai (rẻ hơn)

## 🐛 Troubleshooting

### Lỗi: "No module named 'vieneu_tts'"

```bash
# Cài đặt package
pip install -e .

# Hoặc từ GitHub
pip install git+https://github.com/pnnbao97/VieNeu-TTS.git
```

### Lỗi: "No module named 'utils'"

```bash
# Đảm bảo bạn đang ở thư mục gốc của project
cd /path/to/VieNeu-TTS
python api_server.py
```

### API chạy chậm

Đây là bình thường trên CPU. Để tăng tốc:
- Dùng model q4-gguf (nhẹ nhất)
- Giảm `max_batch_size` xuống 1
- Giảm độ dài văn bản
- Hoặc dùng Colab với GPU

### Port 8000 đã được sử dụng

```bash
# Chạy trên port khác
export API_PORT=8080
python api_server.py
```

## ✅ Checklist cài đặt thành công

- [ ] Virtual environment đã tạo và activate
- [ ] `pip install -r requirements-api.txt` thành công
- [ ] `python api_server.py` chạy không lỗi
- [ ] `curl http://localhost:8000/` trả về JSON
- [ ] Load model thành công
- [ ] Synthesize tạo được file WAV

## 📚 Tài liệu tham khảo

- `QUICKSTART_MACOS.md` - Hướng dẫn nhanh cho macOS
- `INSTALL.md` - Hướng dẫn cài đặt chi tiết
- `API_USAGE.md` - Chi tiết API endpoints
- `README_API.md` - Quick start và examples

## 💬 Tóm tắt

1. **Không cần lmdeploy trên macOS** - đây là bình thường
2. **Dùng `requirements-api.txt`** thay vì `requirements.txt`
3. **API vẫn hoạt động đầy đủ** chỉ chậm hơn một chút
4. **Muốn nhanh hơn?** Dùng Google Colab với GPU miễn phí

Giờ bạn có thể chạy API và gọi từ hệ thống thứ 3! 🎉
