from pygame import *
from AnimatedSprite import *
from StillImage import StillImage
from QuestReader import *
import time as pytime
import json

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

play = Buttons(120, 170, 550, 550, "start_button.png", "play")
instructions_button = Buttons(100, 430, 600, 600, "instructions_button.png", "instructions")
start_view_quests = Buttons(100, 300, 600, 600, "view_quests_button.png", "view_quests")
background = StillImage(0, 0, 800, 800, "select_background.png")

text1 = font.SysFont("Arial", 50)
font.rendered_text = text1.render("Welcome to Bones and Blades!", True, (255, 255, 255))
text2 = font.SysFont("Arial", 30)
font.rendered_subtext = text2.render("By Simona", True, (255, 255, 255))

logo = StillImage(303, 160, 200, 200, "Bones and Blades Logo.png")

is_selected = "play"
last_move = 0
move_delay = 150

instructions_open = False
ignore_return_local = False
ignore_until = 0

quests_open = False

def start_screen(window):
    global is_selected, move_delay, last_move, instructions_open, ignore_return_local, quests_open

    pressed = key.get_pressed()
    now_time = time.get_ticks()
    if now_time < ignore_until:
        background.draw(window)
        play.draw(window, is_selected)
        instructions_button.draw(window, is_selected)
        start_view_quests.draw(window, is_selected)
        window.blit(font.rendered_text, (120, 50))
        window.blit(font.rendered_subtext, (340, 110))
        logo.draw(window)
        return True

    if ignore_return_local:
        background.draw(window)
        play.draw(window, is_selected)
        instructions_button.draw(window, is_selected)
        start_view_quests.draw(window, is_selected)
        window.blit(font.rendered_text, (120, 50))
        window.blit(font.rendered_subtext, (340, 110))
        logo.draw(window)
        if pressed[K_RETURN]:
            return True
        else:
            ignore_return_local = False

    if instructions_open == False and quests_open == False:

        background.draw(window)
        play.draw(window, is_selected)
        instructions_button.draw(window, is_selected)
        start_view_quests.draw(window, is_selected)
        
        window.blit(font.rendered_text, (120, 50))
        window.blit(font.rendered_subtext, (340, 110))
        logo.draw(window)

        pressed = key.get_pressed()
        now = time.get_ticks()
        if pressed[K_UP] and now - last_move >= move_delay:
            if is_selected == "instructions":
                is_selected = "view_quests"
            elif is_selected == "view_quests":
                is_selected = "play"
            else:
                is_selected = "instructions"
            last_move = now
        elif pressed[K_DOWN] and now - last_move >= move_delay:
            if is_selected == "play":
                is_selected = "view_quests"
            elif is_selected == "view_quests":
                is_selected = "instructions"
            else:
                is_selected = "play"
            last_move = now

        if pressed[K_RETURN]:
            if is_selected == "play":
                return False
            elif is_selected == "instructions":
                instructions_open = instructions_menu(window)
            else:
                quests_open = quests_menu(window)

    elif instructions_open == True:
        instructions_menu(window)
    else:
        quests_menu(window)
    
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

quest_titles = []
quest_details = []
rewards_gain = []

quest_title_mapping = []
for idx, (quest_id, quest) in enumerate(quests.items()):

    for level_index in range(len(quest["title"])):
        if level_index < len(quest["title"]):
            quest_title_mapping.append((quest_id, level_index))

        title_font = font.SysFont(None, 50)
        detail_font = font.SysFont(None, 30)
        rewards_font = font.SysFont(None, 50)

        rendered_quest_title = title_font.render(quest["title"][level_index], True, (255, 255, 255))
        rendered_quest_detail = detail_font.render(quest["details"][level_index], True, (200, 200, 200))
        
        xp_amount = quest["reward"]["xp"][level_index]
        rendered_quest_rewards = rewards_font.render(f"{xp_amount} XP", True, (212, 148, 11))

        quest_titles.append(rendered_quest_title)
        quest_details.append(rendered_quest_detail)
        rewards_gain.append(rendered_quest_rewards)

quest_list_word_text = font.SysFont(None, 100)
font.rendered_quest_list_word = quest_list_word_text.render("Quests:", True, (255, 255, 255))

padlock = StillImage(580, 20, 60, 60, "padlock.png")

quests_boxes = []
total_levels = sum(len(quest["title"]) for quest in quests.values())

for i in range(total_levels):

    box = Rect(150, 110 + (i * 80), 630, 80)
    quests_boxes.append(box)

scroll_y = 0
scroll_speed = 20
TOP_LIMIT = 80

def quests_menu(window):
    global instructions_open, ignore_return_local, ignore_until, quests_open, scroll_y, scroll_speed

    mouse_x, mouse_y = mouse.get_pos()

    quest_title_mapping = []
    for idx, (quest_id, quest) in enumerate(quests.items()):
        unlocked_level = quests_levels[idx].level
        for level_index in range(len(quest["title"])):
            quest_title_mapping.append((quest_id, level_index, level_index > unlocked_level))

    max_scroll = max((len(quest_title_mapping)* 80 - (window.get_height() - TOP_LIMIT), 0)) + 50

    background.draw(window)
    house_button.draw(window)
    window.blit(font.rendered_quest_list_word, (150, 20))
    
    for i, (quest_id, level_index, is_locked) in enumerate(quest_title_mapping):

        y_offset = 120 + (80 * i) + scroll_y
       
        quest = quests[quest_id]

        if y_offset > TOP_LIMIT:

            if is_locked:
                padlock.rect.y = y_offset
                padlock.draw(window)

            title_font = font.SysFont(None, 50)
            detail_font = font.SysFont(None, 30)
            rewards_font = font.SysFont(None, 50)

            rendered_quest_title = title_font.render(quest["title"][level_index], True, (255, 255, 255))
            rendered_quest_detail = detail_font.render(quest["details"][level_index], True, (200, 200, 200))
            
            xp_amount = quest["reward"]["xp"][level_index]
            rendered_quest_rewards = rewards_font.render(f"{xp_amount} XP", True, (212, 148, 11))

            adjusted_box = Rect(150, y_offset - 10, 630, 80)
            draw.rect(window, (135, 84, 3), adjusted_box, width=2)

            if quest["isCompleted"][level_index]:
                s = Surface((630, 80), SRCALPHA)
                s.fill((58, 117, 6, 200))
                window.blit(s, (adjusted_box.x, adjusted_box.y))

            elif not quest["isCompleted"][level_index]:
                first_incomplete = False
                for li in range(len(quest["title"])):
                    if not quest["isCompleted"][li]:
                        if li == level_index:
                            first_incomplete = True
                        break
                if first_incomplete:
                    s = Surface((630, 80), SRCALPHA)
                    s.fill((166, 41, 3, 100))
                    window.blit(s, (adjusted_box.x, adjusted_box.y))

            window.blit(rendered_quest_title, (155, y_offset))
            window.blit(rendered_quest_detail, (170, y_offset + 40))
            window.blit(rendered_quest_rewards, (650, y_offset + 15))
    
    if (mouse_x >= house_button.rect.x and mouse_x <= house_button.rect.x + house_button.rect.width and mouse_y >= house_button.rect.y and mouse_y <= house_button.rect.y + house_button.rect.height):
        if mouse.get_pressed()[0]:
            quests_open = False
            ignore_return_local = True
            ignore_until = time.get_ticks() + 300

    for e in event.get():
        if e.type == QUIT:
            exit()

        elif e.type == MOUSEWHEEL:
            scroll_y += e.y * scroll_speed
            scroll_y = max(min(scroll_y, 0), -max_scroll)

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

pause_box = StillImage(-5, -30, 800, 900, "pause_box.png")
continue_gameplay = Buttons(200, 130, 400, 400, "continue_button.png", "continue_gameplay")
pause_view_quests = Buttons(200, 220, 400, 400, "view_quests_button.png", "view_quests")
exit_gameplay = Buttons(200, 310, 400, 400, "exit_gameplay_button.png", "exit_gameplay")

def pause_screen(window):
    global is_selected, last_move, move_delay, home

    if is_selected not in ("continue_gameplay", "view_quests", "exit_gameplay"):
        is_selected = "continue_gameplay"

    pause_box.draw(window)
    continue_gameplay.draw(window, is_selected)
    pause_view_quests.draw(window, is_selected)
    exit_gameplay.draw(window, is_selected)

    pressed = key.get_pressed()
    now = time.get_ticks()
    if pressed[K_UP] and now - last_move >= move_delay:

        if is_selected == "continue_gameplay":
            is_selected = "exit_gameplay"
        elif is_selected == "view_quests":
            is_selected = "continue_gameplay"
        else:
            is_selected = "view_quests"
        last_move = now
    elif pressed[K_DOWN] and now - last_move >= move_delay:

        if is_selected == "continue_gameplay":
            is_selected = "view_quests"
        elif is_selected == "view_quests":
            is_selected = "exit_gameplay"
        else:
            is_selected = "continue_gameplay"
        last_move = now

    paused_game = True
    is_home = False

    if pressed[K_RETURN]:
        
        if is_selected == "continue_gameplay":
            paused_game = False
        elif is_selected == "exit_gameplay":
            paused_game = False
            is_home = True
            is_selected = "play"
            pytime.sleep(0.2)
        else:
            pass
            # Add quests menu after creating quest log in javascript file seperate
    
    return paused_game, is_home

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