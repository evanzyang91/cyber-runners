import pygame
from tiles import AnimatedTile
import random

class Enemy(AnimatedTile):

    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'Final/visuals/enemies/walk')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = random.randint(3, 5)

    def move(self):
        self.rect.x += self.speed

    def reverseImage(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverseImage()