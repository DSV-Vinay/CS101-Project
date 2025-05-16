import pygame

class FontSprite:
    def __init__(self, image_path):
        self.char_width = 24
        self.char_height = 35
        self.font_image = pygame.image.load(image_path).convert_alpha()
        
        # Character mapping matching font.png layout
        self.chars = (
            "ABCDEFGHI"    # Row 1
            "JKLmnopqR"    # Row 2
            "STUUUHYEO"    # Row 3
            "123456789"    # Row 4
            ".,!? "        # Remaining characters
        )
        
        self.char_map = {
            char: pygame.Rect((i%9)*self.char_width, (i//9)*self.char_height, self.char_width, self.char_height)
            for i, char in enumerate(self.chars)
        }

    def render_text(self, text):
        # Handle empty text case
        if not text:
            return pygame.Surface((0, 0), pygame.SRCALPHA)
        
        # Calculate width with spacing (24px char + 2px spacing)
        width = max(1, (len(text) * 26) - 2)
        
        surface = pygame.Surface(
            (width, self.char_height),
            pygame.SRCALPHA
        )
        
        x_offset = 0
        for char in text:
            if char in self.char_map:
                surface.blit(self.font_image, (x_offset, 0), self.char_map[char])
                x_offset += 26  # 24px character + 2px spacing
        return surface