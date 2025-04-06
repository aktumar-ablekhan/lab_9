#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0
LEVEL = 0 

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

# Loading and playing background music
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)  # Loop the background music indefinitely

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Load different coin images and resize them 
coin_images = [
    pygame.transform.scale(pygame.image.load("coin.png"), (50, 50)),   # Gold
    pygame.transform.scale(pygame.image.load("silver.png"), (40, 40)), # Silver
    pygame.transform.scale(pygame.image.load("bronze.png"), (30, 30))  # Bronze
]

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  

    def move(self):
        global SCORE, SPEED, LEVEL
        self.rect.move_ip(0, SPEED + LEVEL)  
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
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

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = random.randint(0, 2)  # 0 = gold, 1 = silver, 2 = bronze
        self.image = coin_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, 300))

    def move(self):
        self.rect.move_ip(0, (SPEED + LEVEL) // 2)  
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def reset(self):
        self.index = random.randint(0, 2)
        self.image = coin_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, 300))

#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    
    # Draw HUD
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coins_collected = font_small.render("Coins: " + str(COINS), True, BLACK)
    level_text = font_small.render("Level: " + str(LEVEL), True, RED)  # NEW
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coins_collected, (SCREEN_WIDTH - 120, 10))
    DISPLAYSURF.blit(level_text, (150, 10))  # NEW

    # Move and Re-draw all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Coin collision
    if pygame.sprite.spritecollideany(P1, coins):
        if C1.index == 0:       # Gold
            COINS += 15
        elif C1.index == 1:     # Silver
            COINS += 10
        else:                   # Bronze
            COINS += 5
        LEVEL = COINS // 50 
        C1.reset()

    # Player hits enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
        
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)
