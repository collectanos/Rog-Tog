import pygame
import math

class Hint:
    def __init__(self):
        self.key_width = 100
        self.key_height = 40
        
        self.surface = pygame.Surface((self.key_width, self.key_height + 30))
        self.surface.set_colorkey((0,0,0))
        self.rect = self.surface.get_rect()
        
        self.rect.centerx = 1280 // 2
        self.rect.bottom = 800 - 20
        
        self.animation_time = 0
        self.animation_speed = 5
        self.press_offset = 0
        self.max_press_offset = 4
        
        self.square_size = 15
        self.square_y = 0
        self.jump_height = 20
        self.jump_speed = 0.15
        self.jump_time = 0
        
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render("SPACE", True, (0, 0, 0))
        self.text_rect = self.text.get_rect()
        
        self.visible = False
        
        self.key_color = (220, 220, 220)
        self.shadow_color = (100, 100, 100)
        self.outline_color = (50, 50, 50)
        self.square_color = (0, 255, 0)
        
        self.pulse_time = 0
        self.pulse_amplitude = 2
        self.pulse_speed = 0.1

    def show(self):
        self.visible = True
        
    def hide(self):
        self.visible = False
        self.animation_time = 0
        self.press_offset = 0

    def update(self):
        if not self.visible:
            return
            
        self.pulse_time += self.pulse_speed
        
        self.jump_time += self.jump_speed
        self.square_y = -abs(math.sin(self.jump_time) * self.jump_height)
            
        if self.square_y > -2:
            self.animation_time += 1
            self.press_offset = min(self.max_press_offset, 
                                  self.animation_time / self.animation_speed)
        else:
            self.animation_time = max(0, self.animation_time - 1)
            self.press_offset = max(0, 
                                  self.animation_time / self.animation_speed)

    def draw(self, screen):
        if not self.visible:
            return
            
        self.surface.fill((0,0,0))
        
        pulse_offset = math.sin(self.pulse_time) * self.pulse_amplitude
        
        shadow_height = self.key_height - self.press_offset
        shadow_rect = pygame.Rect(2, 32,
                                self.key_width-4, 
                                shadow_height)
        pygame.draw.rect(self.surface, self.shadow_color, shadow_rect)
        
        key_rect = pygame.Rect(0, 30 + self.press_offset,
                             self.key_width-4, 
                             self.key_height-4-self.press_offset)
        
        for i in range(3):
            gradient_rect = pygame.Rect(0, 30 + self.press_offset + i,
                                      self.key_width-4, 
                                      self.key_height-4-self.press_offset)
            color = (max(180, 220 - i*20), max(180, 220 - i*20), max(180, 220 - i*20))
            pygame.draw.rect(self.surface, color, gradient_rect)
        
        pygame.draw.rect(self.surface, self.outline_color, key_rect, 2)
        
        self.text_rect.center = (key_rect.centerx, 
                                key_rect.centery + self.press_offset/2)
        self.surface.blit(self.text, self.text_rect)
        
        highlight_rect = pygame.Rect(4, 30 + self.press_offset + 4,
                                   self.key_width-12, 2)
        pygame.draw.rect(self.surface, (255,255,255,128), highlight_rect)
        
        square_rect = pygame.Rect(
            self.key_width//2 - self.square_size//2,
            30 + self.square_y,
            self.square_size,
            self.square_size
        )
        pygame.draw.rect(self.surface, self.square_color, square_rect)
        
        screen.blit(self.surface, 
                   (self.rect.x, 
                    self.rect.y + pulse_offset))