# 🔥 Quick Guide: Backup & Use Local Models

## 🚀 Quy trình 3 bước

### Bước 1: Download tất cả models về local
```bash
python download_models.py
```

Hoặc chỉ download models cần thiết:
```bash
# Cho GPU users
python download_models.py --models backbone-pytorch codec-standard

# Cho CPU users  
python download_models.py --models backbone-q4 codec-onnx
```

### Bước 2: Chuyển config sang dùng local models
```bash
python switch_to_local_models.py --local --backup
```

### Bước 3: Chạy ứng dụng như bình thường
```bash
python gradio_app.py
```

## 📋 Các lệnh hữu ích

### Xem trạng thái config hiện tại
```bash
python switch_to_local_models.py --status
```

### Xem danh sách models có thể download
```bash
python download_models.py --list
```

### Chuyển về dùng Hugging Face (online)
```bash
python switch_to_local_models.py --remote
```

### Download lại models (force)
```bash
python download_models.py --force
```

## 💾 Backup models sang máy khác

### Nén models:
```bash
# Linux/Mac
tar -czf vieneu_models.tar.gz models_backup/

# Windows (PowerShell)
Compress-Archive -Path models_backup -DestinationPath vieneu_models.zip
```

### Giải nén trên máy mới:
```bash
# Linux/Mac
tar -xzf vieneu_models.tar.gz

# Windows (PowerShell)
Expand-Archive -Path vieneu_models.zip -DestinationPath .
```

### Cấu hình trên máy mới:
```bash
python switch_to_local_models.py --local --no-confirm
python gradio_app.py
```

## 📊 Kích thước models

| Model | Kích thước | Khuyến nghị |
|-------|-----------|-------------|
| backbone-pytorch | ~1.2GB | GPU users |
| backbone-q8 | ~600MB | CPU (chất lượng cao) |
| backbone-q4 | ~350MB | CPU (tốc độ nhanh) ⭐ |
| codec-standard | ~100MB | GPU users |
| codec-onnx | ~50MB | CPU users ⭐ |

**Tổng cộng tất cả**: ~2.3GB

## ⚡ Khuyến nghị

### Cho GPU users (có NVIDIA GPU):
```bash
python download_models.py --models backbone-pytorch codec-standard
```
→ Tổng: ~1.3GB, chất lượng tốt nhất

### Cho CPU users:
```bash
python download_models.py --models backbone-q4 codec-onnx
```
→ Tổng: ~400MB, tốc độ nhanh nhất trên CPU

### Backup đầy đủ (khuyến nghị):
```bash
python download_models.py
```
→ Tổng: ~2.3GB, có tất cả các options

## 🔧 Troubleshooting

### Lỗi "huggingface_hub not found"
```bash
pip install huggingface-hub
```

### Lỗi "Model not found" khi chạy
```bash
# Kiểm tra xem models đã download chưa
python download_models.py --list

# Kiểm tra config
python switch_to_local_models.py --status
```

### Lỗi "Out of disk space"
```bash
# Download từng model một
python download_models.py --models backbone-q4
python download_models.py --models codec-onnx
```

### Muốn xóa models cũ
```bash
rm -rf models_backup/
# Hoặc trên Windows:
# rmdir /s models_backup
```

## 📁 Cấu trúc thư mục

```
VieNeu-TTS/
├── models_backup/              # ← Models được download về đây
│   ├── backbone-pytorch/
│   ├── backbone-q4/
│   ├── backbone-q8/
│   ├── codec-standard/
│   ├── codec-distill/
│   └── codec-onnx/
├── download_models.py          # ← Script download models
├── switch_to_local_models.py   # ← Script chuyển đổi config
├── config.yaml                 # ← Config file (sẽ được sửa tự động)
└── gradio_app.py              # ← Ứng dụng chính
```

## 🎯 Use Cases

### 1. Offline Development
```bash
# Lần đầu (có internet)
python download_models.py
python switch_to_local_models.py --local --backup

# Sau đó (không cần internet)
python gradio_app.py
```

### 2. Deploy lên Server không có internet
```bash
# Máy local (có internet)
python download_models.py
tar -czf models.tar.gz models_backup/
scp models.tar.gz user@server:/path/to/VieNeu-TTS/

# Trên server
tar -xzf models.tar.gz
python switch_to_local_models.py --local --no-confirm
python gradio_app.py
```

### 3. Chia sẻ models cho team
```bash
# Upload lên Google Drive / Dropbox
python download_models.py
tar -czf vieneu_models_$(date +%Y%m%d).tar.gz models_backup/
# Upload file .tar.gz

# Team members download và giải nén
tar -xzf vieneu_models_*.tar.gz
python switch_to_local_models.py --local
```

## 💡 Tips

1. **Backup config trước khi thay đổi**: Luôn dùng `--backup` flag
2. **Kiểm tra trước khi chạy**: Dùng `--status` để xem config hiện tại
3. **Download theo nhu cầu**: Không cần download tất cả nếu chỉ dùng CPU hoặc GPU
4. **Nén khi backup**: Models rất lớn, nên nén trước khi copy/upload
5. **Kiểm tra dung lượng**: Đảm bảo có đủ ~3GB trống trước khi download

## 📞 Support

Nếu gặp vấn đề, check:
1. File `USE_LOCAL_MODELS.md` - Hướng dẫn chi tiết
2. `python download_models.py --help` - Help cho download script
3. `python switch_to_local_models.py --help` - Help cho switch script
