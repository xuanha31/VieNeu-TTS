# VieNeu-TTS API - Hướng dẫn đầy đủ

> Tài liệu tổng hợp đầy đủ về VieNeu-TTS API

**Phiên bản:** 1.0.0  
**Ngày cập nhật:** 2024

---

## 📑 Mục lục

1. [Bắt đầu nhanh](#1-bắt-đầu-nhanh)
2. [Test trên Google Colab](#2-test-trên-google-colab)
3. [Chạy trên macOS](#3-chạy-trên-macos)
4. [Fix lỗi cài đặt macOS](#4-fix-lỗi-cài-đặt-macos)
5. [Hướng dẫn cài đặt đầy đủ](#5-hướng-dẫn-cài-đặt-đầy-đủ)
6. [API Documentation](#6-api-documentation)
7. [Checklist test Colab](#7-checklist-test-colab)
8. [Tổng hợp files](#8-tổng-hợp-files)

---


# 1. Bắt đầu nhanh

## 📋 Tổng quan

Bạn có 2 cách để chạy API:

1. **Google Colab** (Khuyến nghị để test) - Có GPU miễn phí, nhanh
2. **macOS Local** - Chạy trên máy của bạn, chậm hơn nhưng ổn định

## 🎯 Option 1: Test trên Google Colab (Khuyến nghị)

### Tại sao chọn Colab?
- ✅ GPU T4 miễn phí
- ✅ Nhanh hơn CPU 5-10 lần
- ✅ Không cần cài đặt gì trên máy
- ✅ Có lmdeploy (tối ưu tốc độ)
- ✅ Gọi từ bất kỳ đâu qua Ngrok

### Các bước:

1. Upload notebook lên Colab
   - Truy cập: https://colab.research.google.com
   - File → Upload notebook
   - Chọn file `colab_notebook.ipynb`

2. Lấy Ngrok token
   - Đăng ký miễn phí: https://ngrok.com
   - Lấy token: https://dashboard.ngrok.com/get-started/your-authtoken

3. Chạy notebook
   - Runtime → Change runtime type → **GPU**
   - Chạy các cell theo thứ tự
   - Paste Ngrok token khi được hỏi
   - Copy public URL (dạng: `https://xxxx.ngrok-free.app`)

4. Test API
```bash
python test_api.py https://xxxx.ngrok-free.app
```

## 💻 Option 2: Chạy trên macOS Local

### Tại sao chọn Local?
- ✅ Không cần internet
- ✅ Ổn định, không timeout
- ✅ Không giới hạn thời gian
- ⚠️ Chậm hơn (CPU only)
- ⚠️ Không có lmdeploy

### Các bước:

```bash
# 1. Cài đặt
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-api.txt

# 2. Chạy API
python api_server.py

# 3. Test (terminal mới)
python test_api.py
```

## 🔥 Quick Commands

### Gọi API từ Python
```python
import requests

API_URL = "http://localhost:8000"  # Hoặc Ngrok URL

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


# 2. Test trên Google Colab

## 🚀 Quick Start

### Bước 1: Mở Google Colab
1. Truy cập: https://colab.research.google.com
2. Chọn **File** → **Upload notebook**
3. Upload file `colab_notebook.ipynb`

### Bước 2: Lấy Ngrok Token
1. Đăng ký tài khoản miễn phí tại: https://ngrok.com
2. Đăng nhập và truy cập: https://dashboard.ngrok.com/get-started/your-authtoken
3. Copy auth token (dạng: `2abc...xyz`)

### Bước 3: Chạy Notebook
1. Chọn Runtime → Change runtime type → **GPU** (T4)
2. Chạy các cell theo thứ tự
3. Khi đến cell "Setup Ngrok", paste token của bạn
4. Copy public URL (dạng: `https://xxxx-xx-xxx.ngrok-free.app`)

### Bước 4: Test API

```bash
export API_URL="https://xxxx-xx-xxx.ngrok-free.app"

# Test health check
curl $API_URL/

# Load model
curl -X POST "$API_URL/load_model" \
  -H "Content-Type: application/json" \
  -d '{
    "backbone": "VieNeu-TTS (GPU)",
    "codec": "NeuCodec (Standard)",
    "device": "Auto",
    "enable_triton": true,
    "max_batch_size": 8
  }'

# Synthesize
curl -X POST "$API_URL/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Xin chào từ Google Colab!",
    "voice": "Vĩnh (nam miền Nam)",
    "use_batch": true
  }' \
  --output test_colab.wav

# Play audio
afplay test_colab.wav  # macOS
```

## 🐍 Test từ Python

```python
import requests

API_URL = "https://xxxx-xx-xxx.ngrok-free.app"

# Load model
response = requests.post(
    f"{API_URL}/load_model",
    json={
        "backbone": "VieNeu-TTS (GPU)",
        "codec": "NeuCodec (Standard)",
        "device": "Auto",
        "enable_triton": True,
        "max_batch_size": 8
    }
)
print(response.json())

# Synthesize
response = requests.post(
    f"{API_URL}/synthesize",
    json={
        "text": "Đây là test từ Google Colab với GPU!",
        "voice": "Vĩnh (nam miền Nam)",
        "use_batch": True
    }
)

with open("output_colab.wav", "wb") as f:
    f.write(response.content)
```

## ⚠️ Lưu ý quan trọng

1. **Ngrok URL thay đổi** mỗi lần restart Colab
2. **Session timeout** sau 12 giờ (free tier)
3. **GPU quota** có giới hạn
4. **Model download** lần đầu mất 5-10 phút

## 🔧 Troubleshooting

### Lỗi: "Runtime disconnected"
- Colab timeout hoặc hết quota
- Restart runtime và chạy lại

### Lỗi: "CUDA out of memory"
- Giảm `max_batch_size` xuống 4-6
- Hoặc dùng model q8-gguf

### API chậm
- Kiểm tra đã chọn GPU runtime chưa
- Kiểm tra backend có phải "LMDeploy" không

---


# 3. Chạy trên macOS

## Bước 1: Cài đặt

```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies (không bao gồm lmdeploy)
pip install -r requirements-api.txt
```

## Bước 2: Cài đặt VieNeuTTS package

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

## Python Example

```python
import requests

API_URL = "http://localhost:8000"

# Load model
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

# Synthesize
response = requests.post(
    f"{API_URL}/synthesize",
    json={
        "text": "Xin chào từ macOS!",
        "voice": "Vĩnh (nam miền Nam)",
        "use_batch": False
    }
)

with open("output.wav", "wb") as f:
    f.write(response.content)

# Play audio
import os
os.system("afplay output.wav")
```

## 💡 Cấu hình tốt nhất cho macOS

```json
{
  "backbone": "VieNeu-TTS-q4-gguf",
  "codec": "NeuCodec ONNX (Fast CPU)",
  "device": "CPU",
  "enable_triton": false,
  "max_batch_size": 1
}
```

## Troubleshooting

### Lỗi: "No module named 'vieneu_tts'"
```bash
pip install -e .
```

### Lỗi: "No matching distribution found for lmdeploy"
```bash
pip install -r requirements-api.txt
```

### API chạy chậm
- Sử dụng model q4-gguf (nhẹ nhất)
- Giảm `max_batch_size` xuống 1
- Hoặc dùng Colab với GPU

---


# 4. Fix lỗi cài đặt macOS

## Vấn đề

```
ERROR: Could not find a version that satisfies the requirement lmdeploy==0.11.0
ERROR: No matching distribution found for lmdeploy==0.11.0
```

## Nguyên nhân

`lmdeploy` chỉ hỗ trợ Linux với CUDA. Package này **không có** trên macOS.

## ✅ Giải pháp

### Cách 1: Sử dụng requirements-api.txt (Khuyến nghị)

```bash
# Xóa virtual environment cũ
rm -rf venv

# Tạo mới
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies KHÔNG có lmdeploy
pip install -r requirements-api.txt

# Cài đặt VieNeuTTS package
pip install -e .
```

### Cách 2: Chỉnh sửa requirements.txt gốc

```bash
# Comment dòng lmdeploy
sed -i.bak '/lmdeploy/d' requirements.txt

# Cài đặt
pip install -r requirements.txt
```

## 🚀 Hướng dẫn cài đặt đầy đủ

```bash
# 1. Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Upgrade pip
pip install --upgrade pip

# 3. Cài đặt dependencies
pip install -r requirements-api.txt

# 4. Kiểm tra
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"

# 5. Chạy API
python api_server.py
```

## 📦 requirements-api.txt vs requirements.txt

| File | Mục đích | Có lmdeploy? | Dùng cho |
|------|----------|--------------|----------|
| `requirements-api.txt` | API cơ bản | ❌ Không | macOS, Windows, Linux CPU |
| `requirements.txt` | Full features | ✅ Có | Linux với GPU |

## ⚠️ Lưu ý

### API vẫn hoạt động bình thường trên macOS!

- ✅ Tất cả endpoints hoạt động
- ✅ Tất cả giọng nói có sẵn
- ✅ Có thể gọi từ hệ thống thứ 3
- ⚠️ Chỉ chậm hơn so với Linux + GPU + lmdeploy

### Code đã được update

```python
# api_server.py tự động detect lmdeploy
try:
    from vieneu_tts import FastVieNeuTTS
    LMDEPLOY_AVAILABLE = True
except ImportError:
    LMDEPLOY_AVAILABLE = False
    FastVieNeuTTS = None
```

## 🚀 Muốn tốc độ nhanh hơn?

### Option 1: Google Colab (Khuyến nghị)
- GPU miễn phí
- Nhanh hơn 5-10 lần
- Upload `colab_notebook.ipynb` lên Colab

### Option 2: Cloud GPU
- AWS EC2 với GPU
- Google Cloud với GPU
- Azure với GPU

## ✅ Checklist

- [ ] Virtual environment đã tạo
- [ ] `pip install -r requirements-api.txt` thành công
- [ ] `python api_server.py` chạy không lỗi
- [ ] `curl http://localhost:8000/` trả về JSON
- [ ] Load model thành công
- [ ] Synthesize tạo được file WAV

---


# 5. Hướng dẫn cài đặt đầy đủ

## Cài đặt cho macOS / Windows (CPU)

```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# hoặc venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements-api.txt

# Cài đặt VieNeuTTS
pip install -e .

# Chạy API
python api_server.py
```

## Cài đặt cho Linux với GPU

```bash
# Cài đặt CUDA Toolkit trước
nvidia-smi  # Kiểm tra GPU

# Tạo virtual environment
python -m venv venv
source venv/bin/activate

# Cài đặt PyTorch với CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Cài đặt tất cả dependencies (bao gồm lmdeploy)
pip install -r requirements.txt

# Chạy API
python api_server.py
```

## Cài đặt cho Google Colab

1. Upload `colab_notebook.ipynb` lên Colab
2. Chạy các cell theo thứ tự
3. Lấy Ngrok token và paste vào
4. Copy public URL

## Kiểm tra cài đặt

```bash
# Test API
curl http://localhost:8000/

# Chạy test suite
python test_api.py
```

## Cấu hình khuyến nghị

### Máy tính cá nhân (CPU)
```json
{
  "backbone": "VieNeu-TTS-q4-gguf",
  "codec": "NeuCodec ONNX (Fast CPU)",
  "device": "CPU",
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


# 6. API Documentation

## Base URL

- **Local**: `http://localhost:8000`
- **Colab + Ngrok**: `https://xxxx.ngrok-free.app`

## Endpoints

### 1. GET `/` - Health Check
Kiểm tra server hoạt động

**Response:**
```json
{
  "message": "VieNeu-TTS API Server",
  "version": "1.0.0"
}
```

### 2. GET `/status` - Get Status
Lấy thông tin trạng thái server

**Response:**
```json
{
  "status": "running",
  "model_loaded": true,
  "backbone": "VieNeu-TTS (GPU)",
  "using_lmdeploy": true,
  "available_voices": [...]
}
```

### 3. GET `/voices` - List Voices
Danh sách giọng mẫu có sẵn

### 4. POST `/load_model` - Load Model
Load model TTS (bắt buộc gọi trước)

**Request:**
```json
{
  "backbone": "VieNeu-TTS (GPU)",
  "codec": "NeuCodec (Standard)",
  "device": "Auto",
  "enable_triton": true,
  "max_batch_size": 8
}
```

**Backbone options:**
- `"VieNeu-TTS (GPU)"` - Chất lượng cao, cần GPU
- `"VieNeu-TTS-q8-gguf"` - Cân bằng
- `"VieNeu-TTS-q4-gguf"` - Nhẹ nhất, phù hợp CPU

**Codec options:**
- `"NeuCodec (Standard)"` - Codec chuẩn
- `"NeuCodec ONNX (Fast CPU)"` - Tối ưu CPU

### 5. POST `/synthesize` - Synthesize Speech
Chuyển văn bản thành giọng nói

**Request:**
```json
{
  "text": "Xin chào!",
  "voice": "Vĩnh (nam miền Nam)",
  "use_batch": true
}
```

**Response:** File WAV audio

**Example (Python):**
```python
response = requests.post(
    "http://localhost:8000/synthesize",
    json={
        "text": "Xin chào!",
        "voice": "Vĩnh (nam miền Nam)"
    }
)

with open("output.wav", "wb") as f:
    f.write(response.content)
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Xin chào!", "voice": "Vĩnh (nam miền Nam)"}' \
  --output output.wav
```

### 6. POST `/synthesize_base64` - Synthesize (Base64)
Trả về audio dưới dạng base64

**Response:**
```json
{
  "status": "success",
  "audio_base64": "UklGRiQAAABXQVZF...",
  "sample_rate": 24000,
  "duration": 2.5
}
```

### 7. POST `/synthesize_custom` - Custom Voice
Synthesize với giọng mẫu tùy chỉnh

**Request (multipart/form-data):**
- `text`: Văn bản cần chuyển đổi
- `ref_text`: Lời thoại của audio mẫu
- `ref_audio`: File audio mẫu (.wav)

**Example:**
```python
with open("my_voice.wav", "rb") as audio_file:
    response = requests.post(
        "http://localhost:8000/synthesize_custom",
        data={
            "text": "Đây là giọng tùy chỉnh",
            "ref_text": "Xin chào, tôi là người mẫu"
        },
        files={"ref_audio": audio_file}
    )
```

## Available Voices

- **Nam miền Bắc**: Tuyên, Bình
- **Nam miền Nam**: Vĩnh, Nguyên, Sơn
- **Nữ miền Bắc**: Ngọc, Ly, Hương
- **Nữ miền Nam**: Đoan, Dung

## Error Codes

- `400` - Bad Request (thiếu parameters)
- `500` - Internal Server Error

## Best Practices

1. **Load model trước**: Luôn gọi `/load_model` trước
2. **Batch processing**: Bật `use_batch=true` với GPU
3. **Giới hạn text**: Không quá 3000 ký tự
4. **Reuse connection**: Dùng session
5. **Error handling**: Kiểm tra status code

## Interactive Docs

Khi server chạy:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---


# 7. Checklist test Colab

## 📋 Chuẩn bị (5 phút)

- [ ] Có tài khoản Google
- [ ] Đăng ký Ngrok tại https://ngrok.com
- [ ] Lấy Ngrok token tại https://dashboard.ngrok.com/get-started/your-authtoken
- [ ] Copy token (dạng: `2abc...xyz`)

## 🚀 Setup Colab (10 phút)

### Bước 1: Upload Notebook
- [ ] Truy cập https://colab.research.google.com
- [ ] Click **File** → **Upload notebook**
- [ ] Chọn file `colab_notebook.ipynb`
- [ ] Notebook đã mở thành công

### Bước 2: Chọn GPU Runtime
- [ ] Click **Runtime** → **Change runtime type**
- [ ] Chọn **Hardware accelerator**: **GPU**
- [ ] Chọn **GPU type**: **T4**
- [ ] Click **Save**

### Bước 3: Kiểm tra GPU
- [ ] Chạy cell: `!nvidia-smi`
- [ ] Thấy thông tin GPU (Tesla T4)
- [ ] Thấy CUDA version

## 📦 Cài đặt (5-10 phút)

### Bước 4: Clone Repository
- [ ] Chạy cell "Clone Repository"
- [ ] Thay `YOUR_REPO_URL` bằng URL repo
- [ ] Thấy "Cloning into 'vieneu-tts'..."
- [ ] Thấy "done."

### Bước 5: Cài đặt Dependencies
- [ ] Chạy cell "Cài đặt Dependencies"
- [ ] Đợi 5-10 phút
- [ ] Thấy "Successfully installed..."
- [ ] Không có lỗi đỏ

## 🌐 Setup Ngrok (2 phút)

### Bước 6: Configure Ngrok
- [ ] Chạy cell "Setup Ngrok"
- [ ] Paste Ngrok token vào code
- [ ] Thấy "✅ Ngrok configured successfully!"

### Bước 7: Khởi động Server
- [ ] Chạy cell "Khởi động API Server"
- [ ] Đợi 5-10 giây
- [ ] Thấy **Public URL** (https://xxxx.ngrok-free.app)
- [ ] **Copy URL này**
- [ ] Thấy "✅ Server is ready!"

## 🧪 Test API (5 phút)

### Bước 8: Load Model
- [ ] Chạy cell "Load Model"
- [ ] Đợi 2-5 phút (download model lần đầu)
- [ ] Thấy "✅ Model loaded successfully!"
- [ ] Backend: **"LMDeploy"** (không phải "Standard")
- [ ] "using_lmdeploy": **true**

### Bước 9: Test Synthesize
- [ ] Chạy cell "Test Synthesize"
- [ ] Thấy "✅ Speech synthesized successfully!"
- [ ] Audio player xuất hiện
- [ ] Click play và nghe thử
- [ ] Audio nghe rõ ràng

### Bước 10: Test từ máy Mac
```bash
export API_URL="https://xxxx.ngrok-free.app"
curl $API_URL/
```
- [ ] Thấy response JSON

### Bước 11: Test Synthesize từ Mac
```bash
curl -X POST "$API_URL/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Test!", "voice": "Vĩnh (nam miền Nam)"}' \
  --output test.wav

afplay test.wav
```
- [ ] File WAV được tạo
- [ ] Audio play được

### Bước 12: Test Suite
```bash
python test_api.py https://xxxx.ngrok-free.app
```
- [ ] Tất cả tests PASS
- [ ] Không có lỗi
- [ ] "Total: X/X tests passed (100%)"

## ✅ Kết quả mong đợi

- ✅ API chạy trên Colab với GPU
- ✅ Có public URL qua Ngrok
- ✅ Backend sử dụng LMDeploy
- ✅ Gọi được từ máy Mac
- ✅ Tốc độ 5-10x realtime
- ✅ Audio chất lượng tốt

## ⚠️ Troubleshooting

### Không thấy GPU
- Kiểm tra Runtime → Change runtime type → GPU
- Restart runtime và thử lại

### Ngrok không kết nối
- Kiểm tra token đã paste đúng
- Lấy token mới nếu hết hạn

### Model load lâu
- Lần đầu download ~2-3GB mất 5-10 phút
- Lần sau nhanh hơn (đã cache)

### Backend không phải LMDeploy
- Kiểm tra đã chọn GPU runtime
- Xem logs có lỗi gì không

---


# 8. Tổng hợp files

## 📁 Files chính

### API Server
- **api_server.py** - FastAPI server với 7 endpoints
- **colab_notebook.ipynb** - Notebook cho Colab + Ngrok
- **test_api.py** - Test suite tự động

### Dependencies
- **requirements.txt** - Full dependencies (có lmdeploy, cho Linux GPU)
- **requirements-api.txt** - Dependencies cơ bản (không có lmdeploy, cho macOS/CPU)

### Documentation
- **API_COMPLETE_GUIDE.md** - File này - Tổng hợp tất cả
- **START_HERE.md** - Bắt đầu từ đây
- **TEST_ON_COLAB.md** - Hướng dẫn test trên Colab
- **QUICKSTART_MACOS.md** - Quick start cho macOS
- **FIX_MACOS_INSTALL.md** - Fix lỗi lmdeploy
- **API_USAGE.md** - Chi tiết API endpoints
- **README_API.md** - Quick start và examples
- **INSTALL.md** - Hướng dẫn cài đặt đầy đủ
- **COLAB_CHECKLIST.md** - Checklist test Colab
- **API_FILES_SUMMARY.md** - Tổng hợp files

### Scripts
- **install_api.sh** - Script cài đặt tự động

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

## 💡 Tips

### Cho macOS/CPU:
- Dùng `requirements-api.txt`
- Model: `VieNeu-TTS-q4-gguf`
- Codec: `NeuCodec ONNX (Fast CPU)`
- `max_batch_size`: 1-2

### Cho Linux/GPU:
- Dùng `requirements.txt`
- Model: `VieNeu-TTS (GPU)`
- Codec: `NeuCodec (Standard)`
- `max_batch_size`: 8-12
- `enable_triton`: true

### Cho Google Colab:
- Dùng notebook có sẵn
- GPU T4 miễn phí
- Dùng Ngrok để expose
- Model: `VieNeu-TTS (GPU)`

## 🚀 Quick Commands

### Colab
```bash
python test_api.py https://xxxx.ngrok-free.app
```

### macOS
```bash
# Terminal 1
python api_server.py

# Terminal 2
python test_api.py
```

### Python
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

## 📊 Performance

| Environment | Speed | Setup Time |
|-------------|-------|------------|
| Google Colab (GPU) | 5-10x realtime | 10 min |
| macOS (CPU) | 0.5-1x realtime | 5 min |
| Linux + GPU | 5-10x realtime | 15 min |

## ⚠️ Lưu ý

1. **Luôn gọi `/load_model` trước** khi synthesize
2. **macOS không có lmdeploy** - đây là bình thường
3. **Colab có GPU miễn phí** - nhanh hơn nhiều
4. **Ngrok URL thay đổi** mỗi lần restart (free tier)
5. **Model cần download** lần đầu (2-3GB, 5-10 phút)

## 🔗 Links

- API Docs (local): http://localhost:8000/docs
- Ngrok Dashboard: https://dashboard.ngrok.com
- Colab: https://colab.research.google.com

## ✅ Checklist tổng hợp

### Để test trên Colab:
- [ ] Có tài khoản Google
- [ ] Đăng ký Ngrok
- [ ] Lấy Ngrok token
- [ ] Upload `colab_notebook.ipynb`
- [ ] Chọn GPU runtime
- [ ] Chạy các cell
- [ ] Copy Ngrok URL
- [ ] Test từ máy Mac

### Để chạy trên macOS:
- [ ] Cài Python 3.8+
- [ ] Tạo virtual environment
- [ ] Cài `requirements-api.txt`
- [ ] Chạy `python api_server.py`
- [ ] Test với `python test_api.py`

---

## 🎉 Kết luận

Bạn đã có:
- ✅ API server hoàn chỉnh
- ✅ Colab notebook với Ngrok
- ✅ Documentation đầy đủ
- ✅ Test suite tự động
- ✅ Hỗ trợ macOS/Linux/Windows/Colab

**Bắt đầu ngay:**
- Colab: Upload `colab_notebook.ipynb`
- macOS: `pip install -r requirements-api.txt`

**Cần giúp đỡ:**
- Đọc phần tương ứng trong file này
- Hoặc xem các file MD riêng lẻ

**Chúc bạn thành công! 🚀**

---

*Tài liệu này tổng hợp từ 10+ files MD riêng lẻ để bạn dễ theo dõi.*
