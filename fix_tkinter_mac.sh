#!/bin/bash

echo "🔧 Installing pyenv and tcl-tk via Homebrew..."
brew update
brew install pyenv
brew install tcl-tk

echo "✅ Setting environment variables for Tkinter support..."
echo 'export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"' >> ~/.zprofile
echo 'export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"' >> ~/.zprofile
echo 'export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig"' >> ~/.zprofile
echo 'export PATH="/opt/homebrew/opt/tcl-tk/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile

echo "📦 Installing Python 3.11.7 with Tkinter via pyenv..."
env \
  CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include" \
  LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib" \
  PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig" \
  pyenv install 3.11.7

pyenv global 3.11.7

echo "✅ Python 3.11.7 with Tkinter installed and set as default."

echo "🧪 Launching tkinter test window..."
python3 -m tkinter
