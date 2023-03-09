import sys
from PySide6.QtWidgets import (QSizePolicy, QListWidget, QListWidgetItem, QApplication, QMainWindow, QLabel, 
			  QTextEdit, QVBoxLayout, QScrollArea, QDockWidget, QWidget)
from PySide6.QtCore import Qt
from expander import Expander

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Qt Expander Demo")
        self.resize(640, 480)

        edit = QTextEdit()
        edit.setPlainText("Lorem ipsum dolor...")
        self.content = Expander("Content", "parts.svg")
        self.images = Expander("Images", "images.svg")
        self.settings = Expander("Settings", "settings.svg")
        vbox = QVBoxLayout()
        vbox.addWidget(self.content)
        vbox.addWidget(self.images)
        vbox.addWidget(self.settings)
        vbox.addStretch()
        scroll_content = QWidget()
        scroll_content.setLayout(vbox)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        scroll.setMaximumWidth(200)
        scroll.setMinimumWidth(200)
        self.navigationdock = QDockWidget("Navigation", self)
        self.navigationdock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.navigationdock.setWidget(scroll)
        self.navigationdock.setObjectName("Navigation")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.navigationdock)
        self.setCentralWidget(edit)

        # fill content
        self.content_list = QListWidget()
        self.content_list.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        for i in range(5):
            item = QListWidgetItem()
            item.setText("Item " + str(i))
            self.content_list.addItem(item)
        content_box = QVBoxLayout()
        content_box.addWidget(self.content_list)
        self.content.addLayout(content_box)


        # fill images
        self.images_list = QListWidget()
        self.images_list.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        for i in range(5):
            item = QListWidgetItem()
            item.setText("Image " + str(i))
            self.images_list.addItem(item)
        images_box = QVBoxLayout()
        images_box.addWidget(self.images_list)
        self.images.addLayout(images_box)


        #fill settings
        self.settings_list = QListWidget()
        self.settings_list.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        for i in range(5):
            item = QListWidgetItem()
            item.setText("Setting " + str(i))
            self.settings_list.addItem(item)
        settings_box = QVBoxLayout()
        settings_box.addWidget(self.settings_list)
        self.settings.addLayout(settings_box)

        self.content.expanded.connect(self.contentExpanded)
        self.images.expanded.connect(self.imagesExpanded)
        self.settings.expanded.connect(self.settingsExpanded)

    def contentExpanded(self, value):
        if value:
            self.images.setExpanded(False)
            self.settings.setExpanded(False)

    def imagesExpanded(self, value):
        if value:
            self.content.setExpanded(False)
            self.settings.setExpanded(False)

    def settingsExpanded(self, value):
        if value:
            self.content.setExpanded(False)
            self.images.setExpanded(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())