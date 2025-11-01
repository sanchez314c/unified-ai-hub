#!/usr/bin/env python
"""
Unified AI Web Dashboard
Opens multiple AI services in browser tabs or creates a local dashboard
"""

import webbrowser
import time
import sys
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

# AI service URLs
AI_SERVICES = {
    "Claude": "https://claude.ai/",
    "Grok": "https://grok.x.ai/",
    "Gemini": "https://gemini.google.com/",
    "ChatGPT": "https://chatgpt.com/",
    "Perplexity": "https://www.perplexity.ai/"
}

def open_in_tabs():
    """Open each AI service in a new browser tab"""
    print("Opening AI services in browser tabs...")
    for name, url in AI_SERVICES.items():
        print(f"Opening {name}...")
        webbrowser.open_new_tab(url)
        time.sleep(0.5)  # Small delay between tabs
    print("\nAll services opened! Check your browser.")

def create_dashboard_html():
    """Create a local HTML dashboard with iframes"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unified AI Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #1a1a1a;
            color: #fff;
            overflow: hidden;
        }
        .header {
            background: #2a2a2a;
            padding: 10px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 50px;
            border-bottom: 1px solid #444;
        }
        .tabs {
            display: flex;
            gap: 10px;
        }
        .tab {
            padding: 8px 16px;
            background: #3a3a3a;
            border: none;
            color: #fff;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s;
        }
        .tab:hover {
            background: #4a4a4a;
        }
        .tab.active {
            background: #0084ff;
        }
        .content {
            height: calc(100vh - 50px);
            position: relative;
        }
        .frame-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: none;
        }
        .frame-container.active {
            display: block;
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
        .split-view {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            height: 100%;
            gap: 2px;
            background: #444;
            padding: 2px;
        }
        .split-view iframe {
            background: white;
        }
        .controls {
            display: flex;
            gap: 10px;
        }
        .btn {
            padding: 8px 12px;
            background: #4a4a4a;
            border: none;
            color: #fff;
            cursor: pointer;
            border-radius: 5px;
        }
        .btn:hover {
            background: #5a5a5a;
        }
        .notice {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #ff6b6b;
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            display: none;
            animation: slideIn 0.3s ease;
        }
        @keyframes slideIn {
            from { transform: translateX(400px); }
            to { transform: translateX(0); }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="tabs" id="tabs">
            <button class="tab active" data-service="claude">Claude</button>
            <button class="tab" data-service="grok">Grok</button>
            <button class="tab" data-service="gemini">Gemini</button>
            <button class="tab" data-service="chatgpt">ChatGPT</button>
            <button class="tab" data-service="perplexity">Perplexity</button>
        </div>
        <div class="controls">
            <button class="btn" onclick="toggleSplitView()">Toggle Split View</button>
            <button class="btn" onclick="refreshCurrent()">Refresh</button>
            <button class="btn" onclick="openExternal()">Open in Browser</button>
        </div>
    </div>
    
    <div class="content" id="content">
        <div class="frame-container active" id="claude-frame">
            <iframe src="https://claude.ai/" title="Claude"></iframe>
        </div>
        <div class="frame-container" id="grok-frame">
            <iframe src="https://grok.x.ai/" title="Grok"></iframe>
        </div>
        <div class="frame-container" id="gemini-frame">
            <iframe src="https://gemini.google.com/" title="Gemini"></iframe>
        </div>
        <div class="frame-container" id="chatgpt-frame">
            <iframe src="https://chatgpt.com/" title="ChatGPT"></iframe>
        </div>
        <div class="frame-container" id="perplexity-frame">
            <iframe src="https://www.perplexity.ai/" title="Perplexity"></iframe>
        </div>
    </div>
    
    <div class="notice" id="notice">
        Note: Some AI services may not load in iframes due to security policies. 
        Use "Open in Browser" for full access.
    </div>
    
    <script>
        let currentService = 'claude';
        let splitView = false;
        
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const service = tab.dataset.service;
                switchToService(service);
            });
        });
        
        function switchToService(service) {
            if (splitView) return;
            
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelector(`[data-service="${service}"]`).classList.add('active');
            
            document.querySelectorAll('.frame-container').forEach(f => f.classList.remove('active'));
            document.getElementById(`${service}-frame`).classList.add('active');
            
            currentService = service;
        }
        
        function toggleSplitView() {
            splitView = !splitView;
            const content = document.getElementById('content');
            
            if (splitView) {
                content.innerHTML = `
                    <div class="split-view">
                        <iframe src="https://claude.ai/" title="Claude"></iframe>
                        <iframe src="https://grok.x.ai/" title="Grok"></iframe>
                        <iframe src="https://gemini.google.com/" title="Gemini"></iframe>
                    </div>
                `;
            } else {
                location.reload();
            }
        }
        
        function refreshCurrent() {
            if (splitView) {
                location.reload();
            } else {
                const frame = document.getElementById(`${currentService}-frame`).querySelector('iframe');
                frame.src = frame.src;
            }
        }
        
        function openExternal() {
            const urls = {
                claude: 'https://claude.ai/',
                grok: 'https://grok.x.ai/',
                gemini: 'https://gemini.google.com/',
                chatgpt: 'https://chatgpt.com/',
                perplexity: 'https://www.perplexity.ai/'
            };
            window.open(urls[currentService], '_blank');
        }
        
        // Show notice if needed
        setTimeout(() => {
            const notice = document.getElementById('notice');
            notice.style.display = 'block';
            setTimeout(() => {
                notice.style.display = 'none';
            }, 8000);
        }, 2000);
    </script>
</body>
</html>"""
    
    with open('/tmp/unified_ai_dashboard.html', 'w') as f:
        f.write(html)
    return '/tmp/unified_ai_dashboard.html'

def serve_dashboard():
    """Serve the dashboard locally"""
    html_path = create_dashboard_html()
    
    # Simple HTTP server
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = '/unified_ai_dashboard.html'
            return SimpleHTTPRequestHandler.do_GET(self)
    
    os.chdir('/tmp')
    httpd = HTTPServer(('localhost', 8888), Handler)
    
    print("Starting local dashboard server...")
    print("Dashboard available at: http://localhost:8888/")
    print("Press Ctrl+C to stop the server\n")
    
    # Open in browser
    webbrowser.open('http://localhost:8888/')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

def main():
    print("Unified AI Launcher")
    print("=" * 40)
    print("1. Open all services in browser tabs")
    print("2. Create local dashboard (experimental)")
    print("3. Quick open - Claude, Grok, Gemini only")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("Choose option (1-3): ").strip()
    
    if choice == '1':
        open_in_tabs()
    elif choice == '2':
        serve_dashboard()
    elif choice == '3':
        print("Opening Claude, Grok, and Gemini...")
        for name in ['Claude', 'Grok', 'Gemini']:
            webbrowser.open_new_tab(AI_SERVICES[name])
            time.sleep(0.5)
        print("Done!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()