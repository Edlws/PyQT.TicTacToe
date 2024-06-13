from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QFileDialog, QWidget, QColorDialog, QMenu, QMenuBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from avatar.Avatar import avatar
from TicTacToe.TicTacToe import TicTacToe

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(0, 0, 1920, 1080)
        self.menuInit()

        self.nameButton = QPushButton(self)
        self.nameButton.setText("Change names")
        self.nameButton.move(150,900)
        
        self.resetButton = QPushButton(self)
        self.resetButton.setText("Reset game")
        self.resetButton.move(150,930)

        self.player1 = avatar(self)
        self.player1.move(50, 250)

        self.player2 = avatar(self)
        self.player2.move(1350, 250)

        self.field = TicTacToe(self)
        self.field.move(475,150)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.player1)
        self.layout.addWidget(self.field)
        self.layout.addWidget(self.player2)

        self.nameButton.clicked.connect(self.setNames)
        
        self.resetButton.clicked.connect(self.resetGame)
    
    def resetGame(self):
        self.field.resetGame()    
    
    def loadGame(self):
        file = QFileDialog(self)
        fileName = file.getOpenFileName()[0]
        self.field.loadGameState(fileName)

    def saveGame(self):
        file = QFileDialog()
        fileName = file.getOpenFileName()[0]
        self.field.saveGameState(fileName)

    def setNames(self):
        self.field.changePlayerNames(self.player1.getName(), self.player2.getName())
        self.player1.changeName()
        self.player2.changeName()

    def menuInit(self):
        self.menu = QMenuBar(self)
        self.stateMItem = QMenu("State")
        self.editMItem = QMenu("Edit")
        self.menu.addMenu(self.stateMItem)
        self.menu.addMenu(self.editMItem)
        
        self.loadMenuAction = QAction("Load")
        self.loadMenuAction.triggered.connect(self.loadGame)
        self.stateMItem.addAction(self.loadMenuAction)

        self.saveMenuAction = QAction("Save")
        self.saveMenuAction.triggered.connect(self.saveGame)
        self.stateMItem.addAction(self.saveMenuAction)
        
        self.changeCrossColorAction = QAction("Change Cross color", self)
        self.changeCrossColorAction.triggered.connect(self.changeCrossColor)
        self.editMItem.addAction(self.changeCrossColorAction)

        self.changeZeroColorAction = QAction("Change Zero color", self)
        self.changeZeroColorAction.triggered.connect(self.changeZeroColor)
        self.editMItem.addAction(self.changeZeroColorAction)

    def changeCrossColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.field.changeSymbolXColor(color)

    def changeZeroColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.field.changeSymbol0Color(color)    