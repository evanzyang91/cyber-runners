"""
Author: Ethan Yang and Evan Yang
Date: June 19, 2023
Purpose: imports necessary modules and classes, initializes game, defines main game loop and starts game
"""

import pygame
#makes code from settings module available for use
from settings import *
#imports Level class from level module
from level import Level
from layers import level0
from menu import Menu
from ui import UI

class Game:
    """ 
    Represents the game and its logic.
    """

    def __init__(self):
        """
        Initializes the Game object.
        
        Parameters:
        - None
        
        Returns:
        - None
        """

        self.maxLevel = 0
        # Initialize the maximum level to 0

        self.menu = Menu(0, self.maxLevel, screen, self.loadLevel)
        # Create a Menu object with initial values

        self.status = 'menu'
        # Set the initial game status to 'menu'

        self.coins = 0
        # Set the initial number of coins to 0

        self.ui = UI(screen)
        # Create a UI object with the screen

    def loadLevel(self, currentLevel):
        """
        Loads a specific level of the game.
        
        Parameters:
        - currentLevel (int): The level to load.
        
        Returns:
        - None
        """

        self.level = Level(currentLevel, screen, self.loadMenu, self.changeCoins, self.resetCoins)
        # Create a Level object with the specified current level and functions

        self.status = 'level'
        # Set the game status to 'level'

    def loadMenu(self, currentLevel, newMaxLevel):
        """
        Loads the game menu with the specified current level and new maximum level.
        
        Parameters:
        - currentLevel (int): The current level.
        - newMaxLevel (int): The new maximum level.
        
        Returns:
        - None
        """

        if newMaxLevel > self.maxLevel:
            self.maxLevel = newMaxLevel
        # Update the maximum level if the new maximum level is higher

        self.menu = Menu(currentLevel, self.maxLevel, screen, self.loadLevel)
        # Create a new Menu object with the updated values

        self.status = 'menu'
        # Set the game status to 'menu'

    def changeCoins(self, amount):
        """
        Changes the number of coins by the specified amount.
        
        Parameters:
        - amount (int): The amount to change the coins by.
        
        Returns:
        - None
        """

        self.coins += amount
        # Add the specified amount to the current number of coins

    def resetCoins(self):
        """
        Resets the number of coins to 0.
        
        Parameters:
        - None
        
        Returns:
        - None
        """

        self.coins = 0
        # Set the number of coins to 0

    def run(self):
        """
        Runs the game logic based on the current game status.
        
        Parameters:
        - None
        
        Returns:
        - None
        """

        if self.status == 'menu':
            self.menu.run()
            # Run the menu logic if the game status is 'menu'
        else:
            self.level.run()
            self.ui.show_coins(self.coins)
            # Run the level logic and show the number of coins on the UI

# Initializes pygame
pygame.init()

# Creates the screen
screen = pygame.display.set_mode((screenWidth, screenHeight))
# Set the screen size based on the specified width and height

clock = pygame.time.Clock()
# Create a clock object to control the frame rate

game = Game()
# Create a Game object

def main():
    """ 
    Mainline logic.
    """

    pygame.mixer.music.load("Final/sounds/gameloop.mp3")
    # Load the game loop music

    pygame.mixer.music.set_volume(0.05)
    # Set the volume of the music

    pygame.mixer.music.play(-1)
    # Play the music on loop

    pygame.display.set_caption("CYBER // STRIKE")
    # Set the window caption

    background = pygame.Surface(screen.get_size())
    # Create a background surface with the same size as the screen

    background = background.convert()
    # Convert the background surface to improve blitting performance

    background = pygame.image.load("Final/visuals/level/background.jpg")
    # Load the background image

    running = True
    # Set the initial running state to True

    while running:
        # Run the game loop until running is set to False

        clock.tick(60)
        # Limit the frame rate to 60 frames per second

        screen.fill((0, 0, 0))
        # Fill the screen with black color

        screen.blit(background, (0, 0))
        # Blit the background image onto the screen at position (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Quit the game loop if the 'QUIT' event is triggered

        game.run()
        # Run the game logic

        pygame.display.flip()
        # Update the display

    pygame.quit()
    # Quit pygame

main()
# Call the main function to start the game