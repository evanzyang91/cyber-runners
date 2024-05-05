#imports walk method from python operating system
#walk returns the path, name, and files in a directory
from os import walk
import pygame

def importFolder(path):
    surfaces = []
    
    for _,__,imgNames in walk(path):
        for image in imgNames:
            directPath = path + "/" + image
            imageSurface = pygame.image.load(directPath).convert_alpha()
            if 'player' in path:
                imageSurface = pygame.transform.scale_by(imageSurface, 1.88)
            surfaces.append(imageSurface)

    return surfaces