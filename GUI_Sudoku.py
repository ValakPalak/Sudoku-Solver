import pygame
import time

pygame.font.init()


class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]



    def change_sudoku(self,bo,rows, cols):
        for i in range(rows):
            for j in range(cols):
                self.board[i][j] = bo[i][j]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.win = win
        self.model = None
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        # cubes are what we see on window or user interface
        self.selected = None
        self.update_model()

    def update_model(self):
        self.model = [[(self.cubes[i][j].value) for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):  # set the permanent value entered in the selected box if it is correct
        row, col = self.selected

        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

        if valid(self.model, val, (row, col)) and self.solve():
            return True
        else:
            self.cubes[row][col].set(0)
            self.cubes[row][col].set_temp(0)
            self.update_model()
            return False

    def sketch(self, val):  # set temporary value in cell, value when  player has not pressed enter
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    # drawing grid structure
    def draw(self):
        gap = self.width / 9

        for i in range(self.rows + 1):

            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1

            # drawing grid lines: arguments -> surface, color, start point, end point, thickness
            # horizontal grid lines
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            # vertical grid lines
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # draw cubes i.e. put values in cube

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # for selected cell
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):  # clears a cell
        row, col = self.selected

        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):

            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                #self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

        return False

    def quick_solve(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):

            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.update_model()

                if self.quick_solve():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()

        return False



class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.temp = 0
        self.width = width
        self.height = height
        self.selected = False

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

    def draw(self, win):
        # win is sudoku surface
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9  # width of each column in our gui box
        x = gap * self.col
        y = gap * self.row

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))  # text, antialias, color
            win.blit(text, (x + 5, y + 5))  # draw image on screen at given position

        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))  # text, antialias, color
            win.blit(text, (x + (gap / 2 - text.get_width() / 2),
                            y + (gap / 2 - text.get_height() / 2)))  # draw image on screen at given position

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap),
                         0)  # drawing rectangle: (arguments) surface, color, (top corner, width, height), thickness

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def redraw_window(win, board, time, strikes):
    win.fill((255, 255, 255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 30)
    text = fnt.render("Time: " + format_time(time), 1, (255, 0, 0))
    win.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # developer
    fnt = pygame.font.SysFont("comicsans", 20)
    text = fnt.render("Made By Palak", 1, (0, 0, 255))
    win.blit(text, (270 - text.get_width() / 2, 580))

    # Draw grid and board
    board.draw()


def format_time(secs):
    sec = secs % 60
    minutes = secs // 60  # interger division
    hours = minutes // 60

    mat = " " + str(minutes) + ":" + str(sec)
    return mat


def random_valid_sudoku(): #we can make a random generator
    #to avoid unneccesaary cluttering I am just having a list
    #of 3 sudoku

    #print(bo)
    brd = bo[0]
    bo[0] = bo[1]
    bo[1] = bo[2] #rotate the list
    bo[2] = brd
    #print("******************")
    #print(bo)
    return brd


def main():
    win = pygame.display.set_mode((540, 600))  # drawing sudoku board
    pygame.display.set_caption("Sudoku")  # caption of box
    board = Grid(9, 9, 540, 540, win)  # variable of Grid
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():  # event is keypress
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0: #to get another sudoku
                    bo = random_valid_sudoku()
                    #print(bo)
                    board.change_sudoku(bo, 9, 9)
                    board = Grid(9, 9, 540, 540, win)  # variable of Grid
                    key = None
                    run = True
                    start = time.time()
                    strikes = 0

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
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:  # clearing value from a cell
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:  # solving whole sudoku all together
                    board.solve_gui()

                if event.key == pygame.K_q: #quick solve
                    board.quick_solve() #without showing steps


                if event.key == pygame.K_RETURN:  # entering value in cell
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):  # checking if it is correct value for cell
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1  # not correct increasing strikes
                        key = None

                        if board.is_finished():  # checking whether board is finished
                            print("Game over")


            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # getting mouse position
                clicked = board.click(pos)  # checking if it is a valid position
                if clicked:  # if valid, change value of selected function
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:  # board is selected then add key to cell,if key is not none
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)  # redraw board
        pygame.display.update()  # show updates


bo = [

        [
            [3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0]
        ],



        [
        [7, 2, 3, 0, 0, 0, 1, 5, 9],
        [6, 0, 0, 3, 0, 2, 0, 0, 8],
        [8, 0, 0, 0, 1, 0, 0, 0, 2],
        [0, 7, 0, 6, 5, 4, 0, 2, 0],
        [0, 0, 4, 2, 0, 7, 3, 0, 0],
        [0, 5, 0, 9, 3, 1, 0, 4, 0],
        [5, 0, 0, 0, 7, 0, 0, 0, 3],
        [4, 0, 0, 1, 0, 3, 0, 0, 6],
        [9, 3, 2, 0, 0, 0, 7, 1, 4]
    ],





          [
              [7, 8, 0, 4, 0, 0, 1, 2, 0],
              [6, 0, 0, 0, 7, 5, 0, 0, 9],
              [0, 0, 0, 6, 0, 1, 0, 7, 8],
              [0, 0, 7, 0, 4, 0, 2, 6, 0],
              [0, 0, 1, 0, 5, 0, 9, 3, 0],
              [9, 0, 4, 0, 6, 0, 0, 0, 5],
              [0, 7, 0, 3, 0, 0, 0, 1, 2],
              [1, 2, 0, 0, 0, 7, 4, 0, 0],
              [0, 4, 9, 2, 0, 6, 0, 0, 7]
          ]





]



main()
pygame.quit()
