import pygame
import sys
import math
import pymunk
import pymunk.pygame_util

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gorms Program")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

speed = 10
direction = 0

space = pymunk.Space()
space.gravity = (0,0)

class Sprite:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))  # Get the rectangle for positioning

        self.body = pymunk.Body(1, pymunk.moment_for_box(1,(50,50)))
        self.body.position = (x,y)
        self.shape = pymunk.Poly.create_box(self.body)
        self.shape.elasticity = 0.95
        space.add(self.body,self.shape)

    def move(self, angle, distance):
        radians = math.radians(angle)
        force_x = distance * math.cos(radians) * speed
        force_y = distance * math.sin(radians) * speed

        self.body.apply_force_at_world_point((force_x, force_y))

    def draw(self, surface):
        self.rect.topleft = self.body.position
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 2)

class Box:
    def __init__(self, x, y):
        self.image = pygame.Surface((35, 35))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Poly.create_box(self.body,(35,35))
        self.body.position = (x,y)
        space.add(self.body,self.shape)
    
    def draw(self, surface):
        self.rect.topleft = self.body.position
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

    original_position = sprite.rect.topleft

    # Move the sprite in the current direction
    sprite.move(direction, speed)

    # Check for collision with the cube
    if sprite.rect.colliderect(cube.rect):
        # Calculate the overlap in both directions
        overlap_x = sprite.rect.right - cube.rect.left if sprite.rect.right > cube.rect.left else cube.rect.right - sprite.rect.left
        overlap_y = sprite.rect.bottom - cube.rect.top if sprite.rect.bottom > cube.rect.top else cube.rect.bottom - sprite.rect.top

        # Determine the direction of the collision
        if overlap_x < overlap_y:
            # Slide horizontally
            if sprite.rect.centerx < cube.rect.centerx:
                sprite.rect.right = cube.rect.left  # Slide left
            else:
                sprite.rect.left = cube.rect.right  # Slide right
        else:
            # Slide vertically
            if sprite.rect.centery < cube.rect.centery:
                sprite.rect.bottom = cube.rect.top  # Slide up
            else:
                sprite.rect.top = cube.rect.bottom  # Slide down

        # Reset the original position to the new position after sliding
        original_position = sprite.rect.topleft
    else:
        # If no collision, update the original position
        original_position = sprite.rect.topleft


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
    clock.tick(60)
