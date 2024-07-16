import random
import heapq
import pygame
import numpy as np

from src.buttons import Buttons

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

class GUI:
    def __init__(self, cell_size=15):
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.background = WHITE
        
        # Grid
        self.cell_size = cell_size
        self.shift = int(0.1*self.height)
        self.grid_width = self.width//self.cell_size
        self.grid_height = self.width//self.cell_size
        self.grid = np.zeros((self.grid_width, self.grid_height))
        
        # Buttons
        self.buttons = Buttons(height=self.shift)
        self.n_buttons = 5
        
        self.buttons.add_button(x=0, y=0, width=self.width//self.n_buttons, height=self.shift, text="Generate", color=GREEN, function=self.generate)
        self.buttons.add_button(x=self.width//self.n_buttons, y=0, width=self.width//self.n_buttons, height=self.shift, text="Solve", color=RED, function=self.solve)
        self.buttons.add_button(x=2*self.width//self.n_buttons, y=0, width=self.width//self.n_buttons, height=self.shift, text="Clear path", color=BLUE, function=self.clear_path)
        self.buttons.add_button(x=3*self.width//self.n_buttons, y=0, width=self.width//self.n_buttons, height=self.shift, text="Clear walls", color=BLUE, function=self.clear_walls)
        self.buttons.add_button(x=4*self.width//self.n_buttons, y=0, width=self.width//self.n_buttons, height=self.shift, text="Clear all", color=BLUE, function=self.clear)

        # A star
        self.solution_path = []
        self.start = None
        self.goal = None
        self.explored = []

        # animation
        self.animated_speed = 0.01 # seconds
        self.current_path_drawn = 0
        self.current_explored_drawn = 0

    def clear_walls(self):
        # clear walls but keep start and goal
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                if self.grid[i, j] == 1:
                    self.grid[i, j] = 0


    def solve(self):
        if self.start and self.goal:
            
            self.solution_path = self.a_star_search(self.start, self.goal)
            
        else:
            print("Start or goal not set.")

    def clear_path(self):
        # clear everything but the walls
        self.solution_path = []
        self.explored = []
        self.current_path_drawn = 0
        self.current_explored_drawn = 0
        self.start = None
        self.goal = None

    def clear(self):
        # clear everything
        print("Clearing")
        self.grid = np.zeros((self.grid_width, self.grid_height))
        self.solution_path = []
        self.start = None
        self.goal = None
        self.explored = []
        self.current_path_drawn = 0
        self.current_explored_drawn = 0
        
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self, start, goal):
        print("Start:", start, "Goal:", goal)
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0} # cost from start to current node
        f_score = {start: self.heuristic(start, goal)} # heuristic cost from start to goal through current node
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

                    # only updates the path to a neighbor if it has found a shorter path (lower g_score) than previously known, 
                    # or if the neighbor has not been evaluated yet (not in g_score).
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current # path to neighbor
                        # update g_score and f_score
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

            self.explored.append(current)

        return []
    
    def generate(self):
        self.grid = np.ones((self.grid_width, self.grid_height)) # initialize grid with walls
        self._dfs(0,0)
        print("Maze generated")

    def _dfs(self, x, y):
        # Mark the current cell as part of the path (remove wall)
        self.grid[y, x] = 0

        # Define the order of movements (right, down, left, up)
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        np.random.shuffle(directions) 

        # Explore each direction
        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy  
            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                if self.grid[ny, nx] == 1:  # if the next cell is a wall
                    # Remove the wall between the current and next cell
                    self.grid[y + dy, x + dx] = 0
                    self._dfs(nx, ny)  # Recursively call DFS from the next cell

    
    
    def draw_grid(self):
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                if self.grid[i, j] == 1:
                    pygame.draw.rect(self.screen, BLACK, (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size))
                else:
                    
                    pygame.draw.rect(self.screen, BLACK, (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size), 1)

    def draw_path(self):
        if self.current_path_drawn < len(self.solution_path):
            for i, j in self.solution_path[:self.current_path_drawn]:
                pygame.draw.rect(self.screen, GREEN, (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size))
            self.current_path_drawn += 1
            pygame.time.wait(int(self.animated_speed*1000))
        else:
            for i, j in self.solution_path:
                pygame.draw.rect(self.screen, GREEN, (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size))
        

    def draw_explored(self):

        if self.current_explored_drawn < len(self.explored):
            for i, j in self.explored[:self.current_explored_drawn]:
                pygame.draw.rect(self.screen, RED, (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size))
            self.current_explored_drawn += 1
            pygame.time.wait(int(self.animated_speed*1000))

        else:
            for i, j in self.explored:
                pygame.draw.rect(self.screen, RED, (i*self.cell_size, j*self.cell_size+self.shift, self.cell_size, self.cell_size))
    
    def draw_start_goal(self):
        if self.start is not None:
            pygame.draw.rect(self.screen, ORANGE, (self.start[0]*self.cell_size, self.start[1]*self.cell_size+self.shift, self.cell_size, self.cell_size))
        if self.goal is not None:
            pygame.draw.rect(self.screen, PURPLE, (self.goal[0]*self.cell_size, self.goal[1]*self.cell_size+self.shift, self.cell_size, self.cell_size))
    
    def draw(self):
        self.screen.fill(self.background)
        self.draw_grid()
        self.buttons.draw()
        self.draw_explored()
        if self.current_explored_drawn == len(self.explored):
            self.draw_path()
        self.draw_start_goal()
        pygame.display.flip()

    

    

    def handle_left_click(self, pos):
        x, y = pos[0] // self.cell_size, (pos[1] - self.shift) // self.cell_size
        if self.grid[x, y] == 0:
            if self.start is None:
                self.start = (x, y)
                self.grid[x, y] = 2
            elif self.goal is None:
                self.goal = (x, y)
                self.grid[x, y] = 3
            else:
                self.grid[x, y] = 1

    def handle_right_click(self, pos):
        x, y = pos[0] // self.cell_size, (pos[1] - self.shift) // self.cell_size
        if self.grid[x, y] in {1, 2, 3}:
            self.grid[x, y] = 0
            if (x, y) == self.start:
                self.start = None
            elif (x, y) == self.goal:
                self.goal = None


    def run(self):
        run = True
        drawing = False
        erasing = False

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[1] > self.shift:
                        if event.button == 1:  # Left click
                            if not self.start or not self.goal:
                                self.handle_left_click(pos)
                            else:
                                drawing = True
                                self.handle_left_click(pos)
                        elif event.button == 3:  # Right click
                            erasing = True
                            self.handle_right_click(pos)

                    self.buttons.check_click(pos)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left click
                        drawing = False
                    if event.button == 3:  # Right click
                        erasing = False
                        
                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    if pos[1] > self.shift:
                        if drawing:
                            self.handle_left_click(pos)
                        if erasing:
                            self.handle_right_click(pos)
            self.draw()
