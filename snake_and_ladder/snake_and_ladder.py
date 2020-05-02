import pygame
from pygame.locals import *
import time,random

w,h=840,700
screen_color = (110,0,200)
pygame.init()
screen=pygame.display.set_mode((w,h),0,32,pygame.HWSURFACE)
screen.fill(screen_color)
myfont = pygame.font.SysFont("Comic Sans MS", 20)
block_size=70

class Dice:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        img1 = pygame.image.load('1.png').convert_alpha()
        img2 = pygame.image.load('2.png').convert_alpha()
        img3 = pygame.image.load('3.png').convert_alpha()
        img4 = pygame.image.load('4.png').convert_alpha()
        img5 = pygame.image.load('5.png').convert_alpha()
        img6 = pygame.image.load('6.png').convert_alpha()

        self.dices = [img1,img2,img3,img4,img5,img6]

    def show(self,chosen_dice):
        dice = self.dices[chosen_dice]
        screen.blit(dice,(self.x,self.y))
        lab2 = myfont.render(str(chosen_dice+1), 20, (255, 255, 255))
        screen.blit(lab2,(self.x+30,self.y+74))

class Cell:
    def __init__(self,x,y,digit):
        self.x = x
        self.y = y
        self.color = (220,150,120)
        self.digit = digit

    def show(self):
        rect = (self.x,self.y,block_size-1,block_size-1)              #48,48
        pygame.draw.rect(screen, self.color, rect)
        lab2 = myfont.render(str(self.digit), 5, (255, 255, 255))
        screen.blit(lab2,(self.x+10,self.y+10))

class Player:
    def __init__(self, color, name= None, id = None, status = 1):
        self.x = 35
        self.y = 665
        self.color = color
        self.name = name
        self.row = 0
        self.id = id
        self.radius = 35
        self.status = status
        self.triumph = False

    def move(self):
        if not self.triumph:
            if self.row%2 == 0:
                self.x += block_size
            else:
                self.x -= block_size

            if self.x>=(w-2*block_size) or self.x<=0:
                if self.x>=(w-2*block_size):
                    self.x=((w-block_size)-3*self.radius)
                else:
                    self.x=self.radius
                self.y-=block_size
                self.row += 1

            if (self.x-self.radius,self.y-self.radius) in pixel_to_id:
                self.status = pixel_to_id[(self.x-self.radius,self.y-self.radius)].digit

    def got_connector(self):
        for con in connectors:
            if con.begin == self.status:
                self.x = con.finish[0] + 35
                self.y = con.finish[1] + 35
                self.status = con.end
                self.row = con.end //10

    def show(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)
        lab2 = myfont.render(str(self.id),5, (0,0,0))
        screen.blit(lab2,(self.x-5,self.y-14))

class Connectors:
    def __init__(self,attr = None, begin = None,end = None):
        self.begin = begin
        self.end = end
        self.attr = attr

        self.start = id_to_pix[self.begin]
        self.finish = id_to_pix[self.end]
        if attr == 's':
            self.color = (255,0,0)
        elif attr == 'l':
            self.color = (0,255,0)

    def show(self):
        pygame.draw.line(screen,self.color,(self.start[0]+35,self.start[1]+35),(self.finish[0]+35,self.finish[1]+35),10)

start = False
cells = []
x= 0
y=0
odd = 0

#dice class
dice = Dice(730,300)
#board class
pixel_to_id = {}
id_to_pix = {}
for i in range(100,0,-1):
    c = Cell(x=x,y=y,digit=i)
    pixel_to_id[(x,y)] = c
    id_to_pix[c.digit] = (x,y)
    if odd%2==0:
        x+=block_size
    else:
        x-=block_size
    if x>=(w-2*block_size) or x<0:
        if x>=(w-2*block_size):
            x=(w-3*block_size)
        else:
            x=0
        y+=block_size
        odd+=1
    cells.append(c)

#players class
players = []
MAX_PLAYERS = 2
colors = [[0,255,0],[255,0,0],[0,0,255],[255,255,0]]
for i in range(MAX_PLAYERS):
    color_idx = random.choice([x for x in range(len(colors))])
    p = Player(color = colors[color_idx], id = i)
    players.append(p)
    colors.pop(color_idx)

#connector class
num_of_snakes = 4
connectors = []
for _ in range(num_of_snakes):
    begin = random.randint(30,100)
    end = random.randint(2,begin-5)
    conn = Connectors(attr='s',begin=begin,end=end)
    connectors.append(conn)


num_of_ladders = 4
for _ in range(num_of_ladders):
    begin = random.randint(0,55)
    end = random.randint(begin+15,98)
    conn = Connectors(attr='l',begin=begin,end=end)
    connectors.append(conn)

prev_choice = 0
player_turn = 0
move_now = False
while True:
    for e in pygame.event.get():
        if e.type == KEYDOWN:
            if e.key == K_q:
                break

            if e.key == K_s:
                start =True
    screen.fill(screen_color)
    if start:
        for c in cells:
            c.show()
        num_chosen = prev_choice

        for conn in connectors:
            conn.show()

        for p in players:
            p.show()

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rotation = random.randint(250,275)
                for _ in range(rotation):
                    num_chosen = random.randint(0,5)
                    dice.show(num_chosen)
                prev_choice = num_chosen
                move_now = True

        if e.type == KEYUP:
            if e.key == K_SPACE:
                if move_now:
                    player_to_move = players[player_turn]
                    if player_to_move.triumph:
                        player_turn = (player_turn + 1) % len(players)
                        continue
                    count_recieved = num_chosen + 1

                    if player_to_move.status + count_recieved <= 100:
                        for _ in range(count_recieved):
                            player_to_move.move()
                        if player_to_move.status is not None:
                            if player_to_move.status == 100:
                                player_to_move.triumph = True

                        player_to_move.got_connector()
                    if count_recieved != 6:
                        player_turn = (player_turn + 1) % len(players)
                move_now = False

        dice.show(num_chosen)

        for p_id in range(len(players)-1,-1,-1):
            p = players[p_id]
            if p.triumph == True:
                lab_won = myfont.render("player {} WON".format(p.id),4, (255,255,255))
                screen.blit(lab_won,(703, 215))
        try:
            lab2 = myfont.render("TURN OF : {}".format(players[player_turn].id),5, (255,255,255))
            screen.blit(lab2,(705, 255))
        except:
            pass

    pygame.display.update()
