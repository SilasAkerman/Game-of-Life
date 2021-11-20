from hashlib import new
import pygame
import sys

class Board:
    SPACING = 10
    FPS = 0
    SQUARE_PROXIMITY = (
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1)
    )

    def __init__(self, win):
        self.win = win
    
    def init_board(self):
        self.rows = self.win.get_height() // self.SPACING
        self.cols = self.win.get_width() // self.SPACING
        self.board = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.buffer_board = [[False for _ in range(self.cols)] for _ in range(self.rows)]
    
    def display(self):
        self.win.fill((0, 0, 0))
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col]:
                    self.display_square(row, col)
        if self.grid:
            self.display_grid()
        pygame.display.update()

    def display_grid(self):
        for col in range(self.cols + 1):
            pygame.draw.line(self.win, (100, 100, 100), (col*self.SPACING, 0), (col*self.SPACING, self.win.get_height()), int(self.SPACING*0.1))
        for row in range(self.rows + 1):
            pygame.draw.line(self.win, (100, 100, 100), (0, row*self.SPACING), (self.win.get_width(), row*self.SPACING), int(self.SPACING*0.1))

    def display_square(self, row, col):
        pos_x = col * self.SPACING
        pos_y = row * self.SPACING
        pygame.draw.rect(self.win, (255, 255, 255), (pos_x, pos_y, self.SPACING, self.SPACING))

    def run(self):
        self.grid = False
        self.init_board()
        self.Clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self.Clock.tick(self.FPS)
            self.check_events()
            self.display()
            self.evaluate_board()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.square_from_mouse()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paus()
                if event.key == pygame.K_g:
                    self.grid = not self.grid

    def paus(self):
        paus = True
        while paus:
            self.Clock.tick(self.FPS)
            self.display()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.square_from_mouse()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paus = False
                    if event.key == pygame.K_g:
                        self.grid = not self.grid
            

    def evaluate_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.evaluate_square(row, col)
        self.board = self.buffer_board
        self.buffer_board = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def change_square(self, row, col, buffer=False):
        if buffer:
            self.buffer_board[row][col] = not self.buffer_board[row][col]
        else:
            self.board[row][col] = not self.board[row][col]

    def evaluate_square(self, row, col):
        count = self.count_around_square(row, col)
        if count == 2 and self.board[row][col]:
            self.buffer_board[row][col] = True
        if count == 3:
            self.buffer_board[row][col] = True

    def count_around_square(self, row, col):
        count = 0
        for proximity in self.SQUARE_PROXIMITY:
            new_row = row + proximity[0]
            new_col = col + proximity[1]
            
            if new_row < 0:
                # new_row = self.rows - 1
                return
            if new_row >= self.rows:
                # new_row = 0
                return
            if new_col < 0:
                # new_col = self.cols - 1
                return
            if new_col >= self.cols:
                # new_col = 0
                return

            if self.board[new_row][new_col]:
                count += 1
        return count


    def square_from_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1] // self.SPACING
        col = mouse_pos[0] // self.SPACING
        if not (row < 0 or row >= self.rows or col < 0 or col >= self.cols):
            self.change_square(row, col)




def main():
    pygame.init()
    WIN = pygame.display.set_mode((1300, 750))
    Life = Board(WIN)
    Life.run()


if __name__ == "__main__":
    main()