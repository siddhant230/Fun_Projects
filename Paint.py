import pygame,sys
from pygame.locals import *

pygame.init()
screen=pygame.display.set_mode((820,700),0,32)
screen.fill((255,255,255))
color=(0,0,0)
points=[]
Text_space=150
start=False

while True:
    myfont = pygame.font.SysFont("Comic Sans MS", 30)
    label = myfont.render("Press r for red | Press g for green | Press b for Blue", 1, (0,0,0))
    lab2=myfont.render("Press q to clear with your mouseup",1,(0,0,0))
    screen.blit(label, (40,20))
    screen.blit(lab2,(40,60))
    x,y=pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type==KEYUP:
            if e.key==K_q:
                screen.fill((255,255,255))
        if e.type==KEYDOWN:
            if e.key==K_r:
                color=(255,0,0)
            if e.key==K_b:
                color=(0,0,255)
            if e.key==K_g:
                color=(0,255,0)
            points=[]
        if e.type==QUIT:
            pygame.quit()
            sys.exit()
        if e.type==MOUSEBUTTONDOWN and start==False:
            start=True
        elif e.type==MOUSEBUTTONDOWN and start==True:
            start=False
            points=[]
    if start==True:
        x,y=pygame.mouse.get_pos()
        if y>Text_space:
            pygame.draw.circle(screen,color,(x,y),2,1)
            points.append((x,y))
        else:
            points=[]
    if len(points)>1:
        pygame.draw.lines(screen,color,False,points,5)

    pygame.display.update()