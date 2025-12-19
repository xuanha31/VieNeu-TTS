# Hướng dẫn cài đặt trên Google Colab

## Cách 1: Cài đặt từng bước (Khuyên dùng)

```python
# Bước 1: Cài PyTorch packages với CUDA 12.1
!pip install torch==2.5.1+cu121 torchaudio==2.5.1+cu121 torchvision==0.20.1+cu121 --index-url https://download.pytorch.org/whl/cu121

# Bước 2: Cài torchao
!pip install torchao==0.14.1

# Bước 3: Loại bỏ các dòng torch packages khỏi requirements.txt
!sed '/^torch==/d; /^torchaudio==/d; /^torchao==/d; /^torchvision==/d' requirements.txt > requirements_temp.txt

# Bước 4: Cài các packages còn lại
!pip install -r requirements_temp.txt
```

## Cách 2: Cài đặt tất cả với index-url

```python
# Cài tất cả packages, chỉ định index-url cho torch
!pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121
```

## Kiểm tra cài đặt

```python
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
```

## Lưu ý

- Google Colab mặc định có CUDA 12.1
- Nếu gặp lỗi về torchvision, hãy dùng **Cách 1**
- Các version tương thích:
  - torch==2.5.1+cu121
  - torchaudio==2.5.1+cu121
  - torchvision==0.20.1+cu121
  - torchao==0.14.1
