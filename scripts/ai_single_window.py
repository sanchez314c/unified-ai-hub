#!/usr/bin/env python
"""
Single Window AI Wrapper - All three AIs in ONE window
"""

import webview
import threading
import time

html = """
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
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            background: #1a1a1a;
            height: 100vh;
            overflow: hidden;
        }
        
        .toolbar {
            background: #2d2d2d;
            padding: 10px;
            display: flex;
            gap: 10px;
            border-bottom: 1px solid #444;
        }
        
        button {
            padding: 8px 16px;
            background: #0084ff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        
        button:hover {
            background: #0066cc;
        }
        
        .container {
            height: calc(100vh - 50px);
            display: flex;
            position: relative;
        }
        
        /* Horizontal layout */
        .horizontal {
            flex-direction: row;
        }
        
        .horizontal iframe {
            width: 33.333%;
            height: 100%;
        }
        
        /* Vertical layout */
        .vertical {
            flex-direction: column;
        }
        
        .vertical iframe {
            width: 100%;
            height: 33.333%;
        }
        
        /* Grid layout */
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
        }
        
        .grid iframe:last-child {
            grid-column: span 2;
        }
        
        /* Focus layout */
        .focus {
            flex-direction: column;
        }
        
        .focus iframe {
            width: 100%;
            height: 70%;
            display: none;
        }
        
        .focus iframe.active {
            display: block;
        }
        
        .focus .mini-frames {
            height: 30%;
            display: flex;
            flex-direction: row;
        }
        
        .focus .mini-frames iframe {
            width: 33.333%;
            height: 100%;
            display: block;
            opacity: 0.7;
            cursor: pointer;
        }
        
        .focus .mini-frames iframe:hover {
            opacity: 1;
        }
        
        iframe {
            border: none;
            background: white;
        }
        
        .divider {
            width: 2px;
            background: #444;
            cursor: col-resize;
        }
        
        .divider-h {
            height: 2px;
            width: 100%;
            background: #444;
            cursor: row-resize;
        }
    </style>
</head>
<body>
    <div class="toolbar">
        <button onclick="setLayout('horizontal')">⬌ Horizontal</button>
        <button onclick="setLayout('vertical')">⬍ Vertical</button>
        <button onclick="setLayout('grid')">⊞ Grid</button>
        <button onclick="setLayout('focus')">◱ Focus</button>
        <button onclick="reloadAll()">↻ Reload All</button>
    </div>
    
    <div class="container horizontal" id="container">
        <iframe src="https://claude.ai/" id="claude"></iframe>
        <iframe src="https://grok.x.ai/" id="grok"></iframe>
        <iframe src="https://gemini.google.com/" id="gemini"></iframe>
    </div>
    
    <script>
        let currentLayout = 'horizontal';
        let focusedFrame = 'claude';
        
        function setLayout(layout) {
            const container = document.getElementById('container');
            container.className = 'container ' + layout;
            currentLayout = layout;
            
            if (layout === 'focus') {
                setupFocusLayout();
            }
        }
        
        function setupFocusLayout() {
            const container = document.getElementById('container');
            container.innerHTML = `
                <iframe src="https://claude.ai/" id="claude" class="active"></iframe>
                <iframe src="https://grok.x.ai/" id="grok"></iframe>
                <iframe src="https://gemini.google.com/" id="gemini"></iframe>
                <div class="mini-frames">
                    <iframe src="https://claude.ai/" onclick="focusFrame('claude')"></iframe>
                    <iframe src="https://grok.x.ai/" onclick="focusFrame('grok')"></iframe>
                    <iframe src="https://gemini.google.com/" onclick="focusFrame('gemini')"></iframe>
                </div>
            `;
        }
        
        function focusFrame(frameId) {
            document.querySelectorAll('.container > iframe').forEach(frame => {
                frame.classList.remove('active');
            });
            document.getElementById(frameId).classList.add('active');
            focusedFrame = frameId;
        }
        
        function reloadAll() {
            document.querySelectorAll('iframe').forEach(frame => {
                frame.src = frame.src;
            });
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === '1' && e.metaKey) {
                setLayout('horizontal');
            } else if (e.key === '2' && e.metaKey) {
                setLayout('vertical');
            } else if (e.key === '3' && e.metaKey) {
                setLayout('grid');
            } else if (e.key === '4' && e.metaKey) {
                setLayout('focus');
            } else if (e.key === 'r' && e.metaKey) {
                e.preventDefault();
                reloadAll();
            }
        });
    </script>
</body>
</html>
"""

def main():
    # Create a window with the HTML content
    window = webview.create_window(
        'Unified AI Hub - All in One Window',
        html=html,
        width=1920,
        height=1080,
        resizable=True,
        fullscreen=False
    )
    
    webview.start()

if __name__ == '__main__':
    print("Starting Unified AI Hub...")
    print("Keyboard shortcuts:")
    print("  Cmd+1: Horizontal layout")
    print("  Cmd+2: Vertical layout (stacked)")
    print("  Cmd+3: Grid layout")
    print("  Cmd+4: Focus layout")
    print("  Cmd+R: Reload all")
    main()