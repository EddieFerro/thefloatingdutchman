# Basic Globals
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MANTIS = (101, 168, 100)
RUFOUS = (163, 32, 21)
LIME = (164, 203, 57)

# Game Settings
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 60

# Menu Button Bounds
WIDTH_LEFT_BOUND = WINDOW_WIDTH * (3 / 8)
WIDTH_RIGHT_BOUND = WINDOW_WIDTH * (5 / 8)

# Game Over 
GAME_OVER_BOUNDS = [[WINDOW_HEIGHT * (9 / 20), WINDOW_HEIGHT * (11 / 20)], #Play Again
                    [WINDOW_HEIGHT * (3 / 5), WINDOW_HEIGHT * (7 / 10)], #Return to Main Menu
                    [WINDOW_HEIGHT * (3 / 4), WINDOW_HEIGHT * (17 / 20)]] #Quit Game

#Pause Menu
PAUSE_BOUNDS = [[WINDOW_HEIGHT * (35 / 100), WINDOW_HEIGHT * ((35 / 100) + (1 / 14))], #Resume
                [WINDOW_HEIGHT * (44 / 100), WINDOW_HEIGHT * ((44 / 100) + (1 / 14))], #View Map
                [WINDOW_HEIGHT * (53 / 100), WINDOW_HEIGHT * ((53 / 100) + (1 / 14))], #View Game Controls
                [WINDOW_HEIGHT * (62 / 100), WINDOW_HEIGHT * ((62 / 100) + (1 / 14))], #Restart
                [WINDOW_HEIGHT * (71 / 100), WINDOW_HEIGHT * ((71 / 100) + (1 / 14))], #Return to Main Menu
                [WINDOW_HEIGHT * (80 / 100), WINDOW_HEIGHT * ((80 / 100) + (1 / 14))]] #Quit Game

#Main Menu
MAIN_MENU_BOUNDS = [[WINDOW_HEIGHT * (40 / 100), WINDOW_HEIGHT * ((40 / 100) + (1 / 12))], #Begin Game
                    [WINDOW_HEIGHT * (50 / 100), WINDOW_HEIGHT * ((50 / 100) + (1 / 12))], #Begin Game with Tutorial
                    [WINDOW_HEIGHT * (60 / 100), WINDOW_HEIGHT * ((60 / 100) + (1 / 12))], #View Game Controls
                    [WINDOW_HEIGHT * (70 / 100), WINDOW_HEIGHT * ((70 / 100) + (1 / 12))]] #Quit Game
