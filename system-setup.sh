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

# Download the correct Piper archive
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz

# Extract it
tar -xzf piper_linux_x86_64.tar.gz

# Move the actual binary into place
mv piper/piper ./piper-linux-x86_64
chmod +x piper-linux-x86_64

# Clean up leftover files
rm -rf piper piper_linux_x86_64.tar.gz


# Download voice model and config
mkdir -p piper_models
cd piper_models

# Voice model
if [ ! -s "en_US-lessac-medium.onnx" ]; then
  echo "⬇️ Downloading Piper ONNX model..."
  wget -O en_US-lessac-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
fi

# Config file
if [ ! -s "en_US-lessac-medium.onnx.json" ]; then
  echo "⬇️ Downloading Piper config..."
  wget -O en_US-lessac-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
fi

cd ..




echo "🧹 Cleaning up..."
apt autoremove -y

echo "✅ RavenSpeak system setup complete!"
