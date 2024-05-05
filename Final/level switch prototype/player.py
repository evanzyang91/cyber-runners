import pygame
from importing import SpriteSheet
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
        self.image = self.animations['idle.png'][self.frameNumber]
        #creates rectangle for surface with top left as position reference
        self.rect = self.image.get_rect(topleft = pos)

        #creates vector (contains x and y directions)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 1
        self.jumpHeight = -20
        self.position = self.rect.x

        
        self.timer = 0

    def animationFrames(self):

        path = "visuals/player/"
        self.animations = {"idle.png":[], "idle_left.png":[], "run.png":[], "run_left.png":[], "jump.png":[], "jump_left.png":[], "fall.png":[], "fall_left.png":[]}

        for animation in self.animations.keys():
            directPath = path + animation
            sheetImage = pygame.image.load(directPath)
            sheetImage.convert_alpha()
            getFrames = SpriteSheet(sheetImage)

            for frame in range(0, int(sheetImage.get_width() / 48)):
                self.animations[animation].append(getFrames.getImage(frame, 48, 48, 2, (0, 0, 0)))

    def animate(self):

        animation = self.animations[self.status]

        self.frameNumber += self.frameSpeed 

        if self.frameNumber >= len(animation):
            self.frameNumber = 0

        self.image = animation[int(self.frameNumber)]

   

    def getInput(self):
        """ 
        Description: Gets user inputs and sets direction.
        Parameters: None.
        Return: None.
        """

        
        jump = pygame.mixer.Sound("jump.mp3")
        jump.set_volume(0.3)

        #gets all keys pressed
        keys = pygame.key.get_pressed()

        #sets player direction right
        if keys[pygame.K_RIGHT]: 
            self.direction.x = 1
        #sets player direction left
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
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
                self.status = "jump.png"
            else:
                self.status = "jump_left.png"
        elif self.direction.y > 1.5:
            if self.direction.x >= 0:
                self.status = "fall.png"
            else:
                self.status = "fall_left.png"
        else:
            if self.direction.x > 0:
                self.status = "run.png"
            elif self.direction.x < 0:
                self.status = "run_left.png"
            else:
                self.status = "idle.png"

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
        


        