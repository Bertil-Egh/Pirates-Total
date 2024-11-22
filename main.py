import pygame
import sys
import math
import random
import pymunk
import pymunk.pygame_util

pygame.init()

width, height = 800, 600
MAP_WIDTH = 1600  # Width of the map
MAP_HEIGHT = 1200  # Height of the map
screen = pygame.display.set_mode((width, height))

ship_image = pygame.image.load("PiratesTotalShipSide2.png")
ship_image1 = pygame.image.load("PiratesTotalShipSide1.png")
ship_image2 = pygame.image.load("PiratesTotalShipSide2.png")
ship_image3 = pygame.image.load("PiratesTotalShipFront.png")
ship_image4 = pygame.image.load("PiratesTotalShipBack.png")

ship_image = pygame.transform.scale(ship_image, (100, 100))
ship_image1 = pygame.transform.scale(ship_image1, (100, 100))
ship_image2 = pygame.transform.scale(ship_image2, (100, 100))
ship_image3 = pygame.transform.scale(ship_image3, (100, 100))
ship_image4 = pygame.transform.scale(ship_image4, (100, 100))

pygame.display.set_caption("Gorms Program")
clock = pygame.time.Clock()
ship_direction = 1

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0)
WATERBLUE = (0, 195, 245)

speed = 4
direction = 0

num_islands = 10  # Number of islands to generate

space = pymunk.Space()
space.gravity = (0, 0)


class Sprite:
    def __init__(self, x, y):
        self.image = ship_image
        self.rect = self.image.get_rect(center=(x, y))
        self.body = pymunk.Body(1, pymunk.moment_for_box(1, (50, 50)))
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body)
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
        self.rect.topleft = (
            self.body.position.x - camera_x,
            self.body.position.y - camera_y,
        )
        surface.blit(self.image, self.rect)
        if direction < 22.5 or direction > 157.5:
            self.image = ship_image2
        if direction < 67.5 and direction > 22.5:
            self.image = ship_image3
        if direction < 112.5 and direction > 67.5:
            self.image = ship_image1
        if direction < 157.5 and direction > 112.5:
            self.image = ship_image4

class Island:
    def __init__(self, vertices, x, y):
        # Create a surface for the island
        self.image = pygame.Surface((200, 200), pygame.SRCALPHA)  # Use SRCALPHA for transparency
        self.image.fill((0, 0, 0, 0))  # Fill with transparent color
        
        # Draw the polygon on the surface
        pygame.draw.polygon(self.image, GREEN, vertices)
        
        # Get the rect for positioning
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Create a static body for the island
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x + 100, y + 100)  # Center the body at the polygon's center
        
        # Create the polygon shape
        self.shape = pymunk.Poly(self.body, vertices)
        self.shape.elasticity = 0.5  # Adjust elasticity as needed
        space.add(self.body, self.shape)

    def draw(self, surface, camera_x, camera_y):
        # Update the rectangle position based on the body's position
        self.rect.topleft = (
            self.body.position.x - camera_x - 100,  # Adjust for the center offset
            self.body.position.y - camera_y - 100,  # Adjust for the center offset
        )
        surface.blit(self.image, self.rect)
        # Draw the polygon outline for visibility
        pygame.draw.polygon(surface, RED, [(v[0] + self.rect.x, v[1] + self.rect.y) for v in self.shape.get_vertices()], 2)


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
        self.rect.topleft = (
            self.body.position.x - camera_x,
            self.body.position.y - camera_y,
        )
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 2)

def generate_random_polygon(num_vertices, radius):
    """Generate a random polygon with a specified number of vertices and radius."""
    angle_step = 360 / num_vertices
    vertices = []
    
    for i in range(num_vertices):
        angle = math.radians(i * angle_step + random.uniform(-angle_step / 2, angle_step / 2))
        r = random.uniform(radius * 0.5, radius)  # Randomize the distance from the center
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        vertices.append((x, y))
    
    return vertices


def generate_islands(num_islands):
    islands = []
    for _ in range(num_islands):
        # Randomly generate the number of vertices for the island
        num_vertices = random.randint(3, 8)  # Random number of vertices between 3 and 8
        radius = random.randint(50, 150)  # Random radius for the shape
        
        # Generate random polygon vertices
        vertices = generate_random_polygon(num_vertices, radius)
        
        # Randomly position the island within the map area
        x = random.randint(0 + radius, MAP_WIDTH - radius)
        y = random.randint(0 + radius, MAP_HEIGHT - radius)
        
        # Create the island and add it to the list
        islands.append(Island(vertices, x, y))
    
    return islands


islands = generate_islands(num_islands)

island_vertices = [(10, 0), (100, 5), (100, 50), (4, 50)]

cube = Box(300, 200)
sprite = Sprite(375, 275)
island1 = Island(island_vertices, 200, 300)
island2 = Island(island_vertices, 500, 400)
camera_x, camera_y = 0, 0

while True:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direction -= 2
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction += 2
    while direction > 179:
        direction -= 180
    while direction < 0:
        direction += 180
    sprite.body.angle = math.radians(direction)
    sprite.move(speed, direction)
    space.step(dt)
    camera_x = sprite.body.position.x - width // 2 + sprite.rect.width // 2
    camera_y = sprite.body.position.y - height // 2 + sprite.rect.width // 2
    screen.fill(WATERBLUE)
    sprite.draw(screen, camera_x, camera_y)
    island1.draw(screen, camera_x, camera_y)
    island2.draw(screen, camera_x, camera_y)
    cube.draw(screen, camera_x, camera_y)
    for island in islands:
        island.draw(screen, camera_x, camera_y)
    pygame.display.flip()
