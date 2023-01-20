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
pygame.mixer.init()

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *

# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for all sounds
collision_sound.set_volume(0.5)

# Variable to keep our main loop running
running = True


dirt = pygame.image.load("dirt.jpg")
dirt = pygame.transform.scale(dirt, (TILE_SIZE, TILE_SIZE)).convert()

# Our main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    # Update the position of our enemies and clouds
    enemies.update()
    clouds.update()

    for x in range(0, 15):
        for y in range(0, 20):
            screen.blit(dirt, (x*TILE_SIZE, y*TILE_SIZE))


    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player
        player.kill()

        # Stop any moving sounds and play the collision sound
        collision_sound.play()

        # Stop the loop
        running = False

    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(FPS)

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
