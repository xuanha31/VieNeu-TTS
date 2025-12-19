# VieNeu-TTS API Documentation

Thư mục này chứa tất cả tài liệu về VieNeu-TTS API.

## 📖 Bắt đầu đọc từ đâu?

### 🎯 Đọc 1 file duy nhất (Khuyến nghị)
📘 **[API_COMPLETE_GUIDE.md](./API_COMPLETE_GUIDE.md)** - Tổng hợp TẤT CẢ tài liệu trong 1 file

### 🚀 Đọc nhanh
📗 **[START_HERE.md](./START_HERE.md)** - Bắt đầu từ đây (5 phút)

### 📚 Đọc theo chủ đề

#### Google Colab
- **[TEST_ON_COLAB.md](./TEST_ON_COLAB.md)** - Hướng dẫn test trên Colab
- **[COLAB_CHECKLIST.md](./COLAB_CHECKLIST.md)** - Checklist từng bước

#### macOS
- **[QUICKSTART_MACOS.md](./QUICKSTART_MACOS.md)** - Quick start cho macOS
- **[FIX_MACOS_INSTALL.md](./FIX_MACOS_INSTALL.md)** - Fix lỗi lmdeploy

#### Chi tiết
- **[API_USAGE.md](./API_USAGE.md)** - Chi tiết API endpoints
- **[README_API.md](./README_API.md)** - Quick start và examples
- **[INSTALL.md](./INSTALL.md)** - Hướng dẫn cài đặt đầy đủ

#### Tổng hợp
- **[SUMMARY.md](./SUMMARY.md)** - Tổng kết project
- **[API_FILES_SUMMARY.md](./API_FILES_SUMMARY.md)** - Tổng hợp files
- **[README_FILES.md](./README_FILES.md)** - Hướng dẫn đọc tài liệu

---

## 📁 Cấu trúc files

```
docs/api/
├── README.md                    # File này
│
├── 📖 Tổng hợp
│   ├── API_COMPLETE_GUIDE.md   ⭐ Tổng hợp TẤT CẢ
│   ├── SUMMARY.md               Tổng kết project
│   └── README_FILES.md          Hướng dẫn đọc
│
├── 🚀 Bắt đầu
│   └── START_HERE.md
│
├── 🌐 Google Colab
│   ├── TEST_ON_COLAB.md
│   └── COLAB_CHECKLIST.md
│
├── 💻 macOS
│   ├── QUICKSTART_MACOS.md
│   └── FIX_MACOS_INSTALL.md
│
└── 📚 Chi tiết
    ├── API_USAGE.md
    ├── README_API.md
    ├── INSTALL.md
    ├── API_FILES_SUMMARY.md
    └── API_README_SECTION.md
```

---

## 🎯 Workflow đọc

### Nếu bạn muốn test trên Colab:
```
START_HERE.md → TEST_ON_COLAB.md → COLAB_CHECKLIST.md
```

### Nếu bạn muốn chạy trên macOS:
```
START_HERE.md → QUICKSTART_MACOS.md → FIX_MACOS_INSTALL.md (nếu cần)
```

### Nếu bạn muốn hiểu toàn bộ:
```
API_COMPLETE_GUIDE.md (đọc 1 file duy nhất)
```

---

## 🔍 Tìm nhanh

| Tôi muốn... | Đọc file |
|-------------|----------|
| Bắt đầu nhanh nhất | [START_HERE.md](./START_HERE.md) |
| Test trên Colab | [TEST_ON_COLAB.md](./TEST_ON_COLAB.md) |
| Chạy trên macOS | [QUICKSTART_MACOS.md](./QUICKSTART_MACOS.md) |
| Fix lỗi lmdeploy | [FIX_MACOS_INSTALL.md](./FIX_MACOS_INSTALL.md) |
| Chi tiết API | [API_USAGE.md](./API_USAGE.md) |
| Đọc tất cả | [API_COMPLETE_GUIDE.md](./API_COMPLETE_GUIDE.md) |
| Cài đặt đầy đủ | [INSTALL.md](./INSTALL.md) |
| Tổng kết | [SUMMARY.md](./SUMMARY.md) |

---

## 💡 Khuyến nghị

**Người mới:**
1. Đọc [START_HERE.md](./START_HERE.md) (5 phút)
2. Chọn Colab hoặc macOS
3. Làm theo hướng dẫn

**Người có kinh nghiệm:**
- Đọc [API_COMPLETE_GUIDE.md](./API_COMPLETE_GUIDE.md) (30-45 phút)

**Cần reference nhanh:**
- Đọc [API_USAGE.md](./API_USAGE.md)

---

## 🚀 Quick Start

### Google Colab (GPU - Nhanh)
```bash
# 1. Upload colab_notebook.ipynb lên Colab
# 2. Lấy Ngrok token
# 3. Chạy notebook
# 4. Test API
python test_api.py https://xxxx.ngrok-free.app
```

### macOS (CPU - Ổn định)
```bash
# 1. Cài đặt
pip install -r requirements-api.txt

# 2. Chạy API
python api_server.py

# 3. Test
python test_api.py
```

---

**Bắt đầu ngay:** Mở [START_HERE.md](./START_HERE.md) hoặc [API_COMPLETE_GUIDE.md](./API_COMPLETE_GUIDE.md) 🚀
