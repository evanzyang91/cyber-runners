"""
Author: Ethan Yang and Evan Yang
Date: June 19, 2023
Purpose: intiailizes layers of each level
"""

#Initializes level0 layers
level0 = {
    'icon_pos':(205, 220),  # Position of the level's icon
    'unlock': 1,  # Level unlock status
    'coins':'Final/leveldata/0/level0_coins.csv',  # Path to coins data file
    'constraints':'Final/leveldata/0/level0_constraints.csv',  # Path to constraints data file
    'enemies':'Final/leveldata/0/level0_enemies.csv',  # Path to enemies data file
    'objects':'Final/leveldata/0/level0_objects.csv',  # Path to objects data file
    'player':'Final/leveldata/0/level0_player.csv',  # Path to player data file
    'terrain':'Final/leveldata/0/level0_terrain.csv',  # Path to terrain data file
    'walls':'Final/leveldata/0/level0_walls.csv',  # Path to walls data file
    'icon_img':'Final/visuals/level/level0_cover.png'  # Path to level's icon image
}

#Initializes level1 layers
level1 = {
    'icon_pos':(545, 550),
    'unlock': 2,
    'coins':'Final/leveldata/1/level1_coins.csv',
    'constraints':'Final/leveldata/1/level1_constraints.csv',
    'enemies':'Final/leveldata/1/level1_enemies.csv',
    'objects':'Final/leveldata/1/level1_objects.csv',
    'player':'Final/leveldata/1/level1_player.csv',
    'terrain':'Final/leveldata/1/level1_terrain.csv',
    'walls':'Final/leveldata/1/level1_walls.csv',
    'icon_img':'Final/visuals/level/level1_cover.png'
}

#Initializes level2 layers
level2 = {
    'icon_pos':(965, 350),
    'unlock': 2,
    'coins':'Final/leveldata/2/level2_coins.csv',
    'constraints':'Final/leveldata/2/level2_constraints.csv',
    'enemies':'Final/leveldata/2/level2_enemies.csv',
    'objects':'Final/leveldata/2/level2_objects.csv',
    'player':'Final/leveldata/2/level2_player.csv',
    'terrain':'Final/leveldata/2/level2_terrain.csv',
    'walls':'Final/leveldata/2/level2_walls.csv',
    'icon_img':'Final/visuals/level/level2_cover.png'
}

levels = {
    0: level0,  # Level 0 dictionary
    1: level1,  # Level 1 dictionary
    2: level2  # Level 2 dictionary
}