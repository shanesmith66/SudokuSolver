# SudokuSolver
Generates a unique sudoku puzzle based on difficulty and size specified and solves it using the backtracking algorithm. GUI file and text-based version (solver.py) included. Pycharm required for the GUI. Created using TechWithTim's tutorials and modified to generate a unique board, work for different grid sizes and difficulties, and contain a main menu to specify these variables.

***Use spacebar to solve the puzzle generated and get a visualization of the algorithm***

# Backtracking Algorithm
Starting with an incomplete board:

1. Find some empty space
2. Attempt to place the digits 1-9 in that space
3. Check if that digit is valid in the current spot based on the current board
  a. If the digit is valid, recursively attempt to fill the board using steps 1-3.
  b. If it is not valid, reset the square you just filled and go back to the previous step.
4. Once the board is full by the definition of this algorithm we have found a solution.

# Important Notes
Sometimes it may appear as though the solver GUI is bugging out and stopped working, especially for the harder difficulties on the 16x16 grid. This is simply because this algorithm, while usually efficient, can rarely have an upper bound time complexity of O(9^(n*n)) but is still significantly faster than the brute force method. To get a good demonstration of how fast this algorithm is, please run solver.py which will solve the puzzle within the console.
