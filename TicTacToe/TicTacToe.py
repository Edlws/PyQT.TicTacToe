from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QMessageBox
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt
import json

class TicTacToe(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(9)

        self.buttonMatrix = []
        self.pictureMatrix = []

        for i in range(9):
            buttonRow = []
            pictureRow = []
            for j in range(9):
                button = QPushButton('')
                button.setStyleSheet("opacity:0;")
                button.setFixedSize(70, 70)
                button.setStyleSheet("margin: 0px; border: 0px solid gray;")

                pixmap = QPixmap(70, 70)
                pixmap.fill(Qt.GlobalColor.white)
                picture = QLabel()
                picture.setPixmap(pixmap)
                picture.setFixedSize(70, 70)
                picture.setStyleSheet("margin: 0px; border: 0px solid gray;")

                button.clicked.connect(lambda state, i=i, j=j: self.buttonClicked(i, j))
                buttonRow.append(button)
                pictureRow.append(picture)
                
                self.grid.addWidget(picture, i, j)
                self.grid.addWidget(button, i, j)

            self.buttonMatrix.append(buttonRow)
            self.pictureMatrix.append(pictureRow)

        self.statusLabel = QLabel('Player X\'s turn')
        self.grid.addWidget(self.statusLabel, 9, 0, 1, 9)

        self.setLayout(self.grid)

        self.setFixedSize(750, 900)
        self.playerNames = {'X': 'Player 1', 'O': 'Player 2'}
        self.currentPlayer = 'X'
        self.nextAllowed = (None, None)  
        self.gameState = [['' for _ in range(9)] for _ in range(9)]
        self.tacticalState = [['Game' for _ in range(3)] for _ in range(3)]
        self.tacticalFilled = [[False for _ in range(3)] for _ in range(3)]
        self.symbolColorX = Qt.GlobalColor.black
        self.symbolColor0 = Qt.GlobalColor.black



    def drawCircle(self, picture):
        pixmap = picture.pixmap()
        painter = QPainter(pixmap)
        pen = QPen(self.symbolColor0, 5)
        painter.setPen(pen)
        painter.drawEllipse(10, 10, 50, 50)
        painter.end()
        picture.setPixmap(pixmap)

    def drawCross(self, picture):
        pixmap = picture.pixmap()
        painter = QPainter(pixmap)
        pen = QPen(self.symbolColorX, 5)
        painter.setPen(pen)
        painter.drawLine(10, 10, 60, 60)
        painter.drawLine(10, 60, 60, 10)
        painter.end()
        picture.setPixmap(pixmap)

    def drawSymbol(self, picture, player):
        if player == 'X':
            self.drawCross(picture)
        else:
            self.drawCircle(picture)

    def disableAllButtons(self):
        for row in self.buttonMatrix:
            for button in row:
                button.setEnabled(False)

    def changePlayerNames(self, player1_name, player2_name):
        self.playerNames['X'] = player1_name
        self.playerNames['O'] = player2_name
        self.statusLabel.setText(f'Player {self.playerNames[self.currentPlayer]}\'s turn')

    def buttonClicked(self, row, col):
        if self.nextAllowed != (None, None) and self.nextAllowed != (row // 3, col // 3):
            return
        
        if self.gameState[row][col] == '':
            self.gameState[row][col] = self.currentPlayer
            self.drawSymbol(self.pictureMatrix[row][col], self.currentPlayer)
            
            if self.currentPlayer == 'X':
                self.currentPlayer = 'O'
            else: 
                self.currentPlayer = 'X'
            self.statusLabel.setText(f'Player {self.playerNames[self.currentPlayer]}\'s turn')
            self.checkSmallBoard(row // 3, col // 3)
            if not self.tacticalFilled[row % 3][col % 3]:
                self.nextAllowed = (row % 3, col % 3)
            else:
                self.nextAllowed = (None, None)
            self.checkSmallBoard(row // 3, col // 3)
            self.checkGlobalBoard()
            self.updateColors()
            print(self.tacticalFilled[row//3][col//3])
            print(self.tacticalState[row//3][col//3])
            print(self.nextAllowed)

    def checkSmallBoard(self, row, col):
        #rows
        for i in range(3):
            if self.gameState[row*3+i][col*3] == self.gameState[row*3+i][col*3+1] == self.gameState[row*3+i][col*3+2] != '':
                self.tacticalState[row][col] = self.gameState[row*3+i][col*3]
                self.tacticalFilled[row][col] = True
                self.updateBigSymbol(row, col, self.gameState[row*3+i][col*3])
                return

        #cols
        for j in range(3):
            if self.gameState[row*3][col*3+j] == self.gameState[row*3+1][col*3+j] == self.gameState[row*3+2][col*3+j] != '':
                self.tacticalState[row][col] = self.gameState[row*3][col*3+j]
                self.tacticalFilled[row][col] = True
                self.updateBigSymbol(row, col, self.gameState[row*3][col*3+j])
                return

        #diag
        if self.gameState[row*3][col*3] == self.gameState[row*3+1][col*3+1] == self.gameState[row*3+2][col*3+2] != '':
            self.tacticalState[row][col] = self.gameState[row*3][col*3]
            self.tacticalFilled[row][col] = True
            self.updateBigSymbol(row, col, self.gameState[row*3][col*3])
            return
        if self.gameState[row*3][col*3+2] == self.gameState[row*3+1][col*3+1] == self.gameState[row*3+2][col*3] != '':
            self.tacticalState[row][col] = self.gameState[row*3][col*3+2]
            self.tacticalFilled[row][col] = True
            self.updateBigSymbol(row, col, self.gameState[row*3][col*3+2])
            return

        #draw?
        if all(self.gameState[row*3+i][col*3+j] != '' for i in range(3) for j in range(3)):
            self.tacticalState[row][col] = 'Draw'
            self.tacticalFilled[row][col] = True

    def checkGlobalBoard(self):
        #rows
        for i in range(3):
            if self.tacticalState[i][0] == self.tacticalState[i][1] == self.tacticalState[i][2] != 'Game':
                self.disableAllButtons()
                if self.currentPlayer == 'X':
                    self.showResultDialog('O')
                else: self.showResultDialog('X')
                return

        #cols
        for j in range(3):
            if self.tacticalState[0][j] == self.tacticalState[1][j] == self.tacticalState[2][j] != 'Game':
                self.disableAllButtons()
                if self.currentPlayer == 'X':
                    self.showResultDialog('O')
                else: self.showResultDialog('X')
                return

        #diag
        if self.tacticalState[0][0] == self.tacticalState[1][1] == self.tacticalState[2][2] != 'Game':
            self.disableAllButtons()
            if self.currentPlayer == 'X':
                    self.showResultDialog('O')
            else: self.showResultDialog('X')
            return
        if self.tacticalState[0][2] == self.tacticalState[1][1] == self.tacticalState[2][0] != 'Game':
            self.disableAllButtons()
            if self.currentPlayer == 'X':
                self.showResultDialog('0')
            else: self.showResultDialog('X')
            return

        #draw?
        if all(self.tacticalState[i][j] != 'Game' for i in range(3) for j in range(3)):
            self.disableAllButtons()
            self.showResultDialog(None)

    def disableTacticalBoard(self, row, col):
        for i in range(3):
            for j in range(3):
                button = self.buttonMatrix[3*row+i][3*col+j]
                picture = self.pictureMatrix[3*row+i][3*col+j]
                if button.isEnabled():
                    button.setEnabled(False)
                    picture.setStyleSheet("QLabel { background-color: lightgray; }")

    def drawBigCross(self, picture):
        pixmap = QPixmap(picture.size())
        pixmap.fill(Qt.GlobalColor.white)
        pixmap.scaled(228,228)
        painter = QPainter(pixmap)
        pen = QPen(self.symbolColorX, 10) 
        painter.setPen(pen)      
        painter.drawLine(10, 10, pixmap.width() - 10, pixmap.height() - 10)
        painter.drawLine(10, pixmap.height() - 10, pixmap.width() - 10, 10)
        painter.end()
        picture.setPixmap(pixmap)

    def drawBigCircle(self, picture):
        pixmap = QPixmap(picture.size())
        pixmap.fill(Qt.GlobalColor.white)
        pixmap.scaled(228,228)
        painter = QPainter(pixmap)
        pen = QPen(self.symbolColor0, 10)  
        painter.setPen(pen)
        painter.drawEllipse(10, 10, pixmap.width() - 25, pixmap.height() - 25)
        painter.end()
        picture.setPixmap(pixmap)

    def updateBigSymbol(self, row, col, player):
        for i in range(3):
            for j in range(3):
                self.gameState[3*row+i][3*col+j] = '' 
                self.pictureMatrix[3*row+i][3*col+j].setVisible(0) 
                self.buttonMatrix[3*row+i][3*col+j].setEnabled(False) 
        centerPicture = self.pictureMatrix[3*row+1][3*col+1]
        centerPicture.setVisible(1)
        centerPicture.setFixedSize(228,228)
        centerPicture.setStyleSheet("margin: 0px; border: 0px solid gray;")
        self.grid.addWidget(centerPicture, row*3, col*3, 3, 3)
        if player == 'X':
            self.drawBigCross(centerPicture)
        elif player == 'O':
            self.drawBigCircle(centerPicture)
        
    def updateColors(self):
        for i in range(9):
            for j in range(9):
                pixmap = QPixmap(70, 70)
                if self.buttonMatrix[i][j].isEnabled():
                    if not self.tacticalFilled[i // 3][j // 3] and (self.nextAllowed == (None, None) or self.nextAllowed == (i // 3, j // 3)):
                        pixmap.fill(Qt.GlobalColor.white)
                    else:
                        pixmap.fill(Qt.GlobalColor.lightGray)
                else:
                    pixmap.fill(Qt.GlobalColor.lightGray)

                painter = QPainter(pixmap)
                if self.gameState[i][j] == 'X':
                    pen = QPen(self.symbolColorX, 5)
                    painter.setPen(pen)
                    painter.drawLine(10, 10, 60, 60)
                    painter.drawLine(10, 60, 60, 10)
                elif self.gameState[i][j] == 'O':
                    pen = QPen(self.symbolColor0, 5)
                    painter.setPen(pen)
                    painter.drawEllipse(10, 10, 50, 50)
                painter.end()

                if not self.tacticalFilled[i // 3][j // 3]:
                    self.pictureMatrix[i][j].setPixmap(pixmap)
                else:
                    if self.tacticalState[i // 3][j // 3] == 'X':
                        self.updateBigSymbol(i // 3, j // 3, 'X')
                    elif self.tacticalState[i // 3][j // 3] == 'O':
                        self.updateBigSymbol(i // 3, j // 3, 'O')

    def showResultDialog(self, winner=None):
        message = QMessageBox()
        message.setWindowTitle("Game Over")
        if winner:
            message.setText(f"Player {self.playerNames[winner]} wins!")
        else:
            message.setText("It's a draw!")
        message.setStandardButtons(QMessageBox.StandardButton.Ok)
        message.exec()

    def changeSymbolXColor(self, color):
        self.symbolColorX = color 
        for i in range(9):
            for j in range(9):
                pixmap = QPixmap(70, 70)
                if self.buttonMatrix[i][j].isEnabled():
                    if self.tacticalFilled[i//3][j//3] == False and (self.nextAllowed == (None, None) or self.nextAllowed == (i // 3, j // 3)):
                        pixmap.fill(Qt.GlobalColor.white)
                    elif self.tacticalFilled[i//3][j//3] == True:
                        None
                    else:
                        pixmap.fill(Qt.GlobalColor.lightGray)
                else:
                    pixmap.fill(Qt.GlobalColor.lightGray)

                painter = QPainter(pixmap)
                if self.gameState[i][j] == 'X':
                    pen = QPen(self.symbolColorX, 5)  
                    painter.setPen(pen)
                    painter.drawLine(10, 10, 60, 60)
                    painter.drawLine(10, 60, 60, 10)
                elif self.gameState[i][j] == 'O':
                    pen = QPen(self.symbolColor0, 5)  
                    painter.setPen(pen)
                    painter.drawEllipse(10, 10, 50, 50)
                painter.end()
                if self.tacticalFilled[i//3][j//3] == False:
                    self.pictureMatrix[i][j].setPixmap(pixmap)
                else:
                    if self.tacticalState[i//3][j//3] == 'X':
                        self.updateBigSymbol(i//3, j//3, 'X')   
                    else:
                        self.updateBigSymbol(i//3, j//3, 'O')  

    def changeSymbol0Color(self, color):
        self.symbolColor0 = color
        for i in range(9):
            for j in range(9):
                pixmap = QPixmap(70, 70)
                if self.buttonMatrix[i][j].isEnabled():
                    if self.tacticalFilled[i//3][j//3] == False and (self.nextAllowed == (None, None) or self.nextAllowed == (i // 3, j // 3)):
                        pixmap.fill(Qt.GlobalColor.white)
                    elif self.tacticalFilled[i//3][j//3] == True:
                        None
                    else:
                        pixmap.fill(Qt.GlobalColor.lightGray)
                else:
                    pixmap.fill(Qt.GlobalColor.lightGray)

                painter = QPainter(pixmap)
                if self.gameState[i][j] == 'X':
                    pen = QPen(self.symbolColorX, 5)  
                    painter.setPen(pen)
                    painter.drawLine(10, 10, 60, 60)
                    painter.drawLine(10, 60, 60, 10)
                elif self.gameState[i][j] == 'O':
                    pen = QPen(self.symbolColor0, 5)  
                    painter.setPen(pen)
                    painter.drawEllipse(10, 10, 50, 50)
                painter.end()

                if self.tacticalFilled[i//3][j//3] == False:
                    self.pictureMatrix[i][j].setPixmap(pixmap)            
                else:
                    if self.tacticalState[i//3][j//3] == 'X':
                        self.updateBigSymbol(i//3, j//3, 'X')   
                    else:
                        self.updateBigSymbol(i//3, j//3, 'O')    

    def resetGame(self):
        self.currentPlayer = 'X'
        self.nextAllowed = (None, None)
        self.gameState = [['' for _ in range(9)] for _ in range(9)]
        self.tacticalState = [['Game' for _ in range(3)] for _ in range(3)]
        self.tacticalFilled = [[False for _ in range(3)] for _ in range(3)]
        for i in range(9):
            for j in range(9):
                self.buttonMatrix[i][j].setEnabled(True)
                pixmap = QPixmap(70, 70)
                pixmap.fill(Qt.GlobalColor.white)
                self.pictureMatrix[i][j].setPixmap(pixmap)
                self.pictureMatrix[i][j].setVisible(True)
        for row in range(3):
            for col in range(3):
                centerPicture = self.pictureMatrix[3 * row + 1][3 * col + 1]
                if centerPicture.height() == 228 and centerPicture.width() == 228:
                    centerPicture.setFixedSize(70, 70)
                    pixmap = QPixmap(70, 70)
                    pixmap.fill(Qt.GlobalColor.white)
                    centerPicture.setPixmap(pixmap)
                    centerPicture.setStyleSheet("margin: 0px; border: 0px solid gray;")
                    self.grid.addWidget(centerPicture, 3 * row + 1, 3 * col + 1, 1, 1)
        self.statusLabel.setText('Player X\'s turn')
        for row in range(9):
            for col in range(9):
                self.buttonMatrix[row][col].setEnabled(True)
        self.updateColors()

    def saveGameState(self, file):
        data = {
            'playerNames': self.playerNames,
            'currentPlayer': self.currentPlayer,
            'nextAllowed': list(self.nextAllowed),
            'gameState': self.gameState,
            'tacticalState': self.tacticalState,
            'tacticalFilled': self.tacticalFilled,
        }

        with open(file, 'w') as file:
            json.dump(data, file, indent=2)

    def loadGameState(self, file):
        self.resetGame()
        with open(file, 'r') as file:
            data = json.load(file)
            self.playerNames = data['playerNames']
            self.currentPlayer = data['currentPlayer']
            self.nextAllowed = tuple(data['nextAllowed'])
            self.gameState = data['gameState']
            self.tacticalState = data['tacticalState']
            self.tacticalFilled = data['tacticalFilled']
            self.updateColors()