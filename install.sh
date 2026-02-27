#!/bin/bash
set -e

echo "=== Token Oscillator Installer ==="

# Install Python websockets
echo "[1/5] Installing Python dependencies..."
pip3 install websockets --break-system-packages 2>/dev/null || pip3 install websockets

# Install nginx
echo "[2/5] Installing nginx..."
sudo apt-get update -qq
sudo apt-get install -y -qq nginx

# Configure nginx
echo "[3/5] Configuring nginx..."
sudo rm -f /etc/nginx/sites-enabled/default
sudo cp /home/xero/token-oscillator/nginx.conf /etc/nginx/sites-available/token-oscillator
sudo ln -sf /etc/nginx/sites-available/token-oscillator /etc/nginx/sites-enabled/token-oscillator
chmod o+x /home/xero /home/xero/token-oscillator /home/xero/token-oscillator/frontend /home/xero/token-oscillator/frontend/pp
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx

# Install systemd service
echo "[4/5] Installing systemd service..."
sudo cp /home/xero/token-oscillator/token-oscillator.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable token-oscillator
sudo systemctl start token-oscillator

# Verify
echo "[5/5] Verifying..."
sleep 2
if systemctl is-active --quiet token-oscillator; then
    echo "Backend: RUNNING"
else
    echo "Backend: FAILED - check: sudo journalctl -u token-oscillator"
fi

if systemctl is-active --quiet nginx; then
    echo "Nginx:   RUNNING"
else
    echo "Nginx:   FAILED - check: sudo journalctl -u nginx"
fi

IP=$(hostname -I | awk '{print $1}')
echo ""
echo "=== Token Oscillator ready ==="
echo "Open http://${IP} in your browser"
echo "WebSocket: ws://${IP}:8765"
