import cv2,random
import numpy as np
import time,pygame
from pygame.locals import *

#screen=cv2.bitwise_not(screen)
w=1240
h=680
screen=pygame.display.set_mode((w,h),0,32)
screen.fill((0,0,0))
p1='1.png'
p2='2.png'
p3='3.png'
p4='4.png'

fire1=pygame.image.load(p1).convert_alpha()
fire2=pygame.image.load(p2).convert_alpha()
fire3=pygame.image.load(p3).convert_alpha()
fire4=pygame.image.load(p4).convert_alpha()

class Particle:
    def __init__(self,x=random.randint(0,w-1),y=h-2,vel=None,exploded=False,life=None,size=2,col=(255,0,0)):
        self.pos=np.array([x,y],dtype=float)
        self.radius=2
        self.color=col
        if vel is None:
            self.velocity=np.array([0.0,random.randint(-35.0,-30)],dtype=float)
        else:
            self.velocity=vel * random.randint(1,6)
        self.life=life
        self.acceleration=np.zeros(shape=(2,),dtype=float)
        self.exploded=exploded
        self.size=size
        self.img=random.choice([fire1,fire2,fire3,fire4])

    def applyforce(self,force):
        self.acceleration+=force

    def update(self):
        self.velocity+=self.acceleration
        self.pos+=self.velocity
        if self.velocity[1]>=0:
            if self.exploded == False:
                if random.random()>0.6:
                    for _ in range(100):
                        color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
                        particles.append(Particle(x=self.pos[0],y=self.pos[1],
                                            vel=np.array([random.randint(-7,7),random.randint(-8,8)],dtype=float),
                                          life=random.randint(2,6),exploded=True,size=1,col=color))
                else:
                    color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    for _ in range(100):
                        particles.append(Particle(x=self.pos[0],y=self.pos[1],
                                                  vel=np.array([random.randint(-7,7),random.randint(-8,8)],dtype=float),
                                                  life=random.randint(2,6),exploded=True,size=1,col=color))
                self.exploded=True

        self.acceleration*=0

    def show(self):
        pos=(int(self.pos[0]),int(self.pos[1]))
        if self.exploded:
            pygame.draw.circle(screen,self.color,pos,self.radius,self.size)
        else:
            screen.blit(self.img, self.pos)
        #cv2.circle(screen,pos,self.radius,self.color,self.size)

gravity=np.array([0.,1.1])
particles=[]
timer=0
FPS=400
clock=pygame.time.Clock()

while True:
    clock.tick(FPS)
    for e in pygame.event.get():
        if e.type==KEYDOWN:
            if e.key==K_q:
                pygame.quit()
    if timer%25==0:
        screen.fill((0,0,0))

    if timer%75==0:
        particles.append(Particle(random.randint(0,w-1)))

    for i in range(len(particles)-1,-1,-1):
        p=particles[i]
        if p.exploded and p.life==None:
            particles.pop(i)

        elif p.exploded and p.life==0:
            particles.pop(i)
        else:

            if timer%20==0:
                if p.life is not None:
                    p.life-=1
                p.applyforce(gravity)
                p.update()
            p.show()
    timer+=1

    pygame.display.update()
