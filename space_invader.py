import pygame
from pygame.locals import *
import sys
import math
import random
from tkinter import *
from tkinter import messagebox
from PIL import Image

Tk().wm_withdraw()

space_img='/home/parmeet/Downloads/back.jpeg'
rocket_image='/home/parmeet/Downloads/rocket.png'
alien_image='/home/parmeet/Downloads/alien.png'
bullet_image='/home/parmeet/Downloads/bullets.png'
loose='/home/parmeet/Downloads/deft.jpg'


def save_it(screen):
    print('in fun')
    dims = screen.get_size()
    im1 = pygame.image.tostring(screen,'RGB')
    im = Image.frombytes('RGB',(dims),im1)
    im.save('/home/parmeet/Desktop/space.png','PNG')

pygame.init()
screen=pygame.display.set_mode((500,400),0,32)
width=500
height=400
score=0

##background image
background=pygame.image.load(space_img)

##aliens
alien=[]
enemyx=[]
enemyy=[]
change_a_x=[]
change_a_y=[]
number_of_enemies=6

for i in range(number_of_enemies):
    alien.append(pygame.image.load(alien_image).convert_alpha())
    enemyx.append(random.randint(0,460))
    enemyy.append(random.randint(10,150))
    change_a_y.append(20)
    change_a_x.append(1.3)

##rocket
rocket=pygame.image.load(rocket_image).convert_alpha()
r_x,r_y=(width//2)-20,(height//2)+100
playerx=r_x
playery=350
change_r_x=0

##bullet
bullet=pygame.image.load(bullet_image).convert_alpha()
bulletx=0
bullety=r_y+3
bullety_change=2
state='ready'

def player(m_x,m_y):
    screen.blit(rocket,(m_x,m_y))

def enemy(x,y,i):
    screen.blit(alien[i],(x,y))

def bullet_fire(x,y):
    global state
    state='fire'
    screen.blit(bullet,(x,y))

def collision(ex,ey,bx,by):
    thresh=30
    dist=math.sqrt(math.pow((ex-bx),2)+math.pow((ey-by),2))
    if dist<thresh:
        return True
    else:
        return False

def helper():
    lab2 = myfont.render("Enter c to Continue" , 1, (255,255,255))
    screen.blit(lab2, (10,30))
    if e.type==KEYDOWN:
        print('##')
        if e.key==K_c:
            return 'c'

cls=False
while True:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    label = myfont.render("SCORE : "+str(score) , 1, (255,255,255))
    screen.blit(label, (10,10))
    for e in pygame.event.get():
        if e.type==KEYDOWN:
            if e.key==K_SPACE:
                if state!='fire':
                    bulletx=playerx+8
                    bullet_fire(bulletx,playery)
            if e.key==K_LEFT:
                change_r_x=-2.3
            if e.key==K_RIGHT:
                change_r_x=+2.3
            if e.key==K_f:
                res=messagebox.askquestion('Thank you','wanna save it??')
                print(res)
                if res=='yes':
                    save_it(screen)
                pygame.quit()
                sys.exit()
        if e.type==KEYUP:
            if e.key==K_LEFT or e.key==K_RIGHT:
                change_r_x=0

    ##for bullet shooting
    if bullety<2:
        bullety=playery
        state='ready'
    if state=='fire':
        bullet_fire(bulletx,bullety)
        bullety-=bullety_change

    ##for rocket player
    playerx=playerx+change_r_x
    if playerx<0:
        playerx=0
    elif playerx>width-30:
        playerx=width-30

    ##for enemy alien
    for i in range(number_of_enemies):
        enemyx[i]+=change_a_x[i]
        if enemyx[i]<0:
            change_a_x[i]=0.75
            enemyy[i]+=change_a_y[i]
        elif enemyx[i]>width-30:
            change_a_x[i]=-0.75
            enemyy[i]+=change_a_y[i]

        ##collision checker for each alien one by one
        if state=='fire':
            cls=collision(enemyx[i],enemyy[i],bulletx,bullety)
        ## collision check between alien and spaceship
        rocket_alien_coll=collision(playerx,playery,enemyx[i],enemyy[i])
        if rocket_alien_coll:
            screen.fill((0,0,0))
            loose_b=pygame.image.load(loose)
            screen.blit(loose_b,(0,0))
            for _  in range(10000):
                val=helper()

            if val=='c':
                ##aliens
                score=0
                alien=[]
                enemyx=[]
                enemyy=[]
                change_a_x=[]
                change_a_y=[]
                number_of_enemies=6

                for i in range(number_of_enemies):
                    alien.append(pygame.image.load(alien_image).convert_alpha())
                    enemyx.append(random.randint(0,460))
                    enemyy.append(random.randint(10,150))
                    change_a_y.append(20)
                    change_a_x.append(1.3)

                ##rocket
                rocket=pygame.image.load(rocket_image).convert_alpha()
                r_x,r_y=(width//2)-20,(height//2)+100
                playerx=r_x
                playery=350
                change_r_x=0

                ##bullet
                bullet=pygame.image.load(bullet_image).convert_alpha()
                bulletx=0
                bullety=r_y+3
                bullety_change=2
                state='ready'

        if cls==True:
            score+=1
            #print(score)
            bullety=playery
            state='ready'
            enemyx[i]=random.randint(0,460)
            enemyy[i]=random.randint(50,150)
            cls=False
        enemy(enemyx[i],enemyy[i],i)

    player(playerx,playery)

    pygame.display.update()