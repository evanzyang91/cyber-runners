"""
Author: Ethan Yang and Evan Yang
Date: June 19, 2023
Purpose: import and load images
"""

from os import walk  # Importing the walk method from the os module
import pygame

def importFolder(path):
    """
    Import images from a folder.

    Given a path to a folder, this function loads and returns all the images
    found in that folder.

    Parameters:
    - path: The path to the folder containing the images.

    Returns:
    - A list of pygame.Surface objects representing the loaded images.
    """
    surfaces = []  # List to store the loaded image surfaces
    
    for _,__,imgNames in walk(path):  # Walking through the directory and getting image names
        for image in imgNames:
            directPath = path + "/" + image  # Creating the full path to the image
            imageSurface = pygame.image.load(directPath).convert_alpha()  # Loading the image surface
            if 'player' in path:  # Checking if the path contains "player"
                imageSurface = pygame.transform.scale_by(imageSurface, 1.88)  # Scaling the image surface
            surfaces.append(imageSurface)  # Adding the image surface to the list

    return surfaces  # Returning the list of loaded image surfaces