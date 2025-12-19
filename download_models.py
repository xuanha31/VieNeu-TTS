#!/usr/bin/env python3
"""
Script để download tất cả models của VieNeu-TTS về local để backup.
Sau khi download, bạn có thể sử dụng models từ thư mục local thay vì Hugging Face.

Usage:
    python download_models.py
    
    # Hoặc chỉ download một số models cụ thể:
    python download_models.py --models backbone-pytorch backbone-q4
"""

import os
import argparse
from pathlib import Path
from huggingface_hub import snapshot_download
import sys

# Cấu hình thư mục lưu models
MODELS_DIR = Path("./models_backup")

# Danh sách tất cả models cần download
MODELS_CONFIG = {
    "backbone-pytorch": {
        "repo_id": "pnnbao-ump/VieNeu-TTS",
        "description": "Backbone PyTorch (GPU) - Chất lượng cao nhất",
        "size": "~1.2GB"
    },
    "backbone-q4": {
        "repo_id": "pnnbao-ump/VieNeu-TTS-q4-gguf",
        "description": "Backbone Q4 GGUF (CPU) - Nhẹ nhất",
        "size": "~350MB"
    },
    "backbone-q8": {
        "repo_id": "pnnbao-ump/VieNeu-TTS-q8-gguf",
        "description": "Backbone Q8 GGUF (CPU) - Cân bằng",
        "size": "~600MB"
    },
    "codec-standard": {
        "repo_id": "neuphonic/neucodec",
        "description": "Codec chuẩn (PyTorch)",
        "size": "~100MB"
    },
    "codec-distill": {
        "repo_id": "neuphonic/distill-neucodec",
        "description": "Codec distilled (PyTorch)",
        "size": "~80MB"
    },
    "codec-onnx": {
        "repo_id": "neuphonic/neucodec-onnx-decoder",
        "description": "Codec ONNX (CPU tối ưu)",
        "size": "~50MB"
    }
}


def download_model(model_key: str, force: bool = False):
    """
    Download một model từ Hugging Face về local.
    
    Args:
        model_key: Key của model trong MODELS_CONFIG
        force: Nếu True, download lại ngay cả khi đã tồn tại
    """
    if model_key not in MODELS_CONFIG:
        print(f"❌ Model key '{model_key}' không tồn tại!")
        print(f"   Các model hợp lệ: {', '.join(MODELS_CONFIG.keys())}")
        return False
    
    config = MODELS_CONFIG[model_key]
    repo_id = config["repo_id"]
    local_dir = MODELS_DIR / model_key
    
    print(f"\n{'='*70}")
    print(f"📦 Model: {model_key}")
    print(f"   Repo: {repo_id}")
    print(f"   Mô tả: {config['description']}")
    print(f"   Kích thước: {config['size']}")
    print(f"   Thư mục: {local_dir}")
    print(f"{'='*70}")
    
    # Kiểm tra nếu đã tồn tại
    if local_dir.exists() and not force:
        print(f"⚠️  Model đã tồn tại tại {local_dir}")
        response = input("   Bạn có muốn download lại không? (y/N): ").strip().lower()
        if response != 'y':
            print("   ⏭️  Bỏ qua model này.")
            return True
    
    try:
        print(f"⏳ Đang download từ Hugging Face...")
        
        # Download model
        snapshot_download(
            repo_id=repo_id,
            local_dir=str(local_dir),
            local_dir_use_symlinks=False,  # Copy thật, không dùng symlink
            resume_download=True,  # Tiếp tục nếu bị gián đoạn
        )
        
        print(f"✅ Download thành công: {local_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi download model {model_key}: {e}")
        return False


def download_all_models(force: bool = False, selected_models: list = None):
    """
    Download tất cả hoặc một số models đã chọn.
    
    Args:
        force: Nếu True, download lại ngay cả khi đã tồn tại
        selected_models: List các model keys cần download (None = tất cả)
    """
    # Tạo thư mục backup nếu chưa có
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("🚀 VieNeu-TTS Model Downloader")
    print("="*70)
    print(f"📁 Thư mục backup: {MODELS_DIR.absolute()}")
    
    # Xác định models cần download
    if selected_models:
        models_to_download = selected_models
        print(f"📋 Sẽ download {len(models_to_download)} model(s): {', '.join(models_to_download)}")
    else:
        models_to_download = list(MODELS_CONFIG.keys())
        print(f"📋 Sẽ download tất cả {len(models_to_download)} models")
    
    # Tính tổng kích thước ước tính
    def parse_size(size_str):
        """Parse size string like '~1.2GB' or '~350MB' to MB"""
        size_str = size_str.replace("~", "").strip()
        if "GB" in size_str:
            return float(size_str.replace("GB", "")) * 1000
        elif "MB" in size_str:
            return float(size_str.replace("MB", ""))
        return 0
    
    total_size = sum(parse_size(MODELS_CONFIG[k]["size"]) for k in models_to_download)
    
    if total_size >= 1000:
        print(f"💾 Tổng kích thước ước tính: ~{total_size/1000:.1f}GB")
    else:
        print(f"💾 Tổng kích thước ước tính: ~{int(total_size)}MB")
    print()
    
    # Xác nhận trước khi download
    if not force:
        response = input("Bạn có muốn tiếp tục? (Y/n): ").strip().lower()
        if response == 'n':
            print("❌ Đã hủy.")
            return
    
    # Download từng model
    success_count = 0
    failed_models = []
    
    for i, model_key in enumerate(models_to_download, 1):
        print(f"\n[{i}/{len(models_to_download)}] ", end="")
        
        if download_model(model_key, force):
            success_count += 1
        else:
            failed_models.append(model_key)
    
    # Tổng kết
    print("\n" + "="*70)
    print("📊 KẾT QUẢ")
    print("="*70)
    print(f"✅ Thành công: {success_count}/{len(models_to_download)}")
    
    if failed_models:
        print(f"❌ Thất bại: {len(failed_models)}")
        print(f"   Models lỗi: {', '.join(failed_models)}")
    
    print(f"\n📁 Tất cả models đã được lưu tại: {MODELS_DIR.absolute()}")
    print("\n💡 CÁCH SỬ DỤNG MODELS ĐÃ DOWNLOAD:")
    print("   Thay vì dùng repo ID từ Hugging Face, hãy dùng đường dẫn local:")
    print(f"   VD: backbone_repo='./models_backup/backbone-pytorch'")
    print(f"       codec_repo='./models_backup/codec-standard'")


def list_models():
    """Hiển thị danh sách tất cả models có thể download."""
    print("\n" + "="*70)
    print("📋 DANH SÁCH MODELS CÓ THỂ DOWNLOAD")
    print("="*70)
    
    for key, config in MODELS_CONFIG.items():
        status = "✅" if (MODELS_DIR / key).exists() else "⬜"
        print(f"\n{status} {key}")
        print(f"   Repo: {config['repo_id']}")
        print(f"   Mô tả: {config['description']}")
        print(f"   Kích thước: {config['size']}")
        if (MODELS_DIR / key).exists():
            print(f"   📁 Đã có tại: {MODELS_DIR / key}")


def main():
    parser = argparse.ArgumentParser(
        description="Download VieNeu-TTS models từ Hugging Face về local để backup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  # Download tất cả models
  python download_models.py
  
  # Download chỉ backbone PyTorch và codec standard
  python download_models.py --models backbone-pytorch codec-standard
  
  # Download lại ngay cả khi đã tồn tại
  python download_models.py --force
  
  # Xem danh sách models
  python download_models.py --list
        """
    )
    
    parser.add_argument(
        "--models",
        nargs="+",
        choices=list(MODELS_CONFIG.keys()),
        help="Chỉ download các models cụ thể (mặc định: tất cả)"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Download lại ngay cả khi model đã tồn tại"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="Hiển thị danh sách tất cả models"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./models_backup",
        help="Thư mục lưu models (mặc định: ./models_backup)"
    )
    
    args = parser.parse_args()
    
    # Cập nhật thư mục output nếu được chỉ định
    global MODELS_DIR
    MODELS_DIR = Path(args.output_dir)
    
    # Xử lý các lệnh
    if args.list:
        list_models()
    else:
        download_all_models(force=args.force, selected_models=args.models)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Đã hủy bởi người dùng.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
