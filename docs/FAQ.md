# Frequently Asked Questions

## General Questions

### Q: What is UnifiedAI Hub?
A: UnifiedAI Hub is an Electron-based desktop application that provides a unified interface for accessing multiple AI assistants (Claude, Grok, Gemini, ChatGPT, and others) in a single window.

### Q: Which AI services are supported?
A: Currently supports 11 AI services:
- Claude (claude.ai)
- Grok (grok.x.ai)
- Gemini (gemini.google.com)
- ChatGPT (chatgpt.com)
- Meta AI (meta.ai)
- OpenRouter (openrouter.ai)
- Together AI (together.ai)
- Perplexity (perplexity.ai)
- Mistral (mistral.ai)
- DeepSeek (deepseek.com)
- Moonshot AI (moonshot.ai)

### Q: Is UnifiedAI Hub free?
A: Yes, the application itself is free and open-source (MIT license). However, you need accounts with the respective AI services, which may have their own pricing.

## Installation and Setup

### Q: What are the system requirements?
A: 
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 500MB available space
- **CPU**: Intel/AMD x64, Apple Silicon (ARM64)
- **OS**: macOS 10.15+, Windows 10+, or modern Linux

### Q: How do I install UnifiedAI Hub?
A: 
1. Download the appropriate version for your platform
2. Run the installer (DMG/EXE/DEB/AppImage)
3. Launch the application
4. Log in to each AI service you want to use

### Q: Do I need to install each AI service separately?
A: No, UnifiedAI Hub loads the AI services directly from their websites. You just need to log in to each service within the application.

## Usage

### Q: How do I switch between layouts?
A: Use the layout buttons in the control bar or keyboard shortcuts:
- `Cmd/Ctrl + 1`: Horizontal layout
- `Cmd/Ctrl + 2`: Vertical layout
- `Cmd/Ctrl + 3`: Grid layout
- `Cmd/Ctrl + 4`: Four-column layout

### Q: Can I use different AI services in each position?
A: Yes! Use the dropdown menus in the control bar to select which AI service appears in each position.

### Q: Are my sessions saved?
A: Yes, each AI service runs in its own persistent session partition. Your login state and conversation history are maintained between application restarts.

### Q: How do I enable/disable AI services?
A: Use the LLM selection dropdowns to choose which services are active. You can have up to 4 services visible simultaneously.

## Technical Questions

### Q: How does session isolation work?
A: Each AI service runs in a separate BrowserView with its own session partition (`persist:ai-{name}`). This prevents cross-contamination of data and maintains independent authentication.

### Q: Is my data secure?
A: Yes. The application uses:
- Context isolation for security
- Separate session partitions
- No data collection or telemetry
- Direct connections to AI service websites

### Q: Can I use UnifiedAI Hub offline?
A: The application shell works offline, but AI services require an internet connection to function.

## Troubleshooting

### Q: The application won't start
A: Try these solutions:
1. Check if your system meets the requirements
2. Reinstall the application
3. Check antivirus software isn't blocking it
4. Run as administrator (Windows) or with sudo (Linux)

### Q: AI services aren't loading
A: 
1. Check your internet connection
2. Verify the AI service websites are accessible
3. Try reloading with `Cmd/Ctrl + R`
4. Clear cache in settings (if available)

### Q: Layout switching is slow
A: 
1. Close unused AI services
2. Restart the application
3. Check available memory
4. Try a simpler layout

### Q: I can't log in to an AI service
A: 
1. Verify your credentials
2. Check if the AI service is having issues
3. Try logging in directly on their website
4. Clear the session partition for that service

## Development

### Q: How can I contribute?
A: Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### Q: How do I add a new AI service?
A: Add the service to the `llmConfig` object in `src/main.js`. See [DEVELOPMENT.md](DEVELOPMENT.md) for details.

### Q: Can I customize the layouts?
A: Yes, layouts are defined in `src/main.js`. You can modify existing layouts or add new ones.

## Privacy and Security

### Q: Does UnifiedAI Hub collect my data?
A: No, the application does not collect or transmit any user data. All data stays on your local machine.

### Q: Where are my conversations stored?
A: Conversations are stored in the session partitions managed by Electron/Chromium, not by UnifiedAI Hub directly.

### Q: Can I use UnifiedAI Hub in a corporate environment?
A: Yes, but ensure your corporate security policy allows access to the AI service websites.

## Platform-Specific

### Q: Does it work on Apple Silicon Macs?
A: Yes, Universal binaries are provided for both Intel and Apple Silicon Macs.

### Q: Why does Windows show a security warning?
A: This is normal for new applications. Click "More info" and "Run anyway" if you trust the source.

### Q: Can I run it from source on Linux?
A: Yes, use `./run-source-linux.sh` after installing dependencies with `npm install`.

## Still Have Questions?

If your question isn't answered here:
1. Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide
2. Search existing GitHub issues
3. Open a new issue on GitHub
4. Contact the maintainers directly