# SudokuSolver
Generates a unique sudoku puzzle based on difficulty and size specified and solves it using the backtracking algorithm. GUI file and text-based version (solver.py) included. Pycharm required for the GUI. Created using TechWithTim's tutorials and modified to generate a unique board, work for different grid sizes and difficulties, and contain a main menu to specify these variables.

# Backtracking Algorithm
Starting with an incomplete board:

1. Find some empty space
2. Attempt to place the digits 1-9 in that space
3. Check if that digit is valid in the current spot based on the current board
  a. If the digit is valid, recursively attempt to fill the board using steps 1-3.
  b. If it is not valid, reset the square you just filled and go back to the previous step.
4. Once the board is full by the definition of this algorithm we have found a solution.
