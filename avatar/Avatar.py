from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QLineEdit
from PyQt6.QtGui import QPixmap




class avatar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent) 
        self.button1 = QPushButton(self)
        self.button2 = QPushButton(self)
        self.picture = QLabel(self)
        self.name = QLineEdit(self)
        self.nameLabel = QLabel(self)

        self.name.adjustSize()
        self.button1.setText("Load")
        self.button1.move(0,0)
        self.button1.clicked.connect(self.showImage)
        self.picture.setFixedSize(300,300)
        self.button2.setText("Remove")
        self.button2.clicked.connect(self.removeImage)

        
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.picture)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)   

        self.adjustSize()
    
    def getName(self):
        return self.name.text()

    def changeName(self):
        self.nameLabel.setText(self.name.text())

    def removeImage(self):
        self.picture.clear()

    def showImage(self):
        file = QFileDialog()
        fileName = file.getOpenFileName()[0]
        pixmap = QPixmap(fileName)
        pixmap = pixmap.scaled(300,300)
        self.picture.setPixmap(pixmap)
        self.picture.adjustSize()




  
        
        





    