import math
import pygame
import pymunk
import random
import time
import os
import sys
'''
cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
print(cwd + '\\dat')
sys.path.append(cwd + '\\dat')
import constants
'''
def main():
    pygame.init()
   
    BACKGROUND = (150, 150, 150) #making the background color
   
    world = pymunk.Space()
    world.gravity = (0, 1000) #sets gravity
    world.damping = .4 #how much resistance/friction there is in the world
    
    screenSize = constants.screenSize
    print(screenSize)
   
    left = False
    right = False
    up = False
    down = False
    shift = False
    global RUNNING 
    RUNNING = True
    screen = pygame.display.set_mode((screenSize[0]*2, screenSize[1]*2))
    clock = pygame.time.Clock()
   
    pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
   
    class Player():
        def __init__(self, startx, starty, width, height):
            self.ballRadius = radius
            self.ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, self.ballRadius))
            self.ball_body.position = (startx, starty)
            world.add(self.ball_body, self.ball_shape)
            self.image = pygame.image.load("digitalminds.png")
            self.image = pygame.transform.scale(self.image, (self.ballRadius * 2,self.ballRadius * 2))
            self.imageRect = self.image.get_rect(center = self.ball_body.position)
            
        def draw(self):
            self.angle_degrees = math.degrees(self.ball_body.angle)
            self.rotatedimage = pygame.transform.rotate(self.image, -self.angle_degrees)
            self.imageRect = self.rotatedimage.get_rect(center = self.ball_body.position)
            pygame.draw.circle(screen, (0,0,0), (int(self.ball_body.position.x), int(self.ball_body.position.y)), self.ballRadius + 2)
            pygame.draw.circle(screen, (255,255,255), (int(self.ball_body.position.x), int(self.ball_body.position.y)), self.ballRadius) 
            
   
    class Line():
        def __init__(self, firstpoint, secondpoint, ela, fric):
            self.point1, self.point2 = firstpoint, secondpoint
            self.width = screenSize[0]//screenSize[1]*6 #Width of lines
           
            self.lineBody = pymunk.Body(body_type=pymunk.Body.STATIC) #anchoring the floor
            self.lineShape = pymunk.Segment(self.lineBody, (self.point1), (self.point2), self.width) #connecting the two points to form floor line
            self.lineShape.elasticity = ela #what percent of energy goes into bounce
            self.lineShape.friction = fric # idk lol
            world.add(self.lineShape, self.lineBody) #creating the land like god did on the third day  
        def draw(self):
            pygame.draw.line(screen, (0,0,0), (self.point1), (self.point2), self.width)
   
    class text():
        def __init__(self, textFont, textWritten, x, y, size):
            self.x = x
            self.y = y
            self.font = pygame.font.Font(textFont, size)
            self.textWritten = textWritten
            self.text = self.font.render(self.textWritten, True, (0,0,0))
            self.currAnswer = js['answer' + str(qNum)]
           
            self.location = self.text.get_rect(center = (self.x, self.y))
           
        def reWrite(self, textWritten):
            self.textWritten = textWritten
            self.text = self.font.render(self.textWritten, True, (0,0,0),)
            self.location = self.text.get_rect(center = (self.x, self.y))
           
        def draw(self):
            screen.blit(self.text, self.location)
   
    text1 = text('freesansbold.ttf', currAnswers[0], screenSize[0]/8, screenSize[1]/1.222222, 32)

    floor = Line((0,screenSize[1]),(screenSize[0],screenSize[1]), 1, 5)
    wall1 = Line((0,-150),(0,screenSize[1]), 0, 0)
    wall2 = Line((screenSize[0],-150),(screenSize[0],screenSize[1]), 0, 0)
    roof = Line((0,0),(screenSize[0],0), 1, 0)
   
    linelist = []
    linelist.extend([
        Line((0, (3 * (screenSize[1] / 9))), ((2 * (screenSize[0] / 16)), (3 * (screenSize[1] / 9))), 1, 5),
        
    ])
    def background():
        #image
    while RUNNING:
        screen.fill(BACKGROUND) # creating the sky like god did on the second day
        background()
       
        for i in range(len(linelist)):
            linelist[i].draw()
        events = pygame.event.get()
           
        for event in events:
            if event.type == pygame.KEYDOWN: # if there is a key pressed down then check for which key(s) is pressed down
                if event.key == pygame.K_ESCAPE: #if you press the escape key the game game closes
                    RUNNING = False
                if event.key == pygame.K_LEFT: #if you press left arrow then you go.... left
                    left = True
                if event.key == pygame.K_RIGHT: #if you press right arrow then you go..... right
                    right = True
                if event.key == pygame.K_UP: #if you press uparrow it sets up boolean  to true
                    up = True
                if event.key == pygame.K_DOWN:
                    down = True
                if event.key == pygame.K_LSHIFT:
                    shift = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_DOWN:
                    down = False
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_LSHIFT:
                    shift = False
                    
        pygame.display.update()
       
        world.step(1/60.0)
        clock.tick(60)

if __name__ == "__main__":
    main()

pygame.quit()