import pygame
#imports Tile sprite
from tiles import Tile, StaticTile, Object, Coin
#imports necessary variables
from settings import tileSize, screenWidth, screenHeight
#imports player sprite
from player import Player
from support import import_csv_layout, import_cut_graphic
from settings import tileSize
from tiles import Tile
from enemy import Enemy
from game_data import levels



class Level():

    def __init__(self, currentLevel, surface, loadMenu):
        """ 
        Description: Initialization method.
        Parameters: Level data (list format), surface for display.
        Return: None.
        """

        #screen
        self.displaySurface = surface
        #world shift variable
        self.worldShift = 0

        self.loadMenu = loadMenu
        self.currentLevel = currentLevel
        data = levels[self.currentLevel]
        self.newMaxLevel = data['unlock']

        #player setup
        player_layout = import_csv_layout(data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.playerSetup(player_layout)

        #terrain setup
        terrain_layout = import_csv_layout(data['terrain'])
        self.terrain_sprites = self.levelSetup(terrain_layout, 'terrain')

        #background walls setup
        walls_layout = import_csv_layout(data['walls'])
        self.wall_sprites = self.levelSetup(walls_layout, 'walls')

        #background objects setup
        objects_layout = import_csv_layout(data['objects'])
        self.objects_sprites = self.levelSetup(objects_layout, 'objects')

        #coins setup
        coins_layout = import_csv_layout(data['coins'])
        self.coins_sprites = self.levelSetup(coins_layout, 'coins')

        #enemy setup
        enemy_layout = import_csv_layout(data['enemies'])
        self.enemy_sprites = self.levelSetup(enemy_layout, 'enemies')

        #contraint enemy setup
        constraints_layout = import_csv_layout(data['constraints'])
        self.constraints_sprites = self.levelSetup(constraints_layout, 'constraints')
        
        self.dashAvailable = True

        self.timer = 0
        self.offset = 0

    def levelSetup(self, layout, type):
        """ 
        Description: Creates tile and player sprites.
        Parameters: Level layout list.
        Return: None.
        """

        #creates sprite group for tiles
        tiles = pygame.sprite.Group()

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
                        tiles.add(tile)

                    if type == 'walls':
                        grass_tile_list = import_cut_graphic("Final/visuals/level/Tileset.png")
                        tile_surface = grass_tile_list[int(col)]
                        tile = StaticTile(tileSize, x, y, tile_surface)
                        tiles.add(tile)

                    if type == 'objects':
                        if col == '0':
                            tile = Object(tileSize, x, y, '4')
                            tiles.add(tile)
                        elif col == '1':
                            tile = Object(tileSize, x, y, '20')
                            tiles.add(tile)
                        elif col == '2':
                            tile = Object(tileSize, x, y, '25')
                            tiles.add(tile)
                        elif col == '3':
                            tile = Object(tileSize, x, y, '27')
                            tiles.add(tile)
                        elif col == '4':
                            tile = Object(tileSize, x, y, '26')
                            tiles.add(tile)
                        elif col == '5':
                            tile = Object(tileSize, x, y, '24')
                            tiles.add(tile)

                    if type == 'coins':
                        if col == '0':
                            tile = Coin(tileSize, x, y, 'Final/visuals/level/silver_coin')
                        elif col == '1':
                            tile = Coin(tileSize, x, y, 'Final/visuals/level/gold_coin')
                        tiles.add(tile)

                    if type == 'enemies':
                        sprite = Enemy(tileSize, x, y)
                        tiles.add(sprite)

                    if type == 'constraints':
                        barrier = Tile(tileSize, x, y)
                        tiles.add(barrier)

        return tiles
                    
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
        if playerx < screenWidth/4 and directionx < 0: 
            #sets world shift to opposite of player speed
            self.worldShift = 4
            #sets player speed to 0 (map moving creates illusion of player moving)
            player.speed = 0
        #checks if player is moving right and is at threshold coordinates
        elif playerx > 3*screenWidth/4 and directionx > 0:
            #sets world shift to opposite of player speed
            self.worldShift = -4
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
                    self.offset -= 100
                elif player.direction.x > 0:
                    dash.play()
                    self.worldShift = -100
                    player.spawn[0] -= 100
                    self.offset += 100

                self.dashAvailable = False

        if self.timer >= 120:
            self.dashAvailable = True
            
        if player.rect.y > 700:
        
            player.spawn[0] += self.offset
            player.spawn[0] -= self.offset
            self.worldShift = self.offset
            self.offset = 0
            

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
        for sprite in self.terrain_sprites.sprites():
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
        for sprite in self.terrain_sprites.sprites():
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

    def playerSetup(self, layout):

        for rowIndex, row in enumerate(layout):
            for colIndex, col in enumerate(row):
                x = colIndex * tileSize
                y = rowIndex * tileSize
                if col == '0':
                    sprite = Player((x, y), self.displaySurface)
                    self.player.add(sprite)
                if col == '1':
                    endpointSurface = pygame.image.load('Final/visuals/level/endpoint.png')
                    sprite = StaticTile(tileSize, x, y, endpointSurface)
                    self.goal.add(sprite)

    def enemyReverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprites, False):
                enemy.reverse()

    def checkDeath(self):
        if self.player.sprite.rect.top > screenHeight:
            self.loadMenu(self.currentLevel, 0)

    def checkWin(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.loadMenu(self.currentLevel, self.newMaxLevel)

    def run(self):
        """ 
        Description: Runs necessary methods for level.
        Parameters: None.
        Return: None.
        """

        self.wall_sprites.draw(self.displaySurface)
        self.wall_sprites.update(self.worldShift)

        self.objects_sprites.draw(self.displaySurface)
        self.objects_sprites.update(self.worldShift)

        self.terrain_sprites.draw(self.displaySurface)
        self.terrain_sprites.update(self.worldShift)

        self.coins_sprites.draw(self.displaySurface)
        self.coins_sprites.update(self.worldShift)

        self.enemy_sprites.draw(self.displaySurface)
        self.enemy_sprites.update(self.worldShift)
        self.constraints_sprites.update(self.worldShift)
        self.enemyReverse()

        self.goal.draw(self.displaySurface)
        self.goal.update(self.worldShift)

        self.player.update(self.worldShift)
        self.horizontalCollision()
        self.verticalCollision()
        self.cameraScroll()
        self.player.draw(self.displaySurface)

        self.checkDeath()
        self.checkWin()
        
        self.timer += 1
        
        #self.player.draw(self.displaySurface)
        #self.enemy.draw(self.displaySurface)

