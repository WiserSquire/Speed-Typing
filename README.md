# Speed-Typing

GitHub link: https://github.com/WiserSquire/Speed-Typing

## Introduction
This program allows the user to test how fast they can type sentences. 
Once the program starts, a sentence displaying some fact about Python will be displayed and the user needs to type the sentence as fast as possible.
Like with many other speed typing programs, if a letter has been typed correctly, it will have a green background. However, if it has been typed incorrectly, it will have a red background.

Once the last character has been typed, statistics including the user's time, words per minute (WPM), and accuracy will be displayed.
When the statistics are displayed, the user can enter the backquote key (`) to reset their statistics and type in a new sentence.
This program also allows for fullscreen compatability. Press F12 to toggle between fullscreen and windowed mode or press Escape when in fullscreen mode to enter windowed mode.

This program's dependencies that are not included with Python is mainly Pygame. Pygame is used to create the window as well as to display the game objects. Other depencies that are built into Python include os, time, and random.

## Setup
Ensure that Python 3 is installed on your computer. Python 2 is not supported by Pygame. For this program, Python 3.10 was used to code it. However, any Python 3 installation should be supported. The link can be found here: https://www.python.org/downloads/

In addition. Pip should be installed which will be used to install Pygame. The instructions for downloading Pip can be found here: https://pip.pypa.io/en/stable/installation/

Finally, Pygame should be installed by entering the terminal and typing the following line
```console
pip install pygame
```

This program was written with Pygame 2.1.2. To ensure that pygame has been properly installed, type in this command into the terminal to get the information for Pygame:
```console
pip show pygame
```

## Initialization
To initialize the game. Start the __main__.py file inside of the Speed-Typing folder. Make sure that the file hierarchy is not tampered with or else the assets will not load and the program will not work.
