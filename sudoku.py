import random as rnd

class row():
    def __init__(self):
        self.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        print('created row')

class col():
    def __init__(self):
        self.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        
class sub():
    def __init__(self):
        self.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        
class board():
    mode = 'easy'
    won = False
    def __init__(self):
        self.rows = [row(), row(), row(), row(), row(), row() ,row(), row(), row()]
        self.cols = [col(), col(), col(), col(), col(), col(), col(), col(), col()]
        self.subs = [sub(), sub(), sub(), sub(), sub(), sub(), sub(), sub(), sub()]
        print('Board created.')
    
    def setup(self):
        if self.mode == 'easy':
            numtoremove = 40
        if self.mode == 'medium':
            numtoremove = 50
        if self.mode == 'hard':
            numtoremove = 60

        for i in self.rows:
            for j in i.grid:
                j = 0
        
        for i in range(9):
            for j in range(9):
                self.rawplace(i, j, rnd.randint(1, 9))
        self.check()
        for i in range(rnd.randint(numtoremove, numtoremove + 10)):
            self.rawplace(rnd.randint(0, 8), rnd.randint(0, 8), 0)
            
    def clear(self):
        for i in self.rows:
            for j in i.grid:
                j = 0
        for i in self.cols:
            for j in i.grid:
                j = 0
        for i in self.subs:
            for j in i.grid:
                j = 0
            
    def check(self):
        self.error = False
        for i in self.rows:
            #print('checking {}'.format(str(i)))
            for j in range(1, 10):
                instances = findall(i.grid, j)
                #print(instances, end = ' ')
                #print(len(instances))
                if len(instances) > 1:    #check for multiple instances and throw an error
                    self.error = True
                    i.grid[instances[len(instances) - 1]] = 0

                if len(instances) == 0:    #check to see if all grids are filled and set the won variable accordingly
                    self.won = True
                else:
                    self.won = False
        self.carry('rows', 'cols')
        self.carry('rows', 'subs')
        
        for i in self.cols:
            #print('checking {}'.format(str(i)))
            for j in range(1, 10):
                instances = findall(i.grid, j)
                #print(instances, end = ' ')
                #print(len(instances))
                if len(instances) > 1:    #check for multiple instances and throw an error
                    self.error = True
                    i.grid[instances[len(instances) - 1]] = 0

                if len(instances) == 0:    #check to see if all grids are filled and set the won variable accordingly
                    self.won = True
                else:
                    self.won = False
        self.carry('cols', 'rows')
        self.carry('rows', 'subs')
        
        for i in self.subs:
            #print('checking {}'.format(str(i)))
            for j in range(1, 10):
                instances = findall(i.grid, j)
                #print(instances, end = ' ')
                #print(len(instances))
                if len(instances) > 1:    #check for multiple instances and throw an error
                    self.error = True
                    i.grid[instances[len(instances) - 1]] = 0

                if len(instances) == 0:    #check to see if all grids are filled and set the won variable accordingly
                    self.won = True
                else:
                    self.won = False
        self.carry('subs', 'rows')
        self.carry('rows', 'cols')
        
        if self.error:
            self.won = False
            self.check()
                
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
    
    def place(self, xloc, yloc, val):
        try:
            #print(str(xloc) + ', ' + str(yloc) + ', ' + str(val))
            return self.rawplace(int(xloc) - 1, int(yloc) - 1, int(val))
        except:
            return False
    
    def rawplace(self, xloc, yloc, val):
        #print("function: 'rawplace'")
        try:
            if xloc > 8 or xloc < 0 or yloc > 8 or yloc < 0:
                #print('Out of range')
                return False
            else:
                self.rows[yloc].grid[xloc] = val
                self.carry('rows', 'cols')
                self.carry('rows', 'subs')
                return True
        except:
            return False

    def read(self, xloc, yloc):
        try:
            return self.rawread(int(xloc - 1), int(yloc - 1))
        except:
                return False

    def rawread(self, xloc, yloc):
        try:
            if xloc > 8 or xloc < 0 or yloc > 8 or yloc < 0:
                #print('Out of range')
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
            self.subs[0].grid[0] = self.rows[0].grid[0]    #first row
            self.subs[0].grid[1] = self.rows[0].grid[1]
            self.subs[0].grid[2] = self.rows[0].grid[2]
            self.subs[0].grid[3] = self.rows[1].grid[0]
            self.subs[0].grid[4] = self.rows[1].grid[1]
            self.subs[0].grid[5] = self.rows[1].grid[2]
            self.subs[0].grid[6] = self.rows[2].grid[0]
            self.subs[0].grid[7] = self.rows[2].grid[1]
            self.subs[0].grid[8] = self.rows[2].grid[2]
            
            self.subs[1].grid[0] = self.rows[0].grid[3]
            self.subs[1].grid[1] = self.rows[0].grid[4]
            self.subs[1].grid[2] = self.rows[0].grid[5]
            self.subs[1].grid[3] = self.rows[1].grid[3]
            self.subs[1].grid[4] = self.rows[1].grid[4]
            self.subs[1].grid[5] = self.rows[1].grid[5]
            self.subs[1].grid[6] = self.rows[2].grid[3]
            self.subs[1].grid[7] = self.rows[2].grid[4]
            self.subs[1].grid[8] = self.rows[2].grid[5]
            
            self.subs[2].grid[0] = self.rows[0].grid[6]
            self.subs[2].grid[1] = self.rows[0].grid[7]
            self.subs[2].grid[2] = self.rows[0].grid[8]
            self.subs[2].grid[3] = self.rows[1].grid[6]
            self.subs[2].grid[4] = self.rows[1].grid[7]
            self.subs[2].grid[5] = self.rows[1].grid[8]
            self.subs[2].grid[6] = self.rows[2].grid[6]
            self.subs[2].grid[7] = self.rows[2].grid[7]
            self.subs[2].grid[8] = self.rows[2].grid[8]
            
            self.subs[3].grid[0] = self.rows[3].grid[0]    #second row
            self.subs[3].grid[1] = self.rows[3].grid[1]
            self.subs[3].grid[2] = self.rows[3].grid[2]
            self.subs[3].grid[3] = self.rows[4].grid[0]
            self.subs[3].grid[4] = self.rows[4].grid[1]
            self.subs[3].grid[5] = self.rows[4].grid[2]
            self.subs[3].grid[6] = self.rows[5].grid[0]
            self.subs[3].grid[7] = self.rows[5].grid[1]
            self.subs[3].grid[8] = self.rows[5].grid[2]
            
            self.subs[4].grid[0] = self.rows[3].grid[3]
            self.subs[4].grid[1] = self.rows[3].grid[4]
            self.subs[4].grid[2] = self.rows[3].grid[5]
            self.subs[4].grid[3] = self.rows[4].grid[3]
            self.subs[4].grid[4] = self.rows[4].grid[4]
            self.subs[4].grid[5] = self.rows[4].grid[5]
            self.subs[4].grid[6] = self.rows[5].grid[3]
            self.subs[4].grid[7] = self.rows[5].grid[4]
            self.subs[4].grid[8] = self.rows[5].grid[5]
            
            self.subs[5].grid[0] = self.rows[3].grid[6]
            self.subs[5].grid[1] = self.rows[3].grid[7]
            self.subs[5].grid[2] = self.rows[3].grid[8]
            self.subs[5].grid[3] = self.rows[4].grid[6]
            self.subs[5].grid[4] = self.rows[4].grid[7]
            self.subs[5].grid[5] = self.rows[4].grid[8]
            self.subs[5].grid[6] = self.rows[5].grid[6]
            self.subs[5].grid[7] = self.rows[5].grid[7]
            self.subs[5].grid[8] = self.rows[5].grid[8]
            
            self.subs[6].grid[0] = self.rows[6].grid[0]    #third row
            self.subs[6].grid[1] = self.rows[6].grid[1]
            self.subs[6].grid[2] = self.rows[6].grid[2]
            self.subs[6].grid[3] = self.rows[7].grid[0]
            self.subs[6].grid[4] = self.rows[7].grid[1]
            self.subs[6].grid[5] = self.rows[7].grid[2]
            self.subs[6].grid[6] = self.rows[8].grid[0]
            self.subs[6].grid[7] = self.rows[8].grid[1]
            self.subs[6].grid[8] = self.rows[8].grid[2]
            
            self.subs[7].grid[0] = self.rows[6].grid[3]
            self.subs[7].grid[1] = self.rows[6].grid[4]
            self.subs[7].grid[2] = self.rows[6].grid[5]
            self.subs[7].grid[3] = self.rows[7].grid[3]
            self.subs[7].grid[4] = self.rows[7].grid[4]
            self.subs[7].grid[5] = self.rows[7].grid[5]
            self.subs[7].grid[6] = self.rows[8].grid[3]
            self.subs[7].grid[7] = self.rows[8].grid[4]
            self.subs[7].grid[8] = self.rows[8].grid[5]
            
            self.subs[8].grid[0] = self.rows[6].grid[6]
            self.subs[8].grid[1] = self.rows[6].grid[7]
            self.subs[8].grid[2] = self.rows[6].grid[8]
            self.subs[8].grid[3] = self.rows[7].grid[6]
            self.subs[8].grid[4] = self.rows[7].grid[7]
            self.subs[8].grid[5] = self.rows[7].grid[8]
            self.subs[8].grid[6] = self.rows[8].grid[6]
            self.subs[8].grid[7] = self.rows[8].grid[7]
            self.subs[8].grid[8] = self.rows[8].grid[8]
            
        if set1 == 'subs' and set2 == 'rows':
            self.rows[0].grid[0] = self.subs[0].grid[0]    #first row
            self.rows[0].grid[1] = self.subs[0].grid[1]
            self.rows[0].grid[2] = self.subs[0].grid[2]
            self.rows[1].grid[0] = self.subs[0].grid[3]
            self.rows[1].grid[1] = self.subs[0].grid[4]
            self.rows[1].grid[2] = self.subs[0].grid[5]
            self.rows[2].grid[0] = self.subs[0].grid[6]
            self.rows[2].grid[1] = self.subs[0].grid[7]
            self.rows[2].grid[2] = self.subs[0].grid[8]
            
            self.rows[0].grid[3] = self.subs[1].grid[0]
            self.rows[0].grid[4] = self.subs[1].grid[1]
            self.rows[0].grid[5] = self.subs[1].grid[2]
            self.rows[1].grid[3] = self.subs[1].grid[3]
            self.rows[1].grid[4] = self.subs[1].grid[4]
            self.rows[1].grid[5] = self.subs[1].grid[5]
            self.rows[2].grid[3] = self.subs[1].grid[6]
            self.rows[2].grid[4] = self.subs[1].grid[7]
            self.rows[2].grid[5] = self.subs[1].grid[8]
            
            self.rows[0].grid[6] = self.subs[2].grid[0]
            self.rows[0].grid[7] = self.subs[2].grid[1]
            self.rows[0].grid[8] = self.subs[2].grid[2]
            self.rows[1].grid[6] = self.subs[2].grid[3]
            self.rows[1].grid[7] = self.subs[2].grid[4]
            self.rows[1].grid[8] = self.subs[2].grid[5]
            self.rows[2].grid[6] = self.subs[2].grid[6]
            self.rows[2].grid[7] = self.subs[2].grid[7]
            self.rows[2].grid[8] = self.subs[2].grid[8]
            
            self.rows[3].grid[0] = self.subs[3].grid[0]    #second row
            self.rows[3].grid[1] = self.subs[3].grid[1]
            self.rows[3].grid[2] = self.subs[3].grid[2]
            self.rows[4].grid[0] = self.subs[3].grid[3]
            self.rows[4].grid[1] = self.subs[3].grid[4]
            self.rows[4].grid[2] = self.subs[3].grid[5]
            self.rows[5].grid[0] = self.subs[3].grid[6]
            self.rows[5].grid[1] = self.subs[3].grid[7]
            self.rows[5].grid[2] = self.subs[3].grid[8]
            
            self.rows[3].grid[3] = self.subs[4].grid[0]
            self.rows[3].grid[4] = self.subs[4].grid[1]
            self.rows[3].grid[5] = self.subs[4].grid[2]
            self.rows[4].grid[3] = self.subs[4].grid[3]
            self.rows[4].grid[4] = self.subs[4].grid[4]
            self.rows[4].grid[5] = self.subs[4].grid[5]
            self.rows[5].grid[3] = self.subs[4].grid[6]
            self.rows[5].grid[4] = self.subs[4].grid[7]
            self.rows[5].grid[5] = self.subs[4].grid[8]
            
            self.rows[3].grid[6] = self.subs[5].grid[0]
            self.rows[3].grid[7] = self.subs[5].grid[1]
            self.rows[3].grid[8] = self.subs[5].grid[2]
            self.rows[4].grid[6] = self.subs[5].grid[3]
            self.rows[4].grid[7] = self.subs[5].grid[4]
            self.rows[4].grid[8] = self.subs[5].grid[5]
            self.rows[5].grid[6] = self.subs[5].grid[6]
            self.rows[5].grid[7] = self.subs[5].grid[7]
            self.rows[5].grid[8] = self.subs[5].grid[8]
            
            self.rows[6].grid[0] = self.subs[6].grid[0]    #third row
            self.rows[6].grid[1] = self.subs[6].grid[1]
            self.rows[6].grid[2] = self.subs[6].grid[2]
            self.rows[7].grid[0] = self.subs[6].grid[3]
            self.rows[7].grid[1] = self.subs[6].grid[4]
            self.rows[7].grid[2] = self.subs[6].grid[5]
            self.rows[8].grid[0] = self.subs[6].grid[6]
            self.rows[8].grid[1] = self.subs[6].grid[7]
            self.rows[8].grid[2] = self.subs[6].grid[8]
            
            self.rows[6].grid[3] = self.subs[7].grid[0]
            self.rows[6].grid[4] = self.subs[7].grid[1]
            self.rows[6].grid[5] = self.subs[7].grid[2]
            self.rows[7].grid[3] = self.subs[7].grid[3]
            self.rows[7].grid[4] = self.subs[7].grid[4]
            self.rows[7].grid[5] = self.subs[7].grid[5]
            self.rows[8].grid[3] = self.subs[7].grid[6]
            self.rows[8].grid[4] = self.subs[7].grid[7]
            self.rows[8].grid[5] = self.subs[7].grid[8]
            
            self.rows[6].grid[6] = self.subs[8].grid[0]
            self.rows[6].grid[7] = self.subs[8].grid[1]
            self.rows[6].grid[8] = self.subs[8].grid[2]
            self.rows[7].grid[6] = self.subs[8].grid[3]
            self.rows[7].grid[7] = self.subs[8].grid[4]
            self.rows[7].grid[8] = self.subs[8].grid[5]
            self.rows[8].grid[6] = self.subs[8].grid[6]
            self.rows[8].grid[7] = self.subs[8].grid[7]
            self.rows[8].grid[8] = self.subs[8].grid[8]
        
def findall(listin, x):
    occurences = []
    for i in range(len(listin)):
        if listin[i] == x:
            occurences.append(i)
    return occurences