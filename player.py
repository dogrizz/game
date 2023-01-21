import pygame
from settings import *

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_PAGEUP,
    K_PAGEDOWN,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        rotor = pygame.image.load("resources/rotors.png")
        self.rotors_image = pygame.transform.scale(
            rotor, HELI_SIZE).convert_alpha()
        image = pygame.image.load("resources/heli.png")
        self.image = pygame.transform.scale(image, HELI_SIZE)
        self.surf = self.image.convert_alpha()
        self.surf.blit(self.rotors_image, (0, 0))
        self.rect = self.surf.get_rect()
        self.move_x = 0
        self.move_y = 0
        self.realpos = [self.rect.centerx, self.rect.centery]
        self.rotation = 0
        self.rotor_rotation = 0

    def update(self, pressed_keys, map_size, scroll):
        self.accelerate(pressed_keys)
        self.rotate(pressed_keys)
        self.move(map_size, scroll)
        self.redraw()
        self.deccelarate()

    def accelerate(self, pressed_keys):
        accel_speed = ACCELERATION_RATE
        if pressed_keys[K_UP]:
            self.move_y = max(-MAX_SPEED, self.move_y - accel_speed)
        if pressed_keys[K_DOWN]:
            self.move_y = min(MAX_SPEED, self.move_y + accel_speed)
        if pressed_keys[K_LEFT]:
            self.move_x = max(-MAX_SPEED, self.move_x - accel_speed)
        if pressed_keys[K_RIGHT]:
            self.move_x = min(MAX_SPEED, self.move_x + accel_speed)
        self.total_speed = abs(self.move_x) + abs(self.move_y)
        if self.total_speed > MAX_SPEED:
            self.move_x = MAX_SPEED * (self.move_x / self.total_speed)
            self.move_y = MAX_SPEED * (self.move_y / self.total_speed)

    def rotate(self, pressed_keys):
        if pressed_keys[K_PAGEDOWN]:
            self.rotation = self.rotation - 5

    def rotate(self, pressed_keys):
        if pressed_keys[K_PAGEDOWN]:
            self.rotation = self.rotation - 5
        if pressed_keys[K_PAGEUP]:
            self.rotation = self.rotation + 5

    def move(self, map_size, scroll):
        delta = [0, 0]
        if self.move_x != 0 and self.move_y != 0:
            delta[0] = self.move_x/1.444
            delta[1] = self.move_y/1.444
        else:
            delta[0] = self.move_x
            delta[1] = self.move_y

        self.rect.move_ip(delta[0],
                          delta[1])

        self.realpos[0] += delta[0]
        self.realpos[1] += delta[1]

        # TODO it snaps hard, investigate
        # keep player in center when screen starts scrolling
        if (scroll[0] > 0 and scroll[0] + SCREEN_WIDTH < map_size[0]):
            self.rect.centerx = SCREEN_WIDTH/2
        if (scroll[1] > 0 and scroll[1] + SCREEN_HEIGHT < map_size[1]):
            self.rect.centery = SCREEN_HEIGHT/2

        # keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # keep player on map
        if self.realpos[0] < 0:
            self.realpos[0] = 0
        if self.realpos[1] < 0:
            self.realpos[1] = 0
        if (self.realpos[0] > map_size[0] - HELI_SIZE[0]):
            self.realpos[0] = map_size[0] - HELI_SIZE[0]
        elif (self.realpos[1] > map_size[1]-HELI_SIZE[1]):
            self.realpos[1] = map_size[1]-HELI_SIZE[1]

    def deccel(self, val):
        if val == 0 or abs(val) < 0.5:
            return 0
        deccel_rate = DECCELERATION_RATE - \
            ((self.total_speed - abs(val)) / MAX_SPEED)
        if (val < 0):
            return val + deccel_rate
        elif (val > 0):
            return val - deccel_rate

    def deccelarate(self):
        self.move_y = self.deccel(self.move_y)
        self.move_x = self.deccel(self.move_x)

    def redraw(self):
        rotors_image = pygame.transform.rotate(
            self.rotors_image, self.rotor_rotation)
        center = self.rect.center
        image = pygame.transform.rotate(self.image, self.rotation)
        self.surf = image.convert_alpha()
        rotors = rotors_image
        rotor_rect = rotors.get_rect(
            center=(self.surf.get_width()/2, self.surf.get_height()/2))
        self.surf.blit(rotors, rotor_rect)
        self.rect = self.surf.get_rect(center=center)

        self.rotor_rotation += ROTOR_ROTATION
        if self.rotor_rotation >= 360:
            self.rotor_rotation = 0
