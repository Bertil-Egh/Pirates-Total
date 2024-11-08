import pygame
import sys
import tkinter as tk

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gorms Program")

WHITE = (255,255,255)
BLUE = (0,0,255)

class Sprite:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))  # Create a square sprite
        self.image.fill(BLUE)  # Fill it with blue color
        self.rect = self.image.get_rect(topleft=(x, y))  # Get the rectangle for positioning

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Draw the sprite on the surface

sprite = Sprite(375, 275)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        sprite.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        sprite.move(5, 0)
    if keys[pygame.K_UP]:
        sprite.move(0,-5)
    if keys[pygame.K_DOWN]:
        sprite.move(0,5)
    
    screen.fill(WHITE)

    sprite.draw(screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)