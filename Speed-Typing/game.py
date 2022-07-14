"""File which includes the screen class and it's properties/methods"""

import pygame as pg

class Screen():

    def __init__(self):
        pg.init()
        self.width = 750
        self.height = 600
        self.run = True
        self.fullscreen = False
        self.fps = 60
        self.fps_clock = pg.time.Clock()
        self.screen = pg.display.set_mode(
            (self.width, self.height), pg.SCALED)

    def __del__(self):
        pg.quit()

    def background(self, r=0, g=0, b=0):
        self.screen.fill((0, 0, 0))

    def update(self):
        pg.display.flip()
        self.fps_clock.tick(self.fps)

    def set_mode(self, mode):
        self.screen = pg.display.set_mode(
            (self.width, self.height), mode)

    def toggle_fullscreen(self):
        pg.display.toggle_fullscreen()

def game_loop():
    screen = Screen()
    while screen.run:
        screen.background()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                screen.run = False
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_F12 or
                    (event.key == pg.K_ESCAPE and screen.fullscreen)):
                    # If F12 is pressed or ESCAPE is pressed while window is in
                    # fullscreen mode
                    screen.fullscreen = not screen.fullscreen
                    screen.toggle_fullscreen()
        screen.update()
    del screen