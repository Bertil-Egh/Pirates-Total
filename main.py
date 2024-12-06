import pygame
import sys
import math
import pymunk
import pymunk.pygame_util
import time
import json

pygame.init()
pygame.mixer.init()  
pygame.mixer.music.load("WaterSplash.mp3")  
pygame.mixer.music.play(-1)  

width, height = 800, 600
MAP_WIDTH = 1600  # Width of the map
MAP_HEIGHT = 1200  # Height of the map
WATER_TILE_SIZE = 51
screen = pygame.display.set_mode((width, height))

tick = 0

ship_image = pygame.image.load("assets/media/image/PiratesTotalShipSide2.png")
ship_image1 = pygame.image.load("assets/media/image/PiratesTotalShipSide1.png")
ship_image2 = pygame.image.load("assets/media/image/PiratesTotalShipSide2.png")
ship_image3 = pygame.image.load("assets/media/image/PiratesTotalShipFront.png")
ship_image4 = pygame.image.load("assets/media/image/PiratesTotalShipBack.png")
compass_circle = pygame.image.load("assets/media/image/COMPASS.png")
compass_pointer = pygame.image.load("assets/media/image/COMPASSPOINTER.png")

octo_image = pygame.image.load("assets/media/image/OCTOPUSSSS.png")

with open("assets/media/json/water_1.json") as f:
    spritesheet_data = json.load(f)

water_image = pygame.image.load("assets/media/image/water_1.png").convert_alpha()

water_frames = []
for frame_data in spritesheet_data["frames"].values():
    frame = frame_data["frame"]
    rect = pygame.Rect(frame["x"], frame["y"], frame["w"], frame["h"])
    water_frames.append(water_image.subsurface(rect))

# Resize images
ship_image = pygame.transform.scale(ship_image, (100, 100))
ship_image1 = pygame.transform.scale(ship_image1, (100, 100))
ship_image2 = pygame.transform.scale(ship_image2, (100, 100))
ship_image3 = pygame.transform.scale(ship_image3, (100, 100))
ship_image4 = pygame.transform.scale(ship_image4, (100, 100))
compass_circle = pygame.transform.scale(compass_circle, (150, 150))  # Resize compass circle
compass_pointer = pygame.transform.scale(compass_pointer, (120, 120))  # Resize compass pointer
octo_image = pygame.transform.scale(octo_image, (150, 150))
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
        self.body = pymunk.Body(1, pymunk.moment_for_box(1, self.image.get_size()))  # Use image size for moment
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body, self.image.get_size())  # Use image size for hitbox
        self.shape.elasticity = 0.99
        space.add(self.body, self.shape)
        self.max_speed = 50
        self.cannonball_directionR = 0
        self.cannonball_directionL = 180
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
            self.cannonball_directionR = 90
            self.cannonball_directionL = 270
        elif direction < 67.5 and direction > 22.5:
            self.image = ship_image3
            self.cannonball_directionR = 180
            self.cannonball_directionL = 0
        elif direction < 112.5 and direction > 67.5:
            self.image = ship_image1
            self.cannonball_directionR = 270
            self.cannonball_directionL = 90
        elif direction < 157.5 and direction > 112.5:
            self.image = ship_image4
            self.cannonball_directionR = 0
            self.cannonball_directionL = 180

class Water:
    def __init__(self, x, y):
        self.frames = water_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 0.1  # Adjust for speed of animation

    def update(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

    def draw(self, surface, camera_x, camera_y, screen_width, screen_height):
        # Calculate the starting tile positions based on camera position
        start_x = int(camera_x // WATER_TILE_SIZE) * WATER_TILE_SIZE
        start_y = int(camera_y // WATER_TILE_SIZE) * WATER_TILE_SIZE

        # Calculate how many tiles fit on the screen
        num_tiles_x = (screen_width // WATER_TILE_SIZE) + 2  # Extra tiles for scrolling
        num_tiles_y = (screen_height // WATER_TILE_SIZE) + 2  # Extra tiles for scrolling

        # Draw the water tiles
        for i in range(num_tiles_x):
            for j in range(num_tiles_y):
                # Calculate the position of each tile
                tile_x = start_x + i * WATER_TILE_SIZE
                tile_y = start_y + j * WATER_TILE_SIZE

                # Adjust rect position for camera
                adjusted_rect = self.image.get_rect(topleft=(tile_x - camera_x, tile_y - camera_y))
                surface.blit(self.image, adjusted_rect)

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


class Cannonball:
    def __init__(self, x, y, direction, speed=10):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        radians = math.radians(self.direction)
        self.x += self.speed * math.cos(radians)
        self.y += self.speed * math.sin(radians)
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def check_collision(cannonballs, octopus):
    for cannonball in cannonballs[:]:  # Iterate safely over cannonballs
        # Calculate the distance between the cannonball and the octopus
        distance = math.hypot(
            cannonball.x - octopus.body.position.x,
            cannonball.y - octopus.body.position.y
        )
        
        # Define a reasonable collision threshold (based on octopus size)
        collision_threshold = 75  # Adjust as needed
        
        # Check for collision
        if distance < collision_threshold:
            octopus.take_damage(10)  # Apply damage to the octopus
            cannonballs.remove(cannonball)  # Remove the cannonball

        
class Octopuss:
    def __init__(self, x, y, space):
        self.image = octo_image
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 100
        self.max_health = 100
        self.damage = 10
        # Create a static body in Pymunk
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x, y)
        
        # Create a shape for the body
        self.shape = pymunk.Poly.create_box(self.body, (100, 100))
        
        # Add the body and shape to the space
        space.add(self.body, self.shape)

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def update(self):
        # Update the rect position based on the body's position
        self.rect.center = (
            self.body.position.x,
            self.body.position.y,
        )

    def draw(self, surface, camera_x, camera_y):
        # Call update to ensure rect is in sync with body position
        self.update()

        # Adjust rect position for camera
        adjusted_rect = self.rect.move(-camera_x, -camera_y)

        # Draw the octopus image
        surface.blit(self.image, adjusted_rect)

        # Draw the health bar above the octopus
        health_bar_width = 100
        health_bar_height = 10
        pygame.draw.rect(surface, BLUE, (adjusted_rect.x, adjusted_rect.y - 20, health_bar_width + 2, health_bar_height + 2))  # Background
        pygame.draw.rect(surface, RED, (adjusted_rect.x, adjusted_rect.y - 20, health_bar_width, health_bar_height))  # Red part
        pygame.draw.rect(surface, GREEN, (adjusted_rect.x, adjusted_rect.y - 20, (self.health / self.max_health) * health_bar_width, health_bar_height))  # Green part

cube = Box(300, 200, space)
sprite = Sprite(375, 275)
octopus = Octopuss(375, 275, space)  # Position the octopus at (600, 300)
camera_x, camera_y = 0, 0
octopus.draw(screen, camera_x, camera_y)

def draw_gradient(screen, time):
    # Calculate color values based on time
    r = 0
    g = 195
    b = max(230, int((128 + 127 * math.sin(time * 0.006)) % 256))
    for y in range(height):
        color = (r, g, b)
        pygame.draw.line(screen, color, (0, y), (width, y))


# Health bar variables
health = 100
max_health = 100

# Timer variables for cannon cooldown
last_shot_time = time.time()
cooldown = 0.5  # seconds

# Initialize pymunk drawing options
draw_options = pymunk.pygame_util.DrawOptions(screen)

cannonballs = []

while True:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.draw.circle(screen, (255, 255, 0), (int(octopus.body.position.x), int(octopus.body.position.y)), collision_threshold, 1)

    check_collision(cannonballs, octopus)

    # Update cannonballs
    for cannonball in cannonballs:
        cannonball.update()

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

    # Handle shooting
    if time.time() - last_shot_time > cooldown:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            cannonball = Cannonball(sprite.rect.centerx, sprite.rect.centery, sprite.cannonball_directionL)
            cannonballs.append(cannonball)
            last_shot_time = time.time()
        if keys[pygame.K_e]:
            cannonball = Cannonball(sprite.rect.centerx, sprite.rect.centery, sprite.cannonball_directionR)
            cannonballs.append(cannonball)
            last_shot_time = time.time()

    water.update()

    # Clear the screen
    draw_gradient(screen, tick)

    # Draw the ship and box objects
    water.draw(screen, camera_x, camera_y, width, height)
    sprite.draw(screen, camera_x, camera_y)
    cube.draw(screen, camera_x, camera_y)
    octopus.draw(screen, camera_x, camera_y)
    
    # Draw compass
    compass_pos = (width - 150, height - 150)
    screen.blit(compass_circle, compass_pos)

    rotated_pointer = pygame.transform.rotate(compass_pointer, -(direction + direction))
    pointer_rect = rotated_pointer.get_rect(center=(compass_pos[0] + 75, compass_pos[1] + 75))
    screen.blit(rotated_pointer, pointer_rect.topleft)

    health_bar_width = 200
    health_bar_height = 20
    pygame.draw.rect(screen, BLUE, (10, 10, health_bar_width + 2, health_bar_height + 2))
    pygame.draw.rect(screen, RED, (10, 10, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, GREEN, (10, 10, (health / max_health) * health_bar_width, health_bar_height))

    # Update cannonballs
    for cannonball in cannonballs:
        cannonball.update()
        cannonball.draw(screen)

    tick += 1

    # Update the display
    pygame.display.flip()
    space.step(dt)