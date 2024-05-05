import pygame
#imports Tile sprite
from tiles import Tile
#imports necessary variables
from settings import tileSize, screenWidth
#imports player sprite
from player import Player

from enemy import Drone

class Level():

    def __init__(self, data, surface):
        """ 
        Description: Initialization method.
        Parameters: Level data (list format), surface for display.
        Return: None.
        """

        self.displaySurface = surface
        #calls method to set up level
        self.levelSetup(data)

        self.worldShift = 0
        self.currentX = 0

    def levelSetup(self, layout):
        """ 
        Description: Creates tile and player sprites.
        Parameters: Level layout list.
        Return: None.
        """

        #creates sprite group for tiles
        self.tiles = pygame.sprite.Group()
        #creates single sprite group for player
        self.player = pygame.sprite.GroupSingle()

        self.enemy = pygame.sprite.Group()

        #iterates through each string in map list
        #takes row position and row value 
        for rowIndex, row in enumerate(layout):
            #iterates through each character in row string
            #takes character position and character value
            for colIndex, col in enumerate(row):

                #sets x and y coordinates using char indexes
                x = colIndex * tileSize
                y = rowIndex * tileSize
                
                #checks if char value is 1
                if col == "1":
                    #creates tile at respective coordinates
                    tile = Tile((x, y), tileSize)
                    #adds sprite to sprite group
                    self.tiles.add(tile)

                #checks if char value is P
                if col == "P":
                    self.playerSpawnX = x
                    self.playerSpawnY = y
                    #creates player at respective coordinates
                    playerModel = Player((x, y))
                    #adds sprite to sprite group
                    self.player.add(playerModel)

                #checks if char value is E
                #if col == "E":
                    #creates enemy at respective coordinates
                    #drone = Drone((x, y))
                    #adds sprite to sprite group
                    #self.enemy.add(drone) 

    def cameraScroll(self):
        """ 
        Description: Scrolls level after player reaches boundaries to illustrate movement.
        Parameters: None.
        Return: None.
        """

        player = self.player.sprite
        #player center x coordinate
        playerx = player.rect.centerx
        #player lateral direction
        directionx = player.direction.x

        #checks if player is moving left and is at threshold coordinates
        if playerx < (screenWidth / 4) and directionx < 0: 
            #sets world shift to opposite of player speed
            self.worldShift = 4
            #sets player speed to 0 (map moving creates illusion of player moving)
            player.speed = 0
        #checks if player is moving right and is at threshold coordinates
        elif playerx > (screenWidth * 3/4) and directionx > 0:
            #sets world shift to opposite of player speed
            self.worldShift = -4
            #sets player speed to 0
            player.speed = 0
        #when the player has not passed the threshold coordinates
        else: 
            self.worldShift = 0
            player.speed = 4

    def horizontalCollision(self):
        """ 
        Description: Creates lateral movement and checks for lateral collisions.
        Parameters: None.
        Return: None.
        """

        player = self.player.sprite

        #moves player laterally
        player.rect.x += player.direction.x * player.speed

        #iterates through tile sprite list
        for sprite in self.tiles.sprites():
            #checks if player and tile sprite collide
            if sprite.rect.colliderect(player.rect):
                #for left movement
                if player.direction.x < 0:
                    #sets player left coordinate to tile right coordinate (does not allow player to pass tile)
                    player.rect.left = sprite.rect.right
                    player.onLeft = True
                    self.currentX = player.rect.left
                #for right movement
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.rect.right

        '''if player.onLeft and (player.rect.left < self.currentX or player.direction.x >= 0):
            player.onLeft = False
        if player.onRight and (player.rect.right > self.currentX or player.direction.x <= 0):
            player.onRight = False'''

    def verticalCollision(self):

        player = self.player.sprite
        for sprite in self.enemy.sprites():
            sprite.useGravity()

        player.useGravity()

        #iterates through tile sprite list
        for sprite in self.tiles.sprites():
            #checks if player and tile sprite collide
            if sprite.rect.colliderect(player.rect):
                #for moving up
                if player.direction.y < 0:
                    #sets player top coordinate to directly under tile (does not let )
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True
                #for moving down
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                    player.jumpsAvailable = True    

                for nme in self.enemy.sprites():
                    if nme.direction.y > 0:
                        nme.rect.bottom = sprite.rect.top
                        nme.direction.y = 0

        '''if player.onGround == True and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False
        if player.onCeiling == True and player.direction.y > 0:
            player.onCeiling = False'''

    def run(self):
        """ 
        Description: Runs necessary methods for level.
        Parameters: None.
        Return: None.
        """

        self.tiles.update(self.worldShift)
        self.tiles.draw(self.displaySurface)
        self.cameraScroll()

        self.player.update(self.displaySurface)
        self.enemy.update(self.worldShift)
        self.horizontalCollision()
        self.verticalCollision()
        self.player.draw(self.displaySurface)
        self.enemy.draw(self.displaySurface)