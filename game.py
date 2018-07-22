import pygame
import random
import time
import tkinter as tk
import pyglet as sound
from PIL import Image,ImageTk
FPS=25
class startScreen(object):
    def __init__(self):
         self.app = tk.Tk()
         pygame.init()
         pygame.mixer.init()
         pygame.mixer.set_num_channels(3)


    def game(self):
        # starting screen
        s = startGame()
        s.gameLoop()



    def start(self):
        self.app.maxsize(height=400,width=750)
        self.app.minsize(height=400,width=750)
        self.app.resizable(height=False, width=False)
        self.app.title('Snake Game')
        self.page1 = tk.Frame(self.app)
        #Page1
        i=ImageTk.PhotoImage(Image.open('back.png'))
        back_labe=tk.Label(self.page1,image=i,height=400)
        back_labe.pack()
        self.page1.pack()
        pygame.mixer.Channel(0).set_volume(.1)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("snake(1).wav"))
        self.app.update()
        time.sleep(10)
        pygame.mixer.Channel(0).stop()
        self.app.destroy()
        self.game()






class Snake(object):
    # snakeHead image
    direction="up"
    img=pygame.image.load("snake head2.png")
    #snakebody
    img2=pygame.image.load("snakebody.png")
    #snake coordinates
    snake_x=0
    snake_y=0
    #snake length,list,heads
    snakeBlocks=[]
    snakeLength=1
    #snakeHead=snakeList[:-1]
    #snake movement change
    snake_x_change = 0
    snake_y_change = 0
    #how many pixels snake move
    snake_distance=0
    #score
    score=0
    #init which requires win to diplay snake
    #colors
    #position of initially snake displayed
    def __init__(self,win,colors,x,y):
        self.win=win
        self.colors=colors
        self.snake_x=x
        self.snake_y=y

    #snake whose coordinates is update with time to time
    def move(self,direction):
        self.direction=direction
        if self.direction=="up":
            head=self.img
            body=self.img2
        elif self.direction=="down":
            head=pygame.transform.rotate(self.img,180)
            body=pygame.transform.rotate(self.img2,180)
        elif self.direction=="left":
            head=pygame.transform.rotate(self.img,90)
            body = pygame.transform.rotate(self.img2, 90)
        elif self.direction=="right":
            head=pygame.transform.rotate(self.img,270)
            body = pygame.transform.rotate(self.img2, 270)
        self.win.blit(head,self.snakeBlocks[-1])
        for X_Y in self.snakeBlocks[:-1]:
            self.win.blit(body, (X_Y[0], X_Y[1]))


class Apple(object):
    #apple images
    small_apple=pygame.image.load('apple-small.png')
    large_apple = pygame.image.load('apple-large.png')
    #apple coordinates
    apple_x=0
    apple_y=0
    #large apple coordinates
    apple_x_large = 0
    apple_y_large = 0
    #initialization of window colors, assigning random value to x,y co-ordinates
    def __init__(self,win,colors):
        self.win=win
        self.colors=colors
        self.apple_x=random.randrange(80,780)
        self.apple_y=random.randrange(80,780)
        self.apple_x_large = random.randrange(80, 780)
        self.apple_y_large = random.randrange(80, 780)

    #small apple
    def draw(self):
        self.win.blit(self.small_apple,(self.apple_x,self.apple_y))
    #large apple
    def drawLarge(self):
        self.win.blit(self.large_apple, (self.apple_x_large, self.apple_y_large))

    #progressbar functions
    def progress(self,win,x,width):
        if width < 0:
            pass
        else:
            pygame.draw.rect(win, self.colors['light blue'], (x, 20, 200, 20))
            pygame.draw.rect(win,self.colors['blue'],(x,20,width,20))
            prog=self.text("%d"%int((width/200)*100))
            win.blit(prog,[700,15])
    #message displaying function
    def text(self,msg):
        font=pygame.font.SysFont("ComicSansMS",20)
        text=font.render(msg,0,self.colors['red'])
        return text


class Crash(object):
    #snake hits the apple or not
    def collision(self,snake_x,snake_y,apple_x,apple_y,block_size):
        if snake_x-block_size >= apple_x and snake_x+block_size <= apple_x or snake_x+block_size >= apple_x and snake_x-block_size <= apple_x:
            if snake_y-block_size >= apple_y and snake_y+block_size <= apple_y or snake_y+block_size >= apple_y and snake_y-block_size<= apple_y:
                pygame.mixer.Channel(1).pause()
                pygame.mixer.Channel(2).play(pygame.mixer.Sound("snake(2).wav"))
                pygame.mixer.Channel(2).set_volume(0.1)
                pygame.mixer.Channel(1).unpause()
                return True
        else:
            return False



class startGame(object):
    global FPS
    win_height=0
    win_width=0
    colors={}
    win=""
    gameOver=False
    gameOverScreen=False
    gamePauseScreen=False
    channel=""
    audio=pygame.image.load('audio.png')
    audio_state=""
    def __init__(self):
        startGame.FPS=FPS
        self.win_height=800
        self.win_width=800
        self.colors={'white':(255,255,255),'black':(0,0,0),'red':(255,0,0),'green':(0,255,0),'blue':(0,0,255),'light blue':(173,216,230)}
        pygame.mixer.Channel(1).set_volume(0.2)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("numb.wav"))

    #audio button
    def audio_button(self,state):
        if state=="play":
            pygame.mixer.Channel(1).set_volume(0.2)
            startGame.audio = pygame.image.load('audio.png')
        else:
            pygame.mixer.Channel(1).set_volume(0.0)
            startGame.audio = pygame.image.load('no-audio.png')
    #checking bounds of screen
    def outOfScreen(self,x,y):
        # for x-axis
        if x >= self.win_width:
            x = 0
        elif x < 0:
            x = 800
        else:
            pass
        # for y-axis
        if y >= self.win_height:
            y = 60
        elif y-60 < 0:
            y = 800
        else :
            pass
        return x,y

    #message displaying function
    def text(self,msg,size,color):
        font=pygame.font.SysFont("ComicSansMS",size)
        text=font.render(msg,0,self.colors[color])
        return text
    #Game Over Screen
    def GameOver(self,win,x):
        self.FPS=25
        while startGame.gameOverScreen:
            for event in pygame.event.get():
                # exit button on window
                if event.type == pygame.QUIT:
                    startGame.gameOverScreen = False
                    startGame.gameOver = True
                # c is for gamerestart, q is for exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        startGame.gameOverScreen = False
                        x.snakeLength = 1
                        del x.snakeBlocks[:-1]
                        x.score = 0
                    elif event.key == pygame.K_q:
                        startGame.gameOver = True
                        startGame.gameOverScreen = False
            win.fill(self.colors['white'])
            msg_over = self.text("Game Over", 50, 'red')
            msg_score = self.text("Your score: {}".format(x.score), 30, 'black')
            msg_ins = self.text("Press c to restart or q to exit", 25, 'black')
            win.blit(msg_over, [270, 340])
            win.blit(msg_score, [290, 410])
            win.blit(msg_ins, [220, 470])
            pygame.display.update()

    #pause screen
    def PauseScreen(self,win):
        while startGame.gamePauseScreen:
            for event in pygame.event.get():
                # exit button on window
                if event.type == pygame.QUIT:
                    startGame.gamePauseScreen=False
                    startGame.gameOver = True
                # c is for gamerestart, q is for exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.Channel(1).unpause()
                        startGame.gamePauseScreen = False
            win.fill(self.colors['white'])
            msg_pause = self.text("Pause", 50, 'red')
            msg_ins = self.text("Press Escape to continue", 25, 'black')
            win.blit(msg_pause, [340, 340])
            win.blit(msg_ins, [260, 410])
            pygame.display.update()

    def gameLoop(self):
        #window creation in pygame
        pygame.init()
        #progressBar width
        progress_width=200
        win = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Snake Game")
        #-10 for snake Thickness
        x=Snake(win,self.colors,(self.win_width/2)-10,self.win_height/2)
        #apple object
        apple=Apple(win,self.colors)
        #setting up fps clocks
        clock=pygame.time.Clock()
        s = ""
        fps_check = False
        startGame.audio_state="play"
        #for keeping screen active
        while not startGame.gameOver:
            #Event Handling
            for events in pygame.event.get():
                #mosue click for audio
                if pygame.mouse.get_pos()[0]>8 and pygame.mouse.get_pos()[0]<31:
                    if pygame.mouse.get_pos()[1]>21 and pygame.mouse.get_pos()[1]<40:
                        if events.type == pygame.MOUSEBUTTONUP:
                            if startGame.audio_state=='play':
                                startGame.audio_state='mute'
                            else:
                                startGame.audio_state = 'play'
                #exit button on window
                if events.type == pygame.QUIT:
                    startGame.gameOver=True
                #after key pressed
                if events.type == pygame.KEYDOWN:
                    x.snake_distance = 10
                    #movement controls
                    if events.key==pygame.K_LEFT:
                        x.snake_x_change=-x.snake_distance
                        x.snake_y_change=0
                        x.direction="left"
                    elif events.key==pygame.K_RIGHT:
                        x.snake_x_change=x.snake_distance
                        x.snake_y_change = 0
                        x.direction="right"
                    elif events.key==pygame.K_UP:
                        x.snake_y_change=-x.snake_distance
                        x.snake_x_change=0
                        x.direction="up"
                    elif events.key==pygame.K_DOWN:
                        x.snake_y_change = x.snake_distance
                        x.snake_x_change = 0
                        x.direction="down"
                    elif events.key == pygame.K_ESCAPE:
                        #pause music on pause screen
                        pygame.mixer.Channel(1).pause()
                        startGame.gamePauseScreen=True

            #music Checking
            if (pygame.mixer.Channel(1).get_busy()):
                pass
            else:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("numb.wav"))
            #updating movements continuously
            x.snake_x+=x.snake_x_change
            x.snake_y+=x.snake_y_change
            #checking snake goes out of screen
            #then re-updating on screen with opposite direction
            x.snake_x,x.snake_y=self.outOfScreen(x.snake_x,x.snake_y)

            #background color
            win.fill(self.colors['white'])
            #snake creation and movement and length rules
            #GameOver Screen is remaining
            x.snakeBlocks.append([x.snake_x, x.snake_y])
            if len(x.snakeBlocks) > x.snakeLength:
                del x.snakeBlocks[0]

            #fps speed or snake becomes faster after increasing it's length every 4 times
            # fps_check is to control fps rate per loop
            if len(x.snakeBlocks)%8==0 and fps_check ==False:
                startGame.FPS +=1
                fps_check=True
            elif len(x.snakeBlocks)%8!=0 and fps_check ==True:
                fps_check=False
            # gameOver screen
            self.GameOver(win,x)

            #Pause Screen
            self.PauseScreen(win)

            # snake  creation
            x.move(x.direction)

            # selecting snake body without head
            for block in x.snakeBlocks[:-1]:
                if block == x.snakeBlocks[-1]:
                    startGame.gameOverScreen = True


            #score
            score_display=self.text("Score: "+str(x.score),20,'red')
            win.blit(score_display,[50,15])

            # audio button
            # audio button display
            self.audio_button(startGame.audio_state)
            win.blit(startGame.audio, [8, 20])


#Apple Drawing screen and Logic:start
            #for detection of collision between apple and snake
            crash = Crash()
            collide=False

            #checking score greater than 0 and will be mod of 30 and progresswidth greater than 0
            # or checking that the apple has drawn or finish and the width of progress bar is > 0
            if (x.score>0 and x.score%30 == 0 and progress_width>0) or (s=="drawn"and progress_width>0):
                #for apple state
                s="drawn"
                apple.drawLarge()
                collide = crash.collision(x.snake_x, x.snake_y, apple.apple_x_large, apple.apple_y_large, 25)
            # progressbar-activity
                apple.progress(win, 500, progress_width)
            # Crash Detection For apple and large apple
                if collide == True:
                    x.score += 14
                    x.snakeLength += 2
                    #state change if collide
                    s="finish"
                    apple.apple_x_large = random.randrange(80, 780)
                    apple.apple_y_large = random.randrange(80, 780)
                progress_width-=1
            else:
                # state change if PROGRESS WIDTH BECOMES <= 0
                s="finish"
            #everytime when screen starts no logics are implented on this apple
            if x.score>=0:
                apple.draw()
                collide = crash.collision(x.snake_x, x.snake_y, apple.apple_x, apple.apple_y, 15)
                if collide == True:
                        x.score += 2
                        x.snakeLength += 1
                        apple.apple_x = random.randrange(80, 780)
                        apple.apple_y = random.randrange(80, 780)
            #reupdating progress bar after it becomes <=0 and score mode with 30 gives remainder and staet is not drawn
            if (progress_width< 200 and x.score%30 != 0 and s!='drawn'):
                progress_width=200
 # Apple Drawing screen and Logic:ends

            #border line between game and score
            pygame.draw.line(win, self.colors['black'], (0, 60), (800, 60), 2)

            #updating screen per frame
            pygame.display.update()

            #frames per second
            clock.tick(startGame.FPS)

        #Quit events
        pygame.quit()
        quit()


y=startScreen()
y.start()