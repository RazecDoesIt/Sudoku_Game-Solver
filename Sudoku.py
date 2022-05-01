import collections
import copy
import sys
import pygame
import tkinter as tk
import numpy as np
import random


pygame.init()
WIDTH = 900
HEIGHT = 900
ROWS = 9
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoko")
BORDER = pygame.Rect(WIDTH // 2, 0, 10, HEIGHT)
NUMBER_FONT = pygame.font.SysFont('Arial', 60)

d = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (224, 18, 25)
COOL_COLOR = (247, 237, 210)

board = np.zeros((9, 9), dtype=int)


def create_board():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    x = 0 # row
    p = 0
    # cells ( rows first)
    while x < 9:
        y = 0 # col
        numbers_list = copy.deepcopy(numbers)
        while y < 9:
            list = []
            w = 0
            if board[x][y] == 0:
                number_selected = random.choice(numbers_list)
                while w < 9:
                    list.append(board[w][y]) # colune check
                    w += 1

                if number_selected in list:
                    new_numb_selected = 0
                    new_numb_selected = random.choice(numbers_list)
                    if new_numb_selected not in list:
                        number_selected = new_numb_selected
                    if new_numb_selected == number_selected and number_selected in list:
                        number_selected = 0
                        number_selected = random.choice(numbers_list)
                    if new_numb_selected and number_selected in list:
                        while 0 <= y < 9:
                            board[x][y] = 0
                            y -= 1
                            numbers_list = copy.deepcopy(numbers)
                            new_numb_selected = 0
                            number_selected = new_numb_selected

                if number_selected not in list and number_selected != 0:
                    board[x][y] = number_selected
                    numbers_list.remove(number_selected)

                if x == 2 + p and y == 8:
                    list_blank = np.copy(board[p:3 + p]) # sqr check
                    col1 = np.reshape(list_blank[:3, 0:3], (1, 9))
                    col1 = [item for sublist in col1 for item in sublist]
                    dupes1 = [item for item, count in collections.Counter(col1).items() if count > 1]
                    col2 = np.reshape(list_blank[:3, 3:6], (1, 9))
                    col2 = [item for sublist in col2 for item in sublist]
                    dupes2 = [item for item, count in collections.Counter(col2).items() if count > 1]
                    col3 = np.reshape(list_blank[:3, 6:9], (1, 9))
                    col3 = [item for sublist in col3 for item in sublist]
                    dupes3 = [item for item, count in collections.Counter(col3).items() if count > 1]

                    if len(dupes1) != 0 or len(dupes2) != 0 or len(dupes3) != 0:
                        while x != p:
                            y = 8
                            while 0 <= y < 9:
                                board[x][y] = 0
                                y -= 1
                                numbers_list = copy.deepcopy(numbers)
                                new_numb_selected = 0
                                number_selected = new_numb_selected
                            x -= 1
            y += 1

        if x == 2 or x == 5:
            p += 3
            col1, col2, col3 = [], [], []
        x += 1


def select_difficulty_win():
    diff = tk.Tk()
    diff.geometry('200x200')
    diff.title("Select Difficulty")
    btn1 = tk.Button(diff, text="1", command=lambda d=1: [remove_numbers(d, diff)])
    btn2 = tk.Button(diff, text="2", command=lambda d=2: [remove_numbers(d, diff)])
    btn3 = tk.Button(diff, text="3", command=lambda d=3: [remove_numbers(d, diff)])
    btn1.pack()
    btn2.pack()
    btn3.pack()
    diff.mainloop()


def remove_numbers(d, diff):
    if d == 1: # difficulty 1
        random_elements = random.randint(31, 40)
        i = 0
        while i <= random_elements:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            board[x][y] = 0
            i += 1
        diff.destroy()
    if d == 2: # difficulty 2
        random_elements = random.randint(41, 50)
        i = 0
        while i < random_elements:
            random_x = random.randint(0, 8)
            random_y = random.randint(0, 8)
            board[random_x][random_y] = 0
            i += 1
        diff.destroy()
    if d == 3: # difficulty 3
        random_elements = random.randint(51, 70)
        i = 0
        while i < random_elements:
            random_x = random.randint(0, 8)
            random_y = random.randint(0, 8)
            board[random_x][random_y] = 0
            i += 1
        diff.destroy()


def mouse_and_numb(play_board):
    pygame.mouse.set_visible(True)
    mouse = pygame.mouse.get_focused()
    mouse_click = pygame.MOUSEBUTTONDOWN
    # x_mouse, y_mouse = pygame.mouse.get_pos()
    mouse_pos = []
    while mouse:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == mouse_click:
                col = event.pos[0] // (WIDTH // ROWS)
                row = event.pos[1] // (WIDTH // ROWS)
                mouse_pos.append((col, row))
                if board[col][row] != 0:
                    pass
                else:
                    board[col][row] = 0

        for row, col in mouse_pos:
            last_pos = mouse_pos[-1]
            empty_tile_y = last_pos[0]
            empty_tile_x = last_pos[1]
            if board[empty_tile_x][empty_tile_y] == 0: #'⠀' #invis character
                pygame.draw.rect(WIN, RED, (row * (WIDTH // ROWS) + 2, col * (WIDTH // ROWS) + 2, (WIDTH // ROWS) - 2,
                                            (WIDTH // ROWS) - 2), width=5)
                pygame.display.update()
                numb = tk.Tk()
                numb.geometry('100x300')
                numb.title("Select number")
                btn1 = tk.Button(numb, text="1", command=lambda d=1: print_new_numb(d, numb, row, col, play_board))
                btn2 = tk.Button(numb, text="2", command=lambda d=2: print_new_numb(d, numb, row, col, play_board))
                btn3 = tk.Button(numb, text="3", command=lambda d=3: print_new_numb(d, numb, row, col, play_board))
                btn4 = tk.Button(numb, text="4", command=lambda d=4: print_new_numb(d, numb, row, col, play_board))
                btn5 = tk.Button(numb, text="5", command=lambda d=5: print_new_numb(d, numb, row, col, play_board))
                btn6 = tk.Button(numb, text="6", command=lambda d=6: print_new_numb(d, numb, row, col, play_board))
                btn7 = tk.Button(numb, text="7", command=lambda d=7: print_new_numb(d, numb, row, col, play_board))
                btn8 = tk.Button(numb, text="8", command=lambda d=8: print_new_numb(d, numb, row, col, play_board))
                btn9 = tk.Button(numb, text="9", command=lambda d=9: print_new_numb(d, numb, row, col, play_board))
                btn10 = tk.Button(numb, text="Apagar", command=lambda d=0: print_new_numb(d, numb, row, col, play_board))
                btn11 = tk.Button(numb, text="Checar", command=lambda d=99: check_board(play_board))
                btn1.pack()
                btn2.pack()
                btn3.pack()
                btn4.pack()
                btn5.pack()
                btn6.pack()
                btn7.pack()
                btn8.pack()
                btn9.pack()
                btn10.pack()
                btn11.pack()
                tk.mainloop()
                pygame.draw.rect(WIN, BLACK, (row * (WIDTH // ROWS) + 2, col * (WIDTH // ROWS) + 2, (WIDTH // ROWS) - 2,
                                            (WIDTH // ROWS) - 2), width=5)

                mouse_pos.pop()

                if board[empty_tile_x][empty_tile_y] != 0:
                    numb.destroy()
                    pygame.draw.rect(WIN, COOL_COLOR,
                                 (row * (WIDTH // ROWS) + 2, col * (WIDTH // ROWS) + 2, (WIDTH // ROWS) - 2,
                                  (WIDTH // ROWS) - 2), width=5)
                    pygame.display.update()


def print_new_numb(d, numb, row, col, play_board):
    empty_board = play_board
    offset = 40
    if empty_board[col][row] == 0:
        empty_board[col][row] = d
        sudoku_challenge = d
        numb_text = NUMBER_FONT.render(str(sudoku_challenge), True, BLACK)
        WIN.blit(numb_text, ((row * 100 + offset), (col * 100 + offset / 2)))
        pygame.display.update()
        if empty_board[col][row] == d:
            numb.destroy()
    if d == 0:
        empty_board[col][row] = 0
        pygame.draw.rect(WIN, COOL_COLOR,
                         (row * (WIDTH // ROWS) + 2, col * (WIDTH // ROWS) + 2, (WIDTH // ROWS) - 2,
                          (WIDTH // ROWS) - 2), width=0)
        pygame.display.update()


def check_board(play_board):
    wrong = 0
    final_board = np.copy(play_board)
    col = 0
    p = 0
    while col < 9:
        row = 0
        while row < 9:
            row_array = np.reshape(final_board[row][:9], (1, 9))
            row1 = row_array.tolist()
            row_flat = [item for sublist in row1 for item in sublist]
            row_sum = sum(row_flat)
            if row_sum != 45: # every row, col, and sqr must sum 45 (sum 1 to 9)
                wrong += 1
                break
            else:
                row += 1

        col_array = np.reshape(final_board[:9][col], (1, 9))
        col1 = col_array.tolist()
        col_flat = [item for sublist in col1 for item in sublist]
        col_sum = sum(col_flat)
        if col_sum != 45:
            wrong += 1
            break
        else:
            col += 1

        if col == 2 + p and row == 8:
            list_blank = np.copy(final_board[p:3 + p])
            sqr1 = np.reshape(list_blank[:3, 0:3], (1, 9))
            sqr1 = [item for sublist in sqr1 for item in sublist]
            dupes_sqr1 = [item for item, count in collections.Counter(sqr1).items() if count > 1]
            sqr2 = np.reshape(list_blank[:3, 3:6], (1, 9))
            sqr2 = [item for sublist in sqr1 for item in sublist]
            dupes_sqr2 = [item for item, count in collections.Counter(sqr2).items() if count > 1]
            sqr3 = np.reshape(list_blank[:3, 6:9], (1, 9))
            sqr3 = [item for sublist in sqr1 for item in sublist]
            dupes_sqr3 = [item for item, count in collections.Counter(sqr3).items() if count > 1]

            if len(dupes_sqr1) != 0 or len(dupes_sqr2) != 0 or len(dupes_sqr3) != 0:
                wrong += 1

    if wrong != 0:
        print(f"better luck next time pal' :)")

    elif wrong == 0:
        print('you won :)')
        pygame.time.wait(1000000)
        pygame.quit()
        sys.exit()


def draw_grid():
    pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.fill(COOL_COLOR)
    space_btwn = WIDTH // ROWS
    x, y = 0, 0

    for i in range(ROWS):
        x += space_btwn
        y += space_btwn
        thickness = 10 if x % 3 == 0 else 3
        pygame.draw.line(WIN, BLACK, (x, 0), (x, WIDTH), thickness)
        pygame.draw.line(WIN, BLACK, (0, y), (HEIGHT, y), thickness)
        i += 1
    pygame.display.update()


def draw_numbers():
    row = 0
    while row < 9:
        offset = 40
        col = 0
        while col < 9:
            if board[row][col] != 0:
                sudoku_challenge = board[row][col]
                numb_text = NUMBER_FONT.render(str(sudoku_challenge), True, BLACK)
                WIN.blit(numb_text, ((col * 100 + offset), (row * 100 + offset / 2)))
            elif board[row][col] == '⠀': # empty character between ''
                sudoku_challenge = 0
                numb_text = NUMBER_FONT.render(str(sudoku_challenge), True, BLACK)
                WIN.blit(numb_text, ((col * 100 + offset), (row * 100 + offset / 2)))
            col += 1
        row += 1


if __name__ == '__main__':
    draw_grid()
    create_board()
    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if i <= 0:
            select_difficulty_win()
            i += 1
        draw_numbers()
        play_board = np.copy(board)
        empty_board = np.copy(play_board)
        mouse_and_numb(play_board)
        pygame.display.update()




