import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QUrl
from PySide6.QtQuickWidgets import QQuickWidget


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Qt Combo Demo")
        widget= QWidget()
        layout = QVBoxLayout()

        wid = QQuickWidget()
        wid.setSource(QUrl("view.qml"))

        label = QLabel("Hello World")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(wid)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())