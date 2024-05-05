""" 
Authors: Evan Yang and Ethan Yang

Date: June 19, 2023

Purpose: Creates and modifies player for game.
"""

import pygame
from importing import importFolder
import time

class Player(pygame.sprite.Sprite):
    ''' 
    Sprite for player.
    '''

    def __init__(self, pos, surface):
        """ 
        Description: Initializes player sprite.
        Parameters: Player coordinates and display surface.
        Return: None.
        """

        #initializes superclass
        pygame.sprite.Sprite.__init__(self)

        #gets frames for player animation
        self.animationFrames()

        #initializes frame number and speed
        self.frameNumber = 0
        self.frameSpeed = 0.1
        #creates rectangle surface
        self.image = self.animations['run'][self.frameNumber]
        #creates rectangle hitbox for first frame of run animation
        self.rect = self.image.get_rect(topleft = pos)

        self.displaySurface = surface

        #creates vector (contains x and y directions)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 1
        self.jumpHeight = -20
        
        self.timer = 0

        self.status = 'idle'
        self.facingRight = True
        self.healthy = False
        self.invincible = False

        self.jumpsAvailable = True

    def animationFrames(self):
        ''' 
        Gets frame images for player animations.
        '''

        #general path
        path = "Final/visuals/player/"
        #dictionary with end of path as key for list that will be filled with frame images
        self.animations = {"idle":[], "run":[], "jump":[]}

        #iterates through each animation key in dictionary
        for animation in self.animations.keys():
            #creates direct path to folder
            directPath = path + animation
            #adds list of frame images to dictionary item
            #importFolder returns list of images in given folder
            self.animations[animation] = importFolder(directPath)

    def animate(self):
        ''' 
        Iterates through each image in animation frames list and rapidly displays them.
        '''

        #frame image list
        animation = self.animations[self.status]

        #adds frame speed to frame number (acts as a timer)
        self.frameNumber += self.frameSpeed 

        #checks if frame number has exceeded length of frame list
        if self.frameNumber >= len(animation):
            #resets frame number to 0
            self.frameNumber = 0

        #stores temporary image of single frame in frame list
        tempImage = animation[int(self.frameNumber)]

        #sets player image to frame image
        if self.facingRight:
            self.image = tempImage
        #flips image if player is facing to the left
        else: 
            self.image = pygame.transform.flip(tempImage, True, False)
   

    def getInput(self):
        """ 
        Description: Gets user inputs and sets direction.
        Parameters: None.
        Return: None.
        """

        #plays jump sound
        jump = pygame.mixer.Sound("Final/sounds/jump.mp3")
        jump.set_volume(0.3)

        #gets all keys pressed
        keys = pygame.key.get_pressed()

        #sets player direction right
        if keys[pygame.K_RIGHT]: 
            self.direction.x = 1
            self.facingRight = True
        #sets player direction left
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facingRight = False
        else:
            self.direction.x = 0

        #calls jump method
        if keys[pygame.K_UP]:
            #checks if player has jump available
            if self.jumpsAvailable == True:
                jump.play()
                self.jump()
                #sets jump available to false once player has jumped
                self.jumpsAvailable = False


    def getStatus(self):
        ''' 
        Gets status of player to display correct animation.
        '''

        #checks if player y direction is moving up
        if self.direction.y < 0:
                self.status = "jump"
        else:
            #checks if player x direction is either left or right
            if self.direction.x > 0 or self.direction.x < 0:
                self.status = "run"
            #if not then player is standing still
            else:
                self.status = "idle"


    def useGravity(self):
        """ 
        Description: Applies gravity to player sprite.
        Parameters: None.
        Return: None.
        """

        #adds gravity to vertical direction
        self.direction.y += self.gravity
        #adds vertical direction to player hitbox
        self.rect.y += self.direction.y

    def jump(self):
        """ 
        Description: Applies jump height to player sprite.
        Parameters: None.
        Return: None.
        """

        #adds jump height to vertical direction
        self.direction.y = self.jumpHeight
        

    def update(self, surface):
        """ 
        Description: Called every game loop iteration. Calls necessary methods.
        Parameters: None.
        Return: None.
        """

        self.getInput()
        self.getStatus()
        self.animate()


        