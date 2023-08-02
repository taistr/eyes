import numpy
import cv2
import pygame

def create_neon(surf):
    surf_alpha = surf.convert_alpha()
    rgb = pygame.surfarray.array3d(surf_alpha)
    alpha = pygame.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1))
    image = numpy.concatenate((rgb, alpha), 2)
    cv2.GaussianBlur(image, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=image)
    cv2.blur(image, ksize=(5, 5), dst=image)
    bloom_surf = pygame.image.frombuffer(image.flatten(), image.shape[1::-1], 'RGBA')
    return bloom_surf

def main():
    # initialize pygame
    pygame.init()
    
    # define width of screen
    width = 1920
    # define height of screen
    height = 1080
    screen_res = (width, height)
    
    pygame.display.set_caption("Abi eyes")
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #It's a surface
    
    # define colors
    pastel_blue = (171,235,255)
    sheen_pastel_blue = (230, 249, 255)
    black = (0, 0, 0)
    eye_radius = 200 
    sheen_radius = 120
    x_offset = -80
    y_offset = -80

    mouth_radius = 80

    # define eye
    right_eye = pygame.draw.circle(surface=screen, color=pastel_blue, center=[480, 540], radius=eye_radius)
    left_eye = pygame.draw.circle(surface=screen, color=pastel_blue, center=[1440, 540], radius=eye_radius)

    # define mouth
    mouth = pygame.draw.circle(surface=screen, color=pastel_blue, center=[960, 840], radius=mouth_radius)
    
    neon_image = create_neon(screen)
    neon_image = pygame.transform.rotate(neon_image, -90)

    right_eye_sheen = pygame.draw.circle(surface=neon_image, color=sheen_pastel_blue, center=[480, 540], radius=sheen_radius)
    left_eye_sheen = pygame.draw.circle(surface=neon_image, color=sheen_pastel_blue, center=[1440, 540], radius=sheen_radius)

    # game loop
    while True:
        # event loop
        for event in pygame.event.get():
            # check if a user wants to exit the game or not
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
    
        # fill black color on screen
        screen.fill(black)

        screen.blit(neon_image, neon_image.get_rect(center = screen.get_rect().center), special_flags = pygame.BLEND_PREMULTIPLIED)
    
        # update screen
        pygame.display.flip()

if __name__ == "__main__":
    main()