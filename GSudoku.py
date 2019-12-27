from Sudoku import sudoku
import sys
try:
    from PyQt5 import QtWidgets
    from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
except:
    input('Please install PyQt5 before using the GUI system. (press enter to close)')

class sudokuApp(QMainWindow):
    def __init__(self):
        super(sudokuApp, self).__init__()
        self.setWindowTitle('Sudoku')
        self.createUI()
        self.resizeUI()
        self.activateUI()
        self.b1 = sudoku.board()

    def createUI(self):    #Create all the buttons, etcetera
        #nine columns of buttons, nine buttons to a column
        self.grids = [[QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self)],
                      [QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self)],
                      [QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self)],
                      [QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self)],
                      [QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self)],
                      [QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self)],
                      [QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self)],
                      [QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self)],
                      [QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self), QPushButton(self)]]
        
        self.setupBtn = QPushButton(self)
        self.solveBtn = QPushButton(self)
        self.clearBtn = QPushButton(self)
        self.setupBtn.setText('Setup')
        self.solveBtn.setText('Solve')
        self.clearBtn.setText('Clear')

    def resizeUI(self, desiredScale = 1):    #make them all the right size and scale them properly.
        self.scale = desiredScale
        self.gridwidth = 40 * self.scale
        self.gridheight = 40 * self.scale
        self.spacing = 5 * self.scale
        self.boardWidth = self.spacing + (9 * (self.spacing + self.gridwidth))
        self.boardHeight = self.spacing + (9 * (self.spacing + self.gridheight))

        for i in range(9):
            for j in range(9):
                grid = self.grids[i][j]
                grid.setGeometry(self.spacing + (j * (self.spacing + self.gridwidth)), self.spacing + (i * (self.spacing + self.gridheight)), self.gridwidth, self.gridheight)
        self.setupBtn.setGeometry(self.spacing, self.boardHeight, (self.scale * 80), (self.scale * 30))
        self.solveBtn.setGeometry((self.spacing * 2) + (self.scale * 80), self.boardHeight, (self.scale * 80), (self.scale * 30))
        self.clearBtn.setGeometry((self.spacing * 3) + (self.scale * 160), self.boardHeight, (self.scale * 80), (self.scale * 30))
        self.setFixedSize(self.boardWidth, self.boardHeight + (self.scale * 30) + self.spacing)

    def activateUI(self):
        for i in range(9):
            for j in range(9):
                grid = self.grids[i][j]
                grid.clicked.connect(self.setGrid)
                grid.setCheckable(True)
        self.setupBtn.clicked.connect(self.setup)

    def setup(self):
        self.b1.setup()
        for i in range(9):
            for j in range(9):
                val = self.b1.rawread(i, j)
                if val != 0:
                    self.grids[i][j].setText(str(val))

    def setGrid(self):
        for i in range(9):
            for j in range(9):
                grid = self.grids[i][j]
                if grid.isChecked():
                    x = i
                    y = j
        self.grids[x][y].setText('x')

def Game():
    app = QApplication(sys.argv)
    gameInstance = sudokuApp()
    gameInstance.show()
    app.exec_()