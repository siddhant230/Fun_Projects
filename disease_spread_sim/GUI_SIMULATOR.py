import pygame,random,sys
from pygame.locals import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from scipy.spatial import distance
from collections import Counter

style.use('fivethirtyeight')
fig=plt.figure()
val=0
X_I=[]
Y_I=[]

X_H=[]
Y_H=[]

X_C=[]
Y_C=[]

X_D=[]
Y_D=[]

distribution={'H':0,'I':0,'C':0,'D':0}
ax1=fig.add_subplot(1,1,1)
def plotter(i):
    global X_I,X_C,X_D,X_H,distribution,val,Y_I,Y_C,Y_D,Y_H
    val+=1

    #for H
    Y_H.append(distribution['H'])
    X_H.append(val)

    #for I
    Y_I.append(distribution['I'])
    X_I.append(val)

    #for C
    Y_C.append(distribution['C'])
    X_C.append(val)

    #for D
    Y_D.append(distribution['D'])
    X_D.append(val)

    ax1.clear()
    ax1.plot(X_H,Y_H,c='lightgreen',label='Healthy')    #healthy
    ax1.plot(X_I,Y_I,c='r',label='Infected')    #infected
    ax1.plot(X_C,Y_C,c='b',label='Cured')    #cured
    ax1.plot(X_D,Y_D,'k',label='Death')    #dead
    plt.legend()

w,h=850,750

from tkinter import *
from functools import partial

root = Tk()
root.geometry("450x700")

input_list={
            'block':None,
            'condition':None,
            'score':None,
            'healthy_size':None,
            'inf_size':None,
            'doc_size':None
           }
varstate = IntVar()
varblock= IntVar()
def graphics():
    global input_list,varstate,varblock

    def score_check(freed,cnd,safety,healthy,infected,doctors):
        global input_list,root,varstate,varblock

        freed_obtained=freed.get("1.0",END)[:-1]
        cnd_obtained=cnd.get("1.0",END)[:-1]
        safety_obtained=safety.get("1.0",END)[:-1]
        health_obtained=healthy.get("1.0",END)[:-1]
        infected_obtained=infected.get("1.0",END)[:-1]
        doctors_obtained=doctors.get("1.0",END)[:-1]

        input_list['block']=freed_obtained
        input_list['condition']=cnd_obtained
        input_list['score']=safety_obtained
        input_list['healthy_size']=health_obtained
        input_list['inf_size']=infected_obtained
        input_list['doc_size']=doctors_obtained

        root.destroy()
    Label(root,text='--------------------------------------------------------------------------').place(relx=0.06,rely=0.08)
    #blockdown
    Label(root,text='Is there freedom [no blockdown] [y/n] : '.upper()).place(relx=0.06,rely=0.1)
    freed=Text(root,width=2,height=1)
    freed.place(relx=0.06,rely=0.13)
    Label(root,text='--------------------------------------------------------------------------').place(relx=0.06,rely=.19)

    #normal/Isolation
    Label(root,text='What condition is it [normal/isolation] : '.upper()).place(relx=0.06,rely=0.22)
    cnd=Text(root,width=10,height=1)
    cnd.place(relx=0.06,rely=0.25)
    Label(root,text='--------------------------------------------------------------------------').place(relx=0.06,rely=0.34)
    #safety score
    Label(root,text='high safety score means a citizen is obedient and highly aware'.upper()).place(relx=0.06,rely=0.38)
    Label(root,text='low score means he does not pays heed to orders.').place(relx=0.06,rely=0.42)
    Label(root,text='what is his safety score [0-10] : ').place(relx=0.06,rely=0.46)
    safety=Text(root,width=2,height=1)
    safety.place(relx=0.06,rely=0.50)
    Label(root,text='--------------------------------------------------------------------------').place(relx=0.06,rely=0.53)
    #population size
    Label(root,text='Input population size'.upper()).place(relx=0.06,rely=0.56)
    Label(root,text='Healthy Population Size : ').place(relx=0.06,rely=0.60)
    healthy=Text(root,width=5,height=1)
    healthy.place(relx=0.06,rely=0.64)

    Label(root,text='Infected Population Size : ').place(relx=0.06,rely=0.68)
    infected=Text(root,width=5,height=1)
    infected.place(relx=0.06,rely=0.72)

    Label(root,text='Doctors Population Size : ').place(relx=0.06,rely=0.76)
    doctors=Text(root,width=5,height=1)
    doctors.place(relx=0.06,rely=0.80)

    Label(root,text='--------------------------------------------------------------------------').place(relx=0.06,rely=0.84)
    d_button=Button(root,text='Start',width=20,command=partial(score_check,freed,cnd,safety,healthy,infected,doctors))
    d_button.place(relx=0.06,rely=0.87)

class Block:
    def __init__(self):
        self.x = 0
        self.y = h // 2
        self.width = 800
        self.height = 5
        self.color = (0, 0, 0)

    def show(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

matrix=np.zeros((w+1,h+1),dtype='int')

class People:

    def __init__(self,type=0,score=0,move_status='normal',freedom=True):
        self.move_status=move_status
        self.freedom=freedom       #not blockdown

        self.x=random.randint(25,w-20)
        self.y=random.randint(25,h-20)
        good_pos_found=False

        while freedom==False and good_pos_found==False:
            if self.iscollided_with_blockdown():
                self.x=random.randint(25,w-20)
                self.y=random.randint(25,h-20)
            else:
                good_pos_found=True

        self.xspeed=random.choice([2,1,-1,-2])
        self.yspeed=random.choice([2,1,-1,-2])
        color=(0,255,0)
        if type==0:     #normal
            color=(0,255,0)
        if type==1:     #infected
            color=(255,0,0)
        if type==2:     #cured
            color=(200,0,165)
        self.color=color
        self.type=type
        self.radius=4
        self.safety_score=score
        self.factor_x=1
        self.factor_y=1
        self.cured=False
        self.life=random.randint(60,100)
        self.time=100
        if self.type==1 or self.type==2:
            matrix[self.x-self.radius:self.x+self.radius,self.y-self.radius:self.y+self.radius]=np.full(matrix[self.x-self.radius:self.x+self.radius,self.y-self.radius:self.y+self.radius].shape,self.type)

    def get_speed(self):
        return  random.choice([1,-1])

    def update_under_normal(self):
        self.time-=0.5
        org_x,org_y=self.x,self.y

        if self.type==1:
            self.life-=0.3

        self.x+=self.xspeed*self.factor_x
        self.y+=self.yspeed*self.factor_x

        if np.count_nonzero(matrix[self.x-self.radius:self.x+self.radius,self.y-self.radius:self.y+self.radius])>0:
            a=matrix[self.x-self.radius:self.x+self.radius,self.y-self.radius:self.y+self.radius].flatten()
            counts=Counter(list(a))

            if (self.type==1 or self.type==0) and 2 not in counts.keys():
                if self.safety_score<=0:
                    self.color=(255,0,0)
                    self.type=1
                else:
                    self.safety_score-=1
            elif 2 in counts.keys() and self.type==1 and self.cured!=True:
                self.color=(0,0,255)
                self.type=3
                self.cured=True
                self.factor_x*=-1

        matrix[self.x-self.radius:self.x+self.radius,self.y-self.radius:self.y+self.radius]=np.full(matrix[self.x-self.radius:self.x+self.radius,self.y-self.radius:self.y+self.radius].shape,self.type)
        matrix[org_x-self.radius:org_x+self.radius,org_y-self.radius:org_y+self.radius]=np.zeros(matrix[org_x-self.radius:org_x+self.radius,org_y-self.radius:org_y+self.radius].shape)

        if self.freedom==True:
            if self.iscollided_under_normal_and_isolation():
                self.factor_x*=-1
        elif self.freedom==False:
            if self.iscollided_with_blockdown():
                self.factor_x*=-1

    def update_under_isolation(self):
        self.time-=0.5

        org_x,org_y=self.x,self.y

        if self.type==1:
            self.life-=0.3

        #if moving under isloation
        if self.type==2 or self.type==1:
            if self.type==1 and random.random()>0.5:
                self.x+=self.xspeed*self.factor_x
                self.y+=self.yspeed*self.factor_x
            elif self.type==2:
                self.x+=self.xspeed*self.factor_x
                self.y+=self.yspeed*self.factor_x
        elif self.type==0:
            if random.random()>self.safety_score/10:
                self.x+=self.xspeed*self.factor_x
                self.y+=self.yspeed*self.factor_x

        if np.count_nonzero(matrix[self.x-self.radius:self.x+self.radius,self.y-self.radius:self.y+self.radius])>0:
            a=matrix[self.x-self.radius:self.x+self.radius,self.y-self.radius:self.y+self.radius].flatten()
            counts=Counter(list(a))

            if (self.type==1 or self.type==0) and 2 not in counts.keys():
                if self.safety_score<=0:
                    self.color=(255,0,0)
                    self.type=1
                else:
                    self.safety_score-=1
            elif 2 in counts.keys() and self.type==1 and self.cured!=True:
                self.color=(0,0,255)
                self.type=3
                self.cured=True

        matrix[self.x-self.radius:self.x+self.radius,self.y-self.radius:self.y+self.radius]=np.full(matrix[self.x-self.radius:self.x+self.radius,self.y-self.radius:self.y+self.radius].shape,self.type)
        matrix[org_x-self.radius:org_x+self.radius,org_y-self.radius:org_y+self.radius]=np.zeros(matrix[org_x-self.radius:org_x+self.radius,org_y-self.radius:org_y+self.radius].shape)

        if self.freedom==True:
            if self.iscollided_under_normal_and_isolation():
                self.factor_x*=-1
        elif self.freedom==False:
            if self.iscollided_with_blockdown():
                self.factor_x*=-1

    def iscollided_under_normal_and_isolation(self):
        if self.x<=5 or self.y<=5 or self.x>=w-20 or self.y>=h-20:
            return True
        else:
            return False

    def iscollided_with_blockdown(self):
        if self.x <= 5 or self.y <= 5 or self.x >= w - 20 or self.y >= h - 20 or (
                (self.x > block.x and self.x < block.x + block.width) and (
                self.y > block.y and self.y < block.y + block.height)):
            return True
        else:
            return False

    def show(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius-2)

distribution={'H':0,'I':0,'C':0,'D':0,'doc':0}
def get_population_distribution(population):
    global distribution
    distribution={'H':0,'I':0,'C':0,'D':distribution['D'],'doc':0}
    for obj in population:
        if obj.life<=0:
            population.remove(obj)
            distribution['D']+=1
        if obj.type==0 or obj.type==3:
            distribution['H']+=1
        if obj.type==1:
            distribution['I']+=1
        if obj.type==3:
            distribution['C']+=1
        if obj.type==2:
            distribution['doc']+=1

    return distribution,population

block=None
freedom=True
start=False
def create_population(healthy_size=500,infect_size=1,cure_size=5):
    global block,freedom,input_list,start

    population=[]
    done=False
    move_status='normal'
    score=2
    healthy_size=int(input_list['healthy_size'])
    freedom=input_list['block']
    if freedom=='n':
        block = Block()
        freedom=False
    else:
        freedom=True
    move_status=input_list['condition']
    score=int(input_list['score'])
    infect_size=int(input_list['inf_size'])
    cure_size=int(input_list['doc_size'])

    for _ in range(healthy_size):
        population.append(People(type=0,score=score,move_status=move_status,freedom=freedom))
    for _ in range(infect_size):
        population.append(People(type=1,move_status=move_status,freedom=freedom))
    for _ in range(cure_size):
        population.append(People(type=2,freedom=freedom))
    start=True
    return population

pygame.init()
pygame.display.set_caption('LIFE SIM')
screen=pygame.display.set_mode((w,h),0,32,pygame.HWSURFACE)
population=[]
def creator(i):
    global start,population,block,freedom
    for e in pygame.event.get():
        if e.type==KEYDOWN:

            if e.key==K_q:
                pygame.quit()
                sys.exit()

            if e.key==K_s:
                population=create_population()
                start=True

    screen.fill((255,255,255))
    if start:
        if freedom==False:
            block.show()
        for each_person in population:
            if each_person.move_status=='normal':
                each_person.update_under_normal()
            elif each_person.move_status=='isolation':
                each_person.update_under_isolation()
            each_person.show()

        current_distribution,population=get_population_distribution(population)
        #print(current_distribution)
        plotter(None)
        cap='Healthy : {}                           Infected : {}                        Cured : {}                              Death : {}                 Doctors : {}'.format(current_distribution['H'],current_distribution['I'],
                                                                                                                                                    current_distribution['C'],current_distribution['D'],
                                                                                                                                                                                 current_distribution['doc'])
        pygame.display.set_caption(cap)
    pygame.display.update()

if __name__=='__main__':
    graphics()

    ani=animation.FuncAnimation(fig,creator,interval=1)
    plt.show()
