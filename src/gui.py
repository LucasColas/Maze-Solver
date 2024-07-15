import random

import pygame
import numpy as np

from src.buttons import Buttons


class GUI:
    def __init__(self, cell_size=15):
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        self.cell_size = cell_size
        self.shift = int(0.1*self.height)
        
        self.grid_width = self.width//self.cell_size
        self.grid_height = self.width//self.cell_size
        self.grid = np.zeros((self.grid_width, self.grid_height))
        self.background = (255, 255, 255)
        self.buttons = Buttons(height=self.shift)
        self.n_buttons = 3
        self.buttons.add_button(x=0, y=0, width=self.width//self.n_buttons, height=self.shift, text="Generate", color=(0, 255, 0), function=self.generate)
        self.buttons.add_button(x=self.width//self.n_buttons, y=0, width=self.width//self.n_buttons, height=self.shift, text="Solve", color=(255, 0, 0), function=self.solve)
        self.buttons.add_button(x=2*self.width//self.n_buttons, y=0, width=self.width//self.n_buttons, height=self.shift, text="Clear", color=(0, 0, 255), function=self.clear)

    def solve(self):
        print("Solving")
    
    def generate(self):
        self.generate_maze()
    
    def clear(self):
        print("Clearing")
        self.grid = np.zeros((self.grid_width, self.grid_height))

    
    def draw_grid(self):
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                if self.grid[i, j] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size))
                else:
                    #print(i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, (0, 0, 0), (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size), 1)


    def draw(self):
        self.screen.fill(self.background)
        self.draw_grid()
        self.buttons.draw()
        pygame.display.flip()

    def generate_maze(self):
        self.grid = np.zeros((self.grid_height, self.grid_width))

        stack = [(0, 0)]
        visited = set()
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]

        while stack:
            x, y = stack[-1]
            visited.add((x, y))
            self.grid[x, y] = 1

            neighbors = [(x+dx, y+dy) for dx, dy in directions if 0 <= x+dx < self.grid_height and 0 <= y+dy < self.grid_width and (x+dx, y+dy) not in visited]

            if neighbors:
                nx, ny = random.choice(neighbors)
                stack.append((nx, ny))
                self.grid[nx, ny] = 1
                self.grid[(x+nx)//2, (y+ny)//2] = 1
            else:
                stack.pop()

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.buttons.check_click(pos)
            self.draw()
