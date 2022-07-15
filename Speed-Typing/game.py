"""File which includes the screen class and it's properties/methods

The Screen object encapsulates all information about the screen/display of the
program. The game_loop() function is the main function of the program and keeps
running until the window is closed. This function is also called inside 
__main__.py which means that game_loop() can be run by typing

    $ python -m Speed-Typing

into the terminal once Speed-Typing is installed
"""

import pygame as pg
import os

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
        self.run = True
        self.fullscreen = False
        self.fps = 60
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
        self.font = pg.font.Font(self._font_location, 20)
        self.text = self.font.render(
            "The example sentence goes here.", True, (255, 255, 255)) # White
        self.text_rect = self.text.get_rect(
            center=(0.5*screen.width, 0.25*screen.height))
        self.update(screen)

    def _retrieve_font(self):
        self._font_location_str = "assets\spacemono\SpaceMono-Regular.ttf"
        self._file_root_directory = os.path.realpath(os.path.join(
            os.path.dirname(__file__), '..'))
        self._font_location = os.path.join(
            self._file_root_directory, self._font_location_str)

    def update(self, screen):
        screen.display.blit(self.text, self.text_rect)
        pg.display.flip()

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
    while screen.run:
        screen.background()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                screen.run = False # Stops the game loop
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_F12 or
                    (event.key == pg.K_ESCAPE and screen.fullscreen)):
                    # If F12 is pressed or ESCAPE is pressed while window is in
                    # fullscreen mode
                    screen.fullscreen = not screen.fullscreen
                    screen.toggle_fullscreen()
        gui.update(screen)
        screen.update()
    del screen # Causes Pygame to quit