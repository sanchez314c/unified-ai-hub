# Deployment Guide

## Overview

This guide covers deployment of UnifiedAI Hub to various platforms and distribution channels.

## Distribution Methods

### 1. Direct Distribution
Distribute built artifacts directly to users:

#### Artifacts Location
After building, find distributables in the `dist/` directory:

- **macOS**: `Unified AI Hub-*.dmg`, `Unified AI Hub-*.zip`
- **Windows**: `Unified AI Hub Setup *.exe`, `Unified AI Hub-*.zip`
- **Linux**: `unified-ai-hub-*.AppImage`, `*.deb`, `*.rpm`, `*.snap`

### 2. GitHub Releases
Automated releases through GitHub Actions:

#### Release Workflow
```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags:
      - 'v*'
jobs:
  release:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
    steps:
      - uses: actions/checkout@v2
      - name: Build and Release
        uses: electron-builder/action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

### 3. Auto-Update System
Configure electron-updater for automatic updates:

#### Configuration
```javascript
// main.js
const { autoUpdater } = require('electron-updater');

app.on('ready', () => {
  autoUpdater.checkForUpdatesAndNotify();
});

autoUpdater.on('update-available', () => {
  dialog.showMessageBox({
    type: 'info',
    title: 'Update Available',
    message: 'A new version is available. Downloading now...'
  });
});
```

## Platform-Specific Deployment

### macOS

#### App Store Distribution
1. **Prepare for App Store**
   ```bash
   # Build for Mac App Store
   npm run dist:mac -- --mas
   ```

2. **Upload to App Store Connect**
   - Use Xcode Organizer
   - Upload `.pkg` file
   - Complete metadata

3. **Notarization**
   ```bash
   # Automatic notarization with electron-builder
   npm run dist:mac -- --mac.cscKeychainFile=certificate.p12
   ```

#### Direct Distribution
- Distribute DMG files
- Include code signing for security
- Provide installation instructions

### Windows

#### Microsoft Store
1. **Convert to MSIX**
   ```bash
   # Install electron-builder-msix
   npm install --save-dev electron-builder-msix
   
   # Build MSIX package
   npm run dist:win -- --win.msix
   ```

2. **Submit to Microsoft Store**
   - Use Partner Center
   - Upload MSIX package
   - Complete store listing

#### Direct Distribution
- NSIS installer with custom branding
- Code signing for Windows SmartScreen
- Silent installation options

### Linux

#### Snap Store
```bash
# Build snap package
npm run dist:linux -- --linux.snap

# Publish to Snap Store
snapcraft push --release=stable *.snap
```

#### Flatpak
```bash
# Create Flatpak manifest
# Build with flatpak-builder
flatpak-builder build-dir com.unifiedai.hub.json
```

#### Package Managers
- **Debian/Ubuntu**: Upload to PPA
- **Fedora**: Submit to COPR
- **Arch Linux**: Create AUR package

## Deployment Checklist

### Pre-Deployment
- [ ] All tests pass
- [ ] Code signed for target platforms
- [ ] Version number updated
- [ ] CHANGELOG.md updated
- [ ] Dependencies audited for security

### Post-Deployment
- [ ] Verify downloads work correctly
- [ ] Test installation on clean system
- [ ] Check auto-update functionality
- [ ] Monitor crash reports

## Security Considerations

### Code Signing
Always sign distributables:
- macOS: Apple Developer certificate
- Windows: Code signing certificate
- Linux: GPG signing for packages

### Checksums
Provide SHA256 checksums for verification:
```bash
# Generate checksums
sha256sum dist/* > checksums.txt
```

### Secure Distribution
- Use HTTPS for downloads
- Verify integrity before installation
- Keep private keys secure

## Continuous Deployment

### GitHub Actions Workflow
```yaml
name: Build and Release
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      - name: Install dependencies
        run: npm ci
      - name: Build
        run: npm run dist
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: ${{ matrix.os }}-build
          path: dist/
```

## Monitoring and Analytics

### Update Analytics
Track update adoption:
- Version distribution
- Update success rate
- Platform breakdown

### Error Reporting
Implement crash reporting:
- Sentry integration
- Custom error tracking
- User feedback collection

## Rollback Strategy

### Emergency Rollback
1. **Revert to previous version**
   - Update download URLs
   - Push previous version as hotfix

2. **Communicate with users**
   - Post notice on GitHub
   - Send email notification
   - Update in-app messages

3. **Investigate issue**
   - Analyze crash reports
   - Reproduce bug
   - Fix and re-release