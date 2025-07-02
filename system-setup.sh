#!/bin/bash

echo "🛠️  Starting RavenSpeak system setup..."
echo "🔐 This script requires sudo privileges."

# Confirm sudo
if [[ $EUID -ne 0 ]]; then
  echo "Please run as root: sudo ./system-setup.sh"
  exit 1
fi

echo "📦 Updating package lists..."
apt update

echo "⬇️  Installing system utilities and development tools..."
apt install -y \
  curl wget git nano net-tools htop unzip \
  python3-pip python3-venv python3-dev \
  jq sox ffmpeg \
  alsa-utils libasound2-dev portaudio19-dev \
  libffi-dev libssl-dev \
  mosquitto-clients \
  pavucontrol \
  build-essential

echo "✅ System utilities installed."

# Optional: create a placeholder .env file
if [ ! -f ".env" ]; then
  echo "📝 Creating .env file placeholder..."
  cat <<EOF > .env
# API keys and config variables
OPENWEATHER_API_KEY=your_openweather_key
OLLAMA_ENDPOINT=http://192.168.1.60:11435
EOF
  echo "📄 .env file created. Be sure to update with your actual API keys."
fi

echo "🎤 Installing Piper TTS engine..."
wget -q https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz
mkdir -p piper
tar -xzf piper_linux_x86_64.tar.gz -C piper
chmod +x piper/piper
rm piper_linux_x86_64.tar.gz


# Download Piper voice model if not present
mkdir -p piper
if [ ! -f piper/en_US-amy-medium.onnx ]; then
  echo "🎤 Downloading Amy voice model..."
  wget -q https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx \
    -O piper/en_US-amy-medium.onnx
  wget -q https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json \
    -O piper/en_US-amy-medium.onnx.json
fi

cd ..

echo "🧹 Cleaning up..."
apt autoremove -y

echo "✅ RavenSpeak system setup complete!"
