#############################################################################
# Copyright (C) 2023 Olaf Japp
#
# This file is part of Lob.
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
import shutil
import tempfile
from widgets.imageselector import ImageSelector
from PySide6.QtWidgets import QWidget, QDateEdit, QTextEdit, QLineEdit, QComboBox, QGridLayout, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PySide6.QtGui import QImage
from PySide6.QtCore import QDate
import resources


class ClientEditor(QWidget):
    def __init__(self, win):
        QWidget.__init__(self)
        self.win = win
        self.id = 0
        title = QLabel("Client Data")
        fnt = title.font()
        fnt.setPointSize(20)
        fnt.setBold(True)
        title.setFont(fnt)
        self.layout = QGridLayout()
        self.layout.setColumnStretch(0,1)
        self.number = QLineEdit()
        self.name = QLineEdit()
        self.email = QLineEdit()
        self.profession = QLineEdit()
        self.address = QLineEdit()
        self.mobile = QLineEdit()
        self.notes = QTextEdit()
        self.birthday = QDateEdit()
        self.birthday.setCalendarPopup(True)
        self.birthday.setDisplayFormat("dd.MM.yyyy")
        
        self.image = ImageSelector()
        self.image.setMinimumWidth(250)

        self.layout.addWidget(title, 0, 0, 1, 2)
        self.layout.addWidget(QLabel("Id"), 1, 0)
        self.layout.addWidget(self.number, 2, 0)
        
        self.layout.addWidget(QLabel("Name"), 3, 0)
        self.layout.addWidget(self.name, 4, 0)
        self.layout.addWidget(QLabel("Address"), 5, 0)
        self.layout.addWidget(self.address, 6, 0)
        self.layout.addWidget(QLabel("Email"), 7, 0)
        self.layout.addWidget(self.email, 8, 0)
        self.layout.addWidget(QLabel("Mobile"), 9, 0)
        self.layout.addWidget(self.mobile, 10, 0)
        self.layout.addWidget(QLabel("Profession"), 11, 0)
        self.layout.addWidget(self.profession, 12, 0)
        self.layout.addWidget(QLabel("Notes"), 17, 0)
        self.layout.addWidget(self.notes, 18, 0, 1, 2)
        self.layout.addWidget(self.image, 2, 1, 7, 1)
        self.layout.addWidget(QLabel("Birhday"), 9, 1)
        self.layout.addWidget(self.birthday, 10, 1)
        self.setLayout(self.layout)

        self.reload()
        self.number.textEdited.connect(self.clientChanged)
        self.name.textEdited.connect(self.clientChanged)
        self.address.textEdited.connect(self.clientChanged)
        self.email.textEdited.connect(self.clientChanged)
        self.mobile.textEdited.connect(self.clientChanged)
        self.profession.textEdited.connect(self.clientChanged)
        self.notes.textChanged.connect(self.clientChanged)
        self.birthday.dateChanged.connect(self.clientChanged)
        self.image.clicked.connect(self.seek)

    def reload(self):
        self.loading = True
        if self.win.client:
            self.number.setText(self.win.client["number"])
            self.name.setText(self.win.client["name"])
            self.address.setText(self.win.client["address"])
            self.email.setText(self.win.client["email"])
            self.mobile.setText(self.win.client["mobile"])
            self.profession.setText(self.win.client["profession"])
            self.notes.setText(self.win.client["notes"])
            self.birthday.setDate(QDate(self.win.client["birthday_year"], self.win.client["birthday_month"], self.win.client["birthday_day"]))
            name = os.path.join(str(self.win.client.doc_id) + ".png")
            path = os.path.join(self.win.database, "images", name)
            if os.path.exists(path):
                self.image.setImage(QImage(path))
            else:
                self.image.setImage(QImage(":/images/image_placeholder.png"))
        else:
            self.number.setText("")
            self.name.setText("")
            self.address.setText("")
            self.email.setText("")
            self.mobile.setText("")
            self.profession.setText("")
            self.notes.setText("")
            self.birthday.setDate(QDate(1900,1,1))
            self.image.setImage(QImage(":/images/image_placeholder.png"))
        self.loading = False
            
    def clientChanged(self):
        if self.loading:
            return
        self.win.client["number"] = self.number.text()
        self.win.client["name"] = self.name.text()
        self.win.client["address"] = self.address.text()
        self.win.client["email"] = self.email.text()
        self.win.client["mobile"] = self.mobile.text()
        self.win.client["profession"] = self.profession.text()
        self.win.client["notes"] = self.notes.toPlainText()
        self.win.client["birthday_year"] = self.birthday.date().year()
        self.win.client["birthday_month"] = self.birthday.date().month()
        self.win.client["birthday_day"] = self.birthday.date().day()
        self.win.clients.update(self.win.client, doc_ids=[self.win.client.doc_id])
        self.win.updateClient()

    def seek(self):
        fileName = ""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("Images (*.png *.gif *.jpg);;All (*)")
        dialog.setWindowTitle("Load Image")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        if dialog.exec():
            fileName = dialog.selectedFiles()[0]
        del dialog
        if not fileName:
            return

        # copy file to database dir
        name = os.path.join(str(self.win.client.doc_id) + ".png")
        path = os.path.join(self.win.database, "images", name)
        shutil.copy(fileName, path)
        self.image.setImage(QImage(path))
        self.clientChanged()
        
