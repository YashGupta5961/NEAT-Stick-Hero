import pygame
import neat
import time
import os
import random

WIN_WIDTH = 450
WIN_HEIGHT = 800

HERO_W = [  pygame.image.load(os.path.join("Images","walking","1.png")),
            pygame.image.load(os.path.join("Images","walking","2.png")),
            pygame.image.load(os.path.join("Images","walking","3.png")),
            pygame.image.load(os.path.join("Images","walking","4.png"))   ]

HERO_S = [  pygame.image.load(os.path.join("Images","standing","1.png")),
            pygame.image.load(os.path.join("Images","standing","2.png")),
            pygame.image.load(os.path.join("Images","standing","3.png")),
            pygame.image.load(os.path.join("Images","standing","4.png")), 
            pygame.image.load(os.path.join("Images","standing","5.png")),
            pygame.image.load(os.path.join("Images","standing","6.png")), ]

STICK_IMG = pygame.image.load(os.path.join("Images","stick.png"))

        

BG_IMG = pygame.image.load(os.path.join("Images","bg.png"))

BASE_IMG = pygame.image.load(os.path.join("Images","base.png"))


class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = HERO_W[0]
        self.imgCount = 0
    ANIMATION_TIME = 20
    def stand_draw(self, win):
        self.imgCount += 1

        if self.imgCount < self.ANIMATION_TIME:
            self.image = HERO_S[0]
        elif self.imgCount < self.ANIMATION_TIME*2:
            self.image = HERO_S[1]
        elif self.imgCount < self.ANIMATION_TIME*3:
            self.image = HERO_S[2]
        elif self.imgCount < self.ANIMATION_TIME*4:
            self.image = HERO_S[3]
        elif self.imgCount < self.ANIMATION_TIME*5:
            self.image = HERO_S[4]
        elif self.imgCount == self.ANIMATION_TIME*5 + 1:
            self.image = HERO_S[5]
            self.imgCount = 0
        
        win.blit(self.image, (self.x, self.y))

    def walk_draw(self, win):
        if self.x > 450:
            self.x = 0

        self.imgCount += 1
        
        if self.imgCount < self.ANIMATION_TIME:
            self.image = HERO_W[0]
        elif self.imgCount < self.ANIMATION_TIME*2:
            self.image = HERO_W[1]
        elif self.imgCount < self.ANIMATION_TIME*3:
            self.image = HERO_W[2]
        elif self.imgCount < self.ANIMATION_TIME*4:
            self.image = HERO_W[3]
        elif self.imgCount < self.ANIMATION_TIME*5:
            self.image = HERO_S[2]
        elif self.imgCount == self.ANIMATION_TIME*5 + 1:
            self.image = HERO_S[1]
            self.imgCount = 0
        
        win.blit(self.image, (self.x, self.y))

        self.x += 1


class Stick:
    MAX_ROTATION = 90
    ROT_VEL = 20
    def __init__(self, x, y):
        self.length = 0
        self.x = x
        self.y = y
        self.tilt = 0
        self.image = None
    
    def grow(self):
        self.image = STICK_IMG
        self.length += 1
        self.y -= 1
        self.image = pygame.transform.scale(self.image, (4, self.length))

    def draw(self, win):
        if self.image != None:
            win.blit(self.image, (self.x, self.y))


def drawWindow(win, hero, walk, stick):
    win.blit(BG_IMG, (0,0))
    hero.walk_draw(win) if walk else hero.stand_draw(win)
    stick.draw(win)
    pygame.display.update()

def main():
    hero = Hero(60, 470)
    stick = Stick(hero.x + 35, hero.y + 30)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    walk = False
    growing = False
    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if(growing):
                        growing = False
                    else:
                        growing = True
        if growing:
            stick.grow()            
        drawWindow(win, hero, walk, stick)
    pygame.quit()
    quit()

main()