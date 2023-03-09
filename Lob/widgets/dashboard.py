#############################################################################
# Copyright (C) 2023 Olaf Japp
#
# self file is part of Lob.
#
#  Lob is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Lob is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Lob.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QTextBrowser
from PySide6.QtCore import Signal
import resources

class Dashboard(QWidget):
    clients = Signal()
    settings = Signal()

    def __init__(self):
        QWidget.__init__(self)

        vbox = QVBoxLayout()
        layout = QGridLayout()
        title = QLabel()
        title.setText("Dashboard")
        fnt = title.font()
        fnt.setPointSize(20)
        fnt.setBold(True)
        title.setFont(fnt)

        self.browser = QTextBrowser()
        self.browser.setOpenLinks(False)
        text = "Good day,<br>"
        text += "If you want to edit the clients, then please click onto the <a href='clients'>CLIENTS</a> expander.<br>"
        text += "If you want to change some settings like the font size or the path where the data is stored, then click on the <a href='settings'>SETTINGS</a> expander."
        self.browser.setText(text)
        self.info = QLabel()
        self.info.setText("Welcome to Lob...")
        self.browser.anchorClicked.connect(self.navigate)

        space = QWidget()
        space2 = QWidget()
        space3 = QWidget()
        space.setMinimumHeight(30)
        space2.setMinimumHeight(30)
        space3.setMinimumHeight(30)
        layout.addWidget(title, 0, 0, 1, 3)
        layout.addWidget(self.info, 1, 0, 1, 3)
        layout.addWidget(space, 2, 0)
       
        vbox.addLayout(layout)
        vbox.addSpacing(40)
        vbox.addWidget(self.browser)
        self.setLayout(vbox)

    def navigate(self, url):
        if url.toDisplayString() == "clients":
            self.clients.emit()
        elif url.toDisplayString() == "settings":
            self.settings.emit()