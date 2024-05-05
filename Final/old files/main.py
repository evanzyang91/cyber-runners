import pygame
#makes code from settings module available for use
from settings import *
#imports Level class from level module
from level import Level

#initializes pygame
pygame.init()

#creates screen 
screen = pygame.display.set_mode((screenWidth, screenHeight))
#creates clock
clock = pygame.time.Clock()
level = Level(map, screen)

def main():
    """ 
    Mainline logic.
    """

    #sets window caption
    pygame.display.set_caption("Platformer Demo") 
    
    #creates infinite loop until program closed
    running = True
    while running:

        #sets fps
        clock.tick(60)

        #event handling
        for event in pygame.event.get():
            
            #exits game loop
            if event.type == pygame.QUIT:
                running = False 

        #fills screen black
        screen.fill((0, 0, 0))

        #calls run method for level
        level.run()

        #updates display
        pygame.display.flip()

    #exits pygame
    pygame.quit() 

main()