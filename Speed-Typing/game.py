"""File which includes the screen class and it's properties/methods

The Screen object encapsulates all information about the screen/display of the
program. The game_loop() function is the main function of the program and keeps
running until the window is closed. This function is also called inside 
__main__.py which means that game_loop() can be run by typing

    $ python -m Speed-Typing

into the terminal once Speed-Typing is installed
"""

import pygame as pg

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
        screen.update()
    del screen # Causes Pygame to quit