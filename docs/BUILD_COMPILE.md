# Build and Compilation Instructions

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Git

## Development Build

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/unified-ai-wrapper.git
cd unified-ai-wrapper

# Install dependencies
npm install

# Run in development mode
npm start
```

### Development Scripts
```bash
npm start          # Run application in development mode
npm run dev        # Run with hot reload (if configured)
```

## Production Build

### Build for Current Platform
```bash
npm run dist:current
```

### Build for All Platforms
```bash
npm run dist
```

### Platform-Specific Builds

#### macOS
```bash
npm run dist:mac
```
Outputs:
- `dist/Unified AI Hub-*.dmg` (DMG installer)
- `dist/Unified AI Hub-*.zip` (ZIP archive)

#### Windows
```bash
npm run dist:win
```
Outputs:
- `dist/Unified AI Hub Setup *.exe` (NSIS installer)
- `dist/Unified AI Hub-*.zip` (ZIP archive)

#### Linux
```bash
npm run dist:linux
```
Outputs:
- `dist/unified-ai-hub-*.AppImage` (Portable)
- `dist/*.deb` (Debian package)
- `dist/*.rpm` (RPM package)
- `dist/*.snap` (Snap package)

### Test Build (Unpacked)
```bash
npm run pack
```
Creates unpacked build in `dist/` directory for testing.

## Build Configuration

### electron-builder Configuration
Located in `package.json`:

```json
{
  "build": {
    "appId": "com.unifiedai.hub",
    "productName": "Unified AI Hub",
    "directories": {
      "output": "dist"
    },
    "files": [
      "src/**/*",
      "node_modules/**/*",
      "package.json"
    ],
    "mac": {
      "category": "public.app-category.productivity",
      "target": [
        {
          "target": "dmg",
          "arch": ["x64", "arm64"]
        },
        {
          "target": "zip",
          "arch": ["x64", "arm64"]
        }
      ]
    },
    "win": {
      "target": [
        {
          "target": "nsis",
          "arch": ["x64"]
        },
        {
          "target": "zip",
          "arch": ["x64"]
        }
      ]
    },
    "linux": {
      "target": [
        {
          "target": "AppImage",
          "arch": ["x64"]
        },
        {
          "target": "deb",
          "arch": ["x64"]
        },
        {
          "target": "rpm",
          "arch": ["x64"]
        },
        {
          "target": "snap",
          "arch": ["x64"]
        }
      ]
    }
  }
}
```

## Build Optimization

### File Exclusions
The build process excludes:
- Development files
- Source maps
- Test files
- Documentation (except LICENSE)

### Compression
- ASAR packaging enabled by default
- Gzip compression for distributables
- Optimized for size

## Code Signing (Optional)

### macOS
```bash
# Install certificate to keychain
# Set environment variables
export CSC_LINK="path/to/certificate.p12"
export CSC_KEY_PASSWORD="password"

# Build with signing
npm run dist:mac
```

### Windows
```bash
# Set environment variables
export CSC_LINK="path/to/certificate.p12"
export CSC_KEY_PASSWORD="password"

# Build with signing
npm run dist:win
```

## Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Clean install
rm -rf node_modules
npm install
```

#### Build fails on macOS
```bash
# Install Xcode command line tools
xcode-select --install

# Clear npm cache
npm cache clean --force
```

#### Windows build issues
```bash
# Install windows-build-tools
npm install --global --production windows-build-tools
```

### Debug Builds
```bash
# Run with debug output
DEBUG=electron-builder npm run dist

# Verbose logging
npm run dist -- --publish=never
```

## Quick Launch Scripts

### macOS
```bash
./run-source-macos.sh
```

### Linux
```bash
./run-source-linux.sh
```

### Windows
```batch
run-source-windows.bat
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| NODE_ENV | Environment mode | development |
| ELECTRON_IS_DEV | Development flag | true |
| CSC_LINK | Code signing certificate | - |
| CSC_KEY_PASSWORD | Certificate password | - |
| GH_TOKEN | GitHub token for releases | - |