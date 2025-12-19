# Test VieNeu-TTS API trên Google Colab

Hướng dẫn test API trên Google Colab với GPU và Ngrok.

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

Sau khi có public URL, test từ máy local:

```bash
# Thay YOUR_NGROK_URL bằng URL từ Colab
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
# hoặc
vlc test_colab.wav     # Linux/Windows
```

## 🐍 Test từ Python

```python
import requests

API_URL = "https://xxxx-xx-xxx.ngrok-free.app"  # Thay bằng URL của bạn

# 1. Load model
print("Loading model...")
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

# 2. Synthesize
print("\nSynthesizing...")
response = requests.post(
    f"{API_URL}/synthesize",
    json={
        "text": "Đây là test từ Google Colab với GPU!",
        "voice": "Vĩnh (nam miền Nam)",
        "use_batch": True
    }
)

# 3. Save audio
with open("output_colab.wav", "wb") as f:
    f.write(response.content)

print("✅ Saved to output_colab.wav")
```

## 📊 So sánh tốc độ

### macOS CPU (không có lmdeploy)
```json
{
  "backbone": "VieNeu-TTS-q4-gguf",
  "codec": "NeuCodec ONNX (Fast CPU)",
  "device": "CPU",
  "max_batch_size": 2
}
```
⏱️ Tốc độ: ~0.5-1x realtime (chậm)

### Google Colab GPU T4 (có lmdeploy)
```json
{
  "backbone": "VieNeu-TTS (GPU)",
  "codec": "NeuCodec (Standard)",
  "device": "Auto",
  "enable_triton": true,
  "max_batch_size": 8
}
```
⏱️ Tốc độ: ~5-10x realtime (nhanh) 🚀

## 🧪 Test Suite trên Colab

Chạy test suite từ máy local với Ngrok URL:

```bash
python test_api.py https://xxxx-xx-xxx.ngrok-free.app
```

## 📝 Checklist Test

- [ ] Colab đã chọn GPU runtime
- [ ] Ngrok token đã setup
- [ ] Public URL đã copy
- [ ] Health check thành công (`GET /`)
- [ ] Load model thành công (`POST /load_model`)
- [ ] Synthesize thành công (`POST /synthesize`)
- [ ] File audio tạo ra nghe được
- [ ] Backend hiển thị "LMDeploy" (không phải "Standard")

## ⚠️ Lưu ý quan trọng

### 1. Ngrok URL thay đổi mỗi lần restart
- Free tier của Ngrok tạo URL ngẫu nhiên
- Mỗi lần restart Colab, URL sẽ khác
- Cần copy URL mới mỗi lần

### 2. Colab session timeout
- Free tier: 12 giờ
- Sau đó cần restart và lấy URL mới

### 3. GPU quota
- Colab free có giới hạn GPU
- Nếu hết quota, chờ hoặc dùng Colab Pro

### 4. Model download
- Lần đầu chạy sẽ download model (~2-3GB)
- Mất 5-10 phút
- Lần sau nhanh hơn (đã cache)

## 🔧 Troubleshooting

### Lỗi: "Runtime disconnected"
- Colab timeout hoặc hết quota
- Restart runtime và chạy lại

### Lỗi: "Ngrok tunnel not found"
- Token sai hoặc hết hạn
- Lấy token mới từ dashboard

### Lỗi: "CUDA out of memory"
- Giảm `max_batch_size` xuống 4-6
- Hoặc dùng model q8-gguf

### API chậm
- Kiểm tra đã chọn GPU runtime chưa
- Kiểm tra backend có phải "LMDeploy" không
- Kiểm tra `enable_triton` có `true` không

### Không synthesize được
- Kiểm tra đã load model chưa
- Xem logs trong Colab
- Test với văn bản ngắn trước

## 📱 Gọi từ Mobile/Web App

Sau khi có Ngrok URL, bạn có thể gọi từ:

### JavaScript/React
```javascript
const API_URL = 'https://xxxx-xx-xxx.ngrok-free.app';

async function synthesize(text) {
  const response = await fetch(`${API_URL}/synthesize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: text,
      voice: 'Vĩnh (nam miền Nam)',
      use_batch: true
    })
  });
  
  const blob = await response.blob();
  const audio = new Audio(URL.createObjectURL(blob));
  audio.play();
}
```

### Flutter/Dart
```dart
import 'package:http/http.dart' as http;

Future<void> synthesize(String text) async {
  final response = await http.post(
    Uri.parse('https://xxxx-xx-xxx.ngrok-free.app/synthesize'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'text': text,
      'voice': 'Vĩnh (nam miền Nam)',
      'use_batch': true,
    }),
  );
  
  // Save or play audio
  final bytes = response.bodyBytes;
}
```

## 🎯 Use Cases

### 1. Development/Testing
- Test API trên GPU mà không cần máy GPU
- Prototype nhanh
- Demo cho khách hàng

### 2. Production (tạm thời)
- MVP/POC
- Traffic thấp
- Chưa có budget cho server

### 3. Backup
- Khi server chính down
- Khi cần scale nhanh

## 💡 Tips

### Tăng tốc độ
- Bật `enable_triton=true`
- Tăng `max_batch_size` lên 10-12
- Dùng `use_batch=true` khi synthesize

### Tiết kiệm quota
- Chỉ chạy khi cần
- Disconnect khi không dùng
- Dùng model nhẹ hơn (q8-gguf)

### Ổn định hơn
- Upgrade Colab Pro ($10/tháng)
- Hoặc deploy lên cloud (AWS/GCP/Azure)

## 🔗 Links hữu ích

- Colab: https://colab.research.google.com
- Ngrok: https://ngrok.com
- Ngrok Dashboard: https://dashboard.ngrok.com
- API Docs: `https://your-ngrok-url.ngrok-free.app/docs`

## ✅ Kết luận

Google Colab + Ngrok là giải pháp tốt để:
- ✅ Test API với GPU miễn phí
- ✅ Không cần cài đặt local
- ✅ Gọi từ bất kỳ đâu qua internet
- ✅ Nhanh hơn CPU rất nhiều (5-10x)

Nhược điểm:
- ⚠️ URL thay đổi mỗi lần restart
- ⚠️ Session timeout sau 12h
- ⚠️ Có giới hạn GPU quota

Để production, nên deploy lên cloud server riêng! 🚀
