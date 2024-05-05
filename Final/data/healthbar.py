"""
Author: Ethan Yang and Evan Yang
Date: June 18, 2023
Purpose: manage and display a score/health points in the game
"""

import pygame
import random
from player import Player

class ScoreKeeper(pygame.sprite.Sprite):
    """
    ScoreKeeper class representing a sprite that keeps track of and displays a score or health points.
    """

    def __init__(self, x, y, w, h, hp, max_hp):
        """
        Initializes a ScoreKeeper object.

        Parameters:
        - x: The x-coordinate of the ScoreKeeper's position.
        - y: The y-coordinate of the ScoreKeeper's position.
        - w: The width of the ScoreKeeper's image.
        - h: The height of the ScoreKeeper's image.

        Return:
        None.
        """

        super().__init__()  # Initializes the superclass
        self.image = pygame.Surface((w, h))  # Creates a surface with the specified width and height
        self.rect = self.image.get_rect()  # Gets the rectangle representing the image's position and size
        self.rect.x = x  # Sets the x-coordinate of the ScoreKeeper's position
        self.rect.y = y  # Sets the y-coordinate of the ScoreKeeper's position
        self.hp = hp  # Current health points
        self.max_hp = max_hp  # Maximum health points
        self.width = w  # Width of the ScoreKeeper's image
        self.height = h  # Height of the ScoreKeeper's image
        self.update_image()  # Updates the ScoreKeeper's image based on the current health points

    def update_hp(self, new_hp):
        """
        Updates the health points of the ScoreKeeper and updates its image.

        Parameters:
        - new_hp: The new health points value.

        Return:
        None.
        """
        self.hp = new_hp  # Updates the health points
        self.update_image()  # Updates the ScoreKeeper's image based on the new health points

    def update_image(self):
        """
        Updates the ScoreKeeper's image based on the current health points.

        Parameters:
        None.

        Return:
        None.
        """
        ratio = self.hp / self.max_hp  # Calculates the ratio of current health points to maximum health points
        self.image.fill((0, 0, 0))  # Fills the image with black color
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, self.width, self.height))  # Draws a red rectangle representing the maximum health
        health_width = int(self.width * ratio)  # Calculates the width of the green rectangle based on the health points ratio
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, health_width, self.height))  # Draws a green rectangle representing the current health points