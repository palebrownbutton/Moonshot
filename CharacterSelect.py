from pygame import *
from AnimatedSprite import *
from KnightMovement import Knight
from StillImage import *

class Background:

    def __init__(self, x, y, w, h, filename):

        self.image = image.load(filename)
        self.image = transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


knight1 = Knight("Knight_1/Idle.png", -10, -50, 128, 128, "Knight_1")
knight1.resize(640, 640)
knight2 = Knight("Knight_2/Idle.png", 240, -50, 128, 128, "Knight_2")
knight2.resize(640, 640)
knight3 = Knight("Knight_3/Idle.png", 490, -50, 128, 128, "Knight_3")
knight3.resize(640, 640)

background = Background(0, 0, 800, 800, "select_background.png")

xpostions = [-65, 186, 436]
box = Background(xpostions[1], 170, 450, 500, "select_box.png")

position = 2

last_move = 0
move_delay = 150

house_button = StillImage(5, 10, 90, 90, "house.png")

def select_character(window, ignore_return=False):
    global position, last_move

    mouse_x, mouse_y = mouse.get_pos()

    background.draw(window)

    box.draw(window)

    knight1.draw(window)
    knight2.draw(window)
    knight3.draw(window)

    house_button.draw(window)

    pressed = key.get_pressed()
    if ignore_return and pressed[K_RETURN]:
        return None, False
    now = time.get_ticks()
    if pressed[K_LEFT] and now - last_move >= move_delay:
        if position > 1:
            position -= 1
        else:
            position = 3
        last_move = now
    elif pressed[K_RIGHT] and now - last_move >= move_delay:
        if position < 3:
            position += 1
        else:
            position = 1
        last_move = now

    if pressed[K_RETURN]:
        if position == 1:
            return "Knight_1", False
        elif position == 2:
            return "Knight_2", False
        elif position == 3:
            return "Knight_3", False
        
    if pressed[K_ESCAPE]:
        return None, True

    if position == 1:
        box.rect.x = xpostions[0]
    elif position == 2:
        box.rect.x = xpostions[1]
    elif position == 3:
        box.rect.x = xpostions[2]

    if (mouse_x >= house_button.rect.x and mouse_x <= house_button.rect.x + house_button.rect.width and mouse_y >= house_button.rect.y and mouse_y <= house_button.rect.y + house_button.rect.height):
        if mouse.get_pressed()[0]:
            return None, True

    return None, False