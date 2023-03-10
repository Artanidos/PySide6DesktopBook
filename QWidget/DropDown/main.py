import sys
import pycountry
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QGridLayout, 
                             QLineEdit, QRadioButton, QComboBox)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Qt DropDown")
        widget = QWidget()
        layout = QGridLayout()
        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Enter part of countryname")
        self.filter.setMinimumWidth(200)
        self.filter.textChanged.connect(self.filterChanged)
        self.free = QRadioButton("Free")
        self.premium = QRadioButton("Premium")
        self.enterprise = QRadioButton("Enterprise")
        self.combo = QComboBox()
        for country in pycountry.countries:
            self.combo.addItem(country.name)

        layout.addWidget(QLabel("Filter:"), 0, 0)
        layout.addWidget(self.filter, 0, 1)
        layout.addWidget(QLabel("Country"), 1, 0)
        layout.addWidget(self.combo, 1, 1)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def filterChanged(self, text):
        filter = text.lower()
        self.combo.clear()
        for country in pycountry.countries:
            if text in country.name.lower():
                self.combo.addItem(country.name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())