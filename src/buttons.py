import pygame


class Buttons:
    def __init__(self, height=200):
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 36)
        self.width = self.screen.get_width()
        self.height = height
        self.buttons = []
        self.button_texts = []
        self.functions = []
        self.colors = []
        self.animated_colors = []
        self.animations = []
        self.max_animation = 50
        
        

    def add_button(self, x, y, width, height, text, color, function):
        self.buttons.append(pygame.Rect(x, y, width, height))
        text = self.font.render(text, True, (0, 0, 0))
        text_width, text_height = text.get_size()
        pos = (x + width//2 - text_width//2, y + height//2 - text_height//2)
        self.button_texts.append((text, color, pos))
        self.functions.append(function)
        self.colors.append(color)
        self.animated_colors.append(self.darken_color(color))
        self.animations.append(0)

    def draw(self):
        for button, (text, color, pos) in zip(self.buttons, self.button_texts):

            if self.animations[self.buttons.index(button)] > 0:
                self.animations[self.buttons.index(button)] += 1
                color_to_use = self.animated_colors[self.buttons.index(button)]
                if self.animations[self.buttons.index(button)] > self.max_animation:
                    self.animations[self.buttons.index(button)] = 0
                pygame.draw.rect(self.screen, color_to_use, button)
            else:
                pygame.draw.rect(self.screen, color, button)
            self.screen.blit(text, pos)

    def darken_color(self, color):
        return tuple([max(0, c-50) for c in color])

    def animate_button(self, button):
        self.animations[self.buttons.index(button)] = 1
        
        

    def check_click(self, pos):
        for button, function in zip(self.buttons, self.functions):
            if button.collidepoint(pos):
                self.animate_button(button=button)
                function()
                return True
        return False