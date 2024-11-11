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
GREEN = (0, 255, 0)

# Define a constant speed
SPEED = 5

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

class Box:
    def __init__(self, x, y):
        self.image = pygame.Surface((35, 35))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))  # Get the rectangle for positioning
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 2)

# Create a sprite instance
cube = Box(300, 200)  # Adjusted position for better visibility
sprite = Sprite(375, 275)
camera_x, camera_y = 0, 0

# Map dimensions
map_width, map_height = 1600, 1200  # Larger than the window size

# Define a constant speed
SPEED = 5

# Inside the main loop, replace the movement logic with the following:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Get the keys pressed
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -1  # Use -1 to indicate left movement
    if keys[pygame.K_RIGHT]:
        dx = 1   # Use 1 to indicate right movement
    if keys[pygame.K_UP]:
        dy = -1  # Use -1 to indicate upward movement
    if keys[pygame.K_DOWN]:
        dy = 1   # Use 1 to indicate downward movement

    # Calculate the length of the movement vector
    length = (dx**2 + dy**2) ** 0.5

    # Normalize the movement vector if it's not zero
    if length > 0:
        dx /= length  # Normalize x component
        dy /= length  # Normalize y component

    # Scale the normalized vector by the speed
    dx *= SPEED
    dy *= SPEED

    # Store the original position
    original_rect = sprite.rect.copy()
    
    # Move the sprite
    sprite.move(dx, dy)

    # Check for collision with the box
    # Check for collision with the box
    if sprite.rect.colliderect(cube.rect):
        # Calculate the overlap
        overlap_x = (sprite.rect.right - cube.rect.left) if dx > 0 else (sprite.rect.left - cube.rect.right)
        overlap_y = (sprite.rect.bottom - cube.rect.top) if dy > 0 else (sprite.rect.top - cube.rect.bottom)

        # Determine the minimum overlap
        if abs(overlap_x) < abs(overlap_y):
            # Resolve collision in the x direction
            sprite.rect.x -= overlap_x
        else:
            # Resolve collision in the y direction
            sprite.rect.y -= overlap_y


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