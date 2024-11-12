import pygame
import sys
import math

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
GREEN = (0, 255, 0)

max_speed = 2
speed = 2
direction = 0

# Create a sprite class
class Sprite:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))  # Create a square sprite
        self.image.fill(BLUE)  # Fill it with blue color
        self.rect = self.image.get_rect(topleft=(x, y))  # Get the rectangle for positioning

    def move(self, angle, distance):
        radians = math.radians(angle)

        dx = distance * math.cos(radians)
        dy = distance * math.sin(radians)

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Draw the sprite on the surface
        pygame.draw.rect(surface, RED, self.rect, 2)  # Draw the hitbox

class Box:
    def __init__(self, x, y):
        self.image = pygame.Surface((35, 35))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))  # Get the rectangle for positioning
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 2)

# Create sprite instance
cube = Box(300, 200)
sprite = Sprite(375, 275)
camera_x, camera_y = 0, 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Get the keys pressed
    keys = pygame.key.get_pressed()
    
    # Update direction based on left and right keys
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direction -= 5  # Turn left
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction += 5  # Turn right

    # Move the sprite in the current direction
    sprite.move(direction, speed)

    # Check for collision with the box
    if sprite.rect.colliderect(cube.rect): # The collission has to be fixed
        # Calculate the overlap
        overlap_x = (sprite.rect.right - cube.rect.left) if speed > 0 else (sprite.rect.left - cube.rect.right)
        overlap_y = (sprite.rect.bottom - cube.rect.top) if speed > 0 else (sprite.rect.top - cube.rect.bottom)

        # Determine the minimum overlap
        if abs(overlap_x) < abs(overlap_y):
            # Resolve collision in the x direction
            sprite.rect.x -= overlap_x
        else:
            # Resolve collision in the y direction
            sprite.rect.y -= overlap_y

        # Assuming you have a variable `angle` that represents the direction of movement
        # Calculate the angle in radians
        radians = math.radians(direction)

        # Calculate the movement vector based on the angle
        move_x = overlap_x * math.cos(radians) + overlap_y * math.sin(radians)
        move_y = overlap_x * -math.sin(radians) + overlap_y * math.cos(radians)

        # Move the sprite back relative to its movement direction
        sprite.rect.x -= move_x
        sprite.rect.y -= move_y

    # Update camera position to follow the sprite
    camera_x = sprite.rect.centerx - width // 2
    camera_y = sprite.rect.centery - height // 2  # Corrected to height

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the sprite (adjust position based on camera)
    sprite.draw(screen)
    cube.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
