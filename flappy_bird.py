import pygame
from pygame.locals import *
import sys
import random
import time

bird_img='/home/parmeet/Downloads/chicken.png'
back_img='/home/parmeet/Downloads/flappy_back.jpeg'
pygame.init()
pygame.display.set_caption('FLAPPY BIRD')

screen=pygame.display.set_mode((600,370),0,32)
back=pygame.image.load(back_img)
screen.blit(back,(0,0))
w,h=600,370
bird=pygame.image.load(bird_img).convert_alpha()
y_bird=165
x_bird=70
y=0
move=0
color=(0,255,0)

##pillar banao
class pipe:

    def __init__(self):
        self.top=random.randint(0,h//2)
        self.bottom=random.randint(0,h//2)
        self.x=w
        self.width_of_pole=45
        self.speed=6
        self.score=0

    def show(self):
        rectT=(self.x,0,self.width_of_pole,self.top)
        rectB=(self.x,self.top+170,self.width_of_pole,h)
        pygame.draw.rect(screen,color,rectT)
        pygame.draw.rect(screen,color,rectB)

    def update(self):
        self.x-=self.speed

    def collision(self,bx,by):
        if bx>self.x and bx<self.x+self.width_of_pole:
            if by<=self.top or by>=self.top+170:
                color=(255,0,0)
                rect_newT=(self.x,0,self.width_of_pole,self.top)
                rect_newB=(self.x,self.top+170,self.width_of_pole,h)
                pygame.draw.rect(screen,color,rect_newT)
                pygame.draw.rect(screen,color,rect_newB)
                return 1
            return 0


def bird_move_up():
    gravity=-0.9
    return gravity

def bird_move_down():
    gravity=0.7
    return gravity

pillar=[]
pillar.append(pipe())

x_start=550
press=0
up=None
start=False
score=0
while True:

    for e in pygame.event.get():
        if e.type==KEYDOWN:

            if e.key==K_q:
                pygame.quit()
                sys.exit()

            if e.key==K_SPACE:
                press=time.time()
                up=True
                y=bird_move_up()

        if e.type==KEYUP:
            if e.key==K_SPACE:
                y=bird_move_down()
                up=False
    screen.fill((0,0,0))
    ##let the bird jump

    if time.time()-press>1 and up==True:
        y=bird_move_down()
        up=False
    y_bird+=y
    if y_bird>340:
        y_bird=340
    if y_bird<25:
        y_bird=25
    screen.blit(bird,(x_bird,y_bird))
    ##making the pillars
    if e.type==KEYDOWN:
        if e.key==K_c:
            start=True
    if start:
        if move%600==0:
            pillar.append(pipe())
        for i in range(len(pillar)):
            pillar[i].show()
            if move%16==0:
                pillar[i].update()
                response=pillar[i].collision(x_bird,y_bird)

                if response==1:
                    score-=1
                if response==0:
                    score+=1
        if len(pillar)>10:
            pillar.pop(0)
    move+=1

    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    label = myfont.render("SCORE : "+str(score//7), 3, (255,0,0))
    screen.blit(label,(10,20))
    lab2=myfont.render("Press c to Start", 10, (255,0,0))
    if start==False:
        screen.blit(lab2,(250,300))

    pygame.display.update()
