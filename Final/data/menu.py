""" 
Authors: Evan Yang and Ethan Yang

Date: June 19, 2023

Purpose: Displays main menu screen for game.
"""

import pygame
from game_data import levels

class Icon(pygame.sprite.Sprite):
    ''' 
    Displays image rect for each level.
    '''

    def __init__(self, pos, speed, path):
        '''
        Initializes image rectangles. Takes position, speed of cursor, and image path.
        '''

        #initializes superclass
        super().__init__()
        
        self.path = path
        #loads image
        self.image = pygame.image.load(self.path).convert_alpha()
        #gets image rect
        self.rect = self.image.get_rect(center = pos)

        #creates endpoint for cursor as a small rectangle 
        #size of rectangle is set to speed so that the cursor does not pass without collision
        self.endpoint = pygame.Rect(self.rect.centerx - (speed/2), self.rect.centery - (speed/2), speed, speed)

    def update(self):
        '''
        Loads image again.
        '''
        self.image = pygame.image.load(self.path).convert_alpha()

class Cursor(pygame.sprite.Sprite):
    ''' 
    Cursor sprite that travels between level icons.
    '''

    def __init__(self, pos):
        ''' 
        Initialization of cursor sprite with position.
        '''
        super().__init__()

        self.pos = pos
        #loads image
        self.image = pygame.image.load('Final/visuals/level/crosshair.png').convert_alpha()
        #doubles size of image
        self.image = pygame.transform.scale2x(self.image)
        #sets center of cursor to position
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        ''' 
        Sets cursor to given position.
        '''
        self.rect.center = self.pos

class Menu():
    ''' 
    Displays main menu where switches between levels are displayed.
    '''
    
    def __init__(self, start, maxLevel, surface, loadLevel):
        ''' 
        Initializes main menu.
        Takes start level, maximum level unlocked, display surface, and loadLevel method from the main file.
        '''

        self.displaySurface = surface
        self.maxLevel = maxLevel
        self.currentLevel = start
        self.loadLevel = loadLevel

        #boolean value to prevent cursor being moved again while travelling
        self.moving = False
        #direction vector for cursor
        self.moveDirection = pygame.math.Vector2(0, 0)
        #speed of cursor
        self.speed = 8

        self.levelSetup()
        self.cursorSetup()

    def levelSetup(self):
        ''' 
        Adds level images to sprite group.
        '''

        #creates sprite group
        self.icons = pygame.sprite.Group()

        #iterates through levels dictionary values
        #data takes value of each level
        for data in levels.values():
            #passes level icon position, icon speed, and icon image path into Icon class to create/display sprites
            iconSprite = Icon(data['icon_pos'], self.speed, data['icon_img'])
            #adds sprite to sprite group
            self.icons.add(iconSprite)   

    def cursorSetup(self):
        ''' 
        Creates sprite for cursor.
        '''

        #creates group single
        self.cursor = pygame.sprite.GroupSingle()
        #calls Cursor class and gives position of current level center
        cursorSprite = Cursor(self.icons.sprites()[self.currentLevel].rect.center)
        self.cursor.add(cursorSprite)

    def drawPaths(self):
        ''' 
        Draws lines between level icons to indicate that they are unlocked.
        '''

        #creates list of points of available levels (less than or equal to max level)
        points = [icon['icon_pos'] for index, icon in enumerate(levels.values()) if index <= self.maxLevel]
        #draws lines between point(s)
        pygame.draw.lines(self.displaySurface, 'orange', False, points, 6)     

    def input(self):
        '''
        Gets user input to move cursor between levels.
        '''

        #gets keys that are being pressed
        keys = pygame.key.get_pressed()

        #checks if cursor is not already moving
        if self.moving == False:
            #checks if next level is unlocked, then moves cursor to next level if valid
            if keys[pygame.K_RIGHT] and self.currentLevel < self.maxLevel:
                self.moveDirection = self.getMovement('next')
                self.currentLevel += 1
                self.moving = True
            #checks if level is not already zero and moves cursor to previous level
            elif keys[pygame.K_LEFT] and self.currentLevel > 0:
                self.moveDirection = self.getMovement('prev')
                self.currentLevel -= 1
                self.moving = True
            #calls loadLevel method to enter playing state
            elif keys[pygame.K_RETURN]:
                self.loadLevel(self.currentLevel)

    def getMovement(self, target):
        ''' 
        Calculates vector (direction) of cursor movement.
        Takes target variable which contains either 'next' or 'prev' for indicated level.
        '''

        #gets start position coordinates (center of current level)
        start = pygame.math.Vector2(self.icons.sprites()[self.currentLevel].rect.center)
        #checks if target level is the next or previous
        if target == 'next':
            #gets coordinates of next level center
            end = pygame.math.Vector2(self.icons.sprites()[self.currentLevel + 1].rect.center)
        else:
            #gets coordinates of previous level center
            end = pygame.math.Vector2(self.icons.sprites()[self.currentLevel - 1].rect.center)
        #calculates coordinate distance and normalizes into vector length of 1 (gets direction instead of distance)
        return (end - start).normalize()

    def updateCursor(self):
        ''' 
        Updates cursor position.
        '''

        #checks if cursor is in movement and there is a direction
        if self.moving and self.moveDirection:
            #moves the cursor position in direction at certain speed
            self.cursor.sprite.pos += self.moveDirection * self.speed
            #gets target point of cursor
            target = self.icons.sprites()[self.currentLevel]
            #checks if target point collides with cursor
            if target.endpoint.collidepoint(self.cursor.sprite.pos):
                #sets moving to false
                self.moving = False
                #resets cursor direction to 0, 0
                self.moveDirection = pygame.math.Vector2(0, 0)

    def run(self):
        ''' 
        Calls methods to make main menu function
        '''

        self.input()
        self.updateCursor()
        self.cursor.update()
        #only draws lines when more than one level is unlocked
        if self.maxLevel > 0:
            self.drawPaths()
        self.icons.draw(self.displaySurface)
        self.cursor.draw(self.displaySurface)

        self.title = pygame.image.load('Final/visuals/level/CYBERSTRIKE.png').convert_alpha()
        self.displaySurface.blit(self.title, (0, 0))