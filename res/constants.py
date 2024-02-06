import tkinter
import pygame
import pymunk
import os
import platform
import math

tk = tkinter.Tk()
screenSize = (tk.winfo_screenwidth(), tk.winfo_screenheight())
Background = (150,150,150)
tk.destroy()

cwd = os.getcwd()
cwd = str(cwd)

if platform.system == 'Windows':
    cwd = cwd.replace('src','')
else:
    cwd = cwd.replace('src','')

class Plinko():
        def __init__(self, startx, starty, radius, world, screen):
            self.ballRadius = radius
            self.ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, self.ballRadius))
            self.ball_body.position = (startx, starty)
            self.ball_shape = pymunk.Circle(self.ball_body, self.ballRadius)
            self.ball_shape.elasticity = 1.1
            self.ball_shape.friction = 3
            self.ball_shape.density = 1
            self.ball_shape.collision_type = 1
            self.notClicked = False
            self.world = world
            self.screen = screen
            self.world.add(self.ball_body, self.ball_shape)
            self.image = pygame.image.load(cwd + "res/circle.png")
            self.image = pygame.transform.scale(self.image, (int(self.ballRadius * 1.9),int(self.ballRadius * 1.9)))
            self.imageRect = self.image.get_rect(center = self.ball_body.position)
            
        def draw(self):
            self.angle_degrees = math.degrees(self.ball_body.angle)
            self.rotatedimage = pygame.transform.rotate(self.image, -self.angle_degrees)
            self.imageRect = self.rotatedimage.get_rect(center = self.ball_body.position)
            pygame.draw.circle(self.screen, (0,0,0), (int(self.ball_body.position.x), int(self.ball_body.position.y)), self.ballRadius + 2)
            pygame.draw.circle(self.screen, (255,255,255), (int(self.ball_body.position.x), int(self.ball_body.position.y)), self.ballRadius) 
            self.screen.blit(self.rotatedimage, self.imageRect)  
class Line():
        def __init__(self, firstpoint, secondpoint, ela, fric, collisionType, world, screen):
            self.point1, self.point2 = firstpoint, secondpoint
            self.width = int(screenSize[0]//screenSize[1]*6)
           
            self.lineBody = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.lineShape = pymunk.Segment(self.lineBody, (self.point1), (self.point2), self.width) 
            self.lineShape.elasticity = ela 
            self.lineShape.friction = fric 
            self.lineShape.collision_type = collisionType
            self.world = world
            self.world.add(self.lineShape, self.lineBody)
            self.screen = screen
        def draw(self):
            pygame.draw.line(self.screen, (0,0,0), (self.point1), (self.point2), self.width)
class ball():
        def __init__(self, startx, starty, radius, world, screen):
            self.ballRadius = radius
            self.ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, self.ballRadius))
            self.ball_body.position = (startx, starty)
            self.ball_body.body_type = pymunk.Body.STATIC
            self.ball_shape = pymunk.Circle(self.ball_body, self.ballRadius)
            self.ball_shape.elasticity = 1.2
            self.ball_shape.friction = 3
            self.ball_shape.density = 1
            self.ball_shape.collision_type = 2
            self.screen = screen
            self.world = world
            self.world.add(self.ball_body, self.ball_shape)
        def draw(self):
            pygame.draw.circle(self.screen, (255,255,255), (int(self.ball_body.position.x), int(self.ball_body.position.y)), self.ballRadius) 
