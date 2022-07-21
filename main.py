import pygame
from random import randint
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Takli Bird')
bg = pygame.image.load("nature.png")
bg = pygame.transform.scale(bg, (800, 600))

done = False

def text_objects(text, font):
    textSurface = font.render(text, True, (150,0,150))
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',80)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((400),(200))
    screen.blit(TextSurf, TextRect)

def play_game(birdY, pipeX, pipeY):
    if 10 < pipeX < 200:
        #print(pipeY - birdY)
        if (pipeY - birdY) < 50:
            #print("Return True")
            return True
    if birdY > 400:
        return True
    return False



class Pipe:
    def __init__(self, i):
        self.pipe1 = pygame.image.load("tools.png")
        self.pipe2 = pygame.image.load("tools.png")
        self.pipe1X = 700 + (200 * i)
        self.pipe2X = 700 + (200 * i)
        self.pipe1_len = 0
        self.pipe2_len = 0
        self.transform_pipes()
        self.pipe1Y = 0
        self.pipe2Y = 600 - self.pipe2_len

    def transform_pipes(self):
        self.pipe1_len = randint(100,300)
        self.pipe2_len = 475 - self.pipe1_len
        self.pipe1 = pygame.transform.scale(self.pipe1, (175, self.pipe1_len))
        self.pipe2 = pygame.transform.scale(self.pipe2, (175, self.pipe2_len))

    def move_pipes(self):
        self.pipe1X -= 1.2
        self.pipe2X -= 1.2

    def reset_pipes(self):
        self.pipe1X = 800
        self.pipe2X = 800

    def detect_collision(self, bird_height, bird_x):
        collided = False
        if not self.pipe1X < bird_x < self.pipe1X + 160:
            return collided
        if bird_height <= self.pipe1_len + 2:
            print("Collision")
            collided = True
        if bird_height >= self.pipe2Y - 2:
            collided = True
        return collided

class bird:
    def __init__(self):
        self.chewchew = pygame.image.load("bird.png")
        self.birdX = 150
        self.birdY = 300
        self.bird_accelerate = 0
        self.allangles = {}

    def move_bird(self):
        self.bird_accelerate += 0.2
        if self.bird_accelerate > 4.0:
            self.bird_accelerate = 4.0
        self.birdY += self.bird_accelerate

    def create_angled_birds(self):
        for i in range(-5, 5):
            angle = (i * 10) * 1.5
            angle = 0 - angle
            if angle < 0:
                angle += 360
            self.allangles[i] = pygame.transform.rotate(bird_obj.chewchew, angle)

    def get_angled_bird(self):
        current_acc = int(self.bird_accelerate)
        current_ang = self.allangles.get(current_acc, 0)
        return current_ang

bird_obj = bird()
bird_obj.create_angled_birds()
pipes = []
for i in range(4):
    pipes.append(Pipe(i))

start = press_up = False
display_text = "Start you fool.!!"

while not done:
    screen.fill((255, 255, 153))
    for event in pygame.event.get():
        # The user clicked 'close' or hit Alt-F4
        if event.type == pygame.QUIT:
            done = True
            print("Quit")
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                bird_obj.bird_accelerate = -5
                start = True
    if done:
        break
    if press_up == True:
        bird_obj.bird_accelerate = -5
        start = True
        press_up = False
    screen.blit(bg, (0, 0))



    if not start:
        pygame.display.update()
        #print(display_text)
        message_display(display_text)
        pygame.display.update()
        time.sleep(0.2)
        continue

    for i in pipes:
        i.move_pipes()
        screen.blit(i.pipe1, (i.pipe1X, i.pipe1Y))
        screen.blit(i.pipe2, (i.pipe2X, i.pipe2Y))
        if i.pipe1X < 0:
            i.reset_pipes()
        done = i.detect_collision(bird_obj.birdY, bird_obj.birdX)
        if not press_up:
            press_up = play_game(bird_obj.birdY, i.pipe2X, i.pipe2Y)
        if done:
            start = False
            done = False
            display_text = "You DIED noob.!!"

    if start == False:
        pipes = []
        for i in range(4):
            pipes.append(Pipe(i))

    bird_obj.chewchew = bird_obj.get_angled_bird()

    bird_obj.move_bird()
    screen.blit(bird_obj.chewchew, (bird_obj.birdX, bird_obj.birdY))



    pygame.display.update()
