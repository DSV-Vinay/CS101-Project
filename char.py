import pygame
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('Test1/Graphics/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(32,32))
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-20, -30)
        # Movement
        self.direction = Vector2()
        self.speed = 210
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

    def move(self, dt):
        # Horizontal
        self.hitbox.x += self.direction.x * self.speed * dt
        self.collide('horizontal')
        
        # Vertical
        self.hitbox.y += self.direction.y * self.speed * dt
        self.collide('vertical')
        
        self.rect.center = self.hitbox.center

    def collide(self, direction):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self, dt):
        self.input()
        self.move(dt)
