from PyQt6.QtWidgets import QWidget, QColorDialog

from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction

class TestMenu(QMenuBar):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setMinimumSize(120, 1)
        
                
        self.stateMItem = QMenu("State")
        self.editMItem = QMenu("Edit")
        self.addMenu(self.stateMItem)
        self.addMenu(self.editMItem)
        
        self.loadMenuAction = QAction("Load")


        self.saveMenuAction = QAction("Save")

        
        self.changeCrossColorAction = QAction("Change Cross color")
        self.changeZeroColorAction = QAction("Change Zero color")
