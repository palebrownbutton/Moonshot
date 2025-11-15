from pygame import *
font.init()

class StillImage:

    def __init__(self, x, y, w, h, filename):

        self.image = image.load(filename)
        self.image = transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class TextRender:

    def __init__(self, font_name, size, colour, text):
        self.font_type = font_name
        self.size = size
        self.font = font.SysFont(self.font_type, self.size)
        self.colour = colour
        self.text = text
        self.rendered_text = self.font.render(self.text, True, self.colour)

    def draw(self, window, position):
        window.blit(self.rendered_text, position)