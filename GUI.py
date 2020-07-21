# GUI.py
import pygame
import sys
import time
from pygame.locals import *
from solver import generate_board, find_empty, valid

pygame.font.init()
pygame.init()
pygame.display.set_caption('Sudoku Solver')

SCREEN_WIDTH = 540
SCREEN_HEIGHT = 600

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fnt = pygame.font.SysFont("comicsans", 40)

menu_background = pygame.image.load('images/menubackground.png')
title_text = pygame.image.load('images/title_text.png')

global board
global n
global m

# default values to create the 9x9 grid
n = 3
m = n**2


class Grid:
    """Grid class to display a GUI grid element."""
    rows = m
    cols = m

    def __init__(self, rows, cols, width, height, win):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        """Updates the grid."""
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        """Places a specified value into the grid."""
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        """Pencils in a temporary value into the grid."""
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # Draw Grid Lines
        gap = self.width / m
        for i in range(self.rows + 1):
            if i % n == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        """clears value within a box on the grid."""
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        Function used to determine where the user clicks within the grid.
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / m
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        """Determines if the board is solved. Works like the find_empty function from solver.py but returns a boolean
        value rather than a coordinate."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve_gui(self):
        """Solves the GUI Sudoku using the backtracking algorithm and recursion. Serves same purpose as solve() in
        solver.py."""
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, m+1):
            pygame.event.get()
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(40)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(40)

        return False


class Cube:
    """Class to represent each individual cube within the sudoku grid."""
    rows = m
    cols = m

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        """Function which draws the numbers into each box."""
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / m
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), n)

    def draw_change(self, win, g=True):
        """Function to illustrate the change of value on the grid within a certain box. """
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / m
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), n)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), n)

    def set(self, val):
        """sets a value in the box"""
        self.value = val

    def set_temp(self, val):
        """sets a temporary value within the box"""
        self.temp = val


def redraw_window(win, board, time, strikes):
    """refereshes the GUI window"""
    win.fill((255, 255, 255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (SCREEN_WIDTH - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw()


def format_time(secs):
    """Formats how the time is displayed within the bottom right corner when playing the game. """
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60
    if sec < 10:
        sec = "0" + str(sec)

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    """
    Main function to run the sudoku game, including controls:
    - Click on a box to select it
    - Press a number to pencil it in
    - Press enter to submit that value
    - If Correct, number will be displayed in the box, if not, red x will be drawn along the bottom of the screen and
    the box will be cleared
    - Press SPACE to solve the puzzle.
    """
    pygame.display.set_caption("Sudoku")
    board = Grid(m, m, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        pygame.display.update()

                        if board.is_finished():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key is not None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


def draw_text(text, font, color, surface, x, y):
    """Function to draw text within the GUI"""
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def draw_menu_buttons(output_type):
    """Draws the menu buttons on the main menu of the program. Returns the options which are selected (What size,
    difficulty the user wants to play with)."""
    if output_type == 'difficulty':
        text1 = pygame.image.load('images/easy_text.png')
        easy_text_hovered = pygame.image.load("images/easy_text_hovered.png")
        text2 = pygame.image.load('images/medium_text.png')
        medium_text_hovered = pygame.image.load("images/medium_text_hovered.png")
        text3 = pygame.image.load('images/hard_text.png')
        hard_text_hovered = pygame.image.load("images/hard_text_hovered.png")

    if output_type == 'size':
        text1 = pygame.image.load("images/4x4_text.png")
        easy_text_hovered = pygame.image.load("images/4x4_text_hovered.png")
        text2 = pygame.image.load("images/9x9_text.png")
        medium_text_hovered = pygame.image.load("images/9x9_text_hovered.png")
        text3 = pygame.image.load("images/16x16_text.png")
        hard_text_hovered = pygame.image.load("images/16x16_text_hovered.png")

    click = False

    while True:

        win.fill((255, 255, 255))
        win.blit(menu_background, (-100, -100))
        win.blit(title_text, (0, 0))

        mx, my = pygame.mouse.get_pos()

        but1 = pygame.Rect(120, 125, 300, 100)
        but2 = pygame.Rect(120, 275, 300, 100)
        but3 = pygame.Rect(120, 425, 300, 100)

        win.blit(text1, but1)
        win.blit(text2, but2)
        win.blit(text3, but3)

        if but1.collidepoint((mx, my)):
            win.blit(easy_text_hovered, but1)
            if click:
                output = 'Easy'
                break
        if but2.collidepoint((mx, my)):
            win.blit(medium_text_hovered, but2)
            if click:
                output = 'Medium'
                break
        if but3.collidepoint((mx, my)):
            win.blit(hard_text_hovered, but3)
            if click:
                output = 'Hard'
                break

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        pygame.time.Clock().tick(60)

    return output


def main_menu():
    """Displays both button pairs for the main menu. Returns the size and difficulty of the board specified in order
    to generate a valid and unique sudoku board."""
    size = draw_menu_buttons('size')
    difficulty = draw_menu_buttons('difficulty')

    print(size)
    print(difficulty)

    return [size, difficulty]


board, n = generate_board(main_menu())
m = n ** 2
