'''
Owen Wendland
APCSP 
Create Task
'''
import pygame
import pymunk
import random
import os
import sys
import platform
#^^^^^ Importing needed imports ^^^^^

cwd = os.getcwd()
cwd = str(cwd)

if platform.system == 'Windows':
    cwd = cwd.replace('src','')
    
else:
    cwd = cwd.replace('/src','')
    
sys.path.append(cwd + '/res')

import constants
#This cwd section takes the 'Current Working Directory' and adds the constants file to it

class Variables():
    def __init__(self):
        self.score = 0
        self.tries = 1
        
var = Variables()

def main():
    pygame.init() #Initializes pygame
   
    BACKGROUND = (constants.Background) #Makes the background a color
   
    world = pymunk.Space() #Making the physics world
    world.gravity = (0, 1000) #Making gravity pull on objects
    world.damping = .3 #Applying air resistance to objects
    
    screenSize = constants.screenSize #Gets the size of your monitor
    
    global RUNNING
    RUNNING = True #Makes running true, running is the variable used to check if game is running
    
    screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN) #Making the screen
    #screen = pygame.display.set_mode(screenSize)
    clock = pygame.time.Clock() #Defining the FPS module of the game 

    plinkoBall = constants.Plinko(200, 200, screenSize[0]//66,world, screen)
    #Makes the plinko circle
    
    balls = []
    for i in range(21):
        balls.extend([
            constants.ball(int(screenSize[0]//5*i//2), int(screenSize[1]//6), int(screenSize[0]//96), world, screen),
            constants.ball(int(screenSize[0]//5*i//2 + (screenSize[0]//5)//4), int(screenSize[1]//6*2), int(screenSize[0]//96), world, screen),
            constants.ball(int(screenSize[0]//5*i//2), int(screenSize[1]//6*3), int(screenSize[0]//96), world, screen),
            constants.ball(int(screenSize[0]//5*i//2 + (screenSize[0]//5)//4), int(screenSize[1]//6*4), int(screenSize[0]//96), world, screen),
            constants.ball(int(screenSize[0]//5*i//2), int(screenSize[1]//6*5), int(screenSize[0]//96), world, screen)
        ])
    #Makes the balls the plinko ball bounces off of by screen size
    
    floor = constants.Line((0,screenSize[1]),(screenSize[0],screenSize[1]), 0, 5, 3, world, screen)
    wallLeft = constants.Line((0,-150),(0,screenSize[1]), 0, 0, 4, world, screen)
    wallRight = constants.Line((screenSize[0],-150),(screenSize[0],screenSize[1]), 0, 0, 4, world, screen)
    roof = constants.Line((0,0),(screenSize[0],0), 1, 0, 4, world, screen)
    #Builds walls around the screen
   
    linelist = []
    linelist.extend([
        floor,
        wallLeft,
        wallRight,
        roof
    ])
    #Makes a list containing the lines for the wall
    
    for i in range(10):
        linelist.extend([
            constants.Line((screenSize[0]//10*i,screenSize[1]),(screenSize[0]//10*i,screenSize[1]//12*10), 1, 5, 4, world, screen)
        ])
    #Adds the sections at the bottom used for containing the ball
        
    textList = [constants.text('freesansbold.ttf', ('score: 0'), screenSize[0]/2, screenSize[1]/10, 64, screen)]
        
    for i in range(10):
        if(i < 5):
            a = i * 0.5
        elif(i == 5):
            a = (i * 0.5) - 0.5
        else:
            a = 2 - ((i - 5) * 0.5)
            
        textList.extend([
            constants.text('freesansbold.ttf', str(round(a,1)), (screenSize[0]//20 * 2 * i) + screenSize[0]//20, screenSize[1]//9 * 8, 32, screen)
        ])
        
    zones = []
    for i in range(11):
        zones.extend([
            (screenSize[0]//10 * i)
        ])
        
    plinkoBall.notClicked = True
    #sets the plinkoBall to notClicked
    
    blip = pygame.mixer.Sound(cwd + "/res/plinko.wav")
    #defines the blip sound used for when the ball bounces

    def sound(arbiter, world, data):
        pygame.mixer.Sound.play(blip) 
    #The sound function used to play a sound when bounced
    def reset(arbiter, world, data):
        
        for i in range(10):
            x = plinkoBall.ball_body.position.x
            if(x > zones[i] and zones[i + 1] > x):
                if(i < 5):
                    a = i * 0.5
                elif(i == 5):
                    a = (i * 0.5) - 0.5
                else:
                    a = 2 - ((i - 5) * 0.5)
                
                var.score += a
                
        text = ('score: ' + str(var.score))
        text = str(text)
        textList[0].reWrite(text)
        
        plinkoBall.notClicked = True
        var.tries += 1
        return(True)
    #The reset function
        
    plink = world.add_collision_handler(1, 2)
    floorPlink = world.add_collision_handler(1, 3)
    #Making the collision handler for the bounce of the ball and when it hits the ground
    plink.separate = sound
    #Runs sound when bouncing
    floorPlink.begin = reset
    #Runs reset when hits floor
    maxTries = 10
    #defines max tries
    lastPos = screenSize[0]//2
    #defining start pos
    while RUNNING:
        screen.fill(BACKGROUND)
        #Fills the background of the screen
        
        for i in range(len(linelist)):
            linelist[i].draw()
            
        #drawing the location of all the lines and walls
        for i in range(len(balls)):
            balls[i].draw()
            
        for i in range(len(textList)):
            textList[i].draw()
        
        #drawing the location of the balls
        plinkoBall.draw()
        #drawing the plinko ball
        events = pygame.event.get()
        #getting all input events
           
        if(plinkoBall.notClicked):#Runs when clicked
            if(pygame.mouse.get_pos()[0] > screenSize[0]//64 and pygame.mouse.get_pos()[0] < screenSize[0]//64 * 63):
                lastPos = (pygame.mouse.get_pos()[0],screenSize[1]//20)#setting the ball to the x position of the mouse/top of the screen
            pos = lastPos
            plinkoBall.ball_body.position = pos #setting the position to the plinkoBall
            plinkoBall.ball_body.velocity = (0,0) #resetting velocity
            plinkoBall.ball_body.angle = 0 #reseting angle
            plinkoBall.ball_body.angular_velocity = 0
            click = True
            
        else:
            if(click):
                click = False
                randNum = random.uniform(-4,4) #Gets random float from -1 to 1
                if randNum == 0.0: #If its zero set it to 1
                    randNum = 5
                plinkoBall.ball_body.angular_velocity = randNum #Sets the angular velocity to random to more randomize chance
                
        for event in events:
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: 
                    RUNNING = False
                    #If the user presses esc key leave game
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(var.tries <= maxTries):
                    plinkoBall.notClicked = False
                    #if the user clicks than drop the ball
        
        pygame.display.update()#Updating the display  
        world.step(1/60.0)
        clock.tick(60)
        #Stepping the physics engine and fps by 60
        
if __name__ == "__main__":
    main()
    #Runs if focused

pygame.quit()
#quits when loop is done