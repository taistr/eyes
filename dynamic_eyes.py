import numpy as np
import cv2
import pygame as pg
from enum import Enum

class State(Enum):
    IDLE = 0
    ACTIVE = 1
    FINISHED = 2

def glassy_blur(pg_surface):
    np_image = pg.surfarray.array3d(pg_surface)
    np_blurred = cv2.GaussianBlur(np_image, ksize=(15, 15), sigmaX=20, sigmaY=20)
    return pg.surfarray.make_surface(np_blurred)

class Eye(pg.sprite.Sprite):
    def __init__(self, centre, iris_color, iris_radius, pupil_color=None, pupil_radius = None, left_eye:bool = None, velocity=None):
        #Call the Sprite constructor
        super().__init__()

        self.state = State.IDLE

        #centre for initial position -> use move and Rect afterwards
        self.iris_color = iris_color
        self.iris_radius = iris_radius
        self.pupil_color = pupil_color
        self.pupil_radius = pupil_radius

        self.vel = velocity
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

    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.rect.move_ip(self.vel, 0)
        if left:
            self.rect.move_ip(-self.vel, 0)
        if down:
            self.rect.move_ip(0, self.vel)
        if up:
            self.rect.move_ip(0, -self.vel)

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
    pupil_radius = 350

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

        #move the eyes
        left_eye.move(key_up, key_down, key_left, key_right)
        right_eye.move(key_up, key_down, key_left, key_right)

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
        