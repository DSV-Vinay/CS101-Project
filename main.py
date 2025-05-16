import pygame
import sys
import os
from pytmx.util_pygame import load_pygame
from settings import TILE_SIZE
from sprites import TerrainTile, CollisionObject, DialogueTrigger
from char import Player
from dialogue import DialogueBox
from settings import dialogues

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Midnight Requiem")
        self.clock = pygame.time.Clock()
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.debug_mode = False

        # Load map
        self.tmx_map = load_pygame(os.path.join(self.base_path, 'Data', 'Maps', 'stage 1.tmx'))

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.manual_triggers = pygame.sprite.Group()
        self.auto_triggers = pygame.sprite.Group()  

        # Setup world
        self.create_terrain()
        self.create_collisions()
        self.create_manual_triggers()
        self.create_auto_triggers()  

        # Player setup
        self.player = Player(
            pos=(200, 200),
            groups=[self.all_sprites],
            collision_sprites=self.collision_sprites
        )
        self.current_manual_trigger = None

        # Dialogue system
        self.dialogues = dialogues
        self.dialogue_box = DialogueBox(
            1280, 720,
            os.path.join(self.base_path, 'Data', 'Fonts', 'MorrisRoman-Black.ttf'),
            24
        )

        # Debug font
        self.debug_font = pygame.font.SysFont("consolas", 16)

        # Show initial dialogue
        self.dialogue_box.activate(self.dialogues["start"])

    def create_terrain(self):
        try:
            layer = self.tmx_map.get_layer_by_name('Tile Layer 1')
            for x, y, surf in layer.tiles():
                TerrainTile(
                    pos=(x * TILE_SIZE, y * TILE_SIZE),
                    surf=surf,
                    groups=[self.all_sprites]
                )
        except Exception as e:
            if self.debug_mode:
                print(f"Terrain Error: {str(e)}")

    def create_collisions(self):
        try:
            collision_layer = self.tmx_map.get_layer_by_name('Object Layer 1')
            for obj in collision_layer:
                CollisionObject(
                    pos=(obj.x, obj.y),
                    size=(obj.width, obj.height),
                    groups=[self.all_sprites, self.collision_sprites]
                )
        except Exception as e:
            if self.debug_mode:
                print(f"Collision Error: {str(e)}")

    def create_manual_triggers(self):
        #enter to trigger
        try:
            trigger_layer = self.tmx_map.get_layer_by_name('ManualTriggers')
            for obj in trigger_layer:
                DialogueTrigger(
                    pos=(obj.x, obj.y),
                    size=(obj.width, obj.height),
                    groups=[self.all_sprites, self.manual_triggers],
                    dialogue_key=obj.properties.get('dialogue_key', 'coffin')
                )
        except Exception as e:
            if self.debug_mode:
                print(f"Manual Trigger Error: {str(e)}")

    def create_auto_triggers(self):
        """For automatic collision-based triggers"""
        try:
            auto_layer = self.tmx_map.get_layer_by_name('AutoTriggers')
            for obj in auto_layer:
                trigger = DialogueTrigger(
                    pos=(obj.x, obj.y),
                    size=(obj.width, obj.height),
                    groups=[self.all_sprites, self.auto_triggers],
                    dialogue_key=obj.properties.get('dialogue_key')
                )
                trigger.has_triggered = False  # one off trigger flag
        except Exception as e:
            if self.debug_mode:
                print(f"Auto Trigger Error: {str(e)}")

    def act_maunual_triggers(self):
        """Manual triggers looping"""
        self.current_manual_trigger = None
        manual_hit_list = pygame.sprite.spritecollide(
            self.player, self.manual_triggers, False,
            collided=lambda spr1, spr2: spr1.hitbox.colliderect(spr2.hitbox)
        )

        if manual_hit_list:
            player_center = pygame.Vector2(self.player.hitbox.center)
            self.current_manual_trigger = min(
                manual_hit_list,
                key=lambda t: pygame.Vector2(t.hitbox.center).distance_to(player_center)
            )

    def act_auto_triggers(self):
        """Automatic triggers looping to check collision at all instants"""
        if not self.dialogue_box.active:
            auto_hit_list = pygame.sprite.spritecollide(
                self.player, self.auto_triggers, False,
                collided=lambda spr1, spr2: spr1.hitbox.colliderect(spr2.hitbox)
            )
            
            for trigger in auto_hit_list:
                if not trigger.has_triggered:
                    self.trigger_dialogue(trigger.dialogue_key)
                    trigger.has_triggered = True

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                if self.current_manual_trigger and not self.dialogue_box.active:
                    self.trigger_dialogue(self.current_manual_trigger.dialogue_key)
                    
    def trigger_dialogue(self, key):
        if key in self.dialogues:
            self.dialogue_box.activate(self.dialogues[key])

    def draw_debug(self):
        debug_info = [
            f"FPS: {self.clock.get_fps():.1f}",
            f"Position: {self.player.rect.x}, {self.player.rect.y}",
            f"Colliding: {len(pygame.sprite.spritecollide(self.player, self.collision_sprites, False)) > 0}",
            f"Near Manual: {bool(self.current_manual_trigger)}",
            f"Active Auto: {len(self.auto_triggers)} triggers"  
        ]

        y_offset = 10
        for line in debug_info:
            text_surf = self.debug_font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surf, (10, y_offset))
            y_offset += 20

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000

            # Event handling(exit and dialouge popup)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.dialogue_box.active:
                    self.dialogue_box.handle_input(event)
                else:
                    self.handle_input(event)

            # Updating game with time 
            if not self.dialogue_box.active:
                self.player.update(dt)
                self.act_maunual_triggers()
                self.act_auto_triggers()  
            
            self.dialogue_box.update()

            # Rendering/drawing
            self.screen.fill((30, 30, 30))
            self.all_sprites.draw(self.screen)
            self.dialogue_box.draw(self.screen)

            if self.debug_mode:
                self.draw_debug()

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()