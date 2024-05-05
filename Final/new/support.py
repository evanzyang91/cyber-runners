from csv import reader
import pygame
from settings import tileSize

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
    
def import_cut_graphic(path):

    surface = pygame.image.load(path).convert_alpha()
    tile_x = int(surface.get_size()[0] / tileSize)
    tile_y = int(surface.get_size()[1] / tileSize)

    cut_tiles = []
    for row in range(tile_y):
        for col in range(tile_x):
            x = col * tileSize
            y = row * tileSize
            new_surf = pygame.Surface((tileSize, tileSize))
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tileSize, tileSize))
            cut_tiles.append(new_surf)

    return cut_tiles
