import pygame
import time
import os
import random
import math
import neat
import pickle

WIN_WIDTH = 450
WIN_HEIGHT = 800
HERO_X = 35
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
        if self.yEnd < 0:
            return True

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
            if(self.width%2 == 1):
                self.width -= 1
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




def drawWindow(win, hero, walk, stick, bases, score, idx):
    score = "{:.2f}".format(score)

    win.blit(BG_IMG, (0,0))
    hero.walk_draw(win) if walk else hero.stand_draw(win)
    stick.draw(win)
    for base in bases:
        base.draw(win)

    text1 = SCORE_FONT.render("ID: " + str(idx), 1, (255,255,255))
    win.blit(text1, (WIN_WIDTH - 10 - text1.get_width(), 10))
    
    text2 = SCORE_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text2, (WIN_WIDTH - 10 - text2.get_width(), 60))
    pygame.display.update()

def evaluate(genomes, config):
    for idx, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)

        baseCount = 0
        perfectCount = 0
        score = 0
        hero = Hero(HERO_X, HERO_Y)
        stick = Stick(hero)
        baselist = list()
        baselist.append(Base(0, 65))
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
        first = True

        while(run):
            addbase = False

            if not rotating and stick.tilt <= math.pi and not walk and not pushback:
                control = True
            else:
                control = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = False

            if control:
                output = net.activate((stick.x, stick.length, baselist[1].x, baselist[1].width))
                # output = net.activate((hero.x/WIN_WIDTH, stick.length/WIN_WIDTH, baselist[1].x/WIN_WIDTH, baselist[1].x/WIN_WIDTH + baselist[1].width/WIN_WIDTH))
                if output[0] > 0.5 and output[1] > 0.5:
                    score -= 1000
                    run = False
                    break
                if output[0] > 0.5 and growing:
                    growing = False
                    rotating = True
                    
                if output[1] > 0.5 and not growing:
                    growing = True
                
                # print(hero.x/WIN_WIDTH, stick.length/WIN_WIDTH, baselist[1].x/WIN_WIDTH, baselist[1].x/WIN_WIDTH + baselist[1].width/WIN_WIDTH)
                # print(output)
                # print("__________")

            if growing:
                if(stick.grow()):
                    score -= stick.length*0.01
                    score -= 1000
                    run = False
                score += 0.01

            if hero.x > 450:
                score -= stick.length*0.01
                run = False

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
                
                center = baselist[1].redX + 2
                dist = abs(stick.xEnd - center)



                if stick.xEnd < baselist[1].x or stick.xEnd > baselist[1].x + baselist[1].width: 
                  # print("You Died! Score:", score)
                    score -= 100
                    run = False
                    break
                else:
                    score += 500 * float(1 - (2*dist)/ baselist[1].width)
          
                if stick.xEnd > baselist[1].redX and stick.xEnd < baselist[1].redX + 4: 
                    score += 200
                    perfectCount += 1
                pushback = True

            if hero.x < 30:
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
                baseCount += 1 
                score += 2000
                baselist.append(Base(base=baselist[-1]))
                stick = Stick(hero)

            for x in rem:
                baselist.remove(x)
                pushdist = 0
            
            rem.clear()

            if first and not growing:
                score = -1000
                run = False

            first = False

            drawWindow(win, hero, walk, stick, baselist, score, idx)
            
            if score > 100000:
                if baseCount == perfectCount:
                    score = 150000 * baseCount
                run = False
                break
            
        div = 1 if (baseCount == 0) else baseCount
        g.fitness = score / div


def run(configF):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         configF)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    

    winner = p.run(evaluate, 50) 

    print('\nBest genome:\n{!s}'.format(winner))


    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()

    # visualize.draw_net(config, winner, True)
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)


                        
            

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)


