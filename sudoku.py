import random as rnd

class row():
    def __init__(self):
        self.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        #print('created row')

class col():
    def __init__(self):
        self.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        
class sub():
    def __init__(self):
        self.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        
class board():
    mode = 'easy'
    won = False
    lockedGrids = []
    def __init__(self):
        self.rows = [row(), row(), row(), row(), row(), row() ,row(), row(), row()]
        self.cols = [col(), col(), col(), col(), col(), col(), col(), col(), col()]
        self.subs = [sub(), sub(), sub(), sub(), sub(), sub(), sub(), sub(), sub()]
        #print('Board created.')
    
    def setup(self):
        if self.mode == 'easy':
            numtoremove = 40
        if self.mode == 'medium':
            numtoremove = 50
        if self.mode == 'hard':
            numtoremove = 60

        self.lockedGrids = []
        self.errors = []
        for i in self.rows:
            for j in i.grid:
                j = 0
        
        for i in range(9):    #fill the board with random numbers
            for j in range(9):
                self.rawplace(i, j, rnd.randint(1, 9))

        self.rawcheck(mode = 'remove')    #remove the problem numbers

        for i in range(rnd.randint(numtoremove, numtoremove + 10)):    #make some more empty spaces
            self.rawplace(rnd.randint(0, 8), rnd.randint(0, 8), 0)

        #debugging
        self.printboard()
        self.printboard(mode = 'rows')
        print('---------')
        self.printboard(mode = 'cols')

        for x in range(9):    #find all the non-zero grids and add them to the list of locked grids.
            for y in range(9):
                if self.rows[y].grid[x] != 0:
                    self.lockedGrids.append((x, y))

        print("lockedGrids: {}".format(self.lockedGrids))
            
    def clear(self):    #set every grid to zero
        for i in self.rows:
            for j in i.grid:
                j = 0
        for i in self.cols:
            for j in i.grid:
                j = 0
        for i in self.subs:
            for j in i.grid:
                j = 0
            
    def check(self, mode = 'flag', ignoreLocked = False):    #check the grids using the 1-9 system
        errors = self.rawcheck(mode = mode, ignoreLocked = ignoreLocked)    #get the 0-8 version
        niceErrors = []    #make an empty list
        for i in errors:    #for each 0-8 error
            a, b = i    #unpack the tuple
            niceErrors.append(a + 1, b + 1)    #make a new tuple with the 1-9 version and add it to the nice errors
        return niceErrors    #return it

    def rawcheck(self, mode = 'flag', ignoreLocked = False):    #check the grids using the 0-8 system
        self.errors = []
        

        #----------rows----------#
        for i in range(9):     #address of the rows
            #print('checking row {}'.format(str(i)))
            for j in range(1, 10):    #numbers to be checked
                #print('Number: {}'.format(str(j)))
                instances = findall(self.rows[i].grid, j)    #find all the instances of the current number
                #print(instances, end = ' ')
                #print(len(instances))
                if len(instances) > 1:    #if there are multiple instances
                    for k in instances:    #for each grid which has an error
                        location = (k, i)
                        isLocked = False
                        for l in self.lockedGrids:
                            if location == l:
                                isLocked = True
                        if not isLocked:
                            self.errors.append(location)    #append the x and y locations of the error in a tuple to the board's list of errors
                            print("added error.")
                    if mode == 'remove':    #if the mode is remove
                        self.rows[i].grid[instances[len(instances) - 1]] = 0    #set that grid to 0

                if len(instances) == 0:    #check to see if all grids are filled and set the won variable accordingly
                    self.won = True
                else:
                    self.won = False
        self.carry('rows', 'cols')    #carry to the other datatypes
        self.carry('rows', 'subs')
        

        #---------columns----------#
        for i in range(9):     #address of the cols
            #print('checking col {}'.format(str(i)))
            for j in range(1, 10):    #numbers to be checked
                #print('Number: {}'.format(str(j)))
                instances = findall(self.cols[i].grid, j)    #find all the instances of the current number
                #print(instances, end = ' ')
                #print(len(instances))
                if len(instances) > 1:    #if there are multiple instances
                    for k in instances:    #for each grid which has an error
                        location = (i, k)
                        isLocked = False
                        for l in self.lockedGrids:
                            if location == l:
                                isLocked = True
                        if not isLocked:
                            self.errors.append(location)    #append the x and y locations of the error in a tuple to the board's list of errors
                            print("added error.")
                    if mode == 'remove':    #if the mode is remove
                        self.cols[i].grid[instances[len(instances) - 1]] = 0    #set that grid to 0

                if len(instances) == 0:    #check to see if all grids are filled and set the won variable accordingly
                    self.won = True
                else:
                    self.won = False
        self.carry('cols', 'rows')    #carry to the other datatypes
        self.carry('cols', 'subs')
        
        
        #----------subgrids----------#
        for i in range(9):     #address of the subs
            #print('checking sub {}'.format(str(i)))
            for j in range(1, 10):    #numbers to be checked
                #print('Number: {}'.format(str(j)))
                instances = findall(self.subs[i].grid, j)    #find all the instances of the current number
                #print(instances, end = ' ')
                #print(len(instances))
                if len(instances) > 1:    #if there are multiple instances
                    for k in instances:    #for each grid which has an error
                        location = self.subsToCoord(i, k)
                        isLocked = False
                        for l in self.lockedGrids:
                            if location == l:
                                isLocked = True
                        if not isLocked:
                            self.errors.append(location)    #append the x and y locations of the error in a tuple to the board's list of errors
                            print("added error.")
                    if mode == 'remove':    #if the mode is remove
                        self.subs[i].grid[instances[len(instances) - 1]] = 0    #set that grid to 0

                if len(instances) == 0:    #check to see if all grids are filled and set the won variable accordingly
                    self.won = True
                else:
                    self.won = False
        self.carry('subs', 'rows')    #carry to the other datatypes
        self.carry('subs', 'cols')

        print("errors: {}  mode: {}".format(self.errors, mode))
        if len(self.errors) and mode == 'remove':    #if there were errors and the mode is remove
            print("Looping...")
            self.won = False    #you haven't won yet
            self.rawcheck(mode = 'remove')    #check it again!!
        else:
            print("Done.")
            
        #----------cleanup----------#
        errorList = []    #This section removes the locked grids from the error list and removes the multiple instances of errors.
        for i in self.errors:
            for j in self.lockedGrids:
                #print("self.errors: {}".format(i))
                #print("self.lockedGrids: {}".format(j))
                if i != j and len(findall(errorList, i)) == 0:
                    errorList.append(i)
        print("self.errors: {}".format(self.errors))
        print("errorList: {}".format(errorList))
        self.errors = errorList

        return self.errors    #return the list of errors.
                
    def printboard(self, mode = 'pretty'):
        if mode == 'rows':
            for i in self.rows:
                for j in range(len(i.grid)):
                    print(i.grid[j], end = ' ')
                print()
        if mode == 'cols':
            for i in range(9):
                for j in self.cols:
                    print(j.grid[i], end = ' ')
                print()
        if mode == 'pretty':
            lnctr = 0
            print('-------------------------')
            for i in self.rows:
                print('| ' + str(i.grid[0]) + ' ' + str(i.grid[1]) + ' ' + str(i.grid[2]) + ' | ' +
                str(i.grid[3]) + ' ' + str(i.grid[4]) + ' ' + str(i.grid[5]) + ' | ' +
                str(i.grid[6]) + ' ' + str(i.grid[7]) + ' ' + str(i.grid[8]) + ' |')
                lnctr += 1
                if lnctr in [3, 6]:
                    print('|-------+-------+-------|')
            print('-------------------------')
    
    def place(self, xloc, yloc, val):    #place a value with the 1-9 convention
        try:
            #print(str(xloc) + ', ' + str(yloc) + ', ' + str(val))
            return self.rawplace(int(xloc) - 1, int(yloc) - 1, int(val))
        except:
            return False
    
    def rawplace(self, xloc, yloc, val):    #place a value with the 0-8 convention
        #print("function: 'rawplace'")
        try:
            if xloc > 8 or xloc < 0 or yloc > 8 or yloc < 0:
                print('Out of range')
                return False
            else:
                self.rows[yloc].grid[xloc] = val
                self.carry('rows', 'cols')
                self.carry('rows', 'subs')
                return True
        except:
            return False

    def read(self, xloc, yloc):    #read a grid with the 1-9 convention
        try:
            return self.rawread(int(xloc - 1), int(yloc - 1))
        except:
                return False

    def rawread(self, xloc, yloc):    #read a grid with the 0-8 convention
        try:
            if xloc > 8 or xloc < 0 or yloc > 8 or yloc < 0:
                print('Out of range')
                return False
            else:
                return self.rows[yloc].grid[xloc]
        except:
            return False
                
    
    def carry(self, set1, set2):
        if set1 == 'rows' and set2 == 'cols':
            for x in range(9):    #for each grid in the board
                for y in range(9):
                    self.cols[x].grid[y] = self.rows[y].grid[x]    #set that col.grid equal to that row.grid
        if set1 == 'cols' and set2 == 'rows':
            for x in range(9):    #for each grid in the board
                for y in range(9):
                    self.rows[y].grid[x] = self.cols[x].grid[y]    #set that row.grid equal to that col.grid
        
        if set1 == 'rows' and set2 == 'subs':
            for i in range(3):    #for each row of subs
                for j in range(3):    #for each row in that row of subs
                    for k in range(3):    #for each third of that row
                        for l in range(3):    #for each grid in that third
                            self.subs[(3 * i) + k].grid[(3 * j) + l] = self.rows[(3 * k) + l].grid[(3 * i) + j]
            
        if set1 == 'subs' and set2 == 'rows':
            for i in range(3):    #for each row of subs
                for j in range(3):    #for each row in that row of subs
                    for k in range(3):    #for each third of that row
                        for l in range(3):    #for each grid in that third
                            self.rows[(3 * k) + l].grid[(3 * i) + j] = self.subs[(3 * i) + k].grid[(3 * j) + l]

        if set1 == 'cols' and set2 == 'subs':
            for i in range(3):    #for each row of subs
                for j in range(3):    #for each row in that row of subs
                    for k in range(3):    #for each third of that row
                        for l in range(3):    #for each grid in that third
                            self.subs[(3 * i) + k].grid[(3 * j) + l] = self.rows[(3 * i) + j].grid[(3 * k) + l]
            
        if set1 == 'subs' and set2 == 'cols':
            for i in range(3):    #for each row of subs
                for j in range(3):    #for each row in that row of subs
                    for k in range(3):    #for each third of that row
                        for l in range(3):    #for each grid in that third
                            self.rows[(3 * i) + j].grid[(3 * k) + l] = self.subs[(3 * i) + k].grid[(3 * j) + l]

    def coordToSubs(self, xIn, yIn):    #function to get a subgrid's address from x, y coordinates
        for i in range(3):    #for each row of subs
            for j in range(3):    #for each row in that row of subs
                for k in range(3):    #for each third of that row
                    for l in range(3):    #for each grid in that third
                        x = (3 * i) + j
                        y = (3 * k) + l
                        subID = (3 * i) + k
                        gridID = (3 * j) + l
                        if x == xIn and y == yIn:
                            return (subID, gridID)

    def subsToCoord(self, subIn, gridIn):    #function to get (x, y) coordinates of a subgrid by its address
        for i in range(3):    #for each row of subs
            for j in range(3):    #for each row in that row of subs
                for k in range(3):    #for each third of that row
                    for l in range(3):    #for each grid in that third
                        x = (3 * k) + l
                        y = (3 * i) + j
                        subID = (3 * i) + k
                        gridID = (3 * j) + l
                        if subID == subIn and gridID == gridIn:
                            return (x, y)
        
def findall(listin, x):    #function to find all occurences of an element in a list
    occurences = []
    for i in range(len(listin)):
        if listin[i] == x:
            occurences.append(i)
    return occurences