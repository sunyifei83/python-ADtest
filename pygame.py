import pygame, sys
import time
from pygame.locals import *

pygame.init()
fpsClock=pygame.time.Clock()
screen= pygame.display.set_mode((640,480))
pygame.display.set_caption('Test')
fontobj= pygame.font.Font('LCD_Solid.ttf',50)
mousex,mousey=0,0
x_1=15
x_2=600 #these varaibles (x_1, x_2) are different, but they are constants-- they will never change; think jon, the paddle will not move from left to right
y=0 #the y variable changes, but for this test it will be the same for both paddles bc they are moving in unisen.
x_ball=320
y_ball=240
direction=""
def draw_stuff (y):
        msg=str(x_ball)
        global x_ball,y_ball,direction
        textobj=fontobj.render(msg, False , pygame.Color('green'))
        screen.blit(textobj,(160,5))
        screen.blit(textobj,(480,5))
        pygame.draw.line(screen,pygame.Color('grey'),(320,0), (320,480), 4)
        pygame.draw.line(screen,pygame.Color('grey'),(0,3), (640,3), 10)
        pygame.draw.line(screen,pygame.Color('grey'),(0,475), (640,475), 10)
        pygame.draw.rect(screen, pygame.Color('grey'),(x_1,y,30,192))
        pygame.draw.rect(screen, pygame.Color('grey'),(x_2,y,30,192))
        if x_ball==60 or x_ball==570:
            print "we have reached the side",fpsClock.get_fps()
            if ball_hit(y,x_ball,y_ball):
                topl,middlel,bottoml=loc_of_ball_hitl(y,x_ball,y_ball)
                topr,middler,bottomr=loc_of_ball_hitr(y,x_ball,y_ball)
                if topl:
                    direction="upleft"
                elif middlel:
                    direction='midleft'
                elif bottoml:
                    direction='downleft'
                elif topr:
                    direction="upright"
                elif middler:
                    direction="midright"
                elif bottomr:
                    direction="downright"
                else:
                    direction=""
        if not direction:
            print "we have ",fpsClock.get_fps()
            x_ball+=2
        elif direction=="upleft":
            x_ball+=2
            y_ball-=2
        elif direction=="midleft":
            x_ball+=2
        elif direction=="downleft":
            x_ball+=2
            y_ball+=2
        elif direction=="upright":
            x_ball-=2
            y_ball-=2
        elif direction=="midright":
            x_ball-=2
        elif direction=="downright":
            x_ball-=2
            y_ball+=2
        ball(x_ball,y_ball)



def ball(x,y):
    pygame.draw.circle(screen, pygame.Color('red'), (x,y), 15, 0)
    pygame.display.update()
def ball_hit(y,ball_x,ball_y):
    if ball_x==60 and ball_y>=y and ball_y<y+192 or ball_x==570 and ball_y>=y and ball_y<y+192:
        return True
    return False
def loc_of_ball_hitl(y,ball_x,ball_y):
   middle=False
   top=False
   bottom=False
   if ball_x==60 and ball_y>=y+64 and ball_y<y+128:
        middle=True
   elif ball_x==60 and ball_y>=y and ball_y<y+64:
        top=True
   elif ball_x==60 and ball_y>=y+128 and ball_y<y+192:
        bottom=True
   return top, middle, bottom
def loc_of_ball_hitr(y,ball_x,ball_y):
   middle=False
   top=False
   bottom=False
   if ball_x==570 and ball_y>=y+64 and ball_y<y+128:
        middle=True
   elif ball_x==570 and ball_y>=y and ball_y<y+64:
        top=True
   elif ball_x==570 and ball_y>=y+128 and ball_y<y+192:
        bottom=True
   return top, middle, bottom
while True:
    screen.fill(pygame.Color('black'))
    if mousey>y:
        draw_stuff(y)
        y+=2
    if mousey<y:
        draw_stuff(y)
        y-=2
    if mousey==y:
        draw_stuff(y)
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type== MOUSEMOTION:
            mousex,mousey=event.pos
    pygame.display.update()
    fpsClock.tick(200)