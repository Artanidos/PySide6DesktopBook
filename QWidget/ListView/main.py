import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QListView
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Qt Demo")
        list = QListView()
        self.model = QStandardItemModel(list)
        cars = [
            'Jaguar',
            'Porsche',
            'Mercedes',
            'Jeep',
            'Toyota'
        ]
 
        for car in cars:
            item = QStandardItem(car)
            item.setCheckable(True)
            self.model.appendRow(item)
 
        list.setModel(self.model)
        self.setCentralWidget(list)

        self.model.itemChanged.connect(self.onItemChanged)

    def onItemChanged(self, item):
        if not item.checkState():
            print(item.text() + " has been unchecked")
        else:
            print(item.text() + " has been checked")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())