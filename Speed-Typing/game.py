"""File which includes the screen class and it's properties/methods

The Screen object encapsulates all information about the screen/display of the
program. The game_loop() function is the main function of the program and keeps
running until the window is closed. This function is also called inside 
__main__.py which means that game_loop() can be run by typing

    $ python -m Speed-Typing

into the terminal once Speed-Typing is installed
"""

import os
import time as t
import typing
import pygame as pg


"""CONSTANTS"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
class Screen():
    """The screen which will display all game assets

    This screen should be instantiated only once. However, there is no
    singleton architecture built into this class yet. It might be added later
    but it would probably be redundant.

    Attributes
    ----------
    width: int
        The width of the screen
    height: int
        The height of the screen
    fullscreen: bool
        Determines if the window is in fullscreen mode or not
    fps: int
        The frames per second of the screen
    fps_clock: Clock
        Uses the Pygame Clock object to set the correct fps. The fps is set
        inside the update() method inside the Screen class
    display: Surface
        Uses the Pygame Surface object to actually create the window. The
        display mode is initially set to pygame.SCALED which automatically
        changes the resolution of the window depending on desktop size and
        scale graphics. See the Pygame docs to get a full list of display modes
    """

    def __init__(self):
        pg.init()
        self.width = 750
        self.height = 600
        self.fullscreen = False
        self.fps = 30
        self.fps_clock = pg.time.Clock()
        self.display = pg.display.set_mode(
            (self.width, self.height), pg.SCALED)

    def __del__(self):
        pg.quit()

    def background(self, rgb_vals=(0, 0, 0)):
        """Fills the background of the display with the inputted rgb values
        
        Parameters
        ----------
        rgb_vals: tuple
            Requires 3 values to properly represent the color of the 
            background. The default color is black
        """
        self.display.fill(rgb_vals)

    def update(self):
        """Updates the screen and advances to the next frame"""
        pg.display.flip()
        self.fps_clock.tick(self.fps)

    def set_mode(self, mode):
        """Sets the desired display mode
        
        A complete list of display modes can be found in the Pygame docs.
        However, only pg.FULLSCREEN and pg.SCALED are supported. Using the
        other modes can lead to very undesirable consequences
        """
        self.display = pg.display.set_mode(
            (self.width, self.height), mode)

    def toggle_fullscreen(self):
        """Switches between pg.SCALED and pg.FULLSCREEN"""
        pg.display.toggle_fullscreen()

class GUI():
    def __init__(self, screen):
        self._retrieve_font()
        self.font_size = 20
        self.width_ratio = 0.6
        self.font = pg.font.Font(self._font_location, self.font_size)
        self.text = "The quick brown fox jumped over the lazy dog."
        self.input_text = ""
        self.comp = []
        self.decomp_sentence(screen)
        #self.update(screen)

    def _retrieve_font(self):
        self._font_location_str = "assets\spacemono\SpaceMono-Regular.ttf"
        self._file_root_directory = os.path.realpath(os.path.join(
            os.path.dirname(__file__), '..'))
        self._font_location = os.path.join(
            self._file_root_directory, self._font_location_str)

    def decomp_sentence(self, screen):
        self.text_letters = list(self.text)
        self.rendered_letters = []
        self.letter_width = self.font_size * self.width_ratio
        y = 0.25 * screen.height
        for idx, letter in enumerate(self.text_letters):
            x = (screen.width / 2) + (idx - (len(self.text_letters) / 2)) \
                * self.letter_width
            letter_render = self.font.render(letter, True, WHITE)
            letter_rect = letter_render.get_rect()
            letter_rect.center = (x, y)
            self.rendered_letters.append((letter_render, letter_rect))
            screen.display.blit(letter_render, letter_rect)
        pg.display.flip()

    def compare_str(self):
        self.comp = []
        for idx, letter in enumerate(self.input_text):
            if len(self.comp) >= len(self.text):
                return self.comp
            else:
                self.comp.append(True if letter == self.text[idx] else False)
        return self.comp

    def update(self, screen):
        for idx, (letter, rect) in enumerate(self.rendered_letters):
            letter_background = letter.copy()
            if idx >= len(self.comp):
                pass
            elif self.comp[idx]:
                letter_background.fill(GREEN)
            else:
                letter_background.fill(RED)
            screen.display.blit(letter_background, rect)
            screen.display.blit(letter, rect)
        pg.display.flip()

class Timer():
    def __init__(self):
        self.start() ## TEMPORARY

    def start(self):
        self.t_start = t.perf_counter()

    def end(self):
        self.t_end = t.perf_counter()

def game_loop():
    """The main loop which is only stopped when the window is closed
    
    Game Loop Order
    ---------------
    1. The background is filled with the desired color
    2. All events are checked for and evaluated if the conditions are matched.
       Events include the window being closed and any key being pressed
    3. The screen is updated
    """
    screen = Screen()
    gui = GUI(screen)
    timer = Timer()

    run = True
    typing = True

    while run:
        screen.background()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False # Stops the game loop
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_F12 or
                    (event.key == pg.K_ESCAPE and screen.fullscreen)):
                    # If F12 is pressed or ESCAPE is pressed while window is in
                    # fullscreen mode
                    screen.fullscreen = not screen.fullscreen
                    screen.toggle_fullscreen()
                elif event.key == pg.K_BACKSPACE and typing:
                    gui.input_text = gui.input_text[:-1]
                    gui.compare_str()
                else:
                    gui.input_text = gui.input_text + event.unicode
                    gui.compare_str()
                    if len(gui.input_text) == len(gui.text):
                        timer.end()
                        print(timer.t_end - timer.t_start)
        gui.update(screen)
        screen.update()
    del screen # Causes Pygame to quit