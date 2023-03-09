
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
from PySide6.QtWidgets import QLabel, QWidget, QStyleOption, QStyle
from PySide6.QtCore import Qt, Signal, Property, QDir, QFile, QIODevice
from PySide6.QtGui import QPixmap, QImage, QPalette, QPainter
import resources


class FlatButton(QLabel):
    clicked = Signal()

    def __init__(self, svg):
        QLabel.__init__(self)
        self.svg = svg
        self._enabled = True
        self.setColors()
        self.setCursor(Qt.PointingHandCursor)

    def setColors(self):
        self.label_normal_color = self.palette().buttonText().color().name()
        self.label_hovered_color = self.palette().highlight().color().name()
        self.label_disabled_color = self.palette().color(QPalette.Disabled, QPalette.ButtonText).name()

        self.normal_icon = QPixmap(self.createIcon(self.svg, self.label_normal_color))
        self.hover_icon = QPixmap(self.createIcon(self.svg, self.label_hovered_color))
        self.disabled_icon = QPixmap(self.createIcon(self.svg, self.label_disabled_color))

        if self.enabled:
            self.setPixmap(self.normal_icon)
        else:
            self.setPixmap(self.disabled_icon)

    def createIcon(self, source, hilite_color):
        bg = self.palette().button().color().name()
        temp = QDir.tempPath()
        file = QFile(source)
        file.open(QIODevice.ReadOnly | QIODevice.Text)
        data = str(file.readAll(), encoding="utf-8")
        file.close()

        out = os.path.join(temp, hilite_color + ".svg")
        with open(out, "w") as fp:
            fp.write(data.replace("#ff00ff", hilite_color).replace("#0000ff", bg))
        return out

    def mousePressEvent(self, event):
        self.setFocus()
        event.accept()

    def mouseReleaseEvent(self, event):
        if self.enabled:
            self.setPixmap(self.hover_icon)
            event.accept()
            self.clicked.emit()

    def enterEvent(self, event):
        if self.enabled:
            self.setPixmap(self.hover_icon)
        QWidget.enterEvent(self, event)

    def leaveEvent(self, event):
        if self.enabled:
            self.setPixmap(self.normal_icon)
        else:
            self.setPixmap(self.disabled_icon)
        QWidget.leaveEvent(self, event)

    @Property(bool)
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        self._enabled = enabled
        if enabled:
            self.setPixmap(self.normal_icon)
        else:
            self.setPixmap(self.disabled_icon)
        self.update()
