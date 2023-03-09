import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView
from PySide6.QtCore import Qt
from treemodel import TreeModel, TreeNode


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        items = []
        items.append(TreeNode("Root"))
        items[0].addChild(TreeNode(["Leaf A", "a", "b"]))
        items[0].addChild(TreeNode(["Leaf B", "c", "d"]))
        items[0].child(1).addChild(TreeNode(["Sub Leaf", "e", "f"]))

        self.setWindowTitle("Qt Demo")
        tree = QTreeView()
        tree.setModel(TreeModel(items))
        tree.setHeaderHidden(True)
        tree.setColumnWidth(0, 150)
        self.setCentralWidget(tree)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())