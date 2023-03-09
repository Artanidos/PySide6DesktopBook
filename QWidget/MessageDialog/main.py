import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Qt Demo")
        widget = QWidget()
        layout = QVBoxLayout()
        simple = QPushButton("Simple")
        save = QPushButton("Save")
        details = QPushButton("Save with details")
        warning = QPushButton("Warning")
        layout.addWidget(simple)
        layout.addWidget(save)
        layout.addWidget(details)
        layout.addWidget(warning)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        simple.clicked.connect(self.simple)
        save.clicked.connect(self.save)
        details.clicked.connect(self.details)
        warning.clicked.connect(self.warning)

    def simple(self):
        msg = QMessageBox()
        msg.setText("This is a simple message.")
        msg.exec()

    def save(self):
        msg = QMessageBox()
        msg.setText("The document has been modified.")
        msg.setInformativeText("Do you want to save your changes?")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Save)
        ret = msg.exec()

    def details(self):
        msg = QMessageBox()
        msg.setText("The document has been modified.")
        msg.setInformativeText("Do you want to save your changes?")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Save)
        msg.setDetailedText("1: First line\n2: Seconds line\n3: Third line")
        ret = msg.exec()

    def warning(self):
        ret = QMessageBox.warning(self, "My Application", 
            "The document has been modified.\n Do you want to save your changes?", 
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, 
            QMessageBox.Save)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())