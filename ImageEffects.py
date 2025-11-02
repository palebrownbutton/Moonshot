from pygame import *
import math

class WavesText:

    def __init__(self, image, position, duration=1000):
        
        self.image = image
        self.original_size = image.get_size()
        self.postion = position
        self.timer = 0
        self.duration = duration
        self.active = True
        self.flash_duration = 100

        self.flash_triggered = False

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
