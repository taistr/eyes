import numpy
import cv2
import pygame

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

def create_neon(surf):
    surf_alpha = surf.convert_alpha()
    rgb = pygame.surfarray.array3d(surf_alpha)
    alpha = pygame.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1))
    image = numpy.concatenate((rgb, alpha), 2)
    cv2.GaussianBlur(image, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=image)
    cv2.blur(image, ksize=(5, 5), dst=image)
    bloom_surf = pygame.image.frombuffer(image.flatten(), image.shape[1::-1], 'RGBA')
    return bloom_surf

image = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.rect(image, (255, 128, 128), (10, 10, 80, 80))
neon_image = create_neon(image)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False          

    window.fill((127, 127, 127))
    window.blit(neon_image, neon_image.get_rect(center = window.get_rect().center), special_flags = pygame.BLEND_PREMULTIPLIED)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exit()