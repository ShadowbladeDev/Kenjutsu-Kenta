import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kenjutsu Kenta - Battle Screen")

# Load images
background = pygame.image.load("assets/images/battlefield.png")
tank_img = pygame.image.load("assets/images/tank.png")
ninja_img = pygame.image.load("assets/images/ninja.png")
voidling_img = pygame.image.load("assets/images/voidling.png")
medic_img = pygame.image.load("assets/images/medic.png")

# Resize images (optional)
tank_img = pygame.transform.scale(tank_img, (150, 150))
ninja_img = pygame.transform.scale(ninja_img, (150, 150))
voidling_img = pygame.transform.scale(voidling_img, (150, 150))
medic_img = pygame.transform.scale(medic_img, (150, 150))

# Character positions
positions = {
    "Tank": (100, 300),
    "Ninja": (300, 300),
    "Voidling": (500, 300),
    "Medic": (700, 300)
}

# Main loop
running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(tank_img, positions["Tank"])
    screen.blit(ninja_img, positions["Ninja"])
    screen.blit(voidling_img, positions["Voidling"])
    screen.blit(medic_img, positions["Medic"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit()
