import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption('                                                (((TIC-TAC-TOE)))')
width,height=451,451
screen=pygame.display.set_mode((width,height),0,32)
screen.fill((255,255,255))

class cell_block:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
        self.side=150
        self.color=(0,0,0)
        self.full=-99
        self.circle_color=(0,255,0)
        self.cross_color=(255,0,0)

    def plot(self):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.side,self.side),2)

    def draw_circle(self):
        pygame.draw.circle(screen,self.circle_color,((self.x+self.side//2),(self.y+self.side//2)),60,2)

    def draw_cross(self):
        pygame.draw.line(screen,self.cross_color,(self.x+10,self.y+10),(self.x+self.side-10,self.y+self.side-10),3)
        pygame.draw.line(screen,self.cross_color,(self.x+self.side-10,self.y+10),(self.x+10,self.y+self.side-10),3)

cells=[]
players_turn=True
def start():
    global cells
    x,y=0,0
    for i in range(9):
        cells.append(cell_block(x,y))
        x+=150
        if x%450==0:
            y+=150
            x=0

def win_line(cell,attr):
    global p,b
    if attr=='ro':
        startx=cell.x+10
        endx=cell.x+430
        starty=cell.y+cell.side//2
        endy=starty

    elif attr=='c':
        startx=cell.x+cell.side//2
        endx=startx
        starty=cell.y+10
        endy=cell.y+430

    elif attr=='l':
        startx=cell[0].x+cell[0].side//2
        endx=cell[1].x+cell[1].side//2
        starty=cell[0].y+cell[0].side//2
        endy=cell[1].y+cell[1].side//2

    elif attr=='r':
        startx=cell[0].x+cell[0].side//2
        endx=cell[1].x+cell[1].side//2
        starty=cell[0].y+cell[0].side//2
        endy=cell[1].y+cell[1].side//2

    col=(255,255,0)
    if p==1:
        col=(0,255,0)
    elif b==1:
        col=(255,0,0)
    pygame.draw.line(screen,col,(startx,starty),(endx,endy),12)
p,b=0,0
def check_win():
    ##along row
    global finished,p,b
    for i in range(0,9,3):
        row=cells[i:i+3]
        p_count,b_count=0,0
        for j in row:
            if j.full==0:
                p_count+=1
            elif j.full==1:
                b_count+=1
        if p_count==3:
            p=1
            win_line(row[0],'ro')
            finished=True
            return
        elif b_count==3:
            b=1
            win_line(row[0],'ro')
            finished=True
            return

    ##along cols
    diff=0
    col1=[cells[i] for i in range(len(cells)) if i%3==diff]
    diff+=1
    col2=[cells[i] for i in range(len(cells)) if i%3==diff]
    diff+=1
    col3=[cells[i] for i in range(len(cells)) if i%3==diff]
    for col in [col1,col2,col3]:
        p_count,b_count=0,0
        for j in col:
            if j.full==0:
                p_count+=1
            elif j.full==1:
                b_count+=1
        if p_count==3:
            p=1
            win_line(col[0],'c')
            finished=True
            return
        elif b_count==3:
            b=1
            win_line(col[0],'c')
            finished=True
            return


    ####for diagonals
    ##left
    diag_left=[cells[0],cells[4],cells[8]]
    p_count,b_count=0,0
    for j in diag_left:
        if j.full==0:
            p_count+=1
        elif j.full==1:
            b_count+=1
    if p_count==3:
        p=1
        win_line([diag_left[0],diag_left[2]],'l')
        finished=True
        return
    elif b_count==3:
        b=1
        win_line([diag_left[0],diag_left[2]],'l')
        finished=True
        return
    ##right
    diag_right=[cells[2],cells[4],cells[6]]
    p_count,b_count=0,0
    for j in diag_right:
        if j.full==0:
            p_count+=1
        elif j.full==1:
            b_count+=1
    if p_count==3:
        p=1
        win_line([diag_right[0],diag_right[2]],'r')
        finished=True
        return
    elif b_count==3:
        b=1
        win_line([diag_right[0],diag_right[2]],'r')
        finished=True
        return
    count=0
    for c in cells:
        if c.full!=-99:
            count+=1
    if count==len(cells) and (p!=1 or b!=1):
        finished=True

def bot_turn():
    global players_turn
    for c in cells:
        ###########this part needs implementation##########
        if c.full==-99:
            c.full=1
            c.draw_cross()
            check_win()
            players_turn=True
            break
finished=False
game=False
myfont = pygame.font.SysFont("Comic Sans MS", 40)
while True:
    x=-1
    y=-1
    for e in pygame.event.get():
        if e.type==KEYDOWN:
            if e.key==K_s:
                p=0
                b=0
                cells=[]
                finished=False
                game=True
                screen.fill((255,255,255))
                start()
                players_turn=True
            if e.key==K_q:
                pygame.quit()
            if e.key==K_r:
                cells=[]
                p=0
                b=0
                finished=False
                players_turn=True
                screen.fill((255,255,255))
                start()
        if e.type==MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()

    if game==False:
        label = myfont.render("PRESS 's' TO START", 3, (255,0,0))
        screen.blit(label,(23,80))

    if finished==False:
        for c in cells:
            if players_turn==True:
                if (x>c.x and x<c.x+c.side) and (y>c.y and y<c.y+c.side):
                    if c.full==-99:
                        c.full=0
                        c.draw_circle()
                        check_win()
                        players_turn=False
            else:
                if finished==False:
                    bot_turn()
            c.plot()
    else:
        winner=''
        if p==1:
            winner='YOU WON!!!'
            col=(0,255,0)
        elif b==1:
            winner='BOT WON!!!'
            col=(255,0,0)
        else:
            winner='!!!DRAW!!!'
        if winner!='':
            label = myfont.render(winner, 3, col)
            screen.blit(label,(10,20))

    pygame.display.update()
