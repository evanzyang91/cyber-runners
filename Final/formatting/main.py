import pygame
#makes code from settings module available for use
from settings import *
#imports Level class from level module
from level import Level
from game_data import level1, level2, level3

#initializes pygame
pygame.init()

#creates screen
screen = pygame.display.set_mode((screenWidth, screenHeight))
#creates clock
clock = pygame.time.Clock()

level1_load = Level(level1, screen)
level2_load = Level(level2, screen)
level3_load = Level(level3, screen)

def main():
    """ 
    Mainline logic.
    """

    #sets window caption
    pygame.display.set_caption("CYBER // STRIKE") 

    background = pygame.Surface(screen.get_size())
    menu_screen = pygame.Surface(screen.get_size())

    menuloop = pygame.mixer.Sound("Final/sounds/menuloop.mp3")
    menuloop.set_volume(0.3)
    menuloop.play()

    play = pygame.mixer.Sound("Final/sounds/play.mp3")
    play.set_volume(0.3)

    background = background.convert()
    background = pygame.image.load("Final/visuals/level/background.jpg")
    menu_screen = pygame.image.load("Final/visuals/level/CYBERSTRIKE.png")

    menu = True
    run_level1 = False
    run_level2 = False
    run_level3 = False
    button = True

    #creates infinite loop until program closed
    running = True
    while running:

        #sets fps
        clock.tick(60)

        #fills screen black
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        if menu == True:
            screen.blit(menu_screen, (0,0))

        #event handling
        for event in pygame.event.get():
            #exits game loop
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if button:
                    if event.key == pygame.K_1:

                        if run_level1 == False:
                            play.play()
                        menu = False
                        run_level1 = True
                        #calls run method for level
                        level1_load.run()
                        menuloop.set_volume(0)
                        pygame.mixer.music.load("Final/sounds/gameloop1.mp3")
                        pygame.mixer.music.set_volume(0.05)
                        pygame.mixer.music.play(-1)
                        button = False
                        
                    elif event.key == pygame.K_2:
                        
                        if run_level2 == False:
                            play.play()
                        menu = False
                        run_level2 = True
                        #calls run method for level
                        level2_load.run()
                        menuloop.set_volume(0)
                        pygame.mixer.music.load("Final/sounds/gameloop2.mp3")
                        pygame.mixer.music.set_volume(0.05)
                        pygame.mixer.music.play(-1)
                        button = False
                        
                    elif event.key == pygame.K_3:
                        
                        if run_level3 == False:
                            play.play()
                        menu = False
                        run_level3 = True
                        #calls run method for level
                        level3_load.run()
                        menuloop.set_volume(0)
                        pygame.mixer.music.load("Final/sounds/gameloop3.mp3")
                        pygame.mixer.music.set_volume(0.05)
                        pygame.mixer.music.play(-1)
                        button = False
                  
        if run_level1:
            level1_load.run()
        
        if run_level2:
            level2_load.run()
            
        if run_level3:
            level3_load.run()

        #updates display
        pygame.display.flip()

    #exits pygame
    pygame.quit() 

main()