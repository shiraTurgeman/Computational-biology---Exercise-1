import random
import sys

import pygame

import subprocess
import pkg_resources
import os
"""
packages = {'numpy', 'pygame'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = packages - installed
if missing:
    print('Download dependencies here: ', os.getcwd())
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    """
import numpy
import pygame

class Cell:
    def __init__(self, P, skepticism_level, is_spreading, col, row, L):
        self.is_man = 1 if numpy.random.uniform(low=0.0, high=1.0, size=1) <= P else 0
        self.skepticism_level = skepticism_level
        self.x = col
        self.y = row
        self.hold_rumor = False
        self.neighbours = 0
        self.l_from_spreading = 0
        self.is_spreading = False
        self.L = L

    def spread_rumor(self, grid, cols, rows):
        if self.is_man and self.is_spreading and self.hold_rumor and self.l_from_spreading == 0:
            neighbour_positions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
            #neighbour_positions = [[-1, 0],[0, -1], [0, 1],[1, 0]]
            #print(f"point: x-{self.x}, y:{self.y}")
            #print(f"x:{self.x}, y:{self.y}, is man:{self.is_man}, hold:{self.hold_rumor}, n:{self.neighbours}, "
            #      f"is spread: {self.is_spreading}, l:{self.l_from_spreading}")
            for pos in neighbour_positions:

                try:
                    if self.x + pos[0] < 0 or self.y + pos[1] < 0 or self.x + pos[0] > cols-1 or self.y + pos[1] > rows-1:
                        continue
                    elif 0 <= self.x + pos[0] <= cols-1 and 0 <= self.y + pos[1] <= rows-1:
                        #print(self.x + pos[0], self.y + pos[1])
                        grid[self.x + pos[0]][self.y + pos[1]].neighbours += 1
                        #grid[self.x + pos[0]][self.y + pos[1]].hold_rumor = True
                        self.l_from_spreading = self.L
                except IndexError:
                    continue

        elif self.is_man and self.l_from_spreading != 0:
            self.l_from_spreading -= 1
            #self.hold_rumor = False
        #print("\n\n")

    def who_get_rumor(self, grid):
        if self.is_man and self.neighbours > 0:
            self.hold_rumor = True
            return True

    def spread_rumor_prob(self, temporary_skepticism_level):
        if temporary_skepticism_level == 1:
            return 1
        elif temporary_skepticism_level == 2:
            return numpy.random.binomial(1, 2/3)
        elif temporary_skepticism_level == 3:
            return numpy.random.binomial(1, 1/3)
        elif temporary_skepticism_level == 4:
            return 0

    def decide_if_spreading_rumor(self):
        if self.neighbours > 1 and self.skepticism_level > 1:
            self.is_spreading = self.spread_rumor_prob(self.skepticism_level - 1)
        else:
            self.is_spreading = self.spread_rumor_prob(self.skepticism_level)

    def draw(self, board, block_size):
        '''
        Draw the cell to a window
        '''

        x = self.x * block_size
        y = self.y * block_size

        r = (x, y, block_size, block_size)

        if not self.is_man:
            self.cell_color = (255, 0, 0)
        elif self.is_man and self.hold_rumor:
             self.cell_color = (255, 255, 0)
        else:
            self.cell_color = (0, 0, 0)
        pygame.draw.rect(board, self.cell_color, r)


def initialize_grid(cols, rows, P,L, skepticism_per):
    # Create array of rows of cells
    grid = []
    # Add rows of cells to the array
    for x in range(cols):
        # Create the row as a list of cells
        this_row = []
        # Add cells to the row
        for y in range(rows):
            """
            if y%10 == 0:
                skepticism_level= 2
            else:
                skepticism_level = 1
                """
            this_row.append(Cell(P=P/100,
                                 #skepticism_level=skepticism_level,
                                 skepticism_level=numpy.random.choice([1, 2, 3, 4], p=skepticism_per),
                                 is_spreading=False,
                                 col=x, row=y, L=L))
        # Add row to list of rows
        grid.append(this_row)

    """ 
    for cellrow in range(dimensions):
        for column in range(dimensions):
            print(f"cell: {cellrow, column}, level: {cells[cellrow][column].skepticism_level},"
                  f"spread_rumor: {cells[cellrow][column].spread_rumor}, is live: {cells[cellrow][column].is_living}")
    """

    rand_row, rand_col = random.randint(0, cols-1), random.randint(0, rows-1)
    while not grid[rand_row][rand_col].is_man:
        rand_row, rand_col = random.randint(0, cols-1), random.randint(0, rows-1)
    #rand_row, rand_col = 0,0
    print(rand_row, rand_col)
    grid[rand_row][rand_col].hold_rumor = True
    grid[rand_row][rand_col].is_spreading = True
    return grid

