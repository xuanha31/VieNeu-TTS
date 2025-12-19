#!/usr/bin/env python3
"""
Script tự động chuyển config.yaml để sử dụng local models thay vì Hugging Face.

Usage:
    # Chuyển sang local models
    python switch_to_local_models.py --local
    
    # Chuyển về Hugging Face
    python switch_to_local_models.py --remote
    
    # Backup config trước khi thay đổi
    python switch_to_local_models.py --local --backup
"""

import yaml
import argparse
import shutil
from pathlib import Path
from datetime import datetime

CONFIG_FILE = Path("config.yaml")
MODELS_DIR = Path("./models_backup")

# Mapping giữa remote repo và local path
REPO_MAPPING = {
    "pnnbao-ump/VieNeu-TTS": "./models_backup/backbone-pytorch",
    "pnnbao-ump/VieNeu-TTS-q8-gguf": "./models_backup/backbone-q8",
    "pnnbao-ump/VieNeu-TTS-q4-gguf": "./models_backup/backbone-q4",
    "neuphonic/neucodec": "./models_backup/codec-standard",
    "neuphonic/distill-neucodec": "./models_backup/codec-distill",
    "neuphonic/neucodec-onnx-decoder": "./models_backup/codec-onnx",
}

# Reverse mapping
LOCAL_TO_REMOTE = {v: k for k, v in REPO_MAPPING.items()}


def backup_config():
    """Backup config.yaml hiện tại."""
    if not CONFIG_FILE.exists():
        print(f"⚠️  File {CONFIG_FILE} không tồn tại!")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = CONFIG_FILE.with_suffix(f".yaml.backup_{timestamp}")
    
    shutil.copy2(CONFIG_FILE, backup_file)
    print(f"✅ Đã backup config tại: {backup_file}")
    return backup_file


def load_config():
    """Load config.yaml."""
    if not CONFIG_FILE.exists():
        print(f"❌ File {CONFIG_FILE} không tồn tại!")
        return None
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(config):
    """Save config.yaml."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    print(f"✅ Đã lưu config tại: {CONFIG_FILE}")


def switch_to_local(config):
    """Chuyển config sang sử dụng local models."""
    print("\n🔄 Đang chuyển sang local models...")
    
    changed = False
    missing_models = []
    
    # Kiểm tra backbone configs
    if "backbone_configs" in config:
        for name, cfg in config["backbone_configs"].items():
            repo = cfg.get("repo", "")
            if repo in REPO_MAPPING:
                local_path = REPO_MAPPING[repo]
                
                # Kiểm tra xem local model có tồn tại không
                if not Path(local_path).exists():
                    missing_models.append(f"{name} ({local_path})")
                    print(f"   ⚠️  {name}: Local model chưa có tại {local_path}")
                else:
                    cfg["repo"] = local_path
                    changed = True
                    print(f"   ✅ {name}: {repo} → {local_path}")
    
    # Kiểm tra codec configs
    if "codec_configs" in config:
        for name, cfg in config["codec_configs"].items():
            repo = cfg.get("repo", "")
            if repo in REPO_MAPPING:
                local_path = REPO_MAPPING[repo]
                
                if not Path(local_path).exists():
                    missing_models.append(f"{name} ({local_path})")
                    print(f"   ⚠️  {name}: Local model chưa có tại {local_path}")
                else:
                    cfg["repo"] = local_path
                    changed = True
                    print(f"   ✅ {name}: {repo} → {local_path}")
    
    if missing_models:
        print(f"\n⚠️  CẢNH BÁO: {len(missing_models)} model(s) chưa được download:")
        for model in missing_models:
            print(f"   - {model}")
        print("\n💡 Chạy lệnh sau để download:")
        print("   python download_models.py")
    
    if not changed:
        print("\n⚠️  Không có thay đổi nào. Config đã sử dụng local models hoặc không có repo nào cần chuyển.")
    
    return config, changed


def switch_to_remote(config):
    """Chuyển config về sử dụng Hugging Face repos."""
    print("\n🔄 Đang chuyển về Hugging Face repos...")
    
    changed = False
    
    # Kiểm tra backbone configs
    if "backbone_configs" in config:
        for name, cfg in config["backbone_configs"].items():
            repo = cfg.get("repo", "")
            if repo in LOCAL_TO_REMOTE:
                remote_repo = LOCAL_TO_REMOTE[repo]
                cfg["repo"] = remote_repo
                changed = True
                print(f"   ✅ {name}: {repo} → {remote_repo}")
    
    # Kiểm tra codec configs
    if "codec_configs" in config:
        for name, cfg in config["codec_configs"].items():
            repo = cfg.get("repo", "")
            if repo in LOCAL_TO_REMOTE:
                remote_repo = LOCAL_TO_REMOTE[repo]
                cfg["repo"] = remote_repo
                changed = True
                print(f"   ✅ {name}: {repo} → {remote_repo}")
    
    if not changed:
        print("\n⚠️  Không có thay đổi nào. Config đã sử dụng Hugging Face repos.")
    
    return config, changed


def show_status(config):
    """Hiển thị trạng thái hiện tại của config."""
    print("\n" + "="*70)
    print("📊 TRẠNG THÁI CONFIG HIỆN TẠI")
    print("="*70)
    
    local_count = 0
    remote_count = 0
    
    print("\n🦜 BACKBONE MODELS:")
    if "backbone_configs" in config:
        for name, cfg in config["backbone_configs"].items():
            repo = cfg.get("repo", "")
            is_local = repo.startswith("./")
            status = "📁 Local" if is_local else "☁️  Remote"
            exists = "✅" if is_local and Path(repo).exists() else ("⚠️" if is_local else "")
            
            print(f"   {status} {exists} {name}")
            print(f"      → {repo}")
            
            if is_local:
                local_count += 1
            else:
                remote_count += 1
    
    print("\n🎵 CODEC MODELS:")
    if "codec_configs" in config:
        for name, cfg in config["codec_configs"].items():
            repo = cfg.get("repo", "")
            is_local = repo.startswith("./")
            status = "📁 Local" if is_local else "☁️  Remote"
            exists = "✅" if is_local and Path(repo).exists() else ("⚠️" if is_local else "")
            
            print(f"   {status} {exists} {name}")
            print(f"      → {repo}")
            
            if is_local:
                local_count += 1
            else:
                remote_count += 1
    
    print("\n" + "="*70)
    print(f"📊 Tổng kết: {local_count} local, {remote_count} remote")
    print("="*70)


def main():
    parser = argparse.ArgumentParser(
        description="Chuyển đổi giữa local models và Hugging Face repos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  # Xem trạng thái hiện tại
  python switch_to_local_models.py --status
  
  # Chuyển sang local models (có backup)
  python switch_to_local_models.py --local --backup
  
  # Chuyển về Hugging Face
  python switch_to_local_models.py --remote
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--local",
        action="store_true",
        help="Chuyển sang sử dụng local models"
    )
    group.add_argument(
        "--remote",
        action="store_true",
        help="Chuyển về sử dụng Hugging Face repos"
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Hiển thị trạng thái hiện tại"
    )
    
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Backup config.yaml trước khi thay đổi"
    )
    
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Không hỏi xác nhận"
    )
    
    args = parser.parse_args()
    
    # Load config
    config = load_config()
    if config is None:
        return
    
    # Xử lý lệnh status
    if args.status:
        show_status(config)
        return
    
    # Backup nếu được yêu cầu
    if args.backup:
        backup_config()
    
    # Thực hiện chuyển đổi
    if args.local:
        new_config, changed = switch_to_local(config)
    else:  # args.remote
        new_config, changed = switch_to_remote(config)
    
    if not changed:
        return
    
    # Xác nhận trước khi lưu
    if not args.no_confirm:
        print("\n" + "="*70)
        response = input("Bạn có muốn lưu thay đổi? (Y/n): ").strip().lower()
        if response == 'n':
            print("❌ Đã hủy. Không có thay đổi nào được lưu.")
            return
    
    # Lưu config mới
    save_config(new_config)
    
    print("\n✅ Hoàn tất!")
    if args.local:
        print("💡 Bây giờ bạn có thể chạy ứng dụng với local models:")
        print("   python gradio_app.py")
    else:
        print("💡 Bây giờ ứng dụng sẽ tải models từ Hugging Face khi chạy.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Đã hủy bởi người dùng.")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
