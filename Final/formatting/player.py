import pygame
from importing import importFolder
import time

#sprite for player character
class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        """ 
        Description: Initializes player sprite.
        Parameters: Player coordinates.
        Return: None.
        """

        #initializes superclass
        pygame.sprite.Sprite.__init__(self)

        self.animationFrames()
        self.frameNumber = 0
        self.frameSpeed = 0.1
        #creates rectangle surface
        self.image = self.animations['run'][self.frameNumber]
        #creates rectangle for surface with top left as position reference
        self.rect = self.image.get_rect(topleft = pos)

        #creates vector (contains x and y directions)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 1
        self.jumpHeight = -20

        self.spawn = [pos[0], pos[1]]
        
        self.timer = 0

        self.status = 'idle'
        self.facingRight = True
        self.onGround = False
        self.onCeiling = False
        self.onRight = False
        self.onLeft = False
        self.falling = False

    def animationFrames(self):

        path = "Final/visuals/player/"
        self.animations = {"idle":[], "run":[], "jump":[]}

        for animation in self.animations.keys():
            directPath = path + animation
            self.animations[animation] = importFolder(directPath)

    def animate(self):

        animation = self.animations[self.status]

        self.frameNumber += self.frameSpeed 

        if self.frameNumber >= len(animation):
            self.frameNumber = 0

        tempImage = animation[int(self.frameNumber)]

        if self.facingRight:
            self.image = tempImage
        else: 
            self.image = pygame.transform.flip(tempImage, True, False)
   

    def getInput(self):
        """ 
        Description: Gets user inputs and sets direction.
        Parameters: None.
        Return: None.
        """

        
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

            if self.jumpsAvailable == True:
                jump.play()
                self.jump()
                self.jumpsAvailable = False


    def getStatus(self):

        if self.direction.y < 0:
            if self.direction.x >= 0:
                self.status = "jump"
        #elif self.direction.y > 1.1:
            #if self.direction.x >= 0:
                #self.status = "fall"
        else:
            if self.direction.x > 0 or self.direction.x < 0:
                self.status = "run"
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
        
    def is_fall(self):
        
        die = pygame.mixer.Sound("Final/sounds/die.mp3")
        die.set_volume(0.5)
        
        if self.rect.y > 700:
            self.rect.topleft = self.spawn
            die.play()
            self.falling = True


    def update(self):
        """ 
        Description: Called every game loop iteration. Calls necessary methods.
        Parameters: None.
        Return: None.
        """

        keys = pygame.key.get_pressed()

        self.getInput()
        self.getStatus()
        self.animate()
        self.is_fall()


        