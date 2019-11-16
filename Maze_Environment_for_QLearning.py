import pygame,sys,time
from pygame import *
from tkinter import messagebox
import tkinter as tk
from time import sleep
root=tk.Tk()
root.withdraw()

pygame.init()

pygame.display.set_caption('STATUS :  ')
width,height=1000,600
b_w=50
b_h=50
screen=pygame.display.set_mode((width,height),0,32)
screen.fill((255,255,255))

class rect:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.color=(0,255,0)
        self.width=50
        self.height=50
        self.status=True

    def plot(self,col=(0,0,0)):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))

class car:
    def __init__(self,x=0,y=0):
        self.x=track[0].x+track[0].width//2
        self.y=track[0].y+track[0].height//2
        self.color=(0,0,245)
        self.r=25

    def move(self):
        pygame.draw.circle(screen,self.color,(c.x,c.y),self.r)

rectangles=[]

for i in range(0,width,b_w):
        for j in range(0,height,b_h):
            rectangles.append(rect(i,j))
for r in rectangles:
        r.plot()
start=False
bound=False
track=[]
start_work=False
cx,cy=0,0
up=down=left=right=pressed=False
pin=0
count=0
while True:
    for e in pygame.event.get():
        if e.type==KEYDOWN:
            pressed=True
            if e.key==K_s:
                start_work=True
                c=car()
                x,y=track[0].x+track[0].width//2,track[0].y+track[0].height//2
                track[0].color=(255,0,255)
            if e.key==K_q:
                pygame.quit()
                sys.exit()
            if e.key==K_r:
                rectangles=[]
                cx,cy=0,0
                for i in range(0,width,b_w):
                        for j in range(0,height,b_h):
                            rectangles.append(rect(i,j))
                for r in rectangles:
                        r.plot()
                print(len(rectangles))
                start=False
                start_work=False
                track=[]

            if e.key==K_LEFT:
                left=True
                right=up=down=False
            elif e.key==K_RIGHT:
                right=True
                left=up=down=False
            elif e.key==K_UP:
                up=True
                left=right=down=False
            elif e.key==K_DOWN:
                down=True
                left=right=up=False

        ##########################CHANGE PART############################
        if start_work==False:
            if e.type==MOUSEBUTTONDOWN:
                start=True
            if e.type==MOUSEBUTTONUP:
                start=False
            if start==True:
                x,y=pygame.mouse.get_pos()
                for i in range(len(rectangles)):
                    if (x>rectangles[i].x and x<rectangles[i].x+rectangles[i].height) and (y>rectangles[i].y and y<rectangles[i].y+rectangles[i].width):
                        rectangles[i].color=(255,255,255)
                        rectangles[i].status=False
                        if rectangles[i] not in track:
                            track.append(rectangles[i])

    for r in rectangles:
        r.plot()

    if pressed==True:
        bound=False
        if up==True:
            cy=-2*c.r
        if down==True:
            cy=+2*c.r
        if left==True:
            cx=-2*c.r
        if right==True:
            cx=+2*c.r
        for i in range(len(track)):
            count+=1
            if (c.x+cx>=track[i].x and c.x+cx<=track[i].x+track[i].width) and (c.y+cy>=track[i].y and c.y+cy<=track[i].y+track[i].height):
                bound=True
                break
            else:
                bound=False
        if start_work==True and bound==True:
            if up==True or down==True and left==False and right==False:
                c.y+=cy
            if left==True or right==True and up==False and down==False:
                c.x+=cx
    if start_work==True:
        c.move()
    cx,cy=0,0
    pressed=False
    up=down=left=right=False
    bound=False

    if count>1:
        pin=1
    count=0
    pygame.display.set_caption('STATUS : MOVING')
    pygame.display.update()
