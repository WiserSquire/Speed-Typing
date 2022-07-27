import os
import time as t
import random as r
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
        Uses the Pygame Surface object to create the window. The display mode 
        is initially set to pygame.SCALED which automatically changes the 
        resolution of the window depending on desktop size and scale graphics. 
        See the Pygame docs to get a full list of display modes.
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
        pg.quit() # Close the screen

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
    """The objects and assets drawn onto the screen

    Like the screen, only one instance of this GUI should be active. This class
    is responsible for rendering all of the letters and sentences. This
    includes the sentence that should be typed, the statistics, and the
    instructions to reset the sentence and type a new one. The font used is
    Space Mono. This font is monospaced, which means that each letter is the
    same width. This was done to simplify the sentence rendering method.

    Attributes
    ----------
    width: int
        The same as the screen width. It is assigned a variable so the screen
        does not need to be a parameter to many of the class's methods.
    height: int
        The same as the screen height.
    font_size: int
        The starting size of the font of the sentence to be typed. It can be
        decreased if it proves to make the sentence too big.
    width_ratio: float
        The width to height ratio of the font used. For Space Mono it is 0.6.
    """
    def __init__(self, screen):
        """The font is retrieved and the sentence is created

        Parameters
        ----------
        screen: Screen class
            The screen instance should be used as a parameter so the GUI has
            access to the width and height of the window
        """
        self._retrieve_font()
        self.width = screen.width
        self.height = screen.height
        self.font_size = 20
        self.width_ratio = 0.6
        self.display_sentence()

    def _retrieve_font(self):
        """Used to find and retrieve the Space Mono font file.
        
        The location can be accessed using _font_location. Nothing in this
        method should be tampered with.
        """
        self._font_location_str = "assets\spacemono\SpaceMono-Regular.ttf"
        self._file_root_directory = os.path.realpath(os.path.join(
            os.path.dirname(__file__), '.')) # The folder this file is located
                                             # in
        self._font_location = os.path.join(
            self._file_root_directory, self._font_location_str)

    def choose_sentence(self):
        """Accesses the sentences.txt file and chooses a random sentence.
        
        The _sentence_location should not be tampered with.
        """
        self._sentence_location = os.path.join(
            self._file_root_directory, "assets/sentences.txt")
        with open(self._sentence_location) as f:
            self.sentences = f.read().splitlines() # Turns into list
        idx = r.randint(0, len(self.sentences) - 1)
        self.text = self.sentences[idx]


    def decomp_sentence(self):
        """Turns the sentence into its individual letters.
        
        This is done so that each letter can have its own shading (red or 
        green) to display if the letter has been correctly been typed.
        """
        self.text_letters = list(self.text)
        self.rendered_letters = []
        self.letter_width = self.font_size * self.width_ratio
        y = 0.25 * self.height
        for idx, letter in enumerate(self.text_letters):
            x = (self.width / 2) + (idx - (len(self.text_letters) / 2)) \
                * self.letter_width
            letter_render = self.font.render(letter, True, WHITE)
            letter_rect = letter_render.get_rect()
            letter_rect.center = (x, y)
            self.rendered_letters.append((letter_render, letter_rect))

    def display_sentence(self):
        """Renders the sentence to be typed
        
        More specifically, a sentence is chosen and then the sentence is 
        decomposed. This method renders each individual letter as its own 
        surface so that each letter can have its own outline (red or greed) in 
        case the letter was typed correctly or incorrectly. 
        """
        self.choose_sentence()
        while len(self.text) * self.font_size * self.width_ratio >= \
                0.9 * self.width:
            self.font_size -= 1
        self.font = pg.font.Font(self._font_location, self.font_size)
        self.font_30 = pg.font.Font(self._font_location, 30)
        self._words = self.text.split()
        self.word_count = len(self._words)
        self.input_text = ""
        self.comp = []
        self.decomp_sentence()

    def compare_str(self):
        """Creates a list comparing the sentence to be typed and the input

        If a letter has been typed correctly, it is represented by a True
        boolean inside self.comp. If it has been typed incorrectly, it is
        represented by a False boolean. Otherwise, it is not inside the list.
        This list will be used to change the outline of each letter.

        Returns
        -------
        comp: List
            Since this is a attribute, it does not necessarely need to be 
            returned. However, if the length of comp is greater than or equal
            to the text, comp is returned early so it is still useful.
        
        """
        self.comp = []
        for idx, letter in enumerate(self.input_text):
            if len(self.comp) >= len(self.text):
                return self.comp
            else:
                # True if the input letter matches the text letter
                self.comp.append(True if letter == self.text[idx] else False)
        return self.comp

    def update(self, screen, states):
        """Displays sentences and letter backgrounds every frame

        If the sentence is still being written, then only the sentence and the
        letter backgrounds will be displayed. If the sentence has been 
        completely typed, then the stats and the prompt to reset will also be
        displayed

        Parameters
        ----------

        screen: Screen class
            Used to display all surfaces onto the screen
        states: Tuple
            Includes whether the game is running or if the user is typing.
            However, only the typing state is used to display the stats and
            reset prompt if True
        
        """
        __, typing = states

        # Render all letter backgrounds
        for idx, (letter, rect) in enumerate(self.rendered_letters):
            letter_background = letter.copy()
            if idx >= len(self.comp): # Letter has not yet been typed
                pass
            elif self.comp[idx]: # Letter is correct
                letter_background.fill(GREEN)
            else: # Letter is incorrect
                letter_background.fill(RED)
            screen.display.blit(letter_background, rect)
            screen.display.blit(letter, rect)

        # Run if sentence has been completed
        if not typing:
            stats_render, stats_render_rect = self.rendered_stats
            screen.display.blit(stats_render, stats_render_rect)

            reset_str = "Press ` to reset"
            reset_render = self.font_30.render(reset_str, True, WHITE)
            reset_render_rect = reset_render.get_rect()
            reset_render_rect.center = (0.5*self.width, 0.75*self.height)
            screen.display.blit(reset_render, reset_render_rect)
        pg.display.flip()

    def stats(self, timer):
        """Display the time, WPM, and accuracy precentage
        
        This method calculates all of the stats and then creates the sentence
        to display them
        """
        self.time = timer.t_end - timer.t_start
        self.wpm = self.word_count / self.time * 60 # Converts from seconds to
                                                    # minutes
        correct = 0
        for i in self.comp:
            if i: correct += 1
        self.accuracy = correct / len(self.comp)
        stat_str = f"Time: {self.time:.2f}s, WPM: {self.wpm:.0f}, " + \
            f"Accuracy: {self.accuracy*100:.0f}%"
        stats_render = self.font_30.render(stat_str, True, WHITE)
        stats_render_rect = stats_render.get_rect()
        stats_render_rect.center = (0.5*self.width, 0.5*self.height)
        self.rendered_stats = (stats_render, stats_render_rect)

class Timer():
    """Class to start and stop time
    
    Uses time module to keep track of the time. More specificallu uses the
    perf_counter() function.

    Attributes
    ----------
    t_start: float
        Start of the timer
    t_end: float
        End of the timer
    """
    def __init__(self):
        self.start()

    def start(self):
        """Start the timer"""
        self.t_start = t.perf_counter()

    def end(self):
        """End the timer"""
        self.t_end = t.perf_counter()

def game_loop():
    """The main loop which is only stopped when the window is closed
    
    Game Loop Order
    ---------------
    1. The background is filled with the desired color

    2. All events are checked for and evaluated if the conditions are matched.
       Events include the window being closed and any key being pressed
        
        a. If the window is closed, the game loop is ended
        b. If F12 is pressed, fullscreen is toggled
        c. If Escape is pressed when the screen is fullscreen, the screen is
           brought back to a windowed mode
        d. If Backspace is pressed, the input string's last element is removed
        e. If any other key is pressed besides Escape, it will be added to the
           input string. If this key press causes the input string to have
           equal length to the sentence, then the statistics will be displayed
           and no more keys will be added to the input string
        f. If backquote is pressed when the sentence has been fully typed, a
           new sentence will be displayed and the timer will be restarted

    3. The screen is updated
    """
    screen = Screen()
    gui = GUI(screen)
    timer = Timer()

    run = True
    typing = True

    while run:
        states = (run, typing)
        screen.background()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False # Stops the game loop
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_F12 or
                    (event.key == pg.K_ESCAPE and screen.fullscreen)):
                    screen.fullscreen = not screen.fullscreen
                    screen.toggle_fullscreen()
                elif event.key == pg.K_BACKSPACE and typing:
                    gui.input_text = gui.input_text[:-1]
                    gui.compare_str()
                elif event.key != pg.K_ESCAPE and typing:
                    gui.input_text = gui.input_text + event.unicode
                    gui.compare_str()
                    if len(gui.input_text) == len(gui.text):
                        timer.end()
                        gui.stats(timer)
                        typing = False
                elif event.key == pg.K_BACKQUOTE and not typing:
                    typing = True
                    gui.display_sentence()
                    timer.start()

        gui.update(screen, states)
        screen.update()
    del screen # Causes Pygame to quit