import numpy as np
import cv2
import pygame as pg
import random
from enum import Enum

class State(Enum):
    IDLE = 0
    ACTIVE = 1
    FINISHED = 2

class Expression(Enum):
    NEUTRAL = 0
    SAD = 1
    ANGRY = 2
    BORED = 3

def glassy_blur(pg_surface):
    np_image = pg.surfarray.array3d(pg_surface)
    np_blurred = cv2.GaussianBlur(np_image, ksize=(15, 15), sigmaX=20, sigmaY=20)
    return pg.surfarray.make_surface(np_blurred)

class Eye(pg.sprite.Sprite):
    def __init__(self, centre, iris_color, iris_radius, pupil_color=None, pupil_radius = None, left_eye:bool = None, velocity=None):
        #Call the Sprite constructor
        super().__init__()

        self.state = State.IDLE
        self.expression = Expression.NEUTRAL
        self.initial_position = centre

        #centre for initial position -> use move and Rect afterwards
        self.iris_color = iris_color
        self.iris_radius = iris_radius
        self.pupil_color = pupil_color
        self.pupil_radius = pupil_radius

        self.idle_velocity = 1
        self._idle_incr = 0
        self._idle_up_flag = True
        self._idle_max_position = 20

        self.movement_velocity = velocity

        self.left_eye = left_eye #0-> right, 1 -> left

        #Initialise the iris
        self._white = (255, 255, 255)
        self.image = pg.Surface((2*iris_radius, 2*iris_radius))
        self.image.set_colorkey(self._white)
        self._draw_iris()
        self._draw_pupil()
        
        #Fetch the rect that has the initial position and dimensions of the surfaces
        self.rect = self.image.get_rect()
        self.rect.move_ip(centre[0]-iris_radius, centre[1]-iris_radius)

    def update(self): #On each iteration update the eye's current state - when added to a pygame group, it can be invoked via group.update() -> for both eyes
        if self.state == State.IDLE:
            #Run the bob animation
            #self.bob()

            #Get keys pressed
            keys = pg.key.get_pressed()

            #TODO: For integration, replace this with a message from 'brain' or equivalent

            #If key pressed, transition to active state and specify which expression to run
            if(keys[pg.K_q]):
                self.expression = Expression.NEUTRAL
                self.state = State.ACTIVE
            elif(keys[pg.K_w]):
                self.expression = Expression.ANGRY
                self.state = State.ACTIVE
            elif(keys[pg.K_e]):
                self.expression = Expression.BORED
                self.state = State.ACTIVE
            elif(keys[pg.K_r]):
                self.expression = Expression.SAD
                self.state = State.ACTIVE

        elif self.state == State.ACTIVE:
            #run an iteration of whichever expression is active
            match self.expression:
                case Expression.NEUTRAL:
                    pass
                case Expression.ANGRY:
                    pass
                case Expression.NEUTRAL:
                    pass
                case Expression.NEUTRAL:
                    pass

        elif self.state == State.FINISHED:
            #clean or finish anything up and transition to idle
            pass

    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.rect.move_ip(self.movement_velocity, 0)
        if left:
            self.rect.move_ip(-self.movement_velocity, 0)
        if down:
            self.rect.move_ip(0, self.movement_velocity)
        if up:
            self.rect.move_ip(0, -self.movement_velocity)
    
    #This is a stylistic choice
    def flicker(self):
        self.rect.move_ip(round(random.uniform(-1, 1)), random.uniform(-1, 1))

    def bob(self):
        if self._idle_up_flag:
            self.rect.move_ip(0, -self.idle_velocity) #move up
            self._idle_incr += 1
        else:
            self.rect.move_ip(0, self.idle_velocity) #move down
            self._idle_incr -= 1
        
        self.rect.move_ip(round(random.uniform(-1, 1)), 0)
    
        if abs(self._idle_incr) >= self._idle_max_position:
            self._idle_up_flag = not(self._idle_up_flag)

    def _draw_iris(self):
        self.image.fill(self._white)
        pg.draw.circle(surface=self.image, color=self.iris_color, center=(self.iris_radius, self.iris_radius), radius=self.iris_radius) 

    def _draw_pupil(self):
        pg.draw.circle(surface=self.image, color=self.pupil_color, center=(self.iris_radius, self.iris_radius), radius=self.pupil_radius)

    def neutral(self):
        self._draw_iris()
        self._draw_pupil()

    def bored(self):
        self._draw_iris()
        self._draw_pupil()
        eyelid_rect = pg.Rect(0, 0, 2 * self.iris_radius, self.iris_radius) 
        pg.draw.rect(surface=self.image, color=self._white, rect=eyelid_rect)

    def angry(self):
        self._draw_iris()
        self._draw_pupil()

        if (self.left_eye):
            pg.draw.polygon(surface=self.image, color=self._white, points=[(0,0), (2*self.iris_radius, 0), (2*self.iris_radius, 0.5*self.iris_radius), (0, self.iris_radius)])
        else:
            pg.draw.polygon(surface=self.image, color=self._white, points=[(0,0), (2*self.iris_radius, 0), (2*self.iris_radius, self.iris_radius), (0, 0.5*self.iris_radius)])
    
    def sad(self):
        self._draw_iris()
        self._draw_pupil()

        if (self.left_eye):
            pg.draw.polygon(surface=self.image, color=self._white, points=[(0,0), (2*self.iris_radius, 0), (2*self.iris_radius, self.iris_radius), (0, 0.5*self.iris_radius)])
        else:
            pg.draw.polygon(surface=self.image, color=self._white, points=[(0,0), (2*self.iris_radius, 0), (2*self.iris_radius, 0.5*self.iris_radius), (0, self.iris_radius)])

def main():
    #TUNE
    black = (0,0,0)
    pastel_blue = (171, 235, 255)
    light_pastel_blue = (196, 233, 245)
    sheen_pastel_blue = (230, 249, 255)

    eye_radius = 400
    pupil_radius = 385

    #initialise pygame
    pg.init()

    #Create a fullscreen display surface
    screen = pg.display.set_mode(flags=pg.FULLSCREEN)

    #Create a pygame clock
    clock = pg.time.Clock()

    #Instantiate the eye sprites
    right_eye = Eye(centre=(480, 540), 
                    iris_color=pastel_blue, 
                    iris_radius=eye_radius, 
                    pupil_color=sheen_pastel_blue, 
                    pupil_radius=pupil_radius,
                    velocity=8)
    left_eye = Eye(centre=(1440, 540), 
                   iris_color=pastel_blue, 
                   iris_radius=eye_radius,  
                   pupil_color=sheen_pastel_blue,
                   pupil_radius=pupil_radius,
                   velocity=8, 
                   left_eye=True)

    #game loop
    while True:
        #input loop
        keys = pg.key.get_pressed()
        key_up = keys[pg.K_UP]
        key_down = keys[pg.K_DOWN]
        key_right = keys[pg.K_RIGHT]
        key_left = keys[pg.K_LEFT]
        key_q = keys[pg.K_q]
        key_w = keys[pg.K_w]
        key_e = keys[pg.K_e]
        key_r = keys[pg.K_r]

        # event loop
        for event in pg.event.get():
            # check if a user wants to exit the game or not
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: #escape key to escape 
                    exit()

        #fill the screen with black
        screen.fill(black)

        #move the eyes #TODO: This should be eventually replaced by left_eye.update() and right_eye.update() or even better eyes.update()
        left_eye.bob()
        right_eye.bob()

        #make an expression
        if(key_q):
            left_eye.neutral()
            right_eye.neutral()
        elif(key_w):
            left_eye.bored()
            right_eye.bored()
        elif(key_e):
            left_eye.sad()
            right_eye.sad()
        elif(key_r):
            left_eye.angry()
            right_eye.angry()
        
        #blit the sprites onto the screen
        screen.blit(left_eye.image, left_eye.rect)
        screen.blit(right_eye.image, right_eye.rect)

        #!Apply any post-processing to the entire display here:
        blurred_screen = glassy_blur(screen)
        screen.blit(blurred_screen, blurred_screen.get_rect(center = screen.get_rect().center), special_flags = pg.BLEND_PREMULTIPLIED)

        pg.display.update()

        #set the frame rate to 60fps 

if __name__ == "__main__":
    main()
        