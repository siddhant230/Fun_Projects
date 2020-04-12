import cv2,random
import numpy as np
import time,pygame

screen=cv2.imread('screen.png')
#screen=cv2.bitwise_not(screen)
w=1240
h=680
screen=cv2.resize(screen,(w,h),interpolation=cv2.INTER_AREA)

class Particle:
    def __init__(self,x=random.randint(0,w-1),y=h-2,vel=None,exploded=False,life=None,size=2):
        self.pos=np.array([x,y],dtype=float)
        self.radius=1
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        if vel is None:
            self.velocity=np.array([0.0,random.randint(-35.0,-30)],dtype=float)
        else:
            self.velocity=vel * random.randint(1,6)
        self.life=life
        self.acceleration=np.zeros(shape=(2,),dtype=float)
        self.exploded=exploded
        self.size=size

    def applyforce(self,force):
        self.acceleration+=force

    def update(self):
        self.velocity+=self.acceleration
        self.pos+=self.velocity
        if self.velocity[1]>=0:
            if self.exploded == False:
                for _ in range(100):
                    particles.append(Particle(x=self.pos[0],y=self.pos[1],vel=np.array([random.randint(-7,7),random.randint(-8,8)],dtype=float),life=random.randint(2,6),exploded=True,size=1))
                self.exploded=True

        self.acceleration*=0

    def show(self):
        pos=(int(self.pos[0]),int(self.pos[1]))
        cv2.circle(screen,pos,self.radius,self.color,self.size)

gravity=np.array([0.,1.1])
particles=[]
timer=0
while True:

    if timer%25==0:
        screen=np.zeros(screen.shape)
    if timer%75==0:
        particles.append(Particle(random.randint(0,w-1)))


    for i in range(len(particles)-1,-1,-1):
        p=particles[i]
        if p.exploded and p.life==None:
            particles.pop(i)

        elif p.exploded and p.life==0:
            particles.pop(i)
        else:

            if timer%10==0:
                if p.life is not None:
                    p.life-=1
                p.applyforce(gravity)
                p.update()
            p.show()
    timer+=1
    cv2.imshow('                                                    fireworks screen',screen)
    if cv2.waitKey(1)==ord('q'):
        break
