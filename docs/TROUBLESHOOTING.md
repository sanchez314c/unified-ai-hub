# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### "Application won't open on macOS"
**Symptoms**: Double-clicking does nothing, or security warning appears

**Solutions**:
1. **Security Settings**:
   - Go to System Preferences > Security & Privacy
   - Click "Open Anyway" for UnifiedAI Hub
   - Or right-click app > Open

2. **Gatekeeper Disabled** (Advanced):
   ```bash
   sudo spctl --master-disable
   ```

3. **Re-download**:
   - DMG may be corrupted
   - Download fresh copy

#### "Windows Defender blocks installation"
**Symptoms**: Security warning during installation

**Solutions**:
1. **Allow Anyway**:
   - Click "More info"
   - Select "Run anyway"

2. **Add Exception**:
   - Windows Security > Virus & threat protection
   - Add exclusion for installer

3. **Disable Temporarily**:
   - Turn off Real-time protection
   - Install, then re-enable

#### "Linux dependencies missing"
**Symptoms**: "File not found" or library errors

**Solutions**:
```bash
# Ubuntu/Debian
sudo apt-get install libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6 xdg-utils libatspi2.0-0 libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxkbcommon0 libasound2

# Fedora/RHEL
sudo dnf install gtk3 libXScrnSaver nss alsa-lib

# Arch Linux
sudo pacman -S gtk3 libxss nss alsa-lib
```

### Runtime Issues

#### "Black screens in AI views"
**Symptoms**: AI service windows appear black

**Solutions**:
1. **Reload Views**:
   - Press `Cmd/Ctrl + R`
   - Or restart application

2. **Check Internet**:
   - Verify connection works
   - Try different network

3. **Disable GPU** (Linux):
   ```bash
   ./unified-ai-hub.AppImage --disable-gpu
   ```

4. **Clear Cache**:
   - Delete app data and re-login

#### "AI services not loading"
**Symptoms**: Loading spinners, no content

**Solutions**:
1. **Network Check**:
   - Can you access AI websites in browser?
   - Check firewall settings

2. **Service Status**:
   - Verify AI services are operational
   - Check service status pages

3. **DNS Issues**:
   ```bash
   # Flush DNS
   # macOS
   sudo dscacheutil -flushcache
   
   # Windows
   ipconfig /flushdns
   
   # Linux
   sudo systemctl restart systemd-resolved
   ```

4. **VPN/Proxy**:
   - Disable VPN or proxy
   - Try direct connection

#### "Layout switching is slow"
**Symptoms**: Delay when changing layouts

**Solutions**:
1. **Reduce Active Views**:
   - Use fewer AI services
   - Close unused positions

2. **Increase Memory**:
   - Close other applications
   - Add more RAM if possible

3. **Restart App**:
   - Memory fragmentation over time
   - Fresh start helps

### Performance Issues

#### "High memory usage"
**Symptoms**: System becomes slow, fans spin up

**Solutions**:
1. **Monitor Usage**:
   - Activity Monitor (macOS)
   - Task Manager (Windows)
   - htop (Linux)

2. **Optimize Settings**:
   - Use 2-3 AI services max
   - Prefer simpler layouts

3. **Update Graphics Drivers**:
   - Outdated drivers cause issues
   - Check manufacturer website

#### "Startup is slow"
**Symptoms**: Application takes >10 seconds to open

**Solutions**:
1. **Clear Cache**:
   - Delete application cache
   - Remove old session data

2. **Check SSD Health**:
   - Slow disk affects startup
   - Run disk utility

3. **Disable Antivirus Scan**:
   - Add exception for app folder
   - Real-time scanning slows startup

### Session Issues

#### "Logged out randomly"
**Symptoms**: Need to re-login frequently

**Solutions**:
1. **Check Service Policies**:
   - Some services have session limits
   - May require re-authentication

2. **Clear Corrupted Data**:
   - Delete specific service partition
   - Login again fresh

3. **Stable Connection**:
   - Network interruptions cause logout
   - Use reliable internet

#### "Can't paste into AI services"
**Symptoms**: Paste is blocked or doesn't work

**Solutions**:
1. **Force Paste**:
   - Use `Cmd/Ctrl + Shift + V`
   - Or right-click context menu

2. **Check Service Settings**:
   - Some services disable paste
   - Check security settings

3. **Restart View**:
   - Reload specific AI view
   - Try again after reload

### Platform-Specific Issues

#### macOS Only
**"App window is blank"**
```bash
# Reset permissions
sudo tccutil reset All com.unifiedai.hub

# Reinstall
rm -rf "/Applications/Unified AI Hub.app"
# Install fresh copy
```

**"Notarization error"**
- Download from official GitHub only
- Verify SHA256 checksum
- Report if issue persists

#### Windows Only
**"Runtime error: JavaScript heap out of memory"**
1. Increase Node.js heap:
   ```batch
   set NODE_OPTIONS=--max-old-space-size=4096
   "C:\Program Files\Unified AI Hub\Unified AI Hub.exe"
   ```

2. Use 64-bit version if on 32-bit

**"Missing MSVCR120.dll"**
- Install Microsoft Visual C++ Redistributable
- Download from Microsoft website
- Restart after installation

#### Linux Only
**"Cannot open display"**
```bash
# Allow X11 connection
xhost +local:unifiedai

# Or run with display
export DISPLAY=:0
./unified-ai-hub.AppImage
```

**"Font rendering issues"**
```bash
# Install font packages
sudo apt-get install fonts-liberation fonts-dejavu-core

# Or use with font config
./unified-ai-hub.AppImage --font-render-hinting=none
```

### Debugging

#### Enable Debug Mode
```bash
# macOS/Linux
DEBUG=electron-builder npm start

# Windows
set DEBUG=electron-builder && npm start
```

#### Check Console Logs
1. Open Developer Tools:
   - Press `F12` (if enabled)
   - Or check View > Developer Tools

2. Look for red errors
3. Search error messages online

#### Report Issues
When reporting bugs, include:
- Operating system and version
- UnifiedAI Hub version
- Steps to reproduce
- Console errors (if any)
- Expected vs actual behavior

### Advanced Troubleshooting

#### Reset Application
```bash
# macOS
rm -rf ~/Library/Preferences/com.unifiedai.hub.plist
rm -rf ~/Library/Application\ Support/UnifiedAIHub

# Windows
del "%APPDATA%\UnifiedAIHub"

# Linux
rm -rf ~/.config/UnifiedAIHub
```

#### Command Line Options
```bash
# Common options
./unified-ai-hub --help
./unified-ai-hub --version
./unified-ai-hub --disable-gpu
./unified-ai-hub --no-sandbox
./unified-ai-hub --enable-logging
```

#### Network Debugging
```bash
# Check DNS resolution
nslookup claude.ai
nslookup grok.x.ai

# Test connectivity
curl -I https://claude.ai
curl -I https://grok.x.ai

# Trace route
traceroute claude.ai
```

## Getting Help

### Self-Service Resources
1. [FAQ.md](FAQ.md) - Common questions
2. [GitHub Issues](https://github.com/yourusername/unified-ai-wrapper/issues) - Search existing issues
3. [Documentation Index](./DOCUMENTATION_INDEX.md) - All documentation

### Community Support
1. GitHub Discussions
2. Discord/Slack community (if available)
3. Stack Overflow with `unified-ai-hub` tag

### Contact Support
1. Create detailed GitHub issue
2. Include system information
3. Attach screenshots if relevant
4. Be patient for response

---

**Last Updated**: October 2024  
**Version**: 1.0.0  
**For version-specific issues, check your version number**