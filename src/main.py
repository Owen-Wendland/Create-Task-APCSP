'''
Owen Wendland
APCSP 
Create Task
'''
import math
import pygame
import pymunk
import random
import time
import os
import sys
import tkinter
import platform
#^^^^^ Importing needed imports ^^^^^

cwd = os.getcwd()
cwd = str(cwd)

if platform.system == 'Windows':
    cwd = cwd.replace('src','')
else:
    cwd = cwd.replace('src','')
    
sys.path.append(cwd + 'res')

import constants
#This cwd section takes the 'Current Working Directory'

def main():
    pygame.init() #Initializes pygame
   
    BACKGROUND = (constants.Background) #Makes the background a color
   
    world = pymunk.Space() #Making the physics world
    world.gravity = (0, 1000) #Making gravity pull on objects
    world.damping = .3 #Applying air resistance to objects
    
    screenSize = constants.screenSize #gets the size of your monitor
    
    global RUNNING
    RUNNING = True #Makes running true, running is the variable used to check if game is running
    
    screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
   
    #pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
           
    class text():
        def __init__(self, textFont, textWritten, x, y, size):
            self.x = x
            self.y = y
            self.font = pygame.font.Font(textFont, size)
            self.textWritten = textWritten
            self.text = self.font.render(self.textWritten, True, (0,0,0))
           
            self.location = self.text.get_rect(center = (self.x, self.y))
           
        def reWrite(self, textWritten):
            self.textWritten = textWritten
            self.text = self.font.render(self.textWritten, True, (0,0,0),)
            self.location = self.text.get_rect(center = (self.x, self.y))
           
        def draw(self):
            screen.blit(self.text, self.location)
   
    plinkoBall = constants.Plinko(200, 200, screenSize[0]//66,world, screen)
    
    balls = []
    for i in range(21):
        balls.extend([
            constants.ball(int(screenSize[0]//5*i//2), int(screenSize[1]//6), int(screenSize[0]//96), world, screen),
            constants.ball(int(screenSize[0]//5*i//2 + (screenSize[0]//5)//4), int(screenSize[1]//6*2), int(screenSize[0]//96), world, screen),
            constants.ball(int(screenSize[0]//5*i//2), int(screenSize[1]//6*3), int(screenSize[0]//96), world, screen),
            constants.ball(int(screenSize[0]//5*i//2 + (screenSize[0]//5)//4), int(screenSize[1]//6*4), int(screenSize[0]//96), world, screen),
            constants.ball(int(screenSize[0]//5*i//2), int(screenSize[1]//6*5), int(screenSize[0]//96), world, screen)
        ])
    
    floor = constants.Line((0,screenSize[1]),(screenSize[0],screenSize[1]), 0, 5, 3, world, screen)
    wallLeft = constants.Line((0,-150),(0,screenSize[1]), 0, 0, 4, world, screen)
    wallRight = constants.Line((screenSize[0],-150),(screenSize[0],screenSize[1]), 0, 0, 4, world, screen)
    roof = constants.Line((0,0),(screenSize[0],0), 1, 0, 4, world, screen)
   
    linelist = []
    linelist.extend([
        floor,
        wallLeft,
        wallRight,
        roof
    ])
    
    for i in range(10):
        linelist.extend([
            constants.Line((screenSize[0]//10*i,screenSize[1]),(screenSize[0]//10*i,screenSize[1]//12*10), 1, 5, 4, world, screen)
        ])
        
    plinkoBall.notClicked = True
    
    blip = pygame.mixer.Sound(cwd + "res/plinko.wav")

    
    def sound(arbiter, world, data):
        pygame.mixer.Sound.play(blip)
    def reset(arbiter, world, data):
        plinkoBall.notClicked = True
        return(True)
        
    plink = world.add_collision_handler(1, 2)
    floorPlink = world.add_collision_handler(1, 3)
    plink.separate = sound
    floorPlink.begin = reset
        
    while RUNNING:
        screen.fill(BACKGROUND) 
        
        for i in range(len(linelist)):
            linelist[i].draw()
        
        for i in range(len(balls)):
            balls[i].draw()
            
        plinkoBall.draw()
        
        events = pygame.event.get()
           
           
        if(plinkoBall.notClicked):
            pos = (pygame.mouse.get_pos()[0],screenSize[1]//20)
            plinkoBall.ball_body.position = pos
            plinkoBall.ball_body.velocity = (0,0)
            plinkoBall.ball_body.angle = 0
                      
        for event in events:
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: 
                    RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                plinkoBall.notClicked = False
                    
                    
        pygame.display.update()
       
        world.step(1/60.0)
        clock.tick(60)

if __name__ == "__main__":
    main()

pygame.quit()
