""" 
Authors: Evan Yang and Ethan Yang

Date: June 19, 2023

Purpose: Creates coin interface.
"""

import pygame

class UI():
    '''Class for coin counter UI.'''

    def __init__(self, surface):
        '''Initializer method.
        Takes display surface parameter.'''

        self.display_surface = surface

        #loads image of coin counter.
        self.coin = pygame.image.load('Final/visuals/level/coin_ui.png')
        #creates rectangle for coin counter
        self.coin_rect = self.coin.get_rect(topleft = (50, 61))
        #sets font of counter
        self.font = pygame.font.SysFont("Comic Sans", 30)

    def show_coins(self, amount):
        ''' 
        Updates and displays the number of coins.
        Takes amount of coins as parameter.
        '''

        #blits the coin ui 
        self.display_surface.blit(self.coin, self.coin_rect)
        #renders font and displays with amount of coints
        coin_amount_surf = self.font.render(str(amount), False, '#ffffff')
        #creates rect for new ui and sets position with offset
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4, self.coin_rect.centery))
        #blits entire coin ui 
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)