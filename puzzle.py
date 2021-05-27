#!/usr/bin/env python3

import random
import copy
from PIL import Image, ImageDraw
import os

# run with ./puzzle.py

#TODO: clean up existing code and optimize it
#TODO: add comments and documentation

#note: unfinished currently includes both uncompleted paths and uncompleteable paths

#still have to manually delete data from previous brute force attemtps when you reset class


class WitnessPuzzle: 
    """ Generate puzzles from The Witness!
        - Assume typical NxN with all vertices present
        - Assume start at bottom left and end at top left
    """
    def __init__(self):
        self.grid = []
        self.trail = []
        self.moves = []
        self.imageNum = 0
        self.puzzleNum = 0

    # Basic puzzle, just draw a path to the end to solve it
    def makeBasicNxN(self, n):
        if n < 1:
            print("Problem: Make sure to use n >= 1 with makeBasicNxN()")
            return
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
        
    # Simple puzzle, path has to cover all required vertices, marked by an X
    def makeDottedNxN(self, n, percent):
        if(percent < 0 or percent > 100):
            print("Problem: Make sure to use 0 < percent < 100 with makeBasicDottedNxN()")
            return
        self.makeBasicNxN(n)
        for x in range(len(self.grid)):
            if x % 2 == 0:
                for y in range(len(self.grid[x])):
                    if self.grid[x][y] == 'v' and random.randint(1,100) <= percent:
                        self.grid[x][y] = 'X'
        return self.grid

    # Simple puzzle, path has to separate squares of different colors
    #TODO: colored square puzzles

    # Manually try to solve a puzzle
    def playPuzzle(self):
        if(len(self.grid) < 3):
            print("Problem: Make sure to create a puzzle before trying playPuzzle()")
            return
        self.trail = [[len(self.grid) - 1, 0]]
        self.moves = []

        state = "Unfinished"
        while(state == "Unfinished"):
            choice = input("Type w,a,s,d for up/left/down/right: ")
            if choice == 'w':
                action = self.moveup()
            elif choice == 'a':
                action = self.moveleft()
            elif choice == 's':
                action = self.movedown()
            elif choice == 'd':
                action = self.moveright()
            else:
                print("Problem: Make sure to choose w/a/s/d in playPuzzle()")
                return
            print(action)
            if action == "Solved" or action == "Finished" or action[0:7] == "Invalid":
                break

    # Movement
    def moveup(self):
        row, col = self.trail[-1]
        if row > 0 and self.grid[row - 1][col] == 'e':
            if self.trail.count([row - 2, col]) > 0:
                return 'Invalid: Crossed Path!'
            self.trail.append([row - 2, col])
            self.moves.append('up')
            return self.checkIfDone()
        return 'Invalid: Out of Bounds!'
    def movedown(self):
        row, col = self.trail[-1]
        if row < len(self.grid) - 1 and self.grid[row + 1][col] == 'e':
            if self.trail.count([row + 2, col]) > 0:
                return 'Invalid: Crossed Path!'
            self.trail.append([row + 2, col])
            self.moves.append('down')
            return self.checkIfDone()
        return 'Invalid: Out of Bounds!'
    def moveleft(self):
        row, col = self.trail[-1]
        if col > 0 and self.grid[row][col-1] == 'e':
            if self.trail.count([row, col - 2]) > 0:
                return 'Invalid: Crossed Path!'
            self.trail.append([row, col - 2])
            self.moves.append('left')
            return self.checkIfDone()
        return 'Invalid: Out of Bounds!'
    def moveright(self):
        row, col = self.trail[-1]
        if col < len(self.grid) - 1 and self.grid[row][col + 1] == 'e':
            if self.trail.count([row, col + 2]) > 0:
                return 'Invalid: Crossed Path!'
            self.trail.append([row, col + 2])
            self.moves.append('right')
            return self.checkIfDone()
        return 'Invalid: Out of Bounds!'

    # After moving, check if the end was reached and if the puzzle was solved
    def checkIfDone(self):
        row, col = self.trail[-1]

        if self.grid[row][col] == 'f':
            gotEveryDot = True
            for x in range(len(self.grid)):
                if gotEveryDot == False: break
                if x % 2 == 0:
                    for y in range(len(self.grid[x])):
                        if self.grid[x][y] == 'X':
                            if [x, y] not in self.trail:
                                gotEveryDot = False
                                break
            if gotEveryDot == True:
                return 'Solved'
            else:
                return 'Finished'
        else:
            return self.moves

    def startBruteForceSolution(self):
        if(len(self.grid) < 3):
            print("Problem: Make sure to create a puzzle before trying startBruteForceSolution()")
            return
        self.trail = [[len(self.grid) - 1, 0]]
        self.moves = []
        self.bruteForceStep('up')
        self.bruteForceStep('left')
        self.bruteForceStep('down')
        self.bruteForceStep('right')
        
        self.puzzleNum += 1
        return 'Brute Force Done!'
        
    def bruteForceStep(self, direction):
        if direction == 'up':
            result = self.moveup()
        elif direction == 'left':
            result = self.moveleft() 
        elif direction == 'down':
            result = self.movedown()
        elif direction == 'right':
            result = self.moveright()

        if result[0:7] == 'Invalid':
            return

        gridToSend = copy.deepcopy(self.grid)
        head = [len(gridToSend[0]) - 1, 0]
        for move in self.moves:
            if move == 'up':
                head[0] -= 1
                gridToSend[head[0]][head[1]] = 'u'
                head[0] -= 1
            elif move == 'left':
                head[1] -= 1
                gridToSend[head[0]][head[1]] = 'l'
                head[1] -= 1
            elif move == 'down':
                head[0] += 1
                gridToSend[head[0]][head[1]] = 'd'
                head[0] += 1
            elif move == 'right':
                head[1] += 1
                gridToSend[head[0]][head[1]] = 'r'
                head[1] += 1
            else:
                print("Error inscribing path in bruteForceStep()")

        if result == 'Solved':
            gridToSend[0][len(gridToSend) - 1] = 'S'
            self.writeGrid(gridToSend)
        elif result == 'Finished':
            gridToSend[0][len(gridToSend) - 1] = 'F'
            self.writeGrid(gridToSend)
        else:
            self.writeGrid(gridToSend)
            
            self.bruteForceStep('up')
            self.bruteForceStep('right')
            self.bruteForceStep('down')
            self.bruteForceStep('left')
            
        self.moves.pop()
        self.trail.pop()

    def writeGrid(self, grid):
        # print(grid[0][-1])

        solved = False
        finished = False
    
        dim = len(grid[0])
        pxSize = 100
        w = dim * pxSize
        h = dim * pxSize

        img  = Image.new( mode = "RGB", size = (w, h) )
        draw = ImageDraw.Draw(img)
        
        for x in range(dim):
            for y in range(dim):
                
                char = grid[y][x]
                if char == 'v': # vertices are grey
                    fillcolor = '#808080'
                elif char == 'X': # required vertices are purple
                    fillcolor = '#800080'
                elif char == 'e': # untouched edge is white
                    fillcolor = '#FFFFFF'
                elif char == ' ': # space is black
                    fillcolor = '#000000'
                    
                elif char == 'u': # all are blue (drawing path)
                    fillcolor = '#0000FF'
                elif char == 'd': 
                    fillcolor = '#0000FF'
                elif char == 'l': 
                    fillcolor = '#0000FF'
                elif char == 'r': 
                    fillcolor = '#0000FF'
                    
                elif char == 'b': # begin is darkkhaki
                    fillcolor = '#BDB76B'
                elif char == 'f': # finish is silver
                    fillcolor = '#C0C0C0'
                elif char == 'S': # solved is silver
                    fillcolor = '#C0C0C0'
                    solved = True
                elif char == 'F': # finished is silver
                    fillcolor = '#C0C0C0'
                    finished = True
                
                draw.rectangle((0 + x * pxSize, 0 + y * pxSize, x * pxSize + w / dim, y * pxSize + h / dim), fill=fillcolor)

        imgfilename = './puzzle'+str(self.puzzleNum)+'/'
        if solved == True:
            imgfilename += 'solved/'
        elif finished == True:
            imgfilename += 'finished/'
        else:
            imgfilename += 'unfinished/'

        if not os.path.exists(imgfilename):
            os.makedirs(imgfilename)
        imgfilename += '/grid'+str(self.imageNum)+'.png'
            
        self.imageNum += 1
        
        img.save(imgfilename)

# Manual Testing
test = WitnessPuzzle()

print(test.makeBasicNxN(1))
test.startBruteForceSolution()

# print(test.makeDottedNxN(1, 0))
# test.startBruteForceSolution()

# print(test.makeDottedNxN(1, 50))
# test.startBruteForceSolution()

# print(test.makeDottedNxN(1, 100))
# test.startBruteForceSolution()
