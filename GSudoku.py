# GSudoku.py
# Version history:
# V 1.0.0
# - Began logging version history. I had made a mistake with Git, so I must now rewrite much of the improvements I hade previously made.
# V 1.0.1
# - Fixed an issue with the active grid remaining active after reset and not clearing the styles of previous active grids.
#

from Sudoku import sudoku
import sys
try:
    from PyQt5 import QtWidgets
    from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
except:
    input('Please install PyQt5 before using the GUI system. (press enter to close)')

class sudokuApp(QMainWindow):
    activeGrid = 'no active grid'
    possibleInputs = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    openStyle = "color: #000000; background-color: #FFFFFF;"
    activeStyle = "color: #000000; background-color: #8080FF;"
    disabledStyle = "color: #000000; background-color: #808080;"
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
        for x in range(9):
            for y in range(9):
                self.grids[x][y].setStyleSheet(self.openStyle)

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
                grid.clicked.connect(self.selectGrid)
                grid.setCheckable(True)
        self.setupBtn.clicked.connect(self.setup)

    def setup(self):
        self.b1.setup()
        self.activeGrid = 'no active grid'
        for x in range(9):
            for y in range(9):
                val = self.b1.rawread(x, y)
                grid = self.grids[x][y]
                if val == 0:
                    grid.setText('')
                    grid.setEnabled(True)
                    grid.setStyleSheet(self.openStyle)
                else:
                    grid.setText(str(val))
                    grid.setEnabled(False)
                    grid.setStyleSheet(self.disabledStyle)


    def selectGrid(self):
        if type(self.activeGrid) == type((8, 7)):
            x, y = self.activeGrid
            self.grids[x][y].setStyleSheet(self.openStyle)
        for x in range(9):
            for y in range(9):
                grid = self.grids[x][y]
                if grid.isChecked():
                    grid.setCheckable(False)    #reset the grid's checkable state, thereby unchecking it.
                    grid.setCheckable(True)
                    self.activeGrid = (x, y)
                    grid.setStyleSheet(self.activeStyle)

    def editGrid(self, key):
        x, y = self.activeGrid
        if len(sudoku.findall(self.possibleInputs, key)) == 1:    #if the input is within the legal range
            self.grids[x][y].setText(str(key))
            sudoku.rawplace(x, y, key)
        elif key == 16777171:
            self.grids[x][y].setText('')
            sudoku.rawplace(x, y, 0)

    def keyPressEvent(self, event):    #This is the keypress detector. I use this to determine input to edit grids.
        try:
            print(event.key())
            key = event.key() - 48
            print(key)
            self.editGrid(key)
        except:
            pass

def Game():
    app = QApplication(sys.argv)
    gameInstance = sudokuApp()
    gameInstance.show()
    app.exec_()

def reloadEngine():
    import importlib
    importlib.reload(sudoku)
    print('Reloaded sudoku game engine.')