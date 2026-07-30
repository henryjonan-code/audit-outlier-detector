#!/bin/bash
cd "$(dirname "$0")"

echo "======================================"
echo "  Hotel FO Anomaly Detector"
echo "======================================"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 tidak ditemukan. Install dari https://python.org"
    exit 1
fi

# Install dependencies
echo "Menginstall dependencies..."
pip3 install -r requirements.txt -q

# Create dirs
mkdir -p uploads outputs

# Run app
echo ""
echo "Aplikasi berjalan di: http://localhost:5050"
echo "Tekan Ctrl+C untuk berhenti."
echo ""
python3 app.py
