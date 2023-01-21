import pygame
from settings import *

tiles = {}


def load_tile(filename):
    tile = pygame.image.load("resources/"+filename)
    tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE)).convert()
    return tile


def load_map(filename):
    map = []
    with open("resources/"+filename, "r") as file:
        line = file.readline().strip()
        while line != '':
            map.append(list(line))
            line = file.readline().strip()
    
    return map


class Map():
    def __init__(self):
        tiles['0'] = load_tile("dirt.jpg")
        tiles['1'] = load_tile("desert.png")
        self.map = load_map("map1.txt")
        self.tiles_dimensions = (len(self.map[0]), len(self.map))
        self.size = (
            self.tiles_dimensions[0] * TILE_SIZE, self.tiles_dimensions[1] * TILE_SIZE)

    def drawOn(self, screen, scroll):
        for x in range(0, self.tiles_dimensions[0]):
            for y in range(0, self.tiles_dimensions[1]):
                screen.blit(
                    tiles[self.map[y][x]],
                    (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1])
                )
