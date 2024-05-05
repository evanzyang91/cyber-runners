import pygame
#imports Tile sprite
from tiles import Tile, StaticTile
#imports necessary variables
from settings import tileSize, screenWidth
#imports player sprite
from player import Player
from support import import_csv_layout, import_cut_graphic
from settings import tileSize
from tiles import Tile
from game_data import level1, level2, level3
import csv
from endpoint import Endpoint


class Level():

    def __init__(self, data, surface):
        """ 
        Description: Initialization method.
        Parameters: Level data (list format), surface for display.
        Return: None.
        """

        self.displaySurface = surface

        terrain_layout = import_csv_layout(data['terrain'])

        self.terrain_sprites = self.levelSetup(terrain_layout, 'terrain')

        self.worldShift = 0

        
        self.dashAvailable = True

        self.timer = 0


    def levelSetup(self, layout, type):
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

        self.endpoint = pygame.sprite.Group()

        #iterates through each string in map list
        #takes row position and row value 
        for rowIndex, row in enumerate(layout):
            #iterates through each character in row string
            #takes character position and character value
            for colIndex, col in enumerate(row):
                if col != "-1":
                    #sets x and y coordinates using char indexes
                    x = colIndex * tileSize
                    y = rowIndex * tileSize
                    
                    #checks if char value is 1
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic("Final/visuals/level/Tileset.png")
                        tile_surface = terrain_tile_list[int(col)]
                        #creates tile at respective coordinates
                        tile = StaticTile(tileSize, x, y, tile_surface)
                        #adds sprite to sprite group
                        self.tiles.add(tile)
                    
                    #checks if char value is 61
                    if col == "61":
                        #creates player at respective coordinates
                        playerModel = Player((x, y))
                        #adds sprite to sprite group
                        self.player.add(playerModel)

                    #checks if char value is 62
                    #if col == "62":
                        #creates enemy at respective coordinates
                        #enemyModel = Enemy((x, y))
                        #adds sprite to sprite group
                        #self.enemy.add(enemyModel) 

                    #checks if char value is 63
                    if col == "63":
                        #creates enemy at respective coordinates
                        endpointModel = Endpoint((x, y))
                        #adds sprite to sprite group
                        self.endpoint.add(endpointModel) 
                    
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
        if playerx < 500 and directionx < 0: 
            #sets world shift to opposite of player speed
            self.worldShift = 4
            player.spawn[0] += 4
            #sets player speed to 0 (map moving creates illusion of player moving)
            player.speed = 0
        #checks if player is moving right and is at threshold coordinates
        elif playerx > 700 and directionx > 0:
            #sets world shift to opposite of player speed
            self.worldShift = -4
            player.spawn[0] -= 4
            #sets player speed to 0
            player.speed = 0
        #when the player has not passed the threshold coordinates
        else: 
            self.worldShift = 0
            player.speed = 4

        #gets all keys pressed
        keys = pygame.key.get_pressed()

        dash = pygame.mixer.Sound("Final/sounds/dash.mp3")
        dash.set_volume(0.1)

        if keys[pygame.K_c]:
            if self.dashAvailable == True:
                self.timer = 0
                if player.direction.x < 0:
                    dash.play()
                    self.worldShift = 100
                    player.spawn[0] += 100
                elif player.direction.x > 0:
                    dash.play()
                    self.worldShift = -100
                    player.spawn[0] -= 100

                self.dashAvailable = False

        if self.timer >= 120:
            self.dashAvailable = True


    def horizontalCollision(self):
        """ 
        Description: Creates lateral movement and checks for lateral collisions.
        Parameters: None.
        Return: None.
        """
    
        player = self.player.sprite

        #moves player laterally
        player.rect.x += player.direction.x * player.speed
        
        
        for sprite in self.endpoint.sprites():
            if sprite.rect.colliderect(player.rect):
                print("colide")
        
        #iterates through tile sprite list
        for sprite in self.tiles.sprites():
            #checks if player and tile sprite collide
            if sprite.rect.colliderect(player.rect):
                #for left movement
                if player.direction.x < 0:
                    #sets player left coordinate to tile right coordinate (does not allow player to pass tile)
                    player.rect.left = sprite.rect.right
                #for right movement
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                
    def verticalCollision(self):

        player = self.player.sprite

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
                #for moving down
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.jumpsAvailable = True
                    
        for sprite in self.endpoint.sprites():
            
            if sprite.rect.colliderect(player.rect):
                
                print("collide")

                
    def run(self):
        """ 
        Description: Runs necessary methods for level.
        Parameters: None.
        Return: None.
        """

        self.tiles.update(self.worldShift)
        self.tiles.draw(self.displaySurface)
        self.cameraScroll()
        self.player.update()
        

        
        self.timer += 1
        
        self.horizontalCollision()
        self.verticalCollision()
        self.player.draw(self.displaySurface)
        self.enemy.draw(self.displaySurface)

