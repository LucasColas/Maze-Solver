import pygame
from src.gui import GUI

# Initialize the game
pygame.init()

def main():
    HEIGHT = 750
    WIDTH = 675
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Solver")
    gui = GUI()
    gui.run()

if __name__ == "__main__":
    main()