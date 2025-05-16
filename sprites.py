import pygame

class TerrainTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = None  

class CollisionObject(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.set_alpha(0)  
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

class DialogueTrigger(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, dialogue_key):
        super().__init__(groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA) 
        self.image.fill((0, 0, 0, 0)) 
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
        self.dialogue_key = dialogue_key
