#!/usr/bin/env python3

import random
import csv
import copy
#from PIL import Image, ImageDraw
# import numpy as np

class WitnessGrid:
    def __init__(self):
        self.grid = []
        self.head = []

        #we can decide which one we'd like to keep
        self.moves = [] # e.g. up, left, etc.
        self.trail = [] # e.g. [4,0] for the vertex 'b'
        
        self.imageNum = 0
    
    def makeBasic2x2(self):
        self.grid = [['v', 'e', 'v', 'e', 'f'], 
                     ['e', ' ', 'e', ' ', 'e'],
                     ['v', 'e', 'v', 'e', 'v'],
                     ['e', ' ', 'e', ' ', 'e'],
                     ['b', 'e', 'v', 'e', 'v']]
        
    def makeBasicNxN(self, n):
        if n > 0:
            self.grid = [['v', 'e', 'v'], 
                         ['e', ' ', 'e'], 
                         ['v', 'e', 'v']]
            for x in range(n - 1):
                self.grid.append(['e', ' ', 'e'])
                self.grid.append(['v', 'e', 'v'])
            for x in range(len(self.grid)):  
                for y in range(n - 1):
                    if x % 2 == 0:
                        self.grid[x].extend(['e', 'v'])
                    else:
                        self.grid[x].extend([' ', 'e'])
            self.grid[0][-1] = 'f'
            self.grid[-1][0] = 'b'
            return self.grid
        else: 
            return 'Choose n >= 1 for grid size!'
        
    # note that when n is odd, a dotted grid may occasionally be unsolvable
    def makeDottedNxN(self, n, percent):
        if n > 0:
            self.grid = [['v', 'e', 'v'], 
                         ['e', ' ', 'e'], 
                         ['v', 'e', 'v']]
            for x in range(n - 1):
                self.grid.append(['e', ' ', 'e'])
                self.grid.append(['v', 'e', 'v'])
            for x in range(len(self.grid)):  
                for y in range(n - 1):
                    if x % 2 == 0:
                        self.grid[x].extend(['e', 'v'])
                    else:
                        self.grid[x].extend([' ', 'e'])
            self.grid[0][-1] = 'f'
            self.grid[-1][0] = 'b'
            
            # add dots
            for x in range(len(self.grid)):
                if x % 2 == 0:
                    for y in range(len(self.grid[x])):
                        if self.grid[x][y] == 'v' and random.randint(1,100) <= percent:
                            self.grid[x][y] = 'X'
            
            return self.grid
        else: 
            return 'Choose n >= 1 for grid size!'
        
    def begin(self):
        self.head = []
        self.trail = []
        self.moves = []
        for row in self.grid:
            for item in row:
                if item == 'b':
                    self.head = [self.grid.index(row), row.index(item)]
                    self.trail.append(self.head)

    # assumes you already had a grid made
    def startBruteForce(self):
        self.head = []
        self.moves = []
        self.trail = []
        self.begin()
        
        self.bruteForceStep('up')
        self.bruteForceStep('right')
        self.bruteForceStep('down')
        self.bruteForceStep('left')
        
        return 'Done!'
        
    def bruteForceStep(self, direction):
        
        if direction == 'up':
            result = self.moveup()
        elif direction == 'down':
            result = self.movedown()
        elif direction == 'left':
            result = self.moveleft() 
        elif direction == 'right':
            result = self.moveright()
            
        if result[0:7] == 'Invalid':
            return
 #             self.write(self.moves + [direction, 'Invalid'])

 #         # was not invalid. save a 'screenshot' of the state of the board.
 #         # this is a hacky solution, won't generalize if start is not in bottom left.
        gridToSend = copy.deepcopy(self.grid)
        head = [len(gridToSend[0]) - 1, 0]
        for move in self.moves:
            if move == 'up':
                head[0] -= 1
                gridToSend[head[0]][head[1]] = 'u'
                head[0] -= 1
            elif move == 'right':
                head[1] += 1
                gridToSend[head[0]][head[1]] = 'r'
                head[1] += 1
            elif move == 'left':
                head[1] -= 1
                gridToSend[head[0]][head[1]] = 'l'
                head[1] -= 1
            elif move == 'down':
                head[0] += 1
                gridToSend[head[0]][head[1]] = 'd'
                head[0] += 1
            else:
                print("error")
                

        if result == 'Solved!':
            gridToSend[0][len(gridToSend) - 1] = 'S'
            self.writeGrid(gridToSend)
 #             self.write(self.moves + ['Solved'])
        elif result[0:8] == 'Finished':
            gridToSend[0][len(gridToSend) - 1] = 'F'
            self.writeGrid(gridToSend)
 #             self.write(self.moves + ['Finished'])
        else:
            self.writeGrid(gridToSend)
 #             self.write(self.moves)
            
            self.bruteForceStep('up')
            self.bruteForceStep('right')
            self.bruteForceStep('down')
            self.bruteForceStep('left')
            
        self.moves.pop()
        self.trail.pop()

    def writeGrid(self, grid):
        filename = "witnessData.csv"
        with open(filename, 'a') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            for row in grid:
                csvwriter.writerow(row) 
            csvwriter.writerow(" ")
            
        #make an image
        # solved = False
        # finished = False
    
        # dim = len(grid[0])
        # pxSize = 100
        
        # w = dim * pxSize #make pixels 100 big
        # h = dim * pxSize

        # img  = Image.new( mode = "RGB", size = (w, h) )
        # draw = ImageDraw.Draw(img)
        
        # for x in range(dim):
        #     for y in range(dim):
                
        #         char = grid[y][x]
        #         if char == 'v': # vertices are grey
        #             fillcolor = '#808080'
        #         elif char == 'X': # required vertices are purple
        #             fillcolor = '#800080'
        #         elif char == 'e': # untouched edge is white
        #             fillcolor = '#FFFFFF'
        #         elif char == ' ': # space is black
        #             fillcolor = '#000000'
                    
        #         elif char == 'u': # all are blue (drawing path)
        #             fillcolor = '#0000FF'
        #         elif char == 'd': 
        #             fillcolor = '#0000FF'
        #         elif char == 'l': 
        #             fillcolor = '#0000FF'
        #         elif char == 'r': 
        #             fillcolor = '#0000FF'
                    
        #         elif char == 'b': # begin is darkkhaki
        #             fillcolor = '#BDB76B'
        #         elif char == 'f': # finish is silver
        #             fillcolor = '#C0C0C0'
        #         elif char == 'S': # solved is silver
        #             fillcolor = '#C0C0C0'
        #             solved = True
        #         elif char == 'F': # finished is silver
        #             fillcolor = '#C0C0C0'
        #             finished = True
                
        #         draw.rectangle((0 + x * pxSize, 0 + y * pxSize, x * pxSize + w / dim, y * pxSize + h / dim), fill=fillcolor)
        
        # imgfilename = './images/'
        # if solved == True:
        #     imgfilename += 'solved/grid'+str(self.imageNum)+'.png'
        # elif finished == True:
        #     imgfilename += 'finished/grid'+str(self.imageNum)+'.png'
        # else:
        #     imgfilename += 'unfinished/grid'+str(self.imageNum)+'.png'
            
        # self.imageNum += 1
        
        # img.save(imgfilename)

            
    # We used this write function before changing how we set up our data    
    # 
    #     def write(self, path): # https://www.geeksforgeeks.org/writing-csv-files-in-python/
    #         filename = "witnessData.csv"
    #         with open(filename, 'a') as csvfile: 
    #             csvwriter = csv.writer(csvfile) 
    #             csvwriter.writerow(path) 
            
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
        
        gotEveryDot = True
        for x in range(len(self.grid)):
            if gotEveryDot == False: break
            if x % 2 == 0:
                for y in range(len(self.grid[x])):
                    if self.grid[x][y] == 'X':
                        if [x, y] not in self.trail:
                            gotEveryDot = False
                            break
        
        if self.grid[curr_row][curr_col] == 'f':
            if gotEveryDot == True:
                return 'Solved!'
            else:
                return 'Finished, but missed one or more dots!'
        else:
            return self.trail

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
            if self.trail.count([row - 2, col]) > 0:
                return 'Invalid: Crossed Path!'
            self.trail.append([row - 2, col])
            return self.evaluateState('up')
        return 'Invalid: Out of Bounds!'

    def movedown(self):
        '''Gets the last position moved and checks if there is an edge
            to the next vertex. If an edge exists, it moves down to the next
            vertex, otherwise it returns and 'invalid' move.
        '''
        row, col = self.trail[-1]
        if row < self.getNumRows() and self.grid[row + 1][col] == 'e':
            if self.trail.count([row + 2, col]) > 0:
                return 'Invalid: Crossed Path!'
            self.trail.append([row + 2, col])
            return self.evaluateState('down')
        return 'Invalid: Out of Bounds!'
    
    def moveleft(self):
        row, col = self.trail[-1]
        if col >= 0 and self.grid[row][col-1] == 'e':
            if self.trail.count([row, col - 2]) > 0:
                return 'Invalid: Crossed Path!'
            self.trail.append([row, col - 2])
            return self.evaluateState('left')
        return 'Invalid: Out of Bounds!'
    
    def moveright(self):
        row, col = self.trail[-1]
        if col < self.getNumCols() and self.grid[row][col + 1] == 'e':
            if self.trail.count([row, col + 2]) > 0:
                return 'Invalid: Crossed Path!'
            self.trail.append([row, col + 2])
            return self.evaluateState('right')
        return 'Invalid: Out of Bounds!'





# #test
        # # testing out the class manually
test = WitnessGrid()
        # # test.makeBasic2x2()
        # # test.makeBasicNxN(3) # make 3x3 grid
        # # test.makeDottedNxN(2, 50) # make 2x2 grid where ~half of the vertices are 'required'
test.makeDottedNxN(3, 26)
print(test.grid)


        # #more
        # #Feel free to try other scenarios to see how the invalid part works.
        # test.begin()
        # step = test.step()
        # print(step)
        # while step != 'Invalid':
        #     step = test.step()
        #     print(step)
        #     if step == 'Solved!' or step == 'Finished, but missed one or more dots!':
        #         break
        # print(test.getMoves())

        #test.startBruteForce()

