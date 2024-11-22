import pygame
import sys
import math
import pymunk
import pymunk.pygame_util

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

ship_image1 = pygame.image.load('PiratesTotalShipSide1.png')
ship_image2 = pygame.image.load('PiratesTotalShipSide2.png')
ship_image3 = pygame.image.load('PiratesTotalShipFront.png')
ship_image4 = pygame.image.load('PiratesTotalShipBack.png')

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

space = pymunk.Space()
space.gravity = (0, 0)

class Sprite:
    def __init__(self, x, y):
        self.image = ship_image2
        self.rect = self.image.get_rect(center=(x, y))
        self.body = pymunk.Body(1, pymunk.moment_for_box(1, (100, 100)))
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
        speed = math.sqrt(current_velocity[0]**2 + current_velocity[1]**2)
        if speed > self.max_speed:
            normalized_velocity = (current_velocity[0] / speed, current_velocity[1] / speed)
            self.body.velocity = (normalized_velocity[0] * self.max_speed, normalized_velocity[1] * self.max_speed)
    def draw(self, surface, camera_x, camera_y):
        self.rect.topleft = (self.body.position.x - camera_x, self.body.position.y - camera_y)
        surface.blit(self.image, self.rect)
        if direction < 22.5 and direction > 157.5:
           self.image = ship_image1
        if direction < 67.5 and direction > 22.5:
           self.image = ship_image2
        if direction < 112.5 and direction > 67.5:
           self.image = ship_image3
        if direction < 157.5 and direction > 112.5:
           self.image = ship_image4
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
        self.rect.topleft = (self.body.position.x - camera_x, self.body.position.y - camera_y)
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 2)

cube = Box(300, 200)
sprite = Sprite(375, 275)
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
    print(direction)
    space.step(dt)
    camera_x = sprite.body.position.x - width // 2 + sprite.rect.width // 2
    camera_y = sprite.body.position.y - height // 2 + sprite.rect.width // 2
    screen.fill(WATERBLUE)
    sprite.draw(screen, camera_x, camera_y)
    cube.draw(screen, camera_x, camera_y)
    pygame.display.flip()
