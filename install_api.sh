#!/bin/bash

# Script cài đặt VieNeu-TTS API
# Hỗ trợ macOS, Linux (CPU và GPU)

set -e

echo "=================================="
echo "VieNeu-TTS API Installation Script"
echo "=================================="
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 không được tìm thấy. Vui lòng cài đặt Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $PYTHON_VERSION"

# Kiểm tra OS
OS=$(uname -s)
echo "✅ Operating System: $OS"

# Kiểm tra CUDA (chỉ trên Linux)
HAS_CUDA=false
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU detected"
    nvidia-smi --query-gpu=name --format=csv,noheader
    HAS_CUDA=true
else
    echo "ℹ️  No NVIDIA GPU detected (CPU mode)"
fi

echo ""
echo "=================================="
echo "Installing dependencies..."
echo "=================================="

# Tạo virtual environment nếu chưa có
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Cài đặt dependencies
if [ "$HAS_CUDA" = true ] && [ "$OS" = "Linux" ]; then
    echo "🚀 Installing with GPU support (including lmdeploy)..."
    
    # Cài đặt PyTorch với CUDA
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    
    # Cài đặt tất cả dependencies
    pip install -r requirements.txt
else
    echo "💻 Installing for CPU/macOS (without lmdeploy)..."
    
    # Cài đặt dependencies cơ bản
    pip install -r requirements-api.txt
fi

echo ""
echo "=================================="
echo "✅ Installation completed!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start API server:"
echo "   python api_server.py"
echo ""
echo "3. Open API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "4. Test API:"
echo "   python test_api.py"
echo ""

if [ "$HAS_CUDA" = false ]; then
    echo "💡 Tip: For best performance on CPU, use:"
    echo "   - Backbone: VieNeu-TTS-q4-gguf"
    echo "   - Codec: NeuCodec ONNX (Fast CPU)"
    echo ""
fi

echo "📖 For more information, see:"
echo "   - INSTALL.md"
echo "   - README_API.md"
echo "   - API_USAGE.md"
echo ""
