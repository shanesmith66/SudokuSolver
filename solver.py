# solver.py
import random


def make_board(bo):
    """Has the same functionality as the solve function (using the backtracking algorithm) but with an element of
    randomness in order to generate a unique board each time."""
    possible_answers = [_ for _ in range(1, m+1)]
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    random.shuffle(possible_answers)  # randomizes the first number being placed in order to create a unique board

    for i in possible_answers:
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if make_board(bo):
                return True

            bo[row][col] = 0

    return False


def solve(bo):
    """solve function which uses the backtracking algorithm and recursion in order to solve the sudoku puzzle"""
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, m+1):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    """function which checks whether a number already exists in the same row, column or square
    which would violate the rules of sudoku"""

    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Checks square
    box_x = pos[1] // n
    box_y = pos[0] // n

    for i in range(box_y * n, box_y * n + n):
        for j in range(box_x * n, box_x * n + n):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(bo):
    """Prints the puzzle board in a clean layout within the console. Only used in the text-version of this game."""
    for i in range(len(bo)):
        if i % n == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % n == 0 and j != 0:
                print(" | ", end="")

            if j == m-1:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty(bo):
    """Returns the first empty square it finds or None, which would indicate that the sudoku has been fully solved."""
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j  # return row, column

    return None


def count_squares(bo):
    """Returns the total amount of filled-in squares within the puzzle. Used when removing numbers in generate_board()
    in order to create a valid sudoku board"""
    count = 0
    for box in bo:
        for num in box:
            if num != 0:
                count += 1

    return count


def generate_board(diff):
    """generates a board with one unique solution based on size and difficulty specified"""
    global n, m  # defines the rows(m = n^2), for a 9x9 board(medium), n = 3
    size, diff = diff[0], diff[1]

    small_difficulty_levels = {"Easy": 10, "Medium": 7, "Hard": 4}
    medium_difficulty_levels = {"Easy": 35, "Medium": 30, "Hard": 24}
    large_difficulty_levels = {"Easy": 150, "Medium": 110, "Hard": 83}

    if size == 'Easy':
        n = 2
        difficulty = small_difficulty_levels[diff]
    elif size == 'Medium':
        n = 3
        difficulty = medium_difficulty_levels[diff]
    elif size == 'Hard':
        n = 4
        difficulty = large_difficulty_levels[diff]

    m = n ** 2

    empty_board = [[0 for _ in range(m)] for _ in range(m)]  # initialize empty board w/ 0's

    make_board(empty_board)  # fill board with random valid numbers
    while count_squares(empty_board) > difficulty:  # remove numbers from the board so long as it remains valid
        x = random.randint(0, m-1)
        y = random.randint(0, m-1)
        if valid(empty_board, empty_board[x][y], (x, y)):
            empty_board[x][y] = 0

    return empty_board, n


# some code to demonstrate the text-based version of the program within the console.
# board = generate_board(["Medium", "Hard"])[0]

# print_board(board)
# print("\n\nSolved Board: \n")
# solve(board)
# print_board(board)
