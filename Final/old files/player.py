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
        self.rect.top = self.rect.top +10
        self.rect.right = self.rect.right - 60

        #creates vector (contains x and y directions)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 1
        self.jumpHeight = -20

        self.status = 'idle'
        self.facingRight = True
        self.onGround = False
        self.onCeiling = False
        self.onRight = False
        self.onLeft = False

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

        '''if self.onGround and self.onRight:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.onGround and self.onLeft:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.onGround:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.onCeiling and self.onRight:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.onCeiling and self.onLeft:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.onCeiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)'''

    def getInput(self):
        """ 
        Description: Gets user inputs and sets direction.
        Parameters: None.
        Return: None.
        """

        start = time.time()

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
                self.jump()
                self.jumpsAvailable = False

        if keys[pygame.K_c]:
            if time.time() - start > 2:
                start = time.time()
                if self.direction.x < 0:
                    self.gravity = 0
                    self.rect.x -= 30
                    self.gravity = 1
                elif self.direction.x > 0:
                    self.gravity = 0
                    self.rect.x += 30
                    self.gravity = 1

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

    def update(self, screen):
        """ 
        Description: Called every game loop iteration. Calls necessary methods.
        Parameters: None.
        Return: None.
        """

        #keys = pygame.key.get_pressed()
        

        self.getInput()
        self.getStatus()
        self.animate()


        