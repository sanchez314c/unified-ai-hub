# Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**:
  - macOS 10.15+ (Catalina or later)
  - Windows 10+ (64-bit)
  - Linux (modern distributions with GTK3)
- **Processor**: Intel/AMD x64, Apple Silicon (ARM64)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB available disk space
- **Network**: Internet connection required for AI services

### Recommended Requirements
- **Memory**: 8GB+ RAM
- **Display**: 1920x1080 resolution or higher
- **Network**: Broadband connection for optimal AI service performance

## Installation Methods

### Method 1: Download Pre-built Binaries (Recommended)

#### macOS
1. Download the latest DMG from [Releases](https://github.com/yourusername/unified-ai-wrapper/releases)
2. Double-click the DMG file
3. Drag Unified AI Hub to Applications folder
4. Launch from Applications or Launchpad

#### Windows
1. Download the latest EXE installer from [Releases](https://github.com/yourusername/unified-ai-wrapper/releases)
2. Run the installer as Administrator
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

#### Linux
**Option A: AppImage (Universal)**
```bash
# Download AppImage
wget https://github.com/yourusername/unified-ai-wrapper/releases/latest/download/unified-ai-hub.AppImage

# Make executable
chmod +x unified-ai-hub.AppImage

# Run
./unified-ai-hub.AppImage
```

**Option B: Debian/Ubuntu**
```bash
# Download DEB package
wget https://github.com/yourusername/unified-ai-wrapper/releases/latest/download/unified-ai-hub.deb

# Install
sudo dpkg -i unified-ai-hub.deb

# Fix dependencies if needed
sudo apt-get install -f
```

**Option C: Fedora/RHEL**
```bash
# Download RPM package
wget https://github.com/yourusername/unified-ai-wrapper/releases/latest/download/unified-ai-hub.rpm

# Install
sudo rpm -i unified-ai-hub.rpm
```

### Method 2: Package Managers

#### Homebrew (macOS)
```bash
# Tap the repository
brew tap yourusername/unified-ai-hub

# Install
brew install unified-ai-hub

# Run
open -a "Unified AI Hub"
```

#### Snap (Linux)
```bash
# Install from Snap Store
sudo snap install unified-ai-hub

# Run
snap run unified-ai-hub
```

#### Chocolatey (Windows)
```bash
# Install
choco install unified-ai-hub

# Run from Start Menu or
unified-ai-hub
```

### Method 3: Build from Source

#### Prerequisites
- Node.js 14+ and npm
- Git
- Build tools for your platform

#### Steps
```bash
# Clone repository
git clone https://github.com/yourusername/unified-ai-wrapper.git
cd unified-ai-wrapper

# Install dependencies
npm install

# Run from source
npm start

# Or build for production
npm run dist
```

## Post-Installation Setup

### 1. First Launch
1. Launch UnifiedAI Hub
2. The application will open with default horizontal layout
3. Each AI service view will show the respective login page

### 2. Configure AI Services
1. Log in to each AI service you want to use:
   - Click in each view to activate it
   - Enter your credentials
   - Complete any 2FA if required

2. Select active AI services:
   - Use dropdown menus in control bar
   - Choose which AI appears in each position
   - Changes are saved automatically

### 3. Customize Layout
1. Try different layouts using buttons or shortcuts:
   - Horizontal: 3 AIs side-by-side
   - Vertical: 3 AIs stacked
   - Grid: 4 AIs in 2x2 arrangement
   - Four-Column: Wide display layout

## Verification

### Check Installation
1. Application launches without errors
2. All AI services load their login pages
3. Layout switching works correctly
4. Keyboard shortcuts function
5. Sessions persist after restart

### Test Features
- [ ] Layout switching
- [ ] AI service selection
- [ ] Keyboard shortcuts
- [ ] Context menus
- [ ] Window controls

## Troubleshooting

### Common Issues

#### "Application won't start"
**macOS**:
1. Check System Preferences > Security & Privacy
2. Allow apps from identified developers
3. Right-click app > Open

**Windows**:
1. Run as Administrator
2. Check Windows Defender isn't blocking
3. Install Microsoft Visual C++ Redistributable

**Linux**:
1. Install missing dependencies:
   ```bash
   sudo apt-get install libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6 xdg-utils libatspi2.0-0 libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxkbcommon0 libasound2
   ```

#### "AI services not loading"
1. Check internet connection
2. Verify firewall settings
3. Try different network
4. Clear application cache

#### "Black screens in AI views"
1. Restart the application
2. Check graphics drivers
3. Disable hardware acceleration:
   ```bash
   # On Linux
   unified-ai-hub --disable-gpu
   ```

### Getting Help

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions
2. Search [GitHub Issues](https://github.com/yourusername/unified-ai-wrapper/issues)
3. Create a new issue with:
   - Operating system and version
   - Error messages
   - Steps to reproduce

## Uninstallation

### macOS
```bash
# Remove application
sudo rm -rf "/Applications/Unified AI Hub.app"

# Remove preferences (optional)
rm -rf ~/Library/Preferences/com.unifiedai.hub.plist
rm -rf ~/Library/Application\ Support/UnifiedAIHub
```

### Windows
1. Use "Add or Remove Programs"
2. Uninstall UnifiedAI Hub
3. Delete user data folder if desired:
   `%APPDATA%/UnifiedAIHub`

### Linux
```bash
# For DEB/Ubuntu
sudo apt-get remove unified-ai-hub

# For RPM/Fedora
sudo rpm -e unified-ai-hub

# For AppImage
rm unified-ai-hub.AppImage

# Remove data (optional)
rm -rf ~/.config/UnifiedAIHub
```

## Next Steps

After successful installation:
1. Read [QUICK_START.md](QUICK_START.md) for basic usage
2. Check [FAQ.md](FAQ.md) for common questions
3. Review [DEVELOPMENT.md](DEVELOPMENT.md) if contributing