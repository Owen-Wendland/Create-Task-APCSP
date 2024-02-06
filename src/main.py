import math
import pygame
import pymunk
import random
import time
import os
import sys
import tkinter
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
   
    BACKGROUND = (150, 150, 150) 
   
    world = pymunk.Space()
    world.gravity = (0, 1000) 
    world.damping = .4 
    
    tk = tkinter.Tk()
    
    screenSize = (tk.winfo_screenwidth(), tk.winfo_screenheight())
    
    print(screenSize)
   
    left = False
    right = False
    up = False
    down = False
    shift = False
    global RUNNING 
    RUNNING = True
    screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
   
    pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
   
    class Plinko():
        def __init__(self, startx, starty, radius):
            self.ballRadius = radius
            self.ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, self.ballRadius))
            self.ball_body.position = (startx, starty)
            self.ball_shape = pymunk.Circle(self.ball_body, self.ballRadius)
            self.ball_shape.elasticity = 1.3
            self.ball_shape.friction = 3
            self.ball_shape.density = 1
            self.ball_shape.collision_type = 1
            self.notClicked = False
            world.add(self.ball_body, self.ball_shape)
            self.image = pygame.image.load("res\\circle.png")
            self.image = pygame.transform.scale(self.image, (self.ballRadius * 1.9,self.ballRadius * 1.9))
            self.imageRect = self.image.get_rect(center = self.ball_body.position)
            
        def draw(self):
            self.angle_degrees = math.degrees(self.ball_body.angle)
            self.rotatedimage = pygame.transform.rotate(self.image, -self.angle_degrees)
            self.imageRect = self.rotatedimage.get_rect(center = self.ball_body.position)
            pygame.draw.circle(screen, (0,0,0), (int(self.ball_body.position.x), int(self.ball_body.position.y)), self.ballRadius + 2)
            pygame.draw.circle(screen, (255,255,255), (int(self.ball_body.position.x), int(self.ball_body.position.y)), self.ballRadius) 
            screen.blit(self.rotatedimage, self.imageRect)   
            
   
    class Line():
        def __init__(self, firstpoint, secondpoint, ela, fric, collisionType):
            self.point1, self.point2 = firstpoint, secondpoint
            self.width = screenSize[0]//screenSize[1]*6
           
            self.lineBody = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.lineShape = pymunk.Segment(self.lineBody, (self.point1), (self.point2), self.width) 
            self.lineShape.elasticity = ela 
            self.lineShape.friction = fric 
            self.lineShape.collision_type = collisionType
            world.add(self.lineShape, self.lineBody)   
        def draw(self):
            pygame.draw.line(screen, (0,0,0), (self.point1), (self.point2), self.width)
   
    class ball():
        def __init__(self, startx, starty, radius):
            self.ballRadius = radius
            self.ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, self.ballRadius))
            self.ball_body.position = (startx, starty)
            self.ball_body.body_type = pymunk.Body.STATIC
            self.ball_shape = pymunk.Circle(self.ball_body, self.ballRadius)
            self.ball_shape.elasticity = 1.2
            self.ball_shape.friction = 3
            self.ball_shape.density = 1
            self.ball_shape.collision_type = 2
            world.add(self.ball_body, self.ball_shape)
        def draw(self):
            pygame.draw.circle(screen, (255,255,255), (int(self.ball_body.position.x), int(self.ball_body.position.y)), self.ballRadius) 
            
            
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
   
    plinkoBall = Plinko(200, 200, 30)
    
    balls = []
    for i in range(21):
        balls.extend([
            ball(screenSize[0]//5*i//2,screenSize[1]//6,screenSize[0]//96),
            ball(screenSize[0]//5*i//2 + (screenSize[0]//5)//4,screenSize[1]//6*2,screenSize[0]//96),
            ball(screenSize[0]//5*i//2,screenSize[1]//6*3,screenSize[0]//96),
            ball(screenSize[0]//5*i//2 + (screenSize[0]//5)//4,screenSize[1]//6*4,screenSize[0]//96),
            ball(screenSize[0]//5*i//2,screenSize[1]//6*5,screenSize[0]//96)
        ])
    
    floor = Line((0,screenSize[1]),(screenSize[0],screenSize[1]), 0, 5, 3)
    wallLeft = Line((0,-150),(0,screenSize[1]), 0, 0, 4)
    wallRight = Line((screenSize[0],-150),(screenSize[0],screenSize[1]), 0, 0, 4)
    roof = Line((0,0),(screenSize[0],0), 1, 0, 4)
   
    linelist = []
    linelist.extend([
        floor,
        wallLeft,
        wallRight,
        roof
    ])
    
    for i in range(10):
        linelist.extend([
            Line((screenSize[0]//10*i,screenSize[1]),(screenSize[0]//10*i,screenSize[1]//12*10), 1, 5, 4)
        ])
        
    plinkoBall.notClicked = True
    
    blip = pygame.mixer.Sound("res\\plinko.wav")

    
    def sound(arbiter, world, data):
        pygame.mixer.Sound.play(blip)
    def reset(arbiter, world, data):
        plinkoBall.notClicked = True
        
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