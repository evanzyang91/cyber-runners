import pygame
import time

#sprite for enemy character
class Drone(pygame.sprite.Sprite):

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

        #creates vector (contains x and y directions)
        self.direction = pygame.math.Vector2(0, 0)
        self.direction.x = 1
        self.gravity = 1
        self.speed = 2

    def useGravity(self):

        self.direction.y += self.gravity
        self.rect.y  += self.direction.y

    def update(self, speed):

        self.rect.x += speed
        self.rect.x += self.direction.x * self.speed

        

        
        