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

def win_line_func(cell,attr):
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
win_line=None
def check_win():
    ##along row
    global finished,p,b,win_line
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
            win_line=(row[0],'ro')
            finished=True
            return
        elif b_count==3:
            b=1
            win_line=(row[0],'ro')
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
            win_line=(col[0],'c')
            finished=True
            return
        elif b_count==3:
            b=1
            win_line=(col[0],'c')
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
        win_line=([diag_left[0],diag_left[2]],'l')
        finished=True
        return
    elif b_count==3:
        b=1
        win_line=([diag_left[0],diag_left[2]],'l')
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
        win_line=([diag_right[0],diag_right[2]],'r')
        finished=True
        return
    elif b_count==3:
        b=1
        win_line=([diag_right[0],diag_right[2]],'r')
        finished=True
        return
    count=0
    for c in cells:
        if c.full!=-99:
            count+=1
    if count==len(cells) and (p!=1 or b!=1):
        finished=True

matrix=[[-99,-99,-99],[-99,-99,-99],[-99,-99,-99]]
def bot_turn():
    global players_turn
    for i in range(3):
        for j in range(3):
            ind=i*3+j
            if cells[ind].full==0:
                matrix[i][j]=0
            elif cells[ind].full==1:
                matrix[i][j]=1

    bestmove()

def bestmove():
    global players_turn
    bestscore=-9999999999
    move=None
    for i in range(3):
        for j in range(3):
            if matrix[i][j]==-99:
                matrix[i][j]=1
                ind=i*3+j
                cells[ind].full=1
                score=minimax(matrix,0,False)
                matrix[i][j]=-99
                cells[ind].full=-99
                if score>bestscore:
                    bestscore=score
                    move=(i,j)
    matrix[move[0]][move[1]]=1
    ind=move[0]*3+move[1]
    cells[ind].full=1
    cells[ind].draw_cross()
    check_win()
    players_turn=True

def minimax(matrix,depth,ismaximizing):
    ##break condition##
    global finished,p,b
    check_win()
    if p==1:
        p=0
        b=0
        finished=False
        return -1
    elif b==1:
        p=0
        b=0
        finished=False
        return 1
    elif finished==True:
        p=0
        b=0
        finished=False
        return 0
    if ismaximizing==True:
        bestscore=-999999999
        for i in range(3):
            for j in range(3):
                if matrix[i][j]==-99:
                    matrix[i][j]=1
                    ind=i*3+j
                    cells[ind].full=1
                    score=minimax(matrix,depth+1,False)
                    matrix[i][j]=-99
                    cells[ind].full=-99
                    if score>bestscore:
                        bestscore=score

        return bestscore
    else:
        bestscore=999999999
        for i in range(3):
            for j in range(3):
                if matrix[i][j]==-99:
                    matrix[i][j]=0
                    ind=i*3+j
                    cells[ind].full=0
                    score=minimax(matrix,depth+1,True)
                    matrix[i][j]=-99
                    cells[ind].full=-99
                    if score<bestscore:
                        bestscore=score

        return bestscore

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
                matrix=[[-99,-99,-99],[-99,-99,-99],[-99,-99,-99]]
                finished=False
                game=True
                screen.fill((255,255,255))
                start()
                players_turn=True
            if e.key==K_q:
                pygame.quit()
            if e.key==K_r:
                cells=[]
                matrix=[[-99,-99,-99],[-99,-99,-99],[-99,-99,-99]]
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
        col=(255,0,255)
        if p==1:
            win_line_func(win_line[0],win_line[1])
            winner='YOU WON!!!'
            col=(0,255,0)
        elif b==1:
            win_line_func(win_line[0],win_line[1])
            winner='BOT WON!!!'
            col=(255,0,0)
        else:
            winner='!!!DRAW!!!'
        if winner!='':
            label = myfont.render(winner, 3, col)
            screen.blit(label,(10,20))

    pygame.display.update()
