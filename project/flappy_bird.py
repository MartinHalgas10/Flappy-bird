import pygame
import random
from pygame.locals import *

global timer
global running
global score
score = 0
running = True
timer = 30

lose_scrren_run = True

class Bird(pygame.sprite.Sprite):
    def __init__(self, vector, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (70, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (vector.x, vector.y)
        self.velocity = 0

    def update(self):
        self.rect.y += self.velocity
        self.velocity += 0.3

    def flap(self):
        self.velocity -= 7

    def checkCollision(self, sprite2):
        col = pygame.sprite.collide_rect(self, sprite2)
        global running
        if col == True or not screen.get_rect().contains(self):
            running = False


class Pipe(pygame.sprite.Sprite):
    def __init__(self, height, image, orientation):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (75, height))
        self.rect = self.image.get_rect()
        if orientation == 2:
            self.image = pygame.transform.flip(self.image, 0, 1)
            self.rect.topleft = (screen_width - 65, 0)
        else:
            self.rect.topleft = (screen_width - 65, screen_height - height)
        self.velocity = 8
        self.point = False
        self.orientation = orientation
    
    def update(self):
        self.rect.x -= self.velocity

def genrate_pipes():
    global timer 
    if timer == 0:
        height = random.randint(30, screen_height / 2)
        pipe1 = Pipe(height, pipe_image, 2)
        pipe2 = Pipe(screen_height - height - 200, pipe_image, 1)
        pipe_group.add(pipe1)
        pipe_group.add(pipe2)
        timer = 60
    else:
        timer -= 1

def print_text(text, font, x, y):
    text = font.render(text, True, ( 255, 0, 0))
    screen.blit(text, ( x, y))

pygame.init()
pygame.mixer.init()
channel1 = pygame.mixer.Channel(1)
channel2 = pygame.mixer.Channel(2)

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

flap_sound = pygame.mixer.Sound("resources/sounds/flap.mp3")
flap_sound.set_volume(0.1)

point_sound = pygame.mixer.Sound("resources/sounds/point.mp3")
point_sound.set_volume(0.1)

bg = pygame.transform.scale(pygame.image.load("resources/images/background.png"), (screen_width, screen_height))
lose_bg_bad = pygame.transform.scale(pygame.image.load("resources/images/lose_screen_bad.jpg"), (screen_width, screen_height))
lose_bg_good = pygame.transform.scale(pygame.image.load("resources/images/lose_screen_good.png").convert_alpha(), (screen_width, screen_height))

pipe_image = pygame.image.load('resources/images/pipe.png').convert_alpha()
pipe_group = pygame.sprite.Group()

bird_image = pygame.image.load('resources/images/bird.png').convert_alpha()
bird_group = pygame.sprite.Group()
bird_pos = pygame.Vector2(screen.get_width() / 10, screen.get_height() / 2)
bird = Bird(bird_pos, bird_image)
bird_group.add(bird)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE: 
                bird.flap()
                channel1.play(flap_sound)

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(bg, (0, 0))

    print_text('Score: ' + str(score), pygame.font.SysFont("arialblack", 40), 0, 0)

    for pipe in pipe_group:
        bird.checkCollision(pipe)
        if bird.rect.x >= pipe.rect.x:
            channel2.play(point_sound)
            if pipe.point == False and pipe.orientation == 1:
                score += 1
                pipe.point = True
        if pipe.rect.x <= -30:
            pipe.kill()

    # RENDER YOUR GAME HERE

    bird_group.update()
    pipe_group.update()
    bird_group.draw(screen)
    pipe_group.draw(screen) 

    genrate_pipes()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

while lose_scrren_run:

    if score >= 10:
        screen.blit(lose_bg_good, (0, 0))
    else:
        screen.blit(lose_bg_bad, (0, 0))

    font = pygame.font.SysFont("arialblack", 40)
    score_text = 'Your Score is: ' + str(score)

    print_text(score_text, font, screen_width / 2 - 200, screen_height / 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lose_scrren_run = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                 lose_scrren_run = False
    
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()