import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Test Qt")
    window.setGeometry(100, 100, 400, 300)
    
    label = QLabel("If you can see this, PyQt6 is working!", window)
    label.setGeometry(50, 100, 300, 50)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()