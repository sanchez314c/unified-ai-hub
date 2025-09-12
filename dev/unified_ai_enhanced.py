import sys
import os
from PyQt6.QtCore import QUrl, Qt, QSettings
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSplitter, 
                             QTabWidget, QVBoxLayout, QWidget, 
                             QPushButton, QHBoxLayout, QToolBar,
                             QStatusBar, QLabel, QMenu, QMenuBar)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtGui import QAction, QKeySequence

class AIWebView(QWebEngineView):
    def __init__(self, name, url, parent=None):
        super().__init__(parent)
        self.name = name
        self.home_url = url
        
        # Enable persistent cookies and storage
        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        
        # Set a proper user agent
        profile.setHttpUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.load(QUrl(url))
        
    def reload_home(self):
        self.load(QUrl(self.home_url))

class UnifiedAIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('UnifiedAI', 'MainWindow')
        self.setWindowTitle("Unified AI Hub")
        
        # Restore window geometry or set default
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.setGeometry(100, 100, 1920, 1080)
        
        # Store AI configurations
        self.ai_configs = [
            ("Claude", "https://claude.ai/"),
            ("Grok", "https://grok.x.ai/"),
            ("Gemini", "https://gemini.google.com/"),
            ("ChatGPT", "https://chatgpt.com/"),
            ("Perplexity", "https://www.perplexity.ai/"),
        ]
        
        self.web_views = {}
        self.setup_ui()
        self.setup_menu()
        self.setup_shortcuts()
        
        # Restore splitter state
        splitter_state = self.settings.value('splitter_state')
        if splitter_state and hasattr(self, 'main_splitter'):
            self.main_splitter.restoreState(splitter_state)
            
        # Restore layout mode
        layout_mode = self.settings.value('layout_mode', 'split')
        if layout_mode == 'tabs':
            self.switch_to_tabs()
        
    def setup_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Layout toggle button
        self.layout_toggle = QPushButton("Switch to Tabs")
        self.layout_toggle.clicked.connect(self.toggle_layout)
        toolbar.addWidget(self.layout_toggle)
        
        toolbar.addSeparator()
        
        # Refresh buttons for each AI
        for name, url in self.ai_configs[:3]:  # Show first 3 in split mode
            refresh_action = QAction(f"Refresh {name}", self)
            refresh_action.triggered.connect(lambda checked, n=name: self.refresh_ai(n))
            toolbar.addAction(refresh_action)
        
        # Create split view (default)
        self.create_split_view()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def create_split_view(self):
        # Create splitter
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create web views for first 3 AIs
        for name, url in self.ai_configs[:3]:
            web_view = AIWebView(name, url)
            self.web_views[name] = web_view
            self.main_splitter.addWidget(web_view)
            
            # Connect load progress
            web_view.loadProgress.connect(lambda p, n=name: self.update_load_status(n, p))
        
        # Set equal sizes
        self.main_splitter.setSizes([self.width()//3] * 3)
        
        # Clear layout and add splitter
        self.clear_layout()
        self.main_layout.addWidget(self.main_splitter)
        self.current_layout = 'split'
        
    def create_tab_view(self):
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs for all AIs
        for name, url in self.ai_configs:
            if name not in self.web_views:
                web_view = AIWebView(name, url)
                self.web_views[name] = web_view
                web_view.loadProgress.connect(lambda p, n=name: self.update_load_status(n, p))
            else:
                web_view = self.web_views[name]
            
            self.tab_widget.addTab(web_view, name)
        
        # Clear layout and add tabs
        self.clear_layout()
        self.main_layout.addWidget(self.tab_widget)
        self.current_layout = 'tabs'
        
    def clear_layout(self):
        # Remove all widgets from layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
                
    def toggle_layout(self):
        if self.current_layout == 'split':
            self.switch_to_tabs()
        else:
            self.switch_to_split()
            
    def switch_to_tabs(self):
        self.create_tab_view()
        self.layout_toggle.setText("Switch to Split")
        self.status_bar.showMessage("Switched to tab view", 2000)
        
    def switch_to_split(self):
        self.create_split_view()
        self.layout_toggle.setText("Switch to Tabs")
        self.status_bar.showMessage("Switched to split view", 2000)
        
    def setup_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Fullscreen action
        fullscreen_action = QAction('Toggle Fullscreen', self)
        fullscreen_action.setShortcut(QKeySequence('F11'))
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        file_menu.addAction(fullscreen_action)
        
        file_menu.addSeparator()
        
        # Quit action
        quit_action = QAction('Quit', self)
        quit_action.setShortcut(QKeySequence('Ctrl+Q'))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        # Reload all action
        reload_all_action = QAction('Reload All', self)
        reload_all_action.setShortcut(QKeySequence('Ctrl+Shift+R'))
        reload_all_action.triggered.connect(self.reload_all)
        view_menu.addAction(reload_all_action)
        
        # Navigate to specific AI
        navigate_menu = menubar.addMenu('Navigate')
        for i, (name, url) in enumerate(self.ai_configs, 1):
            if i <= 9:  # Only first 9 get shortcuts
                action = QAction(f'{name}', self)
                action.setShortcut(QKeySequence(f'Ctrl+{i}'))
                action.triggered.connect(lambda checked, n=name: self.focus_ai(n))
                navigate_menu.addAction(action)
                
    def setup_shortcuts(self):
        # Additional keyboard shortcuts
        
        # Switch layout with Ctrl+L
        switch_layout = QAction(self)
        switch_layout.setShortcut(QKeySequence('Ctrl+L'))
        switch_layout.triggered.connect(self.toggle_layout)
        self.addAction(switch_layout)
        
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.status_bar.showMessage("Exited fullscreen", 2000)
        else:
            self.showFullScreen()
            self.status_bar.showMessage("Entered fullscreen (F11 to exit)", 2000)
            
    def refresh_ai(self, name):
        if name in self.web_views:
            self.web_views[name].reload()
            self.status_bar.showMessage(f"Refreshing {name}...", 2000)
            
    def reload_all(self):
        for web_view in self.web_views.values():
            web_view.reload()
        self.status_bar.showMessage("Reloading all AIs...", 2000)
        
    def focus_ai(self, name):
        if self.current_layout == 'tabs' and name in self.web_views:
            index = list(self.web_views.keys()).index(name)
            if hasattr(self, 'tab_widget'):
                self.tab_widget.setCurrentIndex(index)
                self.status_bar.showMessage(f"Switched to {name}", 2000)
                
    def update_load_status(self, name, progress):
        if progress < 100:
            self.status_bar.showMessage(f"Loading {name}: {progress}%")
        else:
            self.status_bar.showMessage(f"{name} loaded", 1000)
            
    def closeEvent(self, event):
        # Save settings
        self.settings.setValue('geometry', self.saveGeometry())
        if hasattr(self, 'main_splitter'):
            self.settings.setValue('splitter_state', self.main_splitter.saveState())
        self.settings.setValue('layout_mode', self.current_layout)
        event.accept()

def main():
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Unified AI Hub")
    app.setOrganizationName("UnifiedAI")
    
    window = UnifiedAIApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()