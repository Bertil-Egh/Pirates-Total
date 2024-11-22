import pygame
import sys
import math
import pymunk
import pymunk.pygame_util

pygame.init()

pygame.mixer.init()  
pygame.mixer.music.load("Music.mp3")  
pygame.mixer.music.play(-1)  

pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gorms Program")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0)

speed = 4
direction = 0

space = pymunk.Space()
space.gravity = (0, 0)

class Sprite:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Transparent background
        pygame.draw.rect(self.image, BLUE, (0, 0, 50, 50))  # Draw the blue square
        self.rect = self.image.get_rect(center=(x, y))  # Get the rectangle for positioning

        self.body = pymunk.Body(1, pymunk.moment_for_box(1, (50, 50)))
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body)
        self.shape.elasticity = 0.99
        space.add(self.body, self.shape)

        self.max_speed = 50

    def move(self, distance, direction):
        radians = math.radians(direction)  # Convert direction to radians
        force_x = distance * math.cos(radians) * 25
        force_y = distance * math.sin(radians) * 25

        self.body.apply_force_at_local_point((force_x, force_y))
        
        # Clamp the velocity to the maximum speed

        current_velocity = self.body.velocity

        speed = math.sqrt(current_velocity[0]**2 + current_velocity[1]**2)

        if speed > self.max_speed:
            # Normalize the velocity vector and scale it to max_speed
            normalized_velocity = (current_velocity[0] / speed, current_velocity[1] / speed)
            self.body.velocity = (normalized_velocity[0] * self.max_speed, normalized_velocity[1] * self.max_speed)




    def draw(self, surface, camera_x, camera_y):
        # Update the rectangle position based on the camera position
        self.rect.topleft = (self.body.position.x - camera_x, self.body.position.y - camera_y)
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 2)

class Box:
    def __init__(self, x, y):
        self.image = pygame.Surface((35, 35))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Poly.create_box(self.body, (35, 35))
        self.body.position = (x, y)
        space.add(self.body, self.shape)


    def draw(self, surface, camera_x, camera_y):
        # Update the rectangle position based on the camera position
        self.rect.topleft = (self.body.position.x - camera_x, self.body.position.y - camera_y)

        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 2)

# Create sprite instance
cube = Box(300, 200)
sprite = Sprite(375, 275)
camera_x, camera_y = 0, 0

while True:
    dt = clock.tick(60) / 1000.0  # Get the time since the last frame in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the keys pressed
    keys = pygame.key.get_pressed()

    # Update direction based on left and right keys
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direction -= 2  # Turn left
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction += 2  # Turn right

    # Set the body's angle based on the direction
    sprite.body.angle = math.radians(direction)

    sprite.move(speed, direction)

    space.step(dt)
    
    camera_x = sprite.body.position.x - width // 2 + sprite.rect.width // 2
    camera_y = sprite.body.position.y - height // 2 + sprite.rect.width // 2

    
    screen.fill(WHITE)

    
    sprite.draw(screen, camera_x, camera_y)
    cube.draw(screen, camera_x, camera_y)

    pygame.display.flip()
