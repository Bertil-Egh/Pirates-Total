import pygame
import sys
import math
import pymunk
import pymunk.pygame_util

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("assets/media/sounds/Music.mp3")
pygame.mixer.music.play(-1)

width, height = 800, 600
MAP_WIDTH = 1600  # Width of the map
MAP_HEIGHT = 1200  # Height of the map
screen = pygame.display.set_mode((width, height))

ship_image = pygame.image.load("assets/media/image/PiratesTotalShipSide2.png")
ship_image1 = pygame.image.load("assets/media/image/PiratesTotalShipSide1.png")
ship_image2 = pygame.image.load("assets/media/image/PiratesTotalShipSide2.png")
ship_image3 = pygame.image.load("assets/media/image/PiratesTotalShipFront.png")
ship_image4 = pygame.image.load("assets/media/image/PiratesTotalShipBack.png")
compass_circle = pygame.image.load("assets/media/image/COMPASS.png")
compass_pointer = pygame.image.load("assets/media/image/COMPASSPOINTER.png")

# Resize images
ship_image = pygame.transform.scale(ship_image, (100, 100))
ship_image1 = pygame.transform.scale(ship_image1, (100, 100))
ship_image2 = pygame.transform.scale(ship_image2, (100, 100))
ship_image3 = pygame.transform.scale(ship_image3, (100, 100))
ship_image4 = pygame.transform.scale(ship_image4, (100, 100))
compass_circle = pygame.transform.scale(
    compass_circle, (150, 150)
)  # Resize compass circle
compass_pointer = pygame.transform.scale(
    compass_pointer, (120, 120)
)  # Resize compass pointer

pygame.display.set_caption("Gorms Program")
clock = pygame.time.Clock()

# Constants for colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0)
WATERBLUE = (0, 195, 245)

# Movement variables
speed = 4
direction = 0  # Direction of the ship, will be used to rotate the compass pointer

# Initialize Pymunk space
space = pymunk.Space()
space.gravity = (0, 0)

# Define Sprite class for the ship


class Sprite:
    def __init__(self, x, y):
        self.current_speed = 0
        self.image = ship_image

        self.rect = self.image.get_rect(center=(x, y))
        self.body = pymunk.Body(
            1, pymunk.moment_for_box(1, self.image.get_size())
        )  # Use image size for moment
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(
            self.body, self.image.get_size()
        )  # Use image size for hitbox
        self.shape.elasticity = 0.99
        space.add(self.body, self.shape)
        self.max_speed = 50

    def move(self, distance, direction):
        radians = math.radians(direction)
        force_x = distance * math.cos(radians) * 50
        force_y = distance * math.sin(radians) * 50
        self.body.apply_force_at_local_point((force_x, force_y))
        current_velocity = self.body.velocity
        speed = math.sqrt(current_velocity[0] ** 2 + current_velocity[1] ** 2)
        if speed > self.max_speed:

            normalized_velocity = (
                current_velocity[0] / speed,
                current_velocity[1] / speed,
            )
            self.body.velocity = (
                normalized_velocity[0] * self.max_speed,
                normalized_velocity[1] * self.max_speed,
            )

    def draw(self, surface, camera_x, camera_y):
        self.rect.center = (
            self.body.position.x - camera_x,
            self.body.position.y - camera_y,
        )
        surface.blit(self.image, self.rect)

        if direction < 22.5 or direction > 157.5:
            self.image = ship_image2
        elif direction < 67.5 and direction > 22.5:
            self.image = ship_image3
        elif direction < 112.5 and direction > 67.5:
            self.image = ship_image1
        elif direction < 157.5 and direction > 112.5:

            self.image = ship_image4


class Box:
    def __init__(self, x, y, space):
        self.image = pygame.Surface((35, 35))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Create a static body in Pymunk
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Poly.create_box(self.body, (35, 35))
        self.body.position = (x, y)

        # Add the body and shape to the space
        space.add(self.body, self.shape)

    def update(self):
        # Update the rect position based on the body's position
        self.rect.topleft = (
            self.body.position.x - self.rect.width / 2,
            self.body.position.y - self.rect.height / 2,
        )

    def draw(self, surface, camera_x, camera_y):
        # Call update to ensure rect is in sync with body position
        self.update()

        # Adjust rect position for camera
        adjusted_rect = self.rect.move(-camera_x, -camera_y)

        # Draw the image and the outline
        surface.blit(self.image, adjusted_rect)
        pygame.draw.rect(surface, RED, adjusted_rect, 2)


cube = Box(300, 200, space)
sprite = Sprite(375, 275)
camera_x, camera_y = 0, 0

# Initialize pymunk drawing options
draw_options = pymunk.pygame_util.DrawOptions(screen)

while True:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle key inputs for ship movement and direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direction -= 2
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction += 2
    while direction > 179:
        direction -= 180
    while direction < 0:
        direction += 180

    # Apply the direction to the sprite's body
    sprite.body.angle = math.radians(direction)
    sprite.move(speed, direction)

    # Update camera position
    camera_x = sprite.body.position.x - width // 2 + sprite.rect.width // 2
    camera_y = sprite.body.position.y - height // 2 + sprite.rect.width // 2

    # Clear the screen
    screen.fill(WATERBLUE)

    # Draw the ship and box objects
    sprite.draw(screen, camera_x, camera_y)
    cube.draw(screen, camera_x, camera_y)

    # Draw compass
    compass_pos = (width - 150, height - 150)  # Position of the compass circle
    screen.blit(compass_circle, compass_pos)  # Draw the compass circle

    # Rotate and draw the compass pointer
    rotated_pointer = pygame.transform.rotate(
        compass_pointer, -(direction + direction)
    )  # Rotate pointer based on direction
    pointer_rect = rotated_pointer.get_rect(
        center=(compass_pos[0] + 75, compass_pos[1] + 75)
    )  # Position pointer at the center of the compass circle
    screen.blit(rotated_pointer, pointer_rect.topleft)

    # Update the display
    pygame.display.flip()
    space.step(dt)
