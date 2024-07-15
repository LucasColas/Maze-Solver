import random
import heapq
import pygame
import numpy as np

from src.buttons import Buttons


class GUI:
    def __init__(self, cell_size=15):
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.background = (255, 255, 255)
        
        # Grid
        self.cell_size = cell_size
        self.shift = int(0.1*self.height)
        self.grid_width = self.width//self.cell_size
        self.grid_height = self.width//self.cell_size
        self.grid = np.zeros((self.grid_width, self.grid_height))
        
        # Buttons
        self.buttons = Buttons(height=self.shift)
        self.n_buttons = 3
        self.buttons.add_button(x=0, y=0, width=self.width//self.n_buttons, height=self.shift, text="Generate", color=(0, 255, 0), function=self.generate)
        self.buttons.add_button(x=self.width//self.n_buttons, y=0, width=self.width//self.n_buttons, height=self.shift, text="Solve", color=(255, 0, 0), function=self.solve)
        self.buttons.add_button(x=2*self.width//self.n_buttons, y=0, width=self.width//self.n_buttons, height=self.shift, text="Clear", color=(0, 0, 255), function=self.clear)

        # A star
        self.solution_path = []
        self.start = None
        self.goal = None
        self.explored = []

        # animation
        self.animated_speed = 0.01 # seconds
        self.current_path_drawn = 0
        self.current_explored_drawn = 0

    def solve(self):
        if self.start and self.goal:
            print("Solving")
            self.solution_path = self.a_star_search(self.start, self.goal)
            print(self.explored)
        else:
            print("Start or goal not set.")
        
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self, start, goal):
        print("Start:", start, "Goal:", goal)
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        visited = set()


        while open_set:
            current = heapq.heappop(open_set)[1]
            visited.add(current)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if 0 <= neighbor[0] < self.grid_width and 0 <= neighbor[1] < self.grid_height:
                    if self.grid[neighbor[0], neighbor[1]] == 1 or neighbor in visited:
                        continue
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

            self.explored.append(current)




        return []
    
    def generate(self):
        self.generate_maze()
    
    def clear(self):
        print("Clearing")
        self.grid = np.zeros((self.grid_width, self.grid_height))
        self.solution_path = []
        self.start = None
        self.goal = None

    
    def draw_grid(self):
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                if self.grid[i, j] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size))
                else:
                    #print(i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, (0, 0, 0), (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size), 1)

    def draw_path(self):
        if self.current_path_drawn < len(self.solution_path):
            for i, j in self.solution_path[:self.current_path_drawn]:
                pygame.draw.rect(self.screen, (0, 255, 0), (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size))
            self.current_path_drawn += 1
            pygame.time.wait(int(self.animated_speed*1000))
        else:
            for i, j in self.solution_path:
                pygame.draw.rect(self.screen, (0, 255, 0), (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size))
        


    def draw_explored(self):

        if self.current_explored_drawn < len(self.explored):
            for i, j in self.explored[:self.current_explored_drawn]:
                pygame.draw.rect(self.screen, (255, 0, 0), (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size))
            self.current_explored_drawn += 1
            pygame.time.wait(int(self.animated_speed*1000))
        else:
            for i, j in self.explored:
                pygame.draw.rect(self.screen, (255, 0, 0), (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size))
    
    def draw_start_goal(self):
        if self.start is not None:
            pygame.draw.rect(self.screen, (0, 0, 255), (self.start[0]*self.cell_size, self.start[1]*self.cell_size+self.shift, self.cell_size, self.cell_size))
        if self.goal is not None:
            pygame.draw.rect(self.screen, (0, 0, 255), (self.goal[0]*self.cell_size, self.goal[1]*self.cell_size+self.shift, self.cell_size, self.cell_size))
    
    def draw(self):
        self.screen.fill(self.background)
        self.draw_grid()
        self.buttons.draw()
        #if self.current_path_drawn < len(self.solution_path):
            #self.draw_explored(self.solution_path)
        self.draw_explored()
        if self.current_explored_drawn == len(self.explored):
            self.draw_path()
        self.draw_start_goal()
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
                    if pos[1] > self.shift:
                        x,y = pos[0]//self.cell_size, (pos[1]-self.shift)//self.cell_size
                        if self.grid[x, y] == 0:
                            if self.start is None:
                                self.start = (x, y)
                                self.grid[x, y] = 2
                            elif self.goal is None:
                                self.goal = (x, y)
                                self.grid[x, y] = 3
                            else:
                                self.grid[x, y] = 1
            self.draw()