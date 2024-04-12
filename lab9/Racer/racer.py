# Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initialzing
pygame.init()



# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
COINS = 0
SCORE = 0

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, RED)

background = pygame.image.load("Racer/AnimatedStreet.png")
bg_img = pygame.image.load("Racer/black-background.jpg")

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


def get_random_position(exclude_group):
    while True:
        new_position = (random.randint(40, SCREEN_WIDTH - 40), 0)
        new_sprite = pygame.sprite.Sprite()
        new_sprite.rect = pygame.Rect(new_position, (60, 60))
        if not pygame.sprite.spritecollideany(new_sprite, exclude_group):
            return new_position


class Enemy(pygame.sprite.Sprite):
    def __init__(self, exclude):
        super().__init__()
        self.image = pygame.image.load("Racer/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = get_random_position(exclude)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self, exclude):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("Racer/transparent_coin.png"),
            (60, 60),
        )
        self.rect = self.image.get_rect()
        self.rect.center = get_random_position(exclude)
        self.weight = random.choice(
            [1, 2, 5]
        )  # Assign a weight randomly from a set of weights

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = get_random_position(enemies)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Racer/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


# Setting up Sprites
coines = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


P1 = Player()
E1 = Enemy(coines)
C1 = Coin(enemies)

# Creating Sprites Groups
coines.add(C1)
enemies.add(E1)
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

coins_since_last_speed_increase = (
    0  # Track the number of coins collected since the last speed increase
)

# Game Loop
while True:

    # Cycles through all events occuring
    for event in pygame.event.get():
        # if event.type == INC_SPEED:
        #       SPEED += 0.1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(f"Lap: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    coinsssss = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(coinsssss, (300, 10))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("Racer/crash.wav").play()
        time.sleep(1)

        bg_x = (DISPLAYSURF.get_width() - bg_img.get_width()) / 2
        bg_y = (DISPLAYSURF.get_height() - bg_img.get_height()) / 2
        DISPLAYSURF.blit(bg_img, (bg_x, bg_y))
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if pygame.sprite.spritecollideany(P1, coines):
        coin_collected = pygame.sprite.spritecollideany(
            P1, coines
        )  # Get the coin sprite
        COINS += coin_collected.weight
        coin_collected.kill()  # Remove the coin sprite that's been collected
        C1 = Coin(enemies)  # Create a new coin
        coines.add(C1)  # Add the new coin to the coines group
        all_sprites.add(C1)  # Add the new coin to all_sprites group

        coins_since_last_speed_increase += (
            1  # Increment the count of coins collected since the last speed increase
        )

        # Increase speed every 5 coins
        if coins_since_last_speed_increase >= 5:
            SPEED += 2  # Increase speed by 2 units
            coins_since_last_speed_increase = (
                0  # Reset the count for the next speed increase
            )

    pygame.display.update()
    FramePerSec.tick(FPS)