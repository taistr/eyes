import numpy as np
import cv2
import pygame as pg

def create_neon(surf):
    surf_alpha = surf.convert_alpha()
    rgb = pg.surfarray.array3d(surf_alpha)
    alpha = pg.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1))
    image = np.concatenate((rgb, alpha), 2)
    cv2.GaussianBlur(image, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=image)
    cv2.blur(image, ksize=(5, 5), dst=image)
    bloom_surf = pg.image.frombuffer(image.flatten(), image.shape[1::-1], 'RGBA')
    return bloom_surf

class circle(pg.sprite.Sprite):
    def __init__(self, color, centre, radius, velocity=None):
        #Call the Sprite constructor
        super().__init__()

        #centre for initial position -> use move and Rect afterwards
        self.color = color
        self.radius = radius
        self.vel = velocity 

        #Create an image of the block, fill with white (transparent) and draw circle for eyes
        white = (255, 255, 255)
        self.image = pg.Surface((2*radius, 2*radius))
        self.image.fill(white)
        self.image.set_colorkey(white)
        pg.draw.circle(surface=self.image, color=color, center=(radius, radius), radius=radius) 
        
        #Fetch the rect that has the initial position and dimensions of the surfacess
        self.rect = self.image.get_rect()
        self.rect.move_ip(centre[0]-radius, centre[1]-radius)


    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.rect.move_ip(self.vel, 0)
        if left:
            self.rect.move_ip(-self.vel, 0)
        if down:
            self.rect.move_ip(0, self.vel)
        if up:
            self.rect.move_ip(0, -self.vel)
    
    def move_iris():
        pass




def main():
    #TUNE
    black = (0,0,0)
    pastel_blue = (171,235,255)
    sheen_pastel_blue = (230, 249, 255)
    eye_radius = 240

    #initialise pygame
    pg.init()

    #Create a fullscreen display surface
    screen = pg.display.set_mode(flags=pg.FULLSCREEN)

    #Create a pygame clock
    clock = pg.time.Clock()

    #Instantiate the eye sprites
    right_eye = circle(color=pastel_blue, centre=(480, 540), radius=eye_radius, velocity=8)
    left_eye = circle(color=pastel_blue, centre=(1440, 540), radius=eye_radius, velocity=8)

    #game loop
    while True:
        #input loop
        keys = pg.key.get_pressed()
        up = keys[pg.K_UP]
        down = keys[pg.K_DOWN]
        right = keys[pg.K_RIGHT]
        left = keys[pg.K_LEFT]

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
        left_eye.move(up, down, left, right)
        right_eye.move(up, down, left, right)
        
        #blit the sprites onto the screen
        screen.blit(left_eye.image, left_eye.rect)
        screen.blit(right_eye.image, right_eye.rect)

        #!Apply any post-processing to the entire display here:

        pg.display.update()

        #set the frame rate to 60fps
        clock.tick(60) 

if __name__ == "__main__":
    main()
        