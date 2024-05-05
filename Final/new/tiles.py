import pygame
from importing import importFolder

class Tile(pygame.sprite.Sprite):

    def __init__(self, size, x, y):
        
        super().__init__()
        self.image = pygame.Surface((size, size))
        
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, xShift):
        self.rect.x += xShift

class StaticTile(Tile):

    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class Object(StaticTile):

    def __init__(self, size, x, y, name):
        super().__init__(size, x, y, pygame.image.load('Final/visuals/level/bg_objects/' + name + '.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x, offset_y))

class AnimatedTile(Tile):

    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = importFolder(path)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]

    def animate(self):
        self.frameIndex += 0.2
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]

    def update(self, xShift):
        self.animate()
        self.rect.x += xShift

class Coin(AnimatedTile):

    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        centerX = x + int(size / 2)
        centerY = y + int(size / 2)
        self.rect = self.image.get_rect(center = (centerX, centerY))