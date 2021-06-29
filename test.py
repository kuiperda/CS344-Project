#!/usr/bin/env python3

# run this file in its directory with './test.py'

import puzzle

# Manual Testing
''' Note: Save any data you want to keep before running this as 
    previous puzzle data will be deleted by the constructor!'''
test = puzzle.WitnessPuzzle()

test.makeDottedSquaresNxN(3, 25, 33, 33)
test.startBruteForceSolution()

# test.useMyGrid()
# test.startBruteForceSolution()

test.assignHeuristics('./puzzle0')