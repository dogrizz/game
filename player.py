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
        rotor = pygame.image.load("rotors.png")
        self.rotors_image = pygame.transform.scale(rotor, HELI_SIZE)
        image = pygame.image.load("heli.png")
        self.image = pygame.transform.scale(image, HELI_SIZE)
        self.surf = self.image.convert_alpha()
        self.surf.blit(self.rotors_image.convert_alpha(), (0, 0))
        self.rect = self.surf.get_rect()
        self.move_x = 0
        self.move_y = 0
        self.next_rotation = 0
        self.rotation = 0
        self.last_rotation_time = 0
        self.rotation_scheduled = False
        self.rotor_rotation = 0

    def update(self, pressed_keys):
        self.accelerate(pressed_keys)
        self.schedule_rotation(pressed_keys)
        self.move()
        self.rotate()
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

    def schedule_rotation(self, pressed_keys):
        if self.rotation_scheduled:
            return
        if pressed_keys[K_PAGEDOWN]:
            self.rotation_scheduled = True
            self.next_rotation = self.rotation - 45
        if pressed_keys[K_PAGEUP]:
            self.rotation_scheduled = True
            self.next_rotation = self.rotation + 45

    def rotate(self):
        can_do_another = pygame.time.get_ticks() - self.last_rotation_time >= ROTATION_TIMEOUT
        if (self.rotation_scheduled and can_do_another):
            self.rotation = self.next_rotation
            self.last_rotation_time = pygame.time.get_ticks()
            self.rotation_scheduled = False

    def move(self):
        if self.move_x != 0 and self.move_y != 0:
            self.rect.move_ip(self.move_x/1.444, self.move_y/1.444)
        else:
            self.rect.move_ip(self.move_x, self.move_y)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

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
        rotors = rotors_image.convert_alpha()
        rotor_rect = rotors.get_rect(
            center=(self.surf.get_width()/2, self.surf.get_height()/2))
        self.surf.blit(rotors, rotor_rect)
        self.rect = self.surf.get_rect(center=center)

        self.rotor_rotation += ROTOR_ROTATION
        if self.rotor_rotation >= 360:
            self.rotor_rotation = 0
