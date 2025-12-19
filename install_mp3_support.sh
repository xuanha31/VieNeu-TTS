#!/bin/bash

# Install system dependencies for MP3 conversion
echo "📦 Installing ffmpeg for MP3 support..."
apt-get update -qq && apt-get install -y -qq ffmpeg > /dev/null 2>&1

# Install pydub if not already installed
pip install -q pydub

echo "✅ MP3 support ready!"
