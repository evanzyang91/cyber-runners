import pygame
from game_data import levels

class Icon(pygame.sprite.Sprite):

    def __init__(self, pos, status, speed, path):
        super().__init__()
        self.path = path
        self.image = pygame.image.load(self.path)
        if status == 'open':
            self.status = 'open'
        else:
            self.status = 'closed'
        self.rect = self.image.get_rect(center = pos)

        self.endpoint = pygame.Rect(self.rect.centerx - (speed/2), self.rect.centery - (speed/2), speed, speed)

    def update(self):
        self.image = pygame.image.load(self.path)

class Cursor(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('Final/visuals/level/crosshair.png').convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos

class Menu():
    
    def __init__(self, start, maxLevel, surface, loadLevel):

        self.displaySurface = surface
        self.maxLevel = maxLevel
        self.currentLevel = start
        self.loadLevel = loadLevel

        self.moving = False
        self.moveDirection = pygame.math.Vector2(0, 0)
        self.speed = 8

        self.levelSetup()
        self.cursorSetup()

    def levelSetup(self):

        self.icons = pygame.sprite.Group()

        for index, data in enumerate(levels.values()):
            if index <= self.maxLevel:
                iconSprite = Icon(data['icon_pos'], 'open', self.speed, data['icon_img'])
            else:
                iconSprite = Icon(data['icon_pos'], 'closed', self.speed, data['icon_img'])
            self.icons.add(iconSprite)   

    def cursorSetup(self):

        self.cursor = pygame.sprite.GroupSingle()
        cursorSprite = Cursor(self.icons.sprites()[self.currentLevel].rect.center)
        self.cursor.add(cursorSprite)

    def drawPaths(self):
        points = [icon['icon_pos'] for index, icon in enumerate(levels.values()) if index <= self.maxLevel]
        pygame.draw.lines(self.displaySurface, 'red', False, points, 6)     

    def input(self):
        keys = pygame.key.get_pressed()

        if self.moving == False:
            if keys[pygame.K_RIGHT] and self.currentLevel < self.maxLevel:
                self.moveDirection = self.getMovement('next')
                self.currentLevel += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.currentLevel > 0:
                self.moveDirection = self.getMovement('prev')
                self.currentLevel -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.loadLevel(self.currentLevel)

    def getMovement(self, target):
        #gets start position coordinates
        start = pygame.math.Vector2(self.icons.sprites()[self.currentLevel].rect.center)
        if target == 'next':
            #gets coordinates of next level
            end = pygame.math.Vector2(self.icons.sprites()[self.currentLevel + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.icons.sprites()[self.currentLevel - 1].rect.center)
        #calculates coordinate distance and normalizes into vector length of 1 (gets direction instead of distance)
        return (end - start).normalize()

    def updateCursor(self):
        if self.moving and self.moveDirection:
            self.cursor.sprite.pos += self.moveDirection * self.speed
            target = self.icons.sprites()[self.currentLevel]
            if target.endpoint.collidepoint(self.cursor.sprite.pos):
                self.moving = False
                self.moveDirection = pygame.math.Vector2(0, 0)

    def run(self):
        self.input()
        self.updateCursor()
        self.cursor.update()
        if self.maxLevel > 0:
            self.drawPaths()
        self.icons.draw(self.displaySurface)
        self.cursor.draw(self.displaySurface)