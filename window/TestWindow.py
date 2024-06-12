from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QFileDialog
from PyQt6.QtCore import Qt

from menu.TestMenu import TestMenu
from avatar.Avatar import avatar
from TicTacToe.TicTacToe import TicTacToe

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(0, 0, 1920, 1080)
        self.menuBar = TestMenu(self)

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

    def setCrossColor(self, color):
        self.field.changeSymbolXColor(color)
    
    def setZeroColor(self, color):
        self.field.changeSymbol0Color(color)

        