#!/bin/bash
# setup.sh

set -e

echo "📦 Installing system dependencies..."
apt-get update
apt-get install -y python3-pip

echo "🐍 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
