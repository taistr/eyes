import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Center coordinates and radius
center = (200, 200)
center1 = (300, 300)
radius = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(black)  # Fill the screen with black color

    # Draw the red circle with the specified center and radius
    pygame.draw.circle(screen, red, center, radius)

    # Draw a blue dot at the center of the circle
    pygame.draw.circle(screen, blue, center1, 3)

    pygame.display.update()
    clock.tick(60)