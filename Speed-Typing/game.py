"""File which includes the screen class and it's properties/methods"""

import pygame

class Screen():

    def __init__(self):
        pygame.init()
        self.width = 750
        self.height = 600
        self.run = True
        self.fullscreen = False
        self.fps = 60
        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.SCALED)

    def __del__(self):
        pygame.quit()

    def background(self, r=0, g=0, b=0):
        self.screen.fill((0, 0, 0))

    def update(self):
        pygame.display.flip()
        self.fps_clock.tick(self.fps)

    def toggle_fullscreen():
        pygame.display.toggle_fullscreen()

def game_loop():
    screen = Screen()
    while screen.run:
        screen.background()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    screen.fullscreen = not screen.fullscreen
                    screen.toggle_fullscreen()
        screen.update()
    del screen