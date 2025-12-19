# ✅ Checklist Test trên Google Colab

Làm theo checklist này để test API trên Colab thành công.

## 📋 Chuẩn bị (5 phút)

- [ ] **Có tài khoản Google** (để dùng Colab)
- [ ] **Đăng ký Ngrok** tại https://ngrok.com (miễn phí)
- [ ] **Lấy Ngrok token** tại https://dashboard.ngrok.com/get-started/your-authtoken
- [ ] **Copy token** (dạng: `2abc...xyz`) - Lưu lại để dùng

## 🚀 Setup Colab (10 phút)

### Bước 1: Upload Notebook
- [ ] Truy cập https://colab.research.google.com
- [ ] Click **File** → **Upload notebook**
- [ ] Chọn file `colab_notebook.ipynb` từ project
- [ ] Notebook đã mở thành công

### Bước 2: Chọn GPU Runtime
- [ ] Click **Runtime** → **Change runtime type**
- [ ] Chọn **Hardware accelerator**: **GPU**
- [ ] Chọn **GPU type**: **T4** (hoặc bất kỳ)
- [ ] Click **Save**
- [ ] Thấy icon GPU ở góc trên bên phải

### Bước 3: Kiểm tra GPU
- [ ] Chạy cell đầu tiên: `!nvidia-smi`
- [ ] Thấy thông tin GPU (Tesla T4 hoặc tương tự)
- [ ] Thấy CUDA version

## 📦 Cài đặt (5-10 phút)

### Bước 4: Clone Repository
- [ ] Chạy cell "Clone Repository"
- [ ] **Lưu ý:** Thay `YOUR_REPO_URL` bằng URL repo của bạn
  ```python
  # Ví dụ:
  !git clone https://github.com/username/VieNeu-TTS.git vieneu-tts
  %cd vieneu-tts
  ```
- [ ] Thấy "Cloning into 'vieneu-tts'..."
- [ ] Thấy "done."

### Bước 5: Cài đặt Dependencies
- [ ] Chạy cell "Cài đặt Dependencies"
- [ ] Đợi 5-10 phút (download và cài đặt packages)
- [ ] Thấy "Successfully installed..." ở cuối
- [ ] **Không có lỗi đỏ**

## 🌐 Setup Ngrok (2 phút)

### Bước 6: Configure Ngrok
- [ ] Chạy cell "Setup Ngrok"
- [ ] **Paste Ngrok token** của bạn vào dòng:
  ```python
  NGROK_AUTH_TOKEN = "YOUR_NGROK_AUTH_TOKEN"  # Thay bằng token
  ```
- [ ] Chạy cell
- [ ] Thấy "✅ Ngrok configured successfully!"

### Bước 7: Khởi động Server
- [ ] Chạy cell "Khởi động API Server với Ngrok"
- [ ] Đợi 5-10 giây
- [ ] Thấy **Public URL** (dạng: `https://xxxx-xx-xxx.ngrok-free.app`)
- [ ] **Copy URL này** - Rất quan trọng!
- [ ] Thấy "✅ Server is ready!"

## 🧪 Test API (5 phút)

### Bước 8: Load Model
- [ ] Chạy cell "Load Model"
- [ ] Đợi 2-5 phút (download model lần đầu)
- [ ] Thấy "✅ Model loaded successfully!"
- [ ] Thấy backend: **"LMDeploy"** (không phải "Standard")
- [ ] Thấy "using_lmdeploy": **true**

### Bước 9: Test Synthesize
- [ ] Chạy cell "Test API - Synthesize Speech"
- [ ] Đợi vài giây
- [ ] Thấy "✅ Speech synthesized successfully!"
- [ ] Thấy audio player xuất hiện
- [ ] **Click play** và nghe thử
- [ ] Audio nghe rõ ràng, không bị lỗi

### Bước 10: Test Base64
- [ ] Chạy cell "Test API - Get Base64 Audio"
- [ ] Thấy "✅ Speech synthesized successfully!"
- [ ] Thấy duration và sample rate
- [ ] Audio player xuất hiện và play được

## 🖥️ Test từ máy Local (5 phút)

### Bước 11: Test từ Terminal
Mở terminal trên máy Mac và chạy:

```bash
# Thay YOUR_NGROK_URL bằng URL từ Colab
export API_URL="https://xxxx-xx-xxx.ngrok-free.app"

# Test health check
curl $API_URL/
```

- [ ] Thấy response JSON với "message": "VieNeu-TTS API Server"

### Bước 12: Test Synthesize từ Mac
```bash
curl -X POST "$API_URL/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Xin chào từ máy Mac!",
    "voice": "Vĩnh (nam miền Nam)",
    "use_batch": true
  }' \
  --output test_from_mac.wav

# Play audio
afplay test_from_mac.wav
```

- [ ] File `test_from_mac.wav` được tạo
- [ ] Audio play được và nghe rõ

### Bước 13: Test với Python
```python
import requests

API_URL = "https://xxxx.ngrok-free.app"  # Thay URL

response = requests.post(
    f"{API_URL}/synthesize",
    json={
        "text": "Test từ Python!",
        "voice": "Vĩnh (nam miền Nam)"
    }
)

with open("test_python.wav", "wb") as f:
    f.write(response.content)

print("✅ Saved!")
```

- [ ] Script chạy không lỗi
- [ ] File `test_python.wav` được tạo
- [ ] Audio nghe được

### Bước 14: Test Suite
```bash
python test_api.py https://xxxx.ngrok-free.app
```

- [ ] Tất cả tests PASS
- [ ] Không có lỗi đỏ
- [ ] Thấy "Total: X/X tests passed (100%)"

## 📊 Kiểm tra Performance

### Bước 15: Check Speed
- [ ] Synthesize một đoạn văn dài (~500 ký tự)
- [ ] Xem thời gian xử lý trong response
- [ ] Tốc độ nên là **5-10x realtime** (với GPU)
- [ ] Ví dụ: Audio 10s → Xử lý trong 1-2s

### Bước 16: Check Backend
```bash
curl $API_URL/status
```

- [ ] "model_loaded": **true**
- [ ] "using_lmdeploy": **true** (quan trọng!)
- [ ] "backbone": "VieNeu-TTS (GPU)"
- [ ] "device": "Auto" hoặc "CUDA"

## 🎯 Integration Test

### Bước 17: Test từ Web App (Optional)
Tạo file HTML đơn giản:

```html
<!DOCTYPE html>
<html>
<body>
  <button onclick="test()">Test TTS</button>
  <script>
    async function test() {
      const response = await fetch('https://xxxx.ngrok-free.app/synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: 'Test từ web!',
          voice: 'Vĩnh (nam miền Nam)'
        })
      });
      const blob = await response.blob();
      const audio = new Audio(URL.createObjectURL(blob));
      audio.play();
    }
  </script>
</body>
</html>
```

- [ ] Mở file HTML trong browser
- [ ] Click button
- [ ] Audio play được

## ✅ Kết quả mong đợi

Sau khi hoàn thành checklist:

- ✅ API chạy trên Colab với GPU
- ✅ Có public URL qua Ngrok
- ✅ Backend sử dụng LMDeploy (nhanh)
- ✅ Gọi được từ máy Mac
- ✅ Gọi được từ Python
- ✅ Gọi được từ web browser
- ✅ Tốc độ 5-10x realtime
- ✅ Audio chất lượng tốt

## ⚠️ Troubleshooting

### Không thấy GPU
- [ ] Kiểm tra Runtime → Change runtime type → GPU
- [ ] Restart runtime và thử lại
- [ ] Có thể hết quota GPU (chờ hoặc dùng Colab Pro)

### Ngrok không kết nối
- [ ] Kiểm tra token đã paste đúng chưa
- [ ] Token còn hạn không (lấy token mới)
- [ ] Restart cell và thử lại

### Model load lâu
- [ ] Lần đầu download model (~2-3GB) mất 5-10 phút
- [ ] Lần sau nhanh hơn (đã cache)
- [ ] Kiểm tra internet connection

### Backend không phải LMDeploy
- [ ] Kiểm tra đã chọn GPU runtime chưa
- [ ] Kiểm tra lmdeploy đã cài đặt chưa
- [ ] Xem logs có lỗi gì không

### API chậm
- [ ] Kiểm tra backend có phải "LMDeploy" không
- [ ] Kiểm tra "using_lmdeploy": true
- [ ] Tăng max_batch_size lên 10-12
- [ ] Bật enable_triton: true

## 📝 Notes

- **Ngrok URL thay đổi** mỗi lần restart Colab
- **Session timeout** sau 12 giờ (free tier)
- **GPU quota** có giới hạn (free tier)
- **Model cache** trong session, restart sẽ mất

## 🎉 Hoàn thành!

Nếu tất cả checkboxes đều ✅, bạn đã thành công!

Giờ bạn có thể:
- Gọi API từ bất kỳ hệ thống nào
- Integrate vào web/mobile app
- Demo cho khách hàng
- Develop features mới

## 📞 Next Steps

1. **Save Ngrok URL** để dùng
2. **Integrate vào app** của bạn
3. **Test với traffic thật**
4. **Consider Colab Pro** nếu cần ổn định hơn
5. **Deploy production** khi ready

---

**Chúc mừng! Bạn đã setup thành công API trên Colab! 🎉**
