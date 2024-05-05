import pygame
#makes code from settings module available for use
from settings import *
#imports Level class from level module
from level import Level
from game_data import level0
from menu import Menu

class Game:
    
    def __init__(self):

        self.maxLevel = 0        
        self.menu = Menu(0, self.maxLevel, screen, self.loadLevel)
        self.status = 'menu'

    def loadLevel(self, currentLevel):
        self.level = Level(currentLevel, screen, self.loadMenu)
        self.status = 'level'

    def loadMenu(self, currentLevel, newMaxLevel):
        if newMaxLevel > self.maxLevel:
            self.maxLevel = newMaxLevel
        self.menu = Menu(currentLevel, self.maxLevel, screen, self.loadLevel)
        self.status = 'menu'

    def run(self):
        if self.status == 'menu':
            self.menu.run()
        else:
            self.level.run()

#initializes pygame
pygame.init()

#creates screen
screen = pygame.display.set_mode((screenWidth, screenHeight))
#creates clock
clock = pygame.time.Clock()
game = Game()

def main():
    """ 
    Mainline logic.
    """

    #sets window caption
    pygame.display.set_caption("CYBER // STRIKE") 

    background = pygame.Surface(screen.get_size())

    background = background.convert()
    background = pygame.image.load("Final/visuals/level/background.jpg")

    #creates infinite loop until program closed
    running = True
    while running:

        #sets fps
        clock.tick(60)

        #fills screen black
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        #event handling
        for event in pygame.event.get():
            #exits game loop
            if event.type == pygame.QUIT:
                running = False

        #level.run()
        game.run()

        #updates display
        pygame.display.flip()
        

    #exits pygame
    pygame.quit() 

main()