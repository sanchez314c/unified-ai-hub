#!/usr/bin/env python
"""
Unified AI Wrapper - All three AIs in ONE window with multiple view modes
"""

import tkinter as tk
from tkinter import ttk
import webview
import threading
import sys

class UnifiedAIWrapper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Unified AI Wrapper")
        self.root.geometry("1920x1080")
        
        # Make it fullscreen-capable
        self.root.state('zoomed')  # Start maximized
        
        # Current layout mode
        self.layout_mode = "horizontal"
        
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Horizontal Split", command=lambda: self.change_layout("horizontal"))
        view_menu.add_command(label="Vertical Split", command=lambda: self.change_layout("vertical"))
        view_menu.add_command(label="Stacked", command=lambda: self.change_layout("stacked"))
        view_menu.add_command(label="Grid (2x2)", command=lambda: self.change_layout("grid"))
        view_menu.add_separator()
        view_menu.add_command(label="Fullscreen", command=self.toggle_fullscreen)
        
        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create webview windows in separate threads
        self.webviews = {}
        self.create_webviews()
        
        # Start with horizontal layout
        self.change_layout("horizontal")
        
    def create_webviews(self):
        """Create the three webview windows"""
        # We'll use pywebview to create embedded browser windows
        self.claude_window = None
        self.grok_window = None  
        self.gemini_window = None
        
        # Create frames for each AI
        self.claude_frame = ttk.Frame(self.main_frame, relief=tk.SUNKEN, borderwidth=2)
        self.grok_frame = ttk.Frame(self.main_frame, relief=tk.SUNKEN, borderwidth=2)
        self.gemini_frame = ttk.Frame(self.main_frame, relief=tk.SUNKEN, borderwidth=2)
        
        # Add labels for now (webview will replace these)
        ttk.Label(self.claude_frame, text="Claude AI", font=("Arial", 24)).pack(expand=True)
        ttk.Label(self.grok_frame, text="Grok AI", font=("Arial", 24)).pack(expand=True)
        ttk.Label(self.gemini_frame, text="Gemini AI", font=("Arial", 24)).pack(expand=True)
        
    def change_layout(self, mode):
        """Change the layout of the three panels"""
        # Clear current layout
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()
            widget.grid_forget()
        
        self.layout_mode = mode
        
        if mode == "horizontal":
            # Three panels side by side
            self.claude_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.grok_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.gemini_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
        elif mode == "vertical":
            # Three panels stacked vertically
            self.claude_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.grok_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.gemini_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
        elif mode == "stacked":
            # Tabbed interface
            notebook = ttk.Notebook(self.main_frame)
            notebook.pack(fill=tk.BOTH, expand=True)
            notebook.add(self.claude_frame, text="Claude")
            notebook.add(self.grok_frame, text="Grok")
            notebook.add(self.gemini_frame, text="Gemini")
            
        elif mode == "grid":
            # 2x2 grid (one will be larger)
            self.claude_frame.grid(row=0, column=0, sticky="nsew")
            self.grok_frame.grid(row=0, column=1, sticky="nsew")
            self.gemini_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
            
            self.main_frame.grid_rowconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_columnconfigure(1, weight=1)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def create_pywebview_app():
    """Alternative using pywebview for actual web rendering"""
    import webview
    
    class UnifiedAIWebview:
        def __init__(self):
            self.windows = []
            
        def create_windows(self):
            # Create three windows that we'll manage
            self.claude = webview.create_window('Claude', 'https://claude.ai/', 
                                               x=0, y=0, width=640, height=1080)
            self.grok = webview.create_window('Grok', 'https://grok.x.ai/',
                                             x=640, y=0, width=640, height=1080)
            self.gemini = webview.create_window('Gemini', 'https://gemini.google.com/',
                                               x=1280, y=0, width=640, height=1080)
            
            self.windows = [self.claude, self.grok, self.gemini]
            
        def start(self):
            self.create_windows()
            webview.start()
    
    app = UnifiedAIWebview()
    app.start()

# Try pywebview first, fall back to tkinter
try:
    import webview
    print("Starting unified AI wrapper with web rendering...")
    create_pywebview_app()
except ImportError:
    print("pywebview not found, using tkinter interface...")
    print("Install pywebview with: pip install pywebview")
    print("For now, showing layout demo...")
    app = UnifiedAIWrapper()
    app.run()