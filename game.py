import pygame
import time
import os
import random
import math

WIN_WIDTH = 450
WIN_HEIGHT = 800
HERO_X = 60
HERO_Y = 470

pygame.font.init()

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

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

       

BG_IMG = pygame.image.load(os.path.join("Images","bg.png"))




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
    
    def pushBack(self):
        self.x -=1


class Stick:
    def __init__(self, hero):
        self.length = 0
        self.x = hero.x + 35
        self.y = hero.y + 30
        self.xEnd = self.x
        self.yEnd = self.y
        self.tilt = math.pi / 2
    
    def grow(self):
        self.length += 1
        self.yEnd = self.y - self.length

    def rotate(self):
        if self.tilt >= math.pi:
            self.yEnd = 500
            return False
        self.tilt += math.pi / 540
        self.xEnd = self.x - self.length*(math.cos(self.tilt)) 
        self.yEnd = self.y - self.length*(math.sin(self.tilt)) 
        return True
        
    def pushBack(self):
        self.x -= 1
        self.xEnd -= 1

    def draw(self, win):
        if self.length != 0:
            pygame.draw.line(win, (0,0,0), (self.x, self.y), (self.xEnd, self.yEnd), 4)

class Base:
    def __init__(self, x_ = None, w_ = None, base = None):
        if x_ != None:
            self.x = x_
            self.width = w_

        else:
            self.width = random.randint(60, 120)
            end = random.randint(self.width + 5, 380)            
            self.x = base.x + base.width + end - self.width
        
        self.redX = int(self.x + (self.width / 2))
        self.y = 500
        self.height = 300 


    def pushBack(self):
        self.x -= 1
        self.redX -= 1
    
    def draw(self, win):
        pygame.draw.rect(win, (0,0,0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, (255,0,0), (self.redX, self.y, 4, 4))




def drawWindow(win, hero, walk, stick, bases, score):
    win.blit(BG_IMG, (0,0))
    hero.walk_draw(win) if walk else hero.stand_draw(win)
    stick.draw(win)
    for base in bases:
        base.draw(win)

    text = SCORE_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    pygame.display.update()

def main():
    score = 0
    hero = Hero(HERO_X, HERO_Y)
    stick = Stick(hero)
    baselist = list()
    baselist.append(Base(0, 95))
    baselist.append(Base(base=baselist[0]))
    baselist.append(Base(base=baselist[1]))
    rem = list()
    add = list()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    walk = False
    growing = False
    rotating = False
    pushback = False
    while(run):
        addbase = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not rotating and stick.tilt <= math.pi:
                        if growing:
                            growing = False
                            rotating = True
                        else:
                            growing = True

        if growing:
            stick.grow()

        if rotating:
            rotating = stick.rotate()  

        if stick.tilt >= math.pi:
            walk = True

        if stick.xEnd < baselist[1].x:
            if hero.x + 30 >= stick.xEnd:
                walk = False
        else:
            if hero.x + 30 >= max([stick.xEnd, baselist[1].x + baselist[1].width]):
                walk = False

        if not walk and not rotating and not growing and not pushback and stick.length != 0:
            if stick.xEnd < baselist[1].x or stick.xEnd > baselist[1].x + baselist[1].width or stick.xEnd > 450: 
                print("You Died! Score:", score)
                run = False
            if stick.xEnd > baselist[1].redX and stick.xEnd < baselist[1].redX + 4: 
                score += 1
            pushback = True

        if hero.x <= 30:
            pushback = False

        if pushback:
            for base in baselist:
                base.pushBack()
            stick.pushBack()      
            hero.pushBack()

        for base in baselist:
            if base.x + base.width < 0:
                rem.append(base)
                addbase = True
                del stick            

        if addbase: 
            score += 1
            baselist.append(Base(base=baselist[-1]))
            stick = Stick(hero)

        for x in rem:
            baselist.remove(x)
            pushdist = 0

        
        rem.clear()

        drawWindow(win, hero, walk, stick, baselist, score)
    pygame.quit()
    quit()

main()
