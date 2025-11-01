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
instructions_button = Buttons(100, 380, 600, 600, "instructions_button.png", "instructions")
background = StillImage(0, 0, 800, 800, "select_background.png")

text1 = font.SysFont("Arial", 50)
font.rendered_text = text1.render("Welcome to Bones and Blades!", True, (255, 255, 255))
text2 = font.SysFont("Arial", 30)
font.rendered_subtext = text2.render("By Simona", True, (255, 255, 255))

is_selected = "play"
last_move = 0
move_delay = 150

instructions_open = False
ignore_return_local = False
ignore_until = 0

def start_screen(window):
    global is_selected, move_delay, last_move, instructions_open, ignore_return_local

    pressed = key.get_pressed()
    now_time = time.get_ticks()
    if now_time < ignore_until:
        background.draw(window)
        play.draw(window, is_selected)
        instructions_button.draw(window, is_selected)
        window.blit(font.rendered_text, (120, 100))
        window.blit(font.rendered_subtext, (340, 160))
        return True

    if ignore_return_local:
        background.draw(window)
        play.draw(window, is_selected)
        instructions_button.draw(window, is_selected)
        window.blit(font.rendered_text, (120, 100))
        window.blit(font.rendered_subtext, (340, 160))
        if pressed[K_RETURN]:
            return True
        else:
            ignore_return_local = False

    if instructions_open == False:

        background.draw(window)
        play.draw(window, is_selected)
        instructions_button.draw(window, is_selected)
        
        window.blit(font.rendered_text, (120, 100))
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
                instructions_open = instructions_menu(window)

    else:
        instructions_menu(window)
    
    return True

instructions = StillImage(0, 195, 800, 533, "instructions.png")
instructionstxt = font.SysFont("Arial", 70)
font.rendered_instructionstext = instructionstxt.render("Instructions", True, (255, 255, 255))
house_button = StillImage(5, 10, 90, 90, "house.png")

def instructions_menu(window):
    global instructions_open, ignore_return_local, ignore_until

    mouse_x, mouse_y = mouse.get_pos()

    background.draw(window)
    instructions.draw(window)
    window.blit(font.rendered_instructionstext, (250, 60))
    house_button.draw(window)

    pressed_key = key.get_pressed()

    if pressed_key[K_RETURN]:
        instructions_open = False
        ignore_return_local = True
        ignore_until = time.get_ticks() + 300

    elif (mouse_x >= house_button.rect.x and mouse_x <= house_button.rect.x + house_button.rect.width and mouse_y >= house_button.rect.y and mouse_y <= house_button.rect.y + house_button.rect.height):
        if mouse.get_pressed()[0]:
            instructions_open = False
            ignore_return_local = True
            ignore_until = time.get_ticks() + 300


    return True

playAgian = Buttons(100, 200, 600, 600, "play_again_button.png", "playAgain")
home = Buttons(100, 380, 600, 600, "home_button.png", "home")
game_over_txt = font.SysFont("Arial", 150)
font.rendered_game_over = game_over_txt.render("Game Over...", True, (255, 0, 0))
with open ("highscore.txt", 'r') as file:
    lines = file.readlines()
    numbers = [int(line.strip()) for line in lines if line.strip().isdigit()]
highscore = max(numbers) if numbers else 0
highscore_text = font.SysFont("Arial", 50)
font.rendered_highscore = highscore_text.render(f"High Score: {highscore}", True, (255, 255, 255))
def game_over(window):
    global is_selected, move_delay, last_move, instructions_open

    if is_selected not in ("playAgain", "home"):
        is_selected = "playAgain"

    background.draw(window)
    playAgian.draw(window, is_selected)
    home.draw(window, is_selected)
    window.blit(font.rendered_game_over, (45, 50))
    window.blit(font.rendered_highscore, (255, 250))

    pressed= key.get_pressed()
    now = time.get_ticks()
    if pressed[K_UP] and now - last_move >= move_delay:
        if is_selected == "playAgain":
            is_selected = "home"
        else:
            is_selected = "playAgain"
        last_move = now
    elif pressed[K_DOWN] and now - last_move >= move_delay:
        if is_selected == "home":
            is_selected = "playAgain"
        else:
            is_selected = "home"
        last_move = now
    
    if pressed[K_RETURN]:

        if is_selected == "playAgain":
            return False
        else:
            is_selected = "play"
            instructions_open = False
            return True
        
def return_home():

    pass