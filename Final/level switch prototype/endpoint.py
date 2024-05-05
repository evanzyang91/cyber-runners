import pygame
from importing import SpriteSheet
import time

#sprite for enemy character
class Endpoint(pygame.sprite.Sprite):

    def __init__(self, pos):
        """ 
        Description: Initializes player sprite.
        Parameters: Player coordinates.
        Return: None.
        """

        #initializes superclass
        pygame.sprite.Sprite.__init__(self)

        self.frameNumber = 0
        self.frameSpeed = 0.1

        #creates rectangle for surface with top left as position reference
        self.image = pygame.Surface((40, 50)) 
        self.image = self.image.convert() 
        self.image.fill((0, 255, 0)) 
        self.rect = self.image.get_rect(topleft = pos)

