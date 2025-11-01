#!/usr/bin/env python
"""
Unified AI Desktop App - Single Window with Multiple Webviews
Uses pywebview to create a proper desktop app with multiple AI services
"""

import webview
import threading
import json

class UnifiedAIApp:
    def __init__(self):
        self.current_view = 'claude'
        self.layout = 'tabs'
        
    def get_html(self):
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Unified AI Hub</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a1a;
            color: #fff;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .nav {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .tab {
            padding: 10px 20px;
            background: rgba(255,255,255,0.1);
            border: 2px solid transparent;
            color: white;
            cursor: pointer;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .tab:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }
        
        .tab.active {
            background: rgba(255,255,255,0.3);
            border-color: white;
            box-shadow: 0 4px 15px rgba(255,255,255,0.2);
        }
        
        .layouts {
            display: flex;
            gap: 10px;
        }
        
        .layout-btn {
            padding: 8px 16px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            cursor: pointer;
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .layout-btn:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .content {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #2a2a2a;
            position: relative;
        }
        
        .ai-frame {
            width: 100%;
            height: 100%;
            display: none;
            background: white;
            position: absolute;
            top: 0;
            left: 0;
        }
        
        .ai-frame.active {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .welcome {
            text-align: center;
            padding: 40px;
        }
        
        .welcome h1 {
            font-size: 48px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .welcome p {
            font-size: 20px;
            color: #aaa;
            margin-bottom: 30px;
        }
        
        .service-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .service-card {
            background: rgba(255,255,255,0.05);
            padding: 30px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .service-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.1);
            box-shadow: 0 10px 30px rgba(102,126,234,0.3);
        }
        
        .service-card h3 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .service-card p {
            font-size: 14px;
            color: #999;
        }
        
        .instructions {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            padding: 15px 20px;
            border-radius: 8px;
            font-size: 12px;
            max-width: 300px;
        }
        
        .instructions h4 {
            margin-bottom: 10px;
            color: #667eea;
        }
        
        .instructions ul {
            list-style: none;
            color: #aaa;
        }
        
        .instructions li {
            margin: 5px 0;
        }
        
        .instructions kbd {
            background: rgba(255,255,255,0.1);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="nav">
            <button class="tab active" onclick="openAI('claude')">🤖 Claude</button>
            <button class="tab" onclick="openAI('grok')">🚀 Grok</button>
            <button class="tab" onclick="openAI('gemini')">✨ Gemini</button>
            <button class="tab" onclick="openAI('chatgpt')">💬 ChatGPT</button>
            <button class="tab" onclick="openAI('perplexity')">🔍 Perplexity</button>
        </div>
        <div class="layouts">
            <button class="layout-btn" onclick="openAllInBrowser()">🌐 Open All in Browser</button>
            <button class="layout-btn" onclick="window.pywebview.api.toggle_fullscreen()">⛶ Fullscreen</button>
        </div>
    </div>
    
    <div class="content">
        <div class="ai-frame active" id="claude-frame">
            <div class="welcome">
                <h1>Unified AI Hub</h1>
                <p>Click a service above to open it in a new window</p>
                <div class="service-grid">
                    <div class="service-card" onclick="openAI('claude')">
                        <h3>Claude</h3>
                        <p>Anthropic's AI Assistant</p>
                    </div>
                    <div class="service-card" onclick="openAI('grok')">
                        <h3>Grok</h3>
                        <p>X.AI's Witty Assistant</p>
                    </div>
                    <div class="service-card" onclick="openAI('gemini')">
                        <h3>Gemini</h3>
                        <p>Google's AI Model</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="instructions">
        <h4>Quick Tips:</h4>
        <ul>
            <li>Click tabs to switch between AIs</li>
            <li>Each AI opens in its own window</li>
            <li>Use <kbd>Cmd+Tab</kbd> to switch</li>
            <li>Click "Open All" for browser tabs</li>
        </ul>
    </div>
    
    <script>
        const services = {
            claude: 'https://claude.ai/',
            grok: 'https://grok.x.ai/',
            gemini: 'https://gemini.google.com/',
            chatgpt: 'https://chatgpt.com/',
            perplexity: 'https://www.perplexity.ai/'
        };
        
        function openAI(service) {
            // Update active tab
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Call Python to open new window
            window.pywebview.api.open_service(service);
        }
        
        function openAllInBrowser() {
            window.pywebview.api.open_all_browser();
        }
    </script>
</body>
</html>
"""

class API:
    def __init__(self):
        self.windows = {}
        self.main_window = None
        
    def set_main_window(self, window):
        self.main_window = window
        
    def open_service(self, service):
        urls = {
            'claude': 'https://claude.ai/',
            'grok': 'https://grok.x.ai/',
            'gemini': 'https://gemini.google.com/',
            'chatgpt': 'https://chatgpt.com/',
            'perplexity': 'https://www.perplexity.ai/'
        }
        
        if service in urls:
            if service not in self.windows or not self.windows[service]:
                # Create new window for this service
                self.windows[service] = webview.create_window(
                    f'{service.capitalize()} AI',
                    urls[service],
                    width=1200,
                    height=800
                )
            else:
                # Focus existing window
                self.windows[service].show()
                
    def open_all_browser(self):
        import webbrowser
        urls = [
            'https://claude.ai/',
            'https://grok.x.ai/',
            'https://gemini.google.com/'
        ]
        for url in urls:
            webbrowser.open_new_tab(url)
            
    def toggle_fullscreen(self):
        if self.main_window:
            self.main_window.toggle_fullscreen()

def main():
    app = UnifiedAIApp()
    api = API()
    
    # Create main window
    window = webview.create_window(
        'Unified AI Hub',
        html=app.get_html(),
        width=1400,
        height=900,
        js_api=api
    )
    
    api.set_main_window(window)
    
    print("Unified AI Hub Started!")
    print("Click on any AI service to open it in a separate window")
    print("All windows are part of the same application")
    
    webview.start()

if __name__ == '__main__':
    main()