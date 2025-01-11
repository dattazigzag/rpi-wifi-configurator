#!/bin/bash

echo "Setting up WiFi Manager Service..."

# 1. Create systemd user directory
mkdir -p ~/.config/systemd/user/

# 2. Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 3. Replace absolute paths with $HOME in service file
sed "s|/home/[^/]*/|$HOME/|g" "$SCRIPT_DIR/rpi-btn-wifi-manager.service" > "$SCRIPT_DIR/temp.service"

# 4. Copy modified service file to systemd directory
cp "$SCRIPT_DIR/temp.service" ~/.config/systemd/user/rpi-btn-wifi-manager.service

# 5. Clean up temp file
rm "$SCRIPT_DIR/temp.service"

# 6. Reload systemd daemon and enable service
systemctl --user daemon-reload
systemctl --user enable rpi-btn-wifi-manager.service

echo "Service setup complete! You can start it with: systemctl --user start rpi-btn-wifi-manager"