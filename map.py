import pygame
from settings import *

tiles = {}


def load_tile(filename):
    tile = pygame.image.load("resources/"+filename)
    tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE)).convert()
    return tile


class Map():
    def __init__(self):
        self.tiles_dimensions = (30, 40)
        self.size = (
            self.tiles_dimensions[0] * TILE_SIZE, self.tiles_dimensions[1] * TILE_SIZE)
        tiles[0] = load_tile("dirt.jpg")

    def drawOn(self, screen, scroll):
        for x in range(0, self.tiles_dimensions[0]):
            for y in range(0, self.tiles_dimensions[1]):
                screen.blit(
                    tiles[0],
                    (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1])
                )
