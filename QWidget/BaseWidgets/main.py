import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QGridLayout, 
                             QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, 
                             QRadioButton, QCheckBox, QComboBox)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Qt Demo")
        widget = QWidget()
        layout = QGridLayout()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter your full name here")
        self.name_edit.setMinimumWidth(200)
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Enter a valid email address here")
        group = QGroupBox("Select category")
        group.setLayout(vbox)
        self.free = QRadioButton("Free")
        self.premium = QRadioButton("Premium")
        self.enterprise = QRadioButton("Enterprise")
        vbox.addWidget(self.free)
        vbox.addWidget(self.premium)
        vbox.addWidget(self.enterprise)
        self.cb = QCheckBox("Send me an invoice")
        self.combo = QComboBox()
        self.combo.addItem("5 GB")
        self.combo.addItem("10 GB")
        self.combo.addItem("20 GB")
        self.combo.addItem("50 GB")
        self.combo.addItem("100 GB")
        ok_button = QPushButton("Ok")
        cancel_button = QPushButton("Cancel")
        hbox.addStretch()
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)
        layout.addWidget(QLabel("Name:"), 0, 0)
        layout.addWidget(self.name_edit, 0, 1)
        layout.addWidget(QLabel("Email:"), 1, 0)
        layout.addWidget(self.email_edit, 1, 1)
        layout.addWidget(QLabel("Data volume"), 2, 0)
        layout.addWidget(self.combo, 2, 1)
        layout.addWidget(self.cb, 3, 0, 1, 2)
        layout.addWidget(group, 4, 0, 1, 2)
        layout.addLayout(hbox, 5, 0, 1, 2)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        ok_button.clicked.connect(self.okClicked)

    def okClicked(self):
        name = self.name_edit.text()
        email = self.email_edit.text()
        data_volume = self.combo.currentText()
        send_invoice = self.cb.checkState() == Qt.Checked
        if self.free.isChecked():
            category = "Free"
        elif self.premium.isChecked():
            category = "Premium"
        elif self.enterprise.isChecked():
            category = "Enterprise"
        else:
            category = "None"

        print("name:", name)
        print("email:", email)
        print("data:", data_volume)
        print("invoice:", send_invoice)
        print("category:", category)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())