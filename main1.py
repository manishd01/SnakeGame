from pygame import *
from pygame.locals import *
# import pygame
import random
import time
SIZE=25
DISP_X=1300
DISP_Y=650
TIM=0.5
# BG_COLOR=(20,125,195)
class apple:
    def __init__(self,surf):
        self.parent_scr=surf
        self.image=image.load("resources/apple.jpg").convert()
        self.x=SIZE*10
        self.y=SIZE*10
    def drw_blk(self):
        # self.parent_scr.fill((20,125,195))     
        # for i in range(self.length):
        self.parent_scr.blit(self.image,(self.x,self.y))  #used for draw 
        display.flip() 
    def move(self):
        self.x=random.randint(1,25)*SIZE
        self.y=random.randint(1,19)*SIZE
class snake:
    def __init__(self,surf,length):
        self.parent_scr=surf
        self.block=image.load("resources/block.jpg").convert()  #adding small block from directory
        self.length=length  # [3]*4 will output as [3,3,3,3]  , 
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direct='down'
    def increse_len(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)



    def drw_blk(self):
        # self.parent_scr.fill(BG_COLOR)     
        for i in range(self.length):
            self.parent_scr.blit(self.block,(self.x[i],self.y[i]))   
        display.flip()  #to refresh from previvous state
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direct=='up':
            self.y[0]-=SIZE
        elif self.direct=='down':
            self.y[0]+=SIZE
        elif self.direct=='left':
            self.x[0]-=SIZE
        elif self.direct=='right':
            self.x[0]+=SIZE

        self.drw_blk()

    def move_up(self):
        self.direct='up'
        # self.y-=10
        # self.drw_blk()
    def move_down(self):
        self.direct='down'
        # self.y+=10
        # self.drw_blk()
    def move_left(self):
        self.direct='left'
        # self.x-=10
        # self.drw_blk()
    def move_right(self):
        self.direct='right'
        # self.x+=10
        # self.drw_blk()


class Game:
    def __init__(self):
        init()  #intialing pygame
        mixer.init()   #initialising sound and music object
        self.playBGmusic()
        self.surface=display.set_mode((DISP_X,DISP_Y))  #size of window
        self.Snake=snake(self.surface,1)
        self.Snake.drw_blk()
        self.Apple=apple(self.surface)
        self.Apple.drw_blk()
        
    def renderBG(self):
        bg=image.load("resources\BG2.jpg")
        self.surface.blit(bg, (0,0)) 
    def reset(self):
        self.Snake=snake(self.surface,1)
        self.Apple=apple(self.surface)

    def display_scr(self):
        font1=font.SysFont('arial',25)
        score=font1.render(f'Your Score: {self.Snake.length}',True,(0,0,0))# text  ,true,color
        self.surface.blit(score,(870,10))  #display score with these dimension

    def game_over(self):
        # self.surface.fill(BG_COLOR)
        self.renderBG()
        font1=font.SysFont('arial',35)
        line1=font1.render(f'Game is over! Your score is: {self.Snake.length}',True,(0,0,0))
        self.surface.blit(line1,(300,350)) #300,450 =(x-axis,y-axis)
        line2=font1.render(f'To play again press ENTER ,To exit press ESCAPE key',True,(0,0,0))
        self.surface.blit(line2,(300,450)) 
        display.flip()
        mixer.music.pause()
    
    def playBGmusic(self):
        mixer.music.load("resources/bg_music_1.mp3")  #music means constant sound running while sound play once only when any event occurs
        mixer.music.play(-1,0)
    def play_Sound(self,a):
        # if a=="ding.mp3":
        #     sound=mixer.Sound("resources/ding.mp3")
        # elif a=="crash.mp3":                            #working
        #     sound=mixer.Sound("resources/crash.mp3")
        sound=mixer.Sound(f"resources/{a}.mp3")
        mixer.Sound.play(sound)

    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<=x2+SIZE:
            if y1>=y2 and y1<=y2+SIZE:
                return True
        return False

    def play(self):
            self.renderBG()
            self.Snake.walk()
            self.Apple.drw_blk()
            self.display_scr()
            display.flip()
            # for i in range(self.Snake.length):

            #snake collide with apple +1 score
            if self.is_collision(self.Snake.x[0], self.Snake.y[0], self.Apple.x, self.Apple.y):
                print("collisio......")
                # sound = mixer.Sound("resources\ding.mp3")
                # mixer.Sound.play(sound)
                self.play_Sound("ding")
                self.Snake.increse_len()
                self.Apple.move()
                

        #snake collide with itself --game over    
            for i in range(3,self.Snake.length):
                if self.is_collision(self.Snake.x[0], self.Snake.y[0], self.Snake.x[i], self.Snake.y[i]):
                    print("game over.....")
                    # exit(0) not a better way
                    # sound = mixer.Sound("resources\crash.mp3")
                    # mixer.Sound.play(sound)
                    self.play_Sound("crash")
                    raise "Game over"
            # if self.is_collision(self.Snake.x[0],self.Snake.y[0], self.Snake.x[DISP_X+1], self.Snake.y[DISP_Y+1]):
            if not (0<=self.Snake.x[0]<=DISP_X and 0<=self.Snake.y[0]<=DISP_Y):
                # self.game_over() 
                self.play_Sound("crash")
                raise "crossed boundries"          #
    
    
    # d
    def run(self):
        running=True
        pause=False   #for breaking loop after game over
        while running:
            # pass  # if pass become infinite
            for eve in event.get():  # inside pygame.locals
                if eve.type==KEYDOWN:
                    if eve.key==K_ESCAPE:
                        running=False
                    if eve.key==K_RETURN:
                        mixer.music.unpause()
                        pause=False

                    if not pause:
                        if eve.key==K_UP:
                            self.Snake.move_up()
                        if eve.key==K_DOWN:
                            self.Snake.move_down()
                        if eve.key==K_LEFT:
                            self.Snake.move_left()
                        if eve.key==K_RIGHT:
                            self.Snake.move_right()
                        
                    
                elif eve.type==QUIT:  #QUIT is close button on windows title bar ,when equals to this terminate program
                    running=False 
              
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause=True
                self.reset()
                # time.sleep(2)
            # t=int(0.1)
            time.sleep(TIM) #must be here (indent with forloop)-- for auto movement of snake
            # TIM=TIM-t

    
        

        


if __name__=="__main__":
    game=Game()  #object creation
    game.run()  #run F called

   