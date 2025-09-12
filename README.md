####################################################################################
#                                                                                  #
#   ██████╗ ███████╗████████╗    ███████╗██╗    ██╗██╗███████╗████████╗██╗   ██╗ #
#  ██╔════╝ ██╔════╝╚══██╔══╝    ██╔════╝██║    ██║██║██╔════╝╚══██╔══╝╚██╗ ██╔╝ #
#  ██║  ███╗█████╗     ██║       ███████╗██║ █╗ ██║██║█████╗     ██║     ╚████╔╝  #
#  ██║   ██║██╔══╝     ██║       ╚════██║██║███╗██║██║██╔══╝     ██║      ╚██╔╝   #
#  ╚██████╔╝███████╗   ██║       ███████║╚███╔███╔╝██║██╗        ██║       ██║    #
#   ╚═════╝ ╚══════╝   ╚═╝       ╚══════╝ ╚══╝╚══╝ ╚═╝╚═╝        ╚═╝       ╚═╝    #
#                                                                                  #
####################################################################################
#
# Project Name: Unified AI Hub
#
# Author: @spacewelder314
#
# Date Created: 2025-08-22
#
# Last Modified: 2025-09-01
#
# Version: 1.0.0
#
# Description: Unified interface for multiple AI assistants (Claude, Grok, Gemini, 
#              ChatGPT) in a single Electron window with flexible layouts
#
# Language/Framework: JavaScript/Electron
#
# Usage: npm start (development) or run the compiled app from dist/
#
# Dependencies: electron@^27.3.11, electron-builder@^24.13.3
#
# GitHub: https://github.com/spacewelder314/UnifiedAI
#
# Notes: Multi-AI interface with layout switching and persistent sessions
#
####################################################################################

# Unified AI Wrapper

A powerful Electron-based application that provides a unified interface for multiple AI assistants in a single window.

## Features

- **Multi-AI Support**: Access Claude, Grok, Gemini, and ChatGPT simultaneously
- **Flexible Layouts**: 
  - Horizontal split (3 AIs side-by-side)
  - Vertical stack (3 AIs stacked)
  - Grid view (2x2 with 4 AIs)
  - Focus mode (one AI primary, others minimized)
- **Custom Scrollbars**: Elegant, dark-theme optimized scrollbars
- **Context Menu Support**: Full copy/paste functionality with force paste option
- **Keyboard Shortcuts**: Quick layout switching and navigation
- **Persistent Sessions**: Maintains separate sessions for each AI

## Installation

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/unified-ai-wrapper.git
cd unified-ai-wrapper
```

2. Install dependencies:
```bash
npm install
```

3. Run the application:
```bash
npm start
```

## Building

### Build for all platforms:
```bash
npm run build
```

### Platform-specific builds:
```bash
npm run build:mac    # macOS
npm run build:win    # Windows
npm run build:linux  # Linux
```

## Usage

### Keyboard Shortcuts

- `Cmd/Ctrl + 1`: Horizontal layout
- `Cmd/Ctrl + 2`: Vertical layout
- `Cmd/Ctrl + 3`: Grid layout (4 AIs)
- `Cmd/Ctrl + 4`: Focus Claude
- `Cmd/Ctrl + 5`: Focus Grok
- `Cmd/Ctrl + 6`: Focus Gemini
- `Cmd/Ctrl + R`: Reload all views
- `Cmd/Ctrl + Shift + V`: Force paste
- `F11`: Toggle fullscreen

### Layout Options

The application supports multiple layout configurations:

1. **Horizontal Layout**: Three AI assistants side-by-side
2. **Vertical Layout**: Three AI assistants stacked vertically
3. **Grid Layout**: Four AI assistants in a 2x2 grid
4. **Focus Mode**: One AI takes primary view with others minimized

## Project Structure

```
unified-ai-wrapper/
├── src/                    # Source files
│   ├── main.js            # Main process
│   ├── preload.js         # Preload script
│   └── index.html         # Renderer HTML
├── scripts/               # Build and utility scripts
├── build-resources/       # Build assets
│   ├── icons/            # Application icons
│   └── entitlements.mac.plist
├── archive/              # Archived/legacy files
├── docs/                 # Documentation
├── package.json          # Project configuration
└── README.md            # This file
```

## Development

### Running in Development Mode

```bash
npm run dev
```

### Testing

```bash
npm test
```

## Configuration

The application uses separate persistent partitions for each AI service to maintain independent sessions. Configuration can be modified in `main.js`.

## Security

- Each AI service runs in an isolated BrowserView with its own partition
- Context isolation is enabled
- Web security is enforced
- No node integration in renderers

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Electron](https://www.electronjs.org/)
- AI services provided by respective companies (Anthropic, xAI, Google, OpenAI)

## Support

For issues, questions, or suggestions, please open an issue on GitHub.