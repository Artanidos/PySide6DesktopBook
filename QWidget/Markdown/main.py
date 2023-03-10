import sys
import os
from threading import Thread, Lock
from PySide6.QtWidgets import (QApplication, QMainWindow, QSplitter, QTextEdit, 
                             QMessageBox, QFileDialog, QDialog)
from PySide6.QtCore import Qt, QCoreApplication, QSettings, QPoint, QSize, Signal, QUrl
from PySide6.QtGui import QIcon, QKeySequence, QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from markdown2 import markdown


class MainWindow(QMainWindow):
    htmlReady = Signal(str)

    def __init__(self):
        QMainWindow.__init__(self)
        self.cur_file = ""
        self.tread_running = False
        self.splitter = QSplitter()
        self.text_edit = QTextEdit("")
        self.preview = QWebEngineView()
        self.preview.setMinimumWidth(300)
        self.setWindowTitle("Markdown [*]")
        self.splitter.addWidget(self.text_edit)
        self.splitter.addWidget(self.preview)
        self.setCentralWidget(self.splitter)
        self.createMenus()
        self.createStatusBar()
        self.readSettings()
        self.text_edit.document().contentsChanged.connect(self.documentWasModified)
        self.text_edit.textChanged.connect(self.textChanged)

    def closeEvent(self, event):
        if self.maybeSave():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def documentWasModified(self):
        self.setWindowModified(self.text_edit.document().isModified())

    def createMenus(self):
        new_icon = QIcon("./assets/new.png")
        open_icon = QIcon("./assets/open.png")
        save_icon = QIcon("./assets/save.png")
        save_as_icon = QIcon("./assets/save_as.png")
        exit_icon = QIcon("./assets/exit.png")

        new_act = QAction(new_icon, "&New", self)
        new_act.setShortcuts(QKeySequence.New)
        new_act.setStatusTip("Create a new file")
        new_act.triggered.connect(self.newFile)
        
        open_act = QAction(open_icon, "&Open", self)
        open_act.setShortcuts(QKeySequence.Open)
        open_act.setStatusTip("Open an existing file")
        open_act.triggered.connect(self.open)
        
        save_act = QAction(save_icon, "&Save", self)
        save_act.setShortcuts(QKeySequence.Save)
        save_act.setStatusTip("Save the document to disk")
        save_act.triggered.connect(self.save)

        save_as_act = QAction(save_as_icon, "Save &As...", self)
        save_as_act.setShortcuts(QKeySequence.SaveAs)
        save_as_act.setStatusTip("Save the document under a new name")
        save_as_act.triggered.connect(self.saveAs)

        exit_act = QAction(exit_icon, "E&xit", self)
        exit_act.setShortcuts(QKeySequence.Quit)
        exit_act.setStatusTip("Exit the application")
        exit_act.triggered.connect(self.close)

        about_act = QAction("&About", self)
        about_act.triggered.connect(self.about)
        about_act.setStatusTip("Show the application's About box")

        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(new_act)
        file_menu.addAction(open_act)
        file_menu.addAction(save_act)
        file_menu.addAction(save_as_act)
        file_menu.addSeparator()
        file_menu.addAction(exit_act)

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(about_act)

        file_tool_bar = self.addToolBar("File")
        file_tool_bar.addAction(new_act)
        file_tool_bar.addAction(open_act)
        file_tool_bar.addAction(save_act)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def about(self):
        QMessageBox.about(self, "About Markdown",
            "This app demonstrates how to "
               "write modern GUI applications using Qt, with a menu bar, "
               "toolbars, and a status bar.")

    def newFile(self):
        if self.maybeSave():
            self.text_edit.clear()
        self.setCurrentFile("")

    def open(self):
        if self.maybeSave():
            fileName = QFileDialog.getOpenFileName(self)[0]
        if fileName:
            self.loadFile(fileName)

    def save(self):
        if not self.cur_file:
            return self.saveAs()
        else:
            return self.saveFile(self.cur_file)

    def saveAs(self):
        dialog = QFileDialog(self)
        dialog.setWindowModality(Qt.WindowModal)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        if dialog.exec() != QDialog.Accepted:
            return False
        return self.saveFile(dialog.selectedFiles()[0])

    def maybeSave(self):
        if not self.text_edit.document().isModified():
            return True
        ret = QMessageBox.warning(self, "Qt Demo",
                                "The document has been modified.\n"
                                "Do you want to save your changes?",
                                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if ret == QMessageBox.Save:
            return self.save()
        elif ret == QMessageBox.Cancel:
            return False
        return True

    def loadFile(self, fileName):
        with open(fileName, mode= "r") as f:
            text = f.read()

        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.setCurrentFile(fileName)
        self.text_edit.setPlainText(text)
        self.text_edit.document().setModified(False)
        self.setWindowModified(False)
        QApplication.restoreOverrideCursor()        
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        with open(fileName, "w") as f:
            f.write(self.text_edit.toPlainText())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.text_edit.document().setModified(False)
        self.setWindowModified(False)
        self.statusBar().showMessage("File saved", 2000)

    def setCurrentFile(self, fileName):
        self.cur_file = fileName
        shown_name = self.cur_file
        if not self.cur_file:
            shown_name = "untitled.txt"
        self.setWindowFilePath(shown_name)

    def writeSettings(self):
        settings = QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName())
        settings.setValue("geometry", self.saveGeometry())

    def readSettings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)
        self.restoreState(settings.value("state"))

    def textChanged(self):
        text = self.text_edit.toPlainText()
        self.lock = Lock()
        with self.lock:
            if not self.tread_running:
                self.tread_running = True
                self.htmlReady.connect(self.previewReady)
                thread = Thread(target=self.createHtml, args=(text,))
                thread.daemon = True
                thread.start()

    def createHtml(self, text):
        path = os.getcwd()
        html = "<html><head></head><body>"
        html += markdown(self.text_edit.toPlainText())
        html += "</body></html>"
        self.htmlReady.emit(html)

    def previewReady(self, html):
        self.preview.setHtml(html)
        self.htmlReady.disconnect()
        with self.lock:
            self.tread_running = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QCoreApplication.setOrganizationName("Book")
    QCoreApplication.setApplicationName("MarkdownEditor")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())