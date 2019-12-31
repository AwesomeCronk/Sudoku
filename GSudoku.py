# GSudoku.py
# Version history:
# V 1.0.0
# - Began logging version history. I had made a mistake with Git, so I must now rewrite much of the improvements I hade previously made.
# V 1.0.1
# - Fixed an issue with the active grid remaining active after reset and not clearing the styles of previous active grids.
# V 1.0.2
# - Added a directions file. Added ability to clear a grid in the GUI. Changed the default setting for sudoku.b1.printboard() to 'pretty'.
# V 1.0.3
# - Added a clear button and connected it. Updated the directions to a slight degree.
# V 1.0.4
# - Replaced the 200 or so lines of hard code in sudoku.check for the subgrid carry with an algorithm. Utilized that algirithm to find the x, y coordinates of dubgrid locations. Added a mode system to sudoku.check which flags errors instead of clearing them.

from Sudoku import sudoku
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
    errorStyle = "color: #000000; background-color: #FF0000;"
    badGrids = []
    lockedGrids = []
    def __init__(self):
        super(sudokuApp, self).__init__()
        self.setWindowTitle('Sudoku')
        self.createUI()
        self.configureUI()
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
        
        self.setupBtn = QPushButton(self)    #Create the control buttons.
        self.clearBtn = QPushButton(self)
        self.checkBtn = QPushButton(self)
        self.solveBtn = QPushButton(self)

    def configureUI(self, desiredScale = 1):    #Scale, position, and set style sheets and text properly.
        self.scale = desiredScale    #Calculate the sizes needed for the given scale.
        self.gridwidth = 40 * self.scale
        self.gridheight = 40 * self.scale
        self.spacing = 5 * self.scale
        self.boardWidth = self.spacing + (9 * (self.spacing + self.gridwidth))
        self.boardHeight = self.spacing + (9 * (self.spacing + self.gridheight))

        for x in range(9):
            for y in range(9):
                grid = self.grids[x][y]
                grid.setGeometry(self.spacing + (y * (self.spacing + self.gridwidth)), self.spacing + (x * (self.spacing + self.gridheight)), self.gridwidth, self.gridheight)
                grid.setStyleSheet(self.openStyle)

        self.setupBtn.setGeometry(self.spacing, self.boardHeight, (self.scale * 80), (self.scale * 30))
        self.clearBtn.setGeometry((self.spacing * 2) + (self.scale * 80), self.boardHeight, (self.scale * 80), (self.scale * 30))
        self.checkBtn.setGeometry((self.spacing * 3) + (self.scale * 160), self.boardHeight, (self.scale * 80), (self.scale * 30))
        self.solveBtn.setGeometry((self.spacing * 4) + (self.scale * 240), self.boardHeight, (self.scale * 80), (self.scale * 30))

        self.setupBtn.setText('Setup')
        self.clearBtn.setText('Clear')
        self.checkBtn.setText('Check')
        self.solveBtn.setText('Solve')

        self.setFixedSize(self.boardWidth, self.boardHeight + (self.scale * 30) + self.spacing)

    def activateUI(self):    #Connect them to their respective functions.
        for x in range(9):
            for y in range(9):
                grid = self.grids[x][y]
                grid.clicked.connect(self.selectGrid)
                grid.setCheckable(True)
        self.setupBtn.clicked.connect(self.setup)
        self.clearBtn.clicked.connect(self.clear)

    def setup(self):    #Set up the board for a new game.
        self.lockedGrids = []
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
                    self.lockedGrids.append((x, y))
    def clear(self):    #Clear the board.
        self.b1.clear()
        for x in range(9):
            for y in range(9):
                grid = self.grids[x][y]
                grid.setEnabled(True)
                grid.setStyleSheet(self.openStyle)
                grid.setText('')
                self.activeGrid = 'no active grid'

    def check(self):
        for i in self.badGrids:
            x, y = i
            self.grids[x][y].setStyleSheet(self.openStyle)
        self.badGrids = self.b1.rawcheck(mode = 'flag')
        for i in self.badGrids:
            x, y = i
            self.grids[x][y].setStyleSheet(self.errorStyle)

    def selectGrid(self):    #Determine the grid clicked on by the user. Color it and reset its toggled state.
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

    def editGrid(self, key):    #Plug a value into a grid and send it to the sudoku engine.
        x, y = self.activeGrid
        if len(sudoku.findall(self.possibleInputs, key)) == 1:    #if the input is within the legal range
            self.grids[x][y].setText(str(key))
            sudoku.rawplace(x, y, key)
        elif key == 16777171:     #Detect a backspace and clear the grid and put a zero in the sudoku engine.
            self.grids[x][y].setText('')
            sudoku.rawplace(x, y, 0)

    def keyPressEvent(self, event):    #This is the keypress detector. I use this to determine input to edit grids.
        try:
            print(event.key())
            key = event.key() - 48    #Seems that the number keys are keyed in equivalent to their value + 48. This operation is also applied to the backspace key as well.
            print(key)
            self.editGrid(key)
        except:
            pass

def Game():    #Triggers all the magic above.
    app = QApplication([])
    gameInstance = sudokuApp()
    gameInstance.show()
    app.exec_()

def reloadEngine():    #Function to reload the sudoku engine, so that I can continue working in the same terminal.
    import importlib
    importlib.reload(sudoku)
    print('Reloaded sudoku game engine.')