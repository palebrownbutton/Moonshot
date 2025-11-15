from pygame import *
from AnimatedSprite import *
from StillImage import StillImage, TextRender
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
start_view_quests = Buttons(100, 300, 600, 600, "progress.png", "view_quests")
background = StillImage(0, 0, 800, 800, "select_background.png")

text1 = TextRender("Arial", 50, (255, 255, 255), "Welcome to Bones and Blades!")
text2 = TextRender("Arial", 30, (255, 255, 255), "By Simona")

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
        text1.draw(window, (120, 50))
        text2.draw(window, (340, 110))
        logo.draw(window)
        return True

    if ignore_return_local:
        background.draw(window)
        play.draw(window, is_selected)
        instructions_button.draw(window, is_selected)
        start_view_quests.draw(window, is_selected)
        text1.draw(window, (120, 50))
        text2.draw(window, (340, 110))
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
        
        text1.draw(window, (120, 50))
        text2.draw(window, (340, 110))
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
instructionstxt = TextRender(None, 70, (255, 255, 255), "Instructions")
house_button = StillImage(5, 10, 90, 90, "house.png")

def instructions_menu(window):
    global instructions_open, ignore_return_local, ignore_until

    mouse_x, mouse_y = mouse.get_pos()

    background.draw(window)
    instructions.draw(window)
    instructionstxt.draw(window, (250, 60))
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

        rendered_quest_title = TextRender(None, 50, (255, 255, 255), quest["title"][level_index]) 
        rendered_quest_detail = TextRender(None, 30, (200, 200, 200), quest["details"][level_index])
        
        xp_amount = quest["reward"]["xp"][level_index]
        rendered_quest_rewards = TextRender(None, 50, (212, 148, 11), f"{xp_amount} XP")

        quest_titles.append(rendered_quest_title)
        quest_details.append(rendered_quest_detail)
        rewards_gain.append(rendered_quest_rewards)

quest_list_word_text = TextRender(None, 100, (255, 255, 255), "Quests:")

padlock = StillImage(555, 20, 60, 60, "padlock.png")
upgrades_button = StillImage(550, -100, 300, 300, "upgrades.png")

quests_boxes = []
total_levels = sum(len(quest["title"]) for quest in quests.values())

for i in range(total_levels):

    box = Rect(150, 110 + (i * 80), 630, 80)
    quests_boxes.append(box)

scroll_y = 0
scroll_speed = 20
TOP_LIMIT = 80

upgrades_open = False
click_cooldown = False

def quests_menu(window):
    global instructions_open, ignore_return_local, ignore_until, quests_open, scroll_y, scroll_speed, upgrades_open, click_cooldown

    if click_cooldown:
        if not mouse.get_pressed()[0]:
            click_cooldown = False
        return True

    if not upgrades_open:

        mouse_x, mouse_y = mouse.get_pos()

        quest_title_mapping = []
        for idx, (quest_id, quest) in enumerate(quests.items()):
            completed_levels = [i for i, done in enumerate(quest["isCompleted"]) if done]
            unlocked_level = max(completed_levels, default=-1) + 1
            for level_index in range(len(quest["title"])):
                quest_title_mapping.append((quest_id, level_index, level_index > unlocked_level))

        max_scroll = max((len(quest_title_mapping)* 80 - (window.get_height() - TOP_LIMIT), 0)) + 50

        background.draw(window)
        house_button.draw(window)
        upgrades_button.draw(window)
        quest_list_word_text.draw(window, (150, 20))

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

                rendered_quest_title = TextRender(None, 50, (255, 255, 255), quest["title"][level_index]) 
                rendered_quest_detail = TextRender(None, 30, (200, 200, 200), quest["details"][level_index])
                
                xp_amount = quest["reward"]["xp"][level_index]
                rendered_quest_rewards = TextRender(None, 50, (212, 148, 11), f"{xp_amount} XP")

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

                window.blit(rendered_quest_title.rendered_text, (155, y_offset))
                window.blit(rendered_quest_detail.rendered_text, (170, y_offset + 40))
                window.blit(rendered_quest_rewards.rendered_text, (625, y_offset + 15))

        if (mouse_x >= house_button.rect.x and mouse_x <= house_button.rect.x + house_button.rect.width and mouse_y >= house_button.rect.y and mouse_y <= house_button.rect.y + house_button.rect.height):
            if mouse.get_pressed()[0]:
                quests_open = False
                ignore_return_local = True
                ignore_until = time.get_ticks() + 300

        if (mouse_x >= upgrades_button.rect.x and mouse_x <= upgrades_button.rect.x + upgrades_button.rect.width and mouse_y >= upgrades_button.rect.y and mouse_y <= upgrades_button.rect.y + upgrades_button.rect.height):
            if mouse.get_pressed()[0]:
                upgrades_open = True

        for e in event.get():
            if e.type == QUIT:
                exit()

            elif e.type == MOUSEWHEEL:
                scroll_y += e.y * scroll_speed
                scroll_y = max(min(scroll_y, 0), -max_scroll)

    else:
        upgrades_open = upgrade_menu(window)

    return True
    
rect1 = Rect(50, 155, 200, 450)
overlay1 = Surface(rect1.size, SRCALPHA)
overlay1.fill((62, 64, 63, 180))
rect2 = Rect(300, 155, 200, 450)
overlay2 = Surface(rect2.size, SRCALPHA)
overlay2.fill((62, 64, 63, 180))
rect3 = Rect(550, 155, 200, 450)
overlay3 = Surface(rect3.size, SRCALPHA)
overlay3.fill((62, 64, 63, 180))

with open("upgrades.json", "r") as file:
    knight_attributes = json.load(file)[0]

rendered_hp_text = TextRender(None, 30, (255, 255, 255), "HP:") 
rendered_hp_num = TextRender(None, 60, (255, 255, 255), f"{knight_attributes['hp']}")
rendered_strength_text = TextRender(None, 30, (255, 255, 255), "Strength:")
rendered_strength_num = TextRender(None, 60, (255, 255, 255), f"{knight_attributes['strength']}")
rendered_lives_rate = TextRender(None, 30, (255, 255, 255), "Lives spawn rate:")
rendered_lives_rate_num = TextRender(None, 60, (255, 255, 255), f"{int(knight_attributes['life spawn time']/1000)} s")

strength_icon = StillImage(40, 173, 228, 130, "strength_image.png")
hp_icon = StillImage(333, 175, 130, 130, "hearts.png")
lives_rate_icon = StillImage(577, 160, 155, 155, "clock.png")

with open ("upgrades.json", "r") as file:
    data = json.load(file)
    total_xp = data[1]["total_xp"]
    hp_upgrade_level = data[1]["upgrade_level"]["hp_upgrade"]
    strength_upgrade_level = data[1]["upgrade_level"]["strength_upgrade"]
    lives_rate_upgrade_level = data[1]["upgrade_level"]["life_spawn_time_upgrade"]
    hp_required_xp = data[1]["required_xp"]["hp_required_xp"][hp_upgrade_level]
    strength_required_xp = data[1]["required_xp"]["strength_required_xp"][strength_upgrade_level]
    lives_rate_required_xp = data[1]["required_xp"]["lives_spawn_time_required_xp"][lives_rate_upgrade_level]

rendered_total_xp_text = TextRender(None, 60, (255, 255, 255), f"XP: {total_xp}")

rendered_hp_upgrade_level_text = TextRender(None, 50, (255, 255, 255), f"Level: {hp_upgrade_level}/10")
rendered_strength_upgrade_level_text = TextRender(None, 50, (255, 255, 255), f"Level: {strength_upgrade_level}/10")
rendered_lives_rate_upgrade_level_text = TextRender(None, 50, (255, 255, 255), f"Level: {lives_rate_upgrade_level}/10")
rendered_hp_required_xp_text = TextRender(None, 30, (44, 59, 64), f"{hp_required_xp}")
rendered_strength_required_xp_text = TextRender(None, 30, (44, 59, 64), f"{strength_required_xp}")
rendered_lives_rate_required_xp_text = TextRender(None, 30, (44, 59, 64), f"{lives_rate_required_xp}")

back_arrow = StillImage(5, 10, 90, 90, "back_arrow.png")

benefits = []
for i in range(3):
    benefit = StillImage(62 + (i * 250), 470, 175, 175, "benefits_button.png")
    benefits.append(benefit)

def upgrade_menu(window):

    mouse_x, mouse_y = mouse.get_pos()

    background.draw(window)

    back_arrow.draw(window)
    
    window.blit(overlay1, rect1.topleft)
    window.blit(overlay2, rect2.topleft)
    window.blit(overlay3, rect3.topleft)

    rendered_total_xp_text.draw(window, (615, 10))

    rendered_hp_text.draw(window, (350, 330))
    rendered_strength_text.draw(window, (70, 330))
    rendered_lives_rate.draw(window, (565, 330))
    rendered_hp_num.draw(window, (400, 325))
    rendered_strength_num.draw(window, (177, 325))
    rendered_lives_rate_num.draw(window, (612, 360))

    strength_icon.draw(window)
    hp_icon.draw(window)
    lives_rate_icon.draw(window)

    for benefit in benefits:
        benefit.draw(window)

    rendered_hp_upgrade_level_text.draw(window, (310, 430))
    rendered_strength_upgrade_level_text.draw(window, (60, 430))
    rendered_lives_rate_upgrade_level_text.draw(window, (560, 430))

    rendered_hp_required_xp_text.draw(window, (409, 549))
    rendered_strength_required_xp_text.draw(window, (159, 549))
    rendered_lives_rate_required_xp_text.draw(window, (659, 549)) 

    if (mouse_x >= back_arrow.rect.x and mouse_x <= back_arrow.rect.x + back_arrow.rect.width and mouse_y >= back_arrow.rect.y and mouse_y <= back_arrow.rect.y + back_arrow.rect.height):
            if mouse.get_pressed()[0]:
                global click_cooldown
                click_cooldown = True
                return False

    return True

playAgian = Buttons(100, 200, 600, 600, "play_again_button.png", "playAgain")

home = Buttons(100, 380, 600, 600, "home_button.png", "home")
rendered_game_over = TextRender(None, 150, (255, 0, 0), "Game Over...")

with open ("highscore.txt", 'r') as file:
    lines = file.readlines()
    numbers = [int(line.strip()) for line in lines if line.strip().isdigit()]
highscore = max(numbers) if numbers else 0
rendered_highscore = TextRender(None, 50, (255, 255, 255), f"High Score: {highscore}")

pause_box = StillImage(-5, -30, 800, 900, "pause_box.png")
continue_gameplay = Buttons(200, 130, 400, 400, "continue_button.png", "continue_gameplay")
pause_view_quests = Buttons(200, 220, 400, 400, "view_quests_button.png", "view_quests")
exit_gameplay = Buttons(200, 310, 400, 400, "exit_gameplay_button.png", "exit_gameplay")

view_quests = False

def pause_screen(window):
    global is_selected, last_move, move_delay, home, scroll_y, view_quests

    if is_selected not in ("continue_gameplay", "view_quests", "exit_gameplay"):
        is_selected = "continue_gameplay"

    pause_box.draw(window)
    if not view_quests:
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

            view_quests = True

    if view_quests:

        pause_box.draw(window)

        scale_factor = 0.80
        base_x = 145
        base_y = 291
        box_height = int(80 * scale_factor)
        box_width = int(630 * scale_factor)
        font_scale = int(50 * scale_factor)
        detail_font_scale = int(30 * scale_factor)
        rewards_font_scale = int(40 * scale_factor)

        pause_TOP_LIMIT = 290
        pause_BOTTOM_LIMIT = 525

        quest_title_mapping = []
        for idx, (quest_id, quest) in enumerate(quests.items()):
            completed_levels = [i for i, done in enumerate(quest["isCompleted"]) if done]
            unlocked_level = max(completed_levels, default=-1) + 1
            for level_index in range(len(quest["title"])):
                quest_title_mapping.append((quest_id, level_index, level_index > unlocked_level))

        max_scroll = max((len(quest_title_mapping)* 80 - (window.get_height() - pause_TOP_LIMIT), 0)) + 50
        
        for i, (quest_id, level_index, is_locked) in enumerate(quest_title_mapping):

            spacing = 10
            y_offset = base_y + i * (box_height + spacing) + scroll_y
        
            quest = quests[quest_id]

            adjusted_box = Rect(base_x, y_offset - 10, box_width, box_height)

            if y_offset > pause_TOP_LIMIT and y_offset < pause_BOTTOM_LIMIT:

                if is_locked:
                    small_padlock = transform.scale(padlock.image, (int(60 * scale_factor), int(60 * scale_factor)))
                    window.blit(small_padlock, (475, adjusted_box.y + 10))

                title_font = font.SysFont(None, font_scale)
                detail_font = font.SysFont(None, detail_font_scale)
                rewards_font = font.SysFont(None, rewards_font_scale)

                rendered_quest_title = title_font.render(quest["title"][level_index], True, (255, 255, 255))
                rendered_quest_detail = detail_font.render(quest["details"][level_index], True, (200, 200, 200))
                
                xp_amount = quest["reward"]["xp"][level_index]
                rendered_quest_rewards = rewards_font.render(f"{xp_amount} XP", True, (212, 148, 11))

                if quest["isCompleted"][level_index]:
                    s = Surface((box_width, box_height), SRCALPHA)
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
                        s = Surface((box_width, box_height), SRCALPHA)
                        s.fill((166, 41, 3, 100))
                        window.blit(s, (adjusted_box.x, adjusted_box.y))

                draw.rect(window, (135, 84, 3), adjusted_box, width=2)

                window.blit(rendered_quest_title, (adjusted_box.x + 10, y_offset + 5))
                window.blit(rendered_quest_detail, (adjusted_box.x + 15, y_offset + int(box_height / 2)))
                window.blit(rendered_quest_rewards, (adjusted_box.x + box_width - 120, y_offset + 10))

        for e in event.get():
            if e.type == QUIT:
                exit()

            elif e.type == MOUSEWHEEL:
                scroll_y += e.y * scroll_speed
                scroll_y = max(min(scroll_y, 0), -max_scroll)
            
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                view_quests = False     
                is_selected = "continue_gameplay"
                return True, False

    return paused_game, is_home

def game_over(window):
    global is_selected, move_delay, last_move, instructions_open

    if is_selected not in ("playAgain", "home"):
        is_selected = "playAgain"

    background.draw(window)
    playAgian.draw(window, is_selected)
    home.draw(window, is_selected)
    rendered_game_over.draw(window, (45, 50))
    rendered_highscore.draw(window, (255, 250))

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