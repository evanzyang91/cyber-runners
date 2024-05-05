""" 
Authors: Evan Yang and Ethan Yang

Date: June 19, 2023

Purpose: Creates tile sprites for map.
"""

import pygame
from importing import importFolder

class Tile(pygame.sprite.Sprite):
    '''General tile sprite.'''

    def __init__(self, size, x, y):
        ''' 
        Initializer method for tile.
        Takes tile size, x position, and y position of tile.
        '''
        
        super().__init__()

        #sets image to square of tile size
        self.image = pygame.Surface((size, size))
        #gets rect for surface
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, xShift):
        ''' 
        Updates position of tile.
        Takes x shift parameter (number).
        '''

        #adds x shift value to tile
        self.rect.x += xShift

class StaticTile(Tile):
    ''' 
    Sprite class for all non moving tiles. Inherits from Tile.
    '''

    def __init__(self, size, x, y, surface):
        ''' 
        Initializer method.
        Takes tile size, x position, y position, and surface to be displayed on.
        '''
        super().__init__(size, x, y)
        #sets image to given surface
        self.image = surface

class Object(StaticTile):
    '''
    Sprite class for background object tiles. Inherits from StaticTile.
    '''

    def __init__(self, size, x, y, name):
        ''' 
        Initializer method.
        Takes tile size, x position, y position, file name of object.
        '''
        #initializes superclass and passes image path to static tile
        super().__init__(size, x, y, pygame.image.load('Final/visuals/level/bg_objects/' + name + '.png').convert_alpha())
        #offset for tile to be positioned correctly (image is larger than tile size)
        offset_y = y + size
        #sets bottom left of image to new coordinates
        self.rect = self.image.get_rect(bottomleft = (x, offset_y))

class AnimatedTile(Tile):
    '''
    Sprite class for all animated tiles. Inherits from Tile class.
    '''

    def __init__(self, size, x, y, path):
        ''' 
        Initializer method.
        Takes tile size, x position, y position, folder path of tile frames.
        '''
        super().__init__(size, x, y)
        #calls import folder function (returns list of images in folder)
        self.frames = importFolder(path)
        self.frameIndex = 0
        #sets image to first frame of animation
        self.image = self.frames[self.frameIndex]

    def animate(self):
        ''' 
        Continuously iterates through image frames to create animation. Same as animate method for player.
        '''
        #increments frame index (speed of animation)
        self.frameIndex += 0.2
        #resets frame index when it surpasses numbers of images
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        #sets image to current frame
        self.image = self.frames[int(self.frameIndex)]

    def update(self, xShift):
        ''' 
        Calls animate method and updates tile position.
        Takes x shift number parameter.
        '''
        self.animate()
        self.rect.x += xShift

class Coin(AnimatedTile):
    '''Class for coins. Inherits from animated tile.'''

    def __init__(self, size, x, y, path, value):
        ''' 
        Initializer method.
        Takes tile size, x position, y position, folder path of tile frames, and value of coin.
        '''

        super().__init__(size, x, y, path)

        #calculates center x and y of coin (center of tile)
        centerX = x + int(size / 2)
        centerY = y + int(size / 2)

        #sets center of coin rectangle to respective coordinates
        self.rect = self.image.get_rect(center = (centerX, centerY))
        self.value = value