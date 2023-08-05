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

class Mien(Enum):
    OPEN = 0
    CLOSED = 1
    CLOSED_SMILE = 2
    OPEN_SMILE = 3
    CLOSED_SAD = 3
    OPEN_SAD = 4


def glassy_blur(pg_surface):
    np_image = pg.surfarray.array3d(pg_surface)
    np_blurred = cv2.GaussianBlur(np_image, ksize=(33, 33), sigmaX=20, sigmaY=20)
    return pg.surfarray.make_surface(np_blurred)

class Eye(pg.sprite.Sprite):
    def __init__(self, centre, iris_color, iris_radius, pupil_color=(0,0,0), pupil_radius = 0, left_eye:bool = False, velocity=0):
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

        self._expression_incr = 0

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
        keys = pg.key.get_pressed()

        #Update position
        self.move(keys)

        #Update expression
        if self.state == State.IDLE:
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
            
            self.flicker()

        elif self.state == State.ACTIVE:
            #run an iteration of whichever expression is active
            match self.expression:
                case Expression.NEUTRAL:
                    status = self.neutral()
                case Expression.ANGRY:
                    status = self.angry()
                case Expression.BORED:
                    status = self.bored()
                case Expression.SAD:
                    status = self.sad()
            
            if (status):
                self.state = State.FINISHED

        elif self.state == State.FINISHED:
            #clean up and transition to idle
            self._expression_incr = 0
            self.state = State.IDLE

    def move(self, keys):
        if keys[pg.K_RIGHT]:
            self.rect.move_ip(self.movement_velocity, 0)
        if keys[pg.K_LEFT]:
            self.rect.move_ip(-self.movement_velocity, 0)
        if keys[pg.K_DOWN]:
            self.rect.move_ip(0, self.movement_velocity)
        if keys[pg.K_UP]:
            self.rect.move_ip(0, -self.movement_velocity)
    
    #This is purely stylistic
    def flicker(self):
        self.rect.move_ip(round(random.uniform(-1, 1)), random.uniform(-1, 1))

    def _draw_iris(self):
        self.image.fill(self._white)
        pg.draw.circle(surface=self.image, color=self.iris_color, center=(self.iris_radius, self.iris_radius), radius=self.iris_radius) 

    def _draw_pupil(self):
        pg.draw.circle(surface=self.image, color=self.pupil_color, center=(self.iris_radius, self.iris_radius), radius=self.pupil_radius)

    def neutral(self):
        self._draw_iris()
        self._draw_pupil()

        return True

    def bored(self):
        #start from neutral
        self._draw_iris()
        self._draw_pupil()

        #increment counter
        self._expression_incr += 100

        #generate and draw the eyelid
        eyelid_rect = pg.Rect(0, 0, 2 * self.iris_radius, self._expression_incr) 
        pg.draw.rect(surface=self.image, color=self._white, rect=eyelid_rect)

        #return false if not end of animation
        if self._expression_incr >= self.iris_radius:
            return True
        
        return False
        
    def angry(self):
        #start from neutral
        self._draw_iris()
        self._draw_pupil()

        #increment counter
        self._expression_incr += 100

        #draw eyelid
        if (self.left_eye):
            pg.draw.polygon(surface=self.image, color=self._white, points=[(0,0), (2*self.iris_radius, 0), (2*self.iris_radius, self._expression_incr-0.5*self.iris_radius), (0, self._expression_incr)])
        else:
            pg.draw.polygon(surface=self.image, color=self._white, points=[(0,0), (2*self.iris_radius, 0), (2*self.iris_radius, self._expression_incr), (0, self._expression_incr-0.5*self.iris_radius)])
    
        #return false if not end of animation
        if self._expression_incr >= self.iris_radius:
            return True

        return False

    def sad(self):
        self._draw_iris()
        self._draw_pupil()

        #increment counter
        self._expression_incr += 100

        if (self.left_eye):
            pg.draw.polygon(surface=self.image, color=self._white, points=[(0,0), (2*self.iris_radius, 0), (2*self.iris_radius, self._expression_incr), (0, self._expression_incr-0.5*self.iris_radius)])
        else:
            pg.draw.polygon(surface=self.image, color=self._white, points=[(0,0), (2*self.iris_radius, 0), (2*self.iris_radius, self._expression_incr-0.5*self.iris_radius), (0, self._expression_incr)])

        #return false if not end of animation
        if self._expression_incr >= self.iris_radius:
            return True

        return False
    
class Mouth(pg.sprite.Sprite):
    def __init__(self, centre, color, radius, velocity = 0):
        self.state = State.IDLE
        self.mien = Mien.OPEN

        self.centre = centre
        self.color = color
        self.radius = radius
        self.movement_velocity = velocity

        self._white = (255, 255, 255)
        self.image = pg.Surface((2*radius, 2*radius))
        self.image.set_colorkey(self._white)
        self.open()

        #Fetch the rect that has the initial position and dimensions of the surfaces
        self.rect = self.image.get_rect()
        self.rect.move_ip(centre[0]-radius, centre[1]-radius)
    
    def update(self):
        keys = pg.key.get_pressed()

        #Update mien
        if self.state == State.IDLE:
            #TODO: For integration, replace this with a message from 'brain' or equivalent 
            #If key pressed, transition to active state and specify which mien to show on mouth
            if(keys[pg.K_t]):
                self.expression = Mien.CLOSED
                self.state = State.ACTIVE
            elif(keys[pg.K_y]):
                self.expression = Mien.CLOSED_SMILE
                self.state = State.ACTIVE
            elif(keys[pg.K_u]):
                self.expression = Mien.CLOSED_SAD
                self.state = State.ACTIVE
            elif(keys[pg.K_i]):
                self.expression = Mien.OPEN
                self.state = State.ACTIVE
            elif(keys[pg.K_o]):
                self.expression = Mien.OPEN_SMILE
                self.state = State.ACTIVE
            elif(keys[pg.K_p]):
                self.expression = Mien.OPEN_SAD
                self.state = State.ACTIVE
            
        elif self.state == State.ACTIVE:
            #run an iteration of whichever expression is active
            status = False

            match self.expression:
                case Mien.CLOSED:
                    status = self.close()
                case Mien.CLOSED_SMILE:
                    pass
                case Mien.CLOSED_SAD:
                    pass
                case Mien.OPEN:
                    status = self.open()
                case Mien.OPEN_SMILE:
                    status = self.open_smile()
                case Mien.OPEN_SAD:
                    pass

            if (status):
                self.state = State.FINISHED

        elif self.state == State.FINISHED:
            #clean up and transition to idle
            self.state = State.IDLE
    
    def open(self):
        self.image.fill(self._white)
        pg.draw.circle(surface=self.image, color=self.color, center=(self.radius, self.radius), radius=self.radius) 

        return True

    def open_smile(self):
        self.open()
        top_lip_rect = pg.Rect(0, 0, 2 * self.radius, self.radius) 
        pg.draw.rect(surface=self.image, color=self._white, rect=top_lip_rect)

        return True
    
    def close(self):
        self.image.fill(self._white)
        pg.draw.line(surface=self.image, color=self.color, start_pos=(0, self.radius), end_pos=(2*self.radius, self.radius), width=40)

        return True

def main():
    #TUNE
    black = (0,0,0)
    pastel_blue = (171, 235, 255)
    light_pastel_blue = (196, 233, 245)
    sheen_pastel_blue = (230, 249, 255)

    eye_radius = 350
    pupil_radius = int(0.9625 * eye_radius)
    mouth_radius = 100

    #initialise pygame
    pg.init()

    #Create a fullscreen display surface
    screen = pg.display.set_mode(flags=pg.FULLSCREEN, vsync=1)

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
    mouth = Mouth(centre=(960, 810),
                  color=sheen_pastel_blue,
                  radius=mouth_radius)

    #game loop
    while True:
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

        left_eye.update()
        right_eye.update()
        mouth.update()
        
        #blit the sprites onto the screen
        screen.blit(left_eye.image, left_eye.rect)
        screen.blit(right_eye.image, right_eye.rect)
        screen.blit(mouth.image, mouth.rect)

        #!Apply any post-processing to the entire display here:
        blurred_screen = glassy_blur(screen)
        screen.blit(blurred_screen, blurred_screen.get_rect(center = screen.get_rect().center), special_flags = pg.BLEND_PREMULTIPLIED)

        pg.display.update()

        #set the frame rate to 60fps 

if __name__ == "__main__":
    main()
        