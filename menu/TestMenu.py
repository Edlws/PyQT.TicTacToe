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
        self.loadMenuAction.triggered.connect(self.loadAction)
        self.stateMItem.addAction(self.loadMenuAction)

        self.saveMenuAction = QAction("Save")
        self.stateMItem.triggered.connect(self.saveAction)
        self.stateMItem.addAction(self.saveMenuAction)
        
        self.changeCrossColorAction = QAction("Change Cross color", self)
        self.changeCrossColorAction.triggered.connect(self.changeCrossColor)
        self.editMItem.addAction(self.changeCrossColorAction)

        self.changeZeroColorAction = QAction("Change Zero color", self)
        self.changeZeroColorAction.triggered.connect(self.changeZeroColor)
        self.editMItem.addAction(self.changeZeroColorAction)

    def loadAction(self):
        self.parentWidget().loadGame()
        
    def saveAction(self):
        self.parentWidget().saveGame()
        

    def changeCrossColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.parentWidget().setCrossColor(color)

    def changeZeroColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.parentWidget().setZeroColor(color)            