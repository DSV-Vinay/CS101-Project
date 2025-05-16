import pygame 

class DialogueBox:
    def __init__(self, screen_width, screen_height, font_path, font_size):
        self.active = False
        self.lines = []
        self.current_line = 0
        
        self.box = pygame.Rect(50, screen_height - 200, screen_width - 100, 150)
        self.font = pygame.font.Font(font_path, font_size)
        self.text_color = (255, 255, 255)
        self.box_color = (40, 40, 40)
        self.border_color = (255, 215, 0)
        
        self.indicator = pygame.Surface((15, 5))
        self.indicator.fill(self.text_color)
        self.indicator_visible = True
        self.indicator_timer = 0

    def activate(self, lines):
        self.active = True
        self.lines = lines
        self.current_line = 0

    def update(self):
        if self.active:
            self.indicator_timer += 1
            if self.indicator_timer >= 30:
                self.indicator_visible = not self.indicator_visible
                self.indicator_timer = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                if self.current_line < len(self.lines) - 1:
                    self.current_line += 1
                else:
                    self.active = False

    def draw(self, screen):
        if not self.active:
            return
        
        pygame.draw.rect(screen, self.box_color, self.box)
        pygame.draw.rect(screen, self.border_color, self.box, 3)
        
        # Word wrapping 
        text = self.lines[self.current_line]
        words = text.split(' ')
        space = self.font.size(' ')[0]
        max_width = self.box.width - 40  
        
        x, y = self.box.x + 20, self.box.y + 20
        line_height = self.font.get_height()
        
        for word in words:
            word_surface = self.font.render(word, True, self.text_color)
            if x + word_surface.get_width() > self.box.right - 20:
                x = self.box.x + 20
                y += line_height
            screen.blit(word_surface, (x, y))
            x += word_surface.get_width() + space
        
        if self.current_line == len(self.lines) - 1 and self.indicator_visible:
            screen.blit(self.indicator, (self.box.right - 40, self.box.bottom - 30))