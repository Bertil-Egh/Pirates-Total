import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gorms Program")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Create a sprite class
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
        pygame.draw.rect(surface, RED, self.rect, 2)  # Draw the hitbox

# Create a sprite instance
sprite = Sprite(375, 275)
camera_x, camera_y = 0, 0

# Map dimensions
map_width, map_height = 1600, 1200  # Larger than the window size

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Get the keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        sprite.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        sprite.move(5, 0)
    if keys[pygame.K_UP]:
        sprite.move(0, -5)
    if keys[pygame.K_DOWN]:
        sprite.move(0, 5)
    
    # Update camera position to follow the sprite
    camera_x = sprite.rect.centerx - width // 2
    camera_y = sprite.rect.centery - height // 2  # Corrected to height

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the map (for demonstration, we'll just fill a larger area)
    pygame.draw.rect(screen, (0, 255, 0), (0 - camera_x, 0 - camera_y, map_width, map_height))  # Draw the map

    # Draw the sprite (adjust position based on camera)
    sprite.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
print('HI GUYUS!!')