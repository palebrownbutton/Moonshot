from pygame import *
import math

class WavesText:

    def __init__(self, text, font, color, position, duration=1000):
        
        self.text = text
        self.font = font
        self.color = color
        self.postion = position
        self.timer = 0
        self.duration = duration
        self.active = True

        self.image = self.font.render(self.text, True, self.color)
        self.original_size = self.image.get_size()

    def update(self, dt):

        if not self.active:
            return
        
        self.timer += dt
        if self.timer >= self.duration:
            self.active = False
    
    def draw(self, surface):
        
        if not self.active:
            return
    
        progress = self.timer / self.duration
        scale_factor = 1.5 - 0.5 * math.cos(progress * math.pi * 2)

        new_size = (
            int(self.original_size[0] * scale_factor),
            int(self.original_size[1] * scale_factor)
        )
        scaled_image = transform.scale(self.image, new_size)

        x = self.postion[0] - (new_size[0] - self.original_size[0]) // 2
        y = self.postion[1] - (new_size[1] - self.original_size[1]) // 2
        surface.blit(scaled_image, (x, y))
