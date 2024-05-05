""" 
Authors: Evan Yang and Ethan Yang

Date: June 19, 2023

Purpose: Contains functions to import csvs and cut tilesets.
"""

#imports reader from csv (spreadsheet) library
from csv import reader
import pygame
from settings import tileSize

def import_csv_layout(path):
    ''' 
    Imports csv file and places into a list so it can be iterated through.
    Takes path to csv file.
    Returns list with all integer csv values (terrain map).
    '''

    #empty list for csv values (comma seperated values)
    terrain_map = []
    #opens csv file using path
    with open(path) as map:
        #seperates csv value by using the commas
        level = reader(map, delimiter=',')
        #iterates through each row 
        for row in level:
            #adds each row to the empty list
            terrain_map.append(list(row))
        #returns list with csv values
        return terrain_map
    
def import_cut_graphic(path):
    ''' 
    Cuts tileset into individual images.
    Takes path for tileset.
    Returns list of images that have been cut from tileset.
    '''

    #creates surface for tileset image.
    surface = pygame.image.load(path).convert_alpha()
    #gets number of rows and columns in tileset
    tile_x = int(surface.get_size()[0] / tileSize)
    tile_y = int(surface.get_size()[1] / tileSize)

    #creates empty list for cut images
    cut_tiles = []
    #iterates through each row in tileset
    for row in range(tile_y):
        #iterates through each column in tileset
        for col in range(tile_x):
            #sets x and y position of current tile 
            x = col * tileSize
            y = row * tileSize
            #creates new surface for cut tile
            new_surf = pygame.Surface((tileSize, tileSize))
            #blits cut image onto new surface
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tileSize, tileSize))
            #adds cut tile to list
            cut_tiles.append(new_surf)

    #returns list of cut tiles
    return cut_tiles
