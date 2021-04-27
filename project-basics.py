#basic implementation for the matrix representation of the puzzle
#feel free to mess around and change things, this is just a first pass on the idea


class WitnessGrid:
    def __init__(self):
        self.grid = []
        self.head = []

        #we can decide which one we'd like to keep
        self.moves = [] # e.g. up, left, etc.
        self.trail = [] # e.g. [4,0] for the vertex 'b'
    
    def makeBasic2x2(self):
        self.grid = [['v', 'e', 'v', 'e', 'f'], 
                     ['e', 's', 'e', 's', 'e'],
                     ['v', 'e', 'v', 'e', 'v'],
                     ['e', 's', 'e', 's', 'e'],
                     ['b', 'e', 'v', 'e', 'v']]
        
    def begin(self):
        for row in self.grid:
            for item in row:
                if item == 'b':
                    self.head = [self.grid.index(row), row.index(item)]
                    self.trail.append(self.head)
        
                    
    def step(self):
        choice = input("Type u,d,l,r for up/down/left/right: ")
        if choice == 'u':
            return self.moveup()
        elif choice == 'd':
            return self.movedown()
        elif choice == 'l':
            return self.moveleft()
        elif choice == 'r':
            return self.moveright()
        else:
            print("Choose u/d/l/r")
            return
    
    def evaluateState(self, move):
        '''
        This function returns 'Solved' if the current vertex is the final vertex
        otherwise it returns the current trail
        '''
        self.moves.append(move)
        curr_row, curr_col = self.trail[-1] #gets the last row inserted after moving
        return 'Solved' if self.grid[curr_row][curr_col] == 'f' else self.trail

    def getNumRows(self):
        return len(self.grid) - 1
    
    def getNumCols(self):
        return len(self.grid[0]) - 1
    
    def getMoves(self):
        '''Returns the list of moves entered'''
        return self.moves
        
    def moveup(self):
        '''Gets the last position moved and checks if there is an edge
            to the next vertex. If an edge exists, it moves up to the next
            vertex, otherwise it returns and 'invalid' move.
        '''
        row, col = self.trail[-1]
        if row >= 0 and self.grid[row - 1][col] == 'e':
            self.trail.append([row -2, col])
            return self.evaluateState('up')
        return 'Invalid'

    def movedown(self):
        '''Gets the last position moved and checks if there is an edge
            to the next vertex. If an edge exists, it moves down to the next
            vertex, otherwise it returns and 'invalid' move.
        '''
        row, col = self.trail[-1]
        if row < self.getNumRows() and self.grid[row + 1][col] == 'e':
            self.trail.append([row + 2, col])
            return self.evaluateState('down')
        return 'Invalid'
    
    def moveleft(self):
        row, col = self.trail[-1]
        if col >= 0 and self.grid[row][col-1] == 'e':
            self.trail.append([row, col-2])
            return self.evaluateState('left')
        return 'Invalid'
    
    def moveright(self):
        row, col = self.trail[-1]
        if col < self.getNumCols() and self.grid[row][col + 1] == 'e':
            self.trail.append([row, col + 2])
            return self.evaluateState('right')
        return 'Invalid'

if __name__ == '__main__':
    # testing out the class manually
    test = WitnessGrid()
    test.makeBasic2x2()
    test.begin()

    step = test.step()
    print(step)
    while step != 'Invalid':
        step = test.step()
        print(step)
        if step == 'Solved':
            break
    print(test.getMoves())
    