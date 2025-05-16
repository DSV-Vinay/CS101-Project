import pygame
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 255, 0))  # Green rectangle
        self.rect = self.image.get_rect(center=(640, 360))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 5
        self.direction = pygame.math.Vector2()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Reset direction
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        
        # Normalize diagonal movement
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

    def update(self, dt):
        self.pos += self.direction * self.speed * dt * 60
        self.rect.center = self.pos

class Camera:
    def __init__(self):
        self.offset = pygame.math.Vector2()
        self.screen_center = pygame.math.Vector2(screen.get_size()) // 2

    def apply(self, target):
        return target.rect.center - self.offset + self.screen_center

    def update(self, target):
        self.offset.update(target.rect.center - self.screen_center)

# Game Setup
player = Player()
camera = Camera()
all_sprites = pygame.sprite.Group(player)

# Create background (example)
background = pygame.Surface((2000, 2000))
background.fill((30, 30, 30))

while True:
    dt = clock.tick(60) / 1000  # Delta time in seconds
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    # Update
    player.handle_input()
    player.update(dt)
    camera.update(player)

    # Draw
    screen.fill((0, 0, 0))
    
    # Draw background with camera offset
    bg_offset = -camera.offset + camera.screen_center
    screen.blit(background, bg_offset)
    
    # Draw player with camera offset
    screen.blit(player.image, camera.apply(player))
    
    pygame.display.update()