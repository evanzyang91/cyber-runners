"""
Author: Ethan Yang and Evan Yang
Date: June 19, 2023
Purpose: provides method to move enemy, update position, and handle animation
"""

import pygame
from tiles import AnimatedTile  # Importing the AnimatedTile class from the tiles module
import random

class Enemy(AnimatedTile):
    """
    Enemy class represents an enemy object in the game.
    It inherits from the AnimatedTile class.
    """

    def __init__(self, size, x, y):
        """
        Initialize an Enemy object.

        Parameters:
        - size: The size of the enemy.
        - x: The x-coordinate of the enemy's position.
        - y: The y-coordinate of the enemy's position.
        """
        super().__init__(size, x, y, 'Final/visuals/enemies/walk')  # Initializing the parent class (AnimatedTile)
        self.rect.y += size - self.image.get_size()[1]  # Adjusting the y-coordinate of the enemy's position
        self.speed = random.randint(3, 5)  # Setting a random speed for the enemy

    def move(self):
        """
        Move the enemy horizontally based on its speed.
        """
        self.rect.x += self.speed

    def reverseImage(self):
        """
        Reverse the enemy's image if it's moving to the left.
        """
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        """
        Reverse the direction of the enemy by changing its speed sign.
        """
        self.speed *= -1

    def update(self, shift):
        """
        Update the enemy's position, animation, movement, and image reversal.

        Parameters:
        - shift: The amount to shift the enemy's position by.
        """
        self.rect.x += shift  # Adjusting the enemy's x-coordinate based on the level shift
        self.animate()  # Updating the enemy's animation
        self.move()  # Moving the enemy horizontally
        self.reverseImage()  # Reversing the enemy's image if necessary