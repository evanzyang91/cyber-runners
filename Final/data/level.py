"""
Author: Ethan Yang and Evan Yang
Date: June 19, 2023
Purpose: Creates level images and sprites.
"""

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
from healthbar import ScoreKeeper
from layers import levels
from ui import UI

class Level():
    '''Creates level'''

    def __init__(self, currentLevel, surface, loadMenu, changeCoins, resetCoins):
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
        #takes data of current level
        data = levels[self.currentLevel]
        #takes next level value
        self.newMaxLevel = data['unlock']

        #player setup
        #imports csv list
        player_layout = import_csv_layout(data['player'])
        #creates sprite groups
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        #calls method to setup player
        self.playerSetup(player_layout)

        #terrain setup
        #imports csv list
        terrain_layout = import_csv_layout(data['terrain'])
        #calls method to place tiles
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
        self.invincibilityTimer = 0

        self.hp = 100
        
        self.changeCoins = changeCoins
        self.resetCoins = resetCoins


    def levelSetup(self, layout, type):
        """ 
        Description: Places sprites for csv layouts.
        Parameters: Level layout list and type (tile layer name).
        Return: None.
        """

        #creates sprite group for tiles
        tiles = pygame.sprite.Group()

        #creates sprite for health
        self.healthbar = pygame.sprite.Group()

        #iterates through each string in map list
        #takes row position and row value 
        for rowIndex, row in enumerate(layout):
            #iterates through each character in row string
            #takes character position and character value
            for colIndex, col in enumerate(row):
                #-1 represents empty block
                if col != "-1":
                    #sets x and y coordinates using char indexes
                    x = colIndex * tileSize
                    y = rowIndex * tileSize
                    
                    #checks if layer is terrain
                    if type == 'terrain':
                        #imports cut tiles from tileset
                        terrain_tile_list = import_cut_graphic("Final/visuals/level/Tileset.png")
                        #creates surface for each tile
                        tile_surface = terrain_tile_list[int(col)]
                        #creates tile at respective coordinates
                        tile = StaticTile(tileSize, x, y, tile_surface)
                        #adds to sprite group
                        tiles.add(tile)

                    #places background wall tiles
                    if type == 'walls':
                        wall_tile_list = import_cut_graphic("Final/visuals/level/Tileset.png")
                        tile_surface = wall_tile_list[int(col)]
                        tile = StaticTile(tileSize, x, y, tile_surface)
                        tiles.add(tile)

                    #places background detail images
                    if type == 'objects':
                        #uses index to determine which picture to place
                        #index is found in csv file
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

                    #places coins
                    if type == 'coins':
                        #silver coins
                        if col == '0':
                            tile = Coin(tileSize, x, y, 'Final/visuals/level/silver_coin', 1)
                        #gold coins
                        elif col == '1':
                            tile = Coin(tileSize, x, y, 'Final/visuals/level/gold_coin', 2)
                        tiles.add(tile)

                    #places enemies
                    if type == 'enemies':
                        sprite = Enemy(tileSize, x, y)
                        tiles.add(sprite)

                    #places enemy contraints/barriers 
                    if type == 'constraints':
                        barrier = Tile(tileSize, x, y)
                        tiles.add(barrier)

        #returns sprite group of tiles
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
        elif playerx > 3*(screenWidth/4) and directionx > 0:
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

        #creates sound for dash
        dash = pygame.mixer.Sound("Final/sounds/dash.mp3")
        dash.set_volume(0.1)

        #makes player dash
        if keys[pygame.K_c]:
            if self.dashAvailable == True:
                #sets timer that increases every frame
                self.timer = 0
                #simulates dash by moving world instantly
                if player.direction.x < 0:
                    dash.play()
                    self.worldShift = 100
                elif player.direction.x > 0:
                    dash.play()
                    self.worldShift = -100

                self.dashAvailable = False

        #allows player to dash again after 2 seconds
        if self.timer >= 120:
            self.dashAvailable = True
            
        if player.rect.y > 700:
            player.healthy = True

    def coinCollision(self):
        ''' 
        Checks collision of player with coins.
        '''
        
        #creates coin collection sound
        coin_sound = pygame.mixer.Sound("Final/sounds/coin.mp3")
        coin_sound.set_volume(0.5)

        #checks for collision between player and coins
        #destroys coin sprite after collision
        collided = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)

        if collided:
            for coin in collided:
                #adds coin value 
                self.changeCoins(coin.value)
                coin_sound.play()


    def enemyCollision(self):
        ''' 
        Checks for collision between player and enemies.
        '''

        hurt = pygame.mixer.Sound("Final/sounds/hurt.mp3")
        hurt.set_volume(0.5)
        
        enemy_die = pygame.mixer.Sound("Final/sounds/enemy_die.mp3")
        enemy_die.set_volume(0.3)

        #initializes player sprite
        player = self.player.sprite
        #checks if player collides with enemy
        enemyCollisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        #creates health bar
        health_bar = ScoreKeeper(50, 50, 200, 20, self.hp, 100)
        self.healthbar.add(health_bar)

        #resets player health if contidion met
        if player.healthy:
            self.hp = 100
            health_bar.update_hp(self.hp)

        if enemyCollisions:
            #iterates through each enemy in collision
            for enemy in enemyCollisions:
                enemyCenter = enemy.rect.centery
                enemyTop = enemy.rect.top
                playerBottom = self.player.sprite.rect.bottom
                #checks if player bottom is in between enemy center and top (player has hit enemy from above)
                if enemyTop < playerBottom < enemyCenter and self.player.sprite.direction.y >= 0:
                    #kills enemy
                    enemy_die.play()
                    enemy.kill()
                else:
                    #checks if player invincible
                    if player.invincible == False:
                        #resets invincibility timer (activates after player is hit)
                        self.invincibilityTimer = 0
                        #subtracts health
                        self.hp -= 25
                        health_bar.update_hp(self.hp)
                        hurt.play()
                    #makes player invincible for short duration after hit
                    player.invincible = True

        #2 second timer
        if self.invincibilityTimer >= 120:
            player.invincible = False

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
        '''Checks for player vertical collisions. Floor and ceiling.'''

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
                    #resets player direction so does not stick to cieling
                    player.direction.y = 0
                #for moving down
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    #resets direction so player does not fall through floor
                    player.direction.y = 0
                    #allows player to jump again after touching floor
                    player.jumpsAvailable = True

    def playerSetup(self, layout):
        '''Sets up player start position and end goal sprite.
        Takes layout of player start and end.'''

        #iterates through each row in csv 
        for rowIndex, row in enumerate(layout):
            #iterates through each value in csv list
            for colIndex, col in enumerate(row):
                #sets x and y position of tile
                x = colIndex * tileSize
                y = rowIndex * tileSize
                #checks if index is 0 for player start
                if col == '0':
                    #places player at respective coordinates
                    sprite = Player((x, y), self.displaySurface)
                    self.player.add(sprite)
                #checks if index is 1 for player end
                if col == '1':
                    #creates end point image and places at respective coordinates
                    endpointSurface = pygame.image.load('Final/visuals/level/endpoint.png')
                    sprite = StaticTile(tileSize, x, y, endpointSurface)
                    self.goal.add(sprite)
    
    def checkDeath(self):
        ''' 
        Checks for player death.
        '''
        
        die = pygame.mixer.Sound("Final/sounds/die.mp3")
        die.set_volume(0.5)

        #checks if player has fallen off screen or hp reached 0
        if self.player.sprite.rect.top > screenHeight or self.hp == 0:
            #brings back to main menu and resets coins
            self.loadMenu(self.currentLevel, 0)
            self.resetCoins()
            die.play()

    def checkWin(self):
        ''' 
        Checks for player collision with goal.
        '''

        complete = pygame.mixer.Sound("Final/sounds/complete.mp3")
        complete.set_volume(0.3)

        #checks if player has collided with goal sprite
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            #loads menu screen
            self.loadMenu(self.currentLevel, self.newMaxLevel)
            complete.play()
            
    def enemyReverse(self):
        '''Reverses enemy direction upon collision with invisible barriers.'''

        #iterates through each enemy
        for enemy in self.enemy_sprites.sprites():
            #checks for collision with constraint barrier
            if pygame.sprite.spritecollide(enemy, self.constraints_sprites, False):
                #reverses enemy direction
                enemy.reverse()

    def run(self):
        """ 
        Description: Runs necessary methods for level.
        Parameters: None.
        Return: None.
        """

        #draws and updates all tile positions
        self.wall_sprites.draw(self.displaySurface)
        self.wall_sprites.update(self.worldShift)

        self.healthbar.draw(self.displaySurface)  # Draw the health bar


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

        self.player.update(self.worldShift)
        self.horizontalCollision()
        self.verticalCollision()
        self.cameraScroll()
        self.player.draw(self.displaySurface)
        self.goal.draw(self.displaySurface)
        self.goal.update(self.worldShift)
        
        self.checkDeath()
        self.checkWin()
        
        self.coinCollision()
        self.enemyCollision()
        
        self.timer += 1
        self.invincibilityTimer += 1
        
        #self.player.draw(self.displaySurface)
        #self.enemy.draw(self.displaySurface)

