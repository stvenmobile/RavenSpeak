#!/bin/bash

# Name of your virtual environment
VENV_NAME=".venv"

echo "🛠️  RavenSpeak Setup Starting..."

# Step 1: Create virtual environment
if [ ! -d "$VENV_NAME" ]; then
    echo "📦 Creating virtual environment ($VENV_NAME)..."
    python3 -m venv $VENV_NAME
else
    echo "📦 Virtual environment already exists. Skipping..."
fi

# Step 2: Activate it
echo "✅ Activating virtual environment..."
source $VENV_NAME/bin/activate

# Step 3: Upgrade pip and install requirements
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ RavenSpeak setup complete. Virtual environment ready."
echo "👉 Run: source $VENV_NAME/bin/activate"
