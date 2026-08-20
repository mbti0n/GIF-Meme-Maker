#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"

echo "Installing Python dependencies..."
pip3 install --break-system-packages -r "$SCRIPT_DIR/requirements.txt"

mkdir -p "$INSTALL_DIR"

LINK="$INSTALL_DIR/memed"
ln -sf "$SCRIPT_DIR/memed.py" "$LINK"
chmod +x "$SCRIPT_DIR/memed.py"

# Ensure ~/.local/bin is in PATH
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
  SHELL_RC=""
  if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
  elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
  fi
  if [ -n "$SHELL_RC" ]; then
    echo '' >> "$SHELL_RC"
    echo '# Added by gifMemeMaker setup' >> "$SHELL_RC"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
    echo "Added ~/.local/bin to PATH in $SHELL_RC"
    export PATH="$INSTALL_DIR:$PATH"
  fi
fi

echo ""
echo "Done! You can now run: memed --path <image> --caption <text>"
echo "You may need to restart your shell or run: export PATH=\"\$HOME/.local/bin:\$PATH\""
