# Hướng dẫn sử dụng Models đã Download

## 1. Download Models

### Download tất cả models:
```bash
python download_models.py
```

### Download chỉ một số models cụ thể:
```bash
# Chỉ download backbone PyTorch và codec standard
python download_models.py --models backbone-pytorch codec-standard

# Download backbone Q4 (nhẹ cho CPU)
python download_models.py --models backbone-q4 codec-onnx
```

### Xem danh sách models:
```bash
python download_models.py --list
```

### Download lại (force):
```bash
python download_models.py --force
```

## 2. Cấu trúc thư mục sau khi download

```
VieNeu-TTS/
├── models_backup/
│   ├── backbone-pytorch/      # pnnbao-ump/VieNeu-TTS
│   ├── backbone-q4/           # pnnbao-ump/VieNeu-TTS-q4-gguf
│   ├── backbone-q8/           # pnnbao-ump/VieNeu-TTS-q8-gguf
│   ├── codec-standard/        # neuphonic/neucodec
│   ├── codec-distill/         # neuphonic/distill-neucodec
│   └── codec-onnx/            # neuphonic/neucodec-onnx-decoder
├── download_models.py
└── ...
```

## 3. Sử dụng Models Local

### A. Trong code Python

**Trước (dùng Hugging Face):**
```python
from vieneu_tts import VieNeuTTS

tts = VieNeuTTS(
    backbone_repo="pnnbao-ump/VieNeu-TTS",
    codec_repo="neuphonic/neucodec"
)
```

**Sau (dùng local):**
```python
from vieneu_tts import VieNeuTTS

tts = VieNeuTTS(
    backbone_repo="./models_backup/backbone-pytorch",
    codec_repo="./models_backup/codec-standard"
)
```

### B. Sửa file config.yaml

Mở file `config.yaml` và thay đổi:

**Trước:**
```yaml
backbone_configs:
  "VieNeu-TTS (GPU)":
    repo: pnnbao-ump/VieNeu-TTS
    supports_streaming: false
    description: Chất lượng cao nhất, yêu cầu GPU
```

**Sau:**
```yaml
backbone_configs:
  "VieNeu-TTS (GPU)":
    repo: ./models_backup/backbone-pytorch
    supports_streaming: false
    description: Chất lượng cao nhất, yêu cầu GPU
```

Tương tự cho các models khác:
```yaml
backbone_configs:
  "VieNeu-TTS (GPU)":
    repo: ./models_backup/backbone-pytorch
    supports_streaming: false
    description: Chất lượng cao nhất, yêu cầu GPU
  "VieNeu-TTS-q8-gguf":
    repo: ./models_backup/backbone-q8
    supports_streaming: true
    description: Cân bằng giữa chất lượng và tốc độ
  "VieNeu-TTS-q4-gguf":
    repo: ./models_backup/backbone-q4
    supports_streaming: true
    description: Nhẹ nhất, phù hợp CPU

codec_configs:
  "NeuCodec (Standard)":
    repo: ./models_backup/codec-standard
    description: Codec chuẩn, tốc độ trung bình
    use_preencoded: false
  "NeuCodec ONNX (Fast CPU)":
    repo: ./models_backup/codec-onnx
    description: Tối ưu cho CPU, cần pre-encoded codes
    use_preencoded: true
```

### C. Sử dụng với main.py

Sửa file `main.py`:

```python
def main(
    backbone="./models_backup/backbone-q4",  # Thay đổi ở đây
    codec="./models_backup/codec-onnx"       # Thay đổi ở đây
):
    # ... code còn lại giữ nguyên
```

### D. Sử dụng với gradio_app.py

Sau khi sửa `config.yaml` như trên, chạy bình thường:
```bash
python gradio_app.py
```

## 4. Backup và Restore

### Backup models:
```bash
# Nén thư mục models_backup
tar -czf vieneu_tts_models_backup.tar.gz models_backup/

# Hoặc dùng zip
zip -r vieneu_tts_models_backup.zip models_backup/
```

### Restore models:
```bash
# Giải nén
tar -xzf vieneu_tts_models_backup.tar.gz

# Hoặc
unzip vieneu_tts_models_backup.zip
```

## 5. Lưu ý quan trọng

### Kích thước models:
- **backbone-pytorch**: ~1.2GB
- **backbone-q8**: ~600MB
- **backbone-q4**: ~350MB (khuyến nghị cho CPU)
- **codec-standard**: ~100MB
- **codec-onnx**: ~50MB (khuyến nghị cho CPU)

### Khuyến nghị:
- **GPU users**: Download `backbone-pytorch` + `codec-standard`
- **CPU users**: Download `backbone-q4` + `codec-onnx`
- **Backup đầy đủ**: Download tất cả models (~2.3GB)

### Offline mode:
Sau khi download, bạn có thể:
1. Ngắt kết nối internet
2. Sử dụng models local bình thường
3. Không cần truy cập Hugging Face

## 6. Troubleshooting

### Lỗi "Model not found":
- Kiểm tra đường dẫn trong config.yaml
- Đảm bảo thư mục models_backup tồn tại
- Kiểm tra quyền đọc file

### Lỗi khi download:
```bash
# Cài đặt lại huggingface_hub
pip install --upgrade huggingface_hub

# Thử download lại với force
python download_models.py --force
```

### Lỗi "Out of space":
- Kiểm tra dung lượng ổ cứng (cần ~3GB trống)
- Download từng model một thay vì tất cả
- Xóa cache Hugging Face cũ: `rm -rf ~/.cache/huggingface/`

## 7. Di chuyển models sang máy khác

```bash
# Máy 1: Download và nén
python download_models.py
tar -czf models.tar.gz models_backup/

# Copy file models.tar.gz sang máy 2

# Máy 2: Giải nén và sử dụng
tar -xzf models.tar.gz
# Sửa config.yaml để dùng local paths
python gradio_app.py
```
