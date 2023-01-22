from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from player import *
from settings import *
import random
import pygame
from map import Map

def determine_scroll(old_scroll, player, map_size):
    scroll = old_scroll
    x = player.realpos[0] - SCREEN_WIDTH / 2
    y = player.realpos[1] - SCREEN_HEIGHT / 2
    scroll[0] = x
    scroll[1] = y
    if scroll[0] < 0:
        scroll[0] = 0
    if scroll[1] < 0:
        scroll[1] = 0
    if scroll[0] > map_size[0] - SCREEN_WIDTH:
        scroll[0] = map_size[0] - SCREEN_WIDTH
    if scroll[1] > map_size[1]-SCREEN_HEIGHT:
        scroll[1] = map_size[1] - SCREEN_HEIGHT

    return scroll

pygame.mixer.init()
scroll = [0, 0]
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = Player((2600,1600))
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
collision_sound = pygame.mixer.Sound("resources/Collision.ogg")
collision_sound.set_volume(0.5)

running = True

pygame.mouse.set_visible(False)
crosshair = pygame.transform.scale(
    pygame.image.load("resources/crosshair.png"),
    (CROSSHAIR_SIZE, CROSSHAIR_SIZE)
).convert_alpha()

map = Map()

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, map.size, scroll)
    scroll = determine_scroll(scroll, player, map.size)

    enemies.update()

    map.drawOn(screen, scroll)

    crosshair_pos = pygame.mouse.get_pos()
    screen.blit(crosshair, crosshair.get_rect(center=crosshair_pos))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        collision_sound.play()
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.mixer.music.stop()
pygame.mixer.quit()
