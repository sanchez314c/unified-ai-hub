import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView

class UnifiedAIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unified AI Wrapper")
        self.setGeometry(100, 100, 1920, 1080)  # Adjust to your screen size or use self.showMaximized() for fullscreen
        
        # Create splitter for horizontal layout
        splitter = QSplitter(self)
        
        # Claude WebView
        claude_view = QWebEngineView()
        claude_view.load(QUrl("https://claude.ai/"))
        
        # Grok WebView
        grok_view = QWebEngineView()
        grok_view.load(QUrl("https://grok.x.ai/"))  # Or use "https://x.com/grok" if preferred
        
        # Gemini WebView
        gemini_view = QWebEngineView()
        gemini_view.load(QUrl("https://gemini.google.com/"))
        
        # Add views to splitter
        splitter.addWidget(claude_view)
        splitter.addWidget(grok_view)
        splitter.addWidget(gemini_view)
        
        # Set equal sizes (optional)
        splitter.setSizes([self.width()//3, self.width()//3, self.width()//3])
        
        self.setCentralWidget(splitter)
        
        # Optional: Go fullscreen
        # self.showFullScreen()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UnifiedAIApp()
    window.show()
    sys.exit(app.exec())