from pygame import *
from AnimatedSprite import *
from StillImage import StillImage
font.init()

class Buttons():

    def __init__(self, x, y, w, h, filename, name):

        self.image = image.load(filename)
        self.image = transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name

    def draw(self, window, is_selected):
        tick = time.get_ticks() // 500 % 2
        if tick == 0 and is_selected == self.name:
            window.blit(self.image, (self.rect.x, self.rect.y))
        else:
            ghost_image = self.image.copy()
            ghost_image.set_alpha(30)
            window.blit(ghost_image, (self.rect.x, self.rect.y))

play = Buttons(100, 200, 600, 600, "start_button.png", "play")
instructions = Buttons(100, 380, 600, 600, "instructions_button.png", "instructions")
background = StillImage(0, 0, 800, 800, "select_background.png")

text1 = font.SysFont("Arial", 50)
font.rendered_text = text1.render("Welcome to my game!", True, (255, 255, 255))
text2 = font.SysFont("Arial", 30)
font.rendered_subtext = text2.render("By Simona", True, (255, 255, 255))

is_selected = "play"
last_move = 0
move_delay = 150

def start_screen(window):
    global is_selected, move_delay, last_move

    background.draw(window)
    play.draw(window, is_selected)
    instructions.draw(window, is_selected)
    
    window.blit(font.rendered_text, (200, 100))
    window.blit(font.rendered_subtext, (340, 160))

    pressed = key.get_pressed()
    now = time.get_ticks()
    if pressed[K_UP] and now - last_move >= move_delay:
        if is_selected == "instructions":
            is_selected = "play"
        else:
            is_selected = "instructions"
        last_move = now
    elif pressed[K_DOWN] and now - last_move >= move_delay:
        if is_selected == "play":
            is_selected = "instructions"
        else:
            is_selected = "play"
        last_move = now

    if pressed[K_RETURN]:
        if is_selected == "play":
            return False
        else:
            pass 
            # Add intrustions screen later

    return True