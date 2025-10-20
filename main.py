from pygame import *
import random
from AnimatedSprite import *
from StillImage import StillImage
from KnightMovement import Knight
from CharacterSelect import *
from StartScreen import *
from EnemyMovement import *

init()
font.init()

window = display.set_mode((800, 800))
clock = time.Clock()

knight = Knight("Knight_1/Idle.png", 350, 590, 128, 128, "Knight_1")
knight.resize(200, 200)
character = None
prev_space = False
prev_down = False
prev_left = False
prev_right = False
ignore_return = False

enemies = []
for i in range(3):
    enemy = Enemy("Skeleton_Spearman/Idle.png", -200, 590, 128, 128)
    enemy.spawn()
    enemy.resize(200, 200)
    enemies.append(enemy)

background = StillImage(0, 0, 800, 800, "background1.png")

def game_reset():
    global knight, character, enemies, prev_space, prev_down, ignore_return

    knight = Knight("Knight_1/Idle.png", 350, 590, 128, 128, "Knight_1")
    knight.resize(200, 200)
    character = None
    prev_space = False
    prev_down = False
    ignore_return = False

    enemies = []
    for i in range(3):
        enemy = Enemy("Skeleton_Spearman/Idle.png", -200, 590, 128, 128)
        enemy.spawn()
        enemy.resize(200, 200)
        enemies.append(enemy)

is_home = True

lives_image = StillImage(5, -40, 128, 128, "lives.png")
lives = 5
hearts = []
xheart = 135
for i in range(5):
    heart = StillImage(xheart, 0, 45, 45, "hearts.png")
    hearts.append(heart)
    xheart += 50

while True:

    for e in event.get():
        if e.type == QUIT:
            exit()

    if is_home == True:

        is_home = start_screen(window)
        if is_home == False:
            ignore_return = True
        
    else:
    
        if character == None:
            pressed_any = key.get_pressed()
            if ignore_return and not pressed_any[K_RETURN]:
                ignore_return = False
            character = select_character(window, ignore_return)
        else:

            moved = False

            pressed_keys = key.get_pressed()
            current_space = pressed_keys[K_SPACE]
            left = pressed_keys[K_LEFT]
            right = pressed_keys[K_RIGHT]

            if not getattr(knight, 'dead', False):
                if current_space and not prev_space and (left or right) and knight.on_ground:
                    if left:
                        knight.direction = 'left'
                    elif right:
                        knight.direction = 'right'
                    knight.attack_moving(character)
                    knight.resize(200, 200)
                    moved = True

                else:
                    if left:
                        knight.move_left(character)
                        knight.resize(200, 200)
                        moved = True
                    elif right:
                        knight.move_right(character)
                        knight.resize(200, 200)
                        moved = True
                    elif current_space and not prev_space:
                        knight.attack_stationary(character, random.randint(1, 3))
                        knight.resize(200, 200)
                        moved = True

                if knight.attacking == True:

                    for enemy in enemies:
                        if enemy.rect.x < knight.rect.x:
                            distance = knight.rect.x - enemy.rect.x
                        else:
                            distance = enemy.rect.x - knight.rect.x

                        if knight.rect.colliderect(enemy.rect) >= distance:

                            enemy.hp -= 10 
                            if enemy.hp <= 0:
                                enemy.die()

            prev_space = current_space

            if not getattr(knight, 'dead', False) and pressed_keys[K_UP] and knight.on_ground:
                knight.jump(character)
                knight.resize(200, 200)
                moved = True

            down = pressed_keys[K_DOWN]
            if not getattr(knight, 'dead', False) and down and not prev_down and knight.on_ground:
                knight.defend_start(character)
                knight.resize(200, 200)
            if not getattr(knight, 'dead', False) and not down and prev_down:
                knight.defend_stop(character)
                knight.resize(200, 200)

            if not moved and knight.on_ground and not knight.attacking and not knight.defending and not getattr(knight, 'dead', False):
                knight.change_animation(f"{character}/Idle.png", 128, 128)
                knight.resize(200, 200)
            prev_down = down

            knight.update()
            window.fill((0, 0, 0))
            background.draw(window)
            knight.draw(window)
            lives_image.draw(window)
            
            for heart in hearts:
                heart.draw(window)
            
            for enemy in enemies:
                
                enemy.update()
                enemy.draw(window)
                enemy.resize(200, 200)

                if enemy.rect.x < knight.rect.x:
                    distance = (knight.rect.x - enemy.rect.x) - 30
                else:
                    distance = enemy.rect.x - knight.rect.x

                if distance <= 60:
            
                    if not getattr(enemy, 'attacking', False):
                        enemy.attack()
                        enemy.resize(200, 200)

                    if getattr(enemy, 'attacking', False) and not getattr(enemy, 'play_once_done', False):
                        if not getattr(knight, 'took_damage', False) and not getattr(knight, 'dead', False):
                            knight.hp = max(0, knight.hp - 5)
                            knight.took_damage = True
                            try:
                                knight.change_animation(f"{character}/Hurt.png", 128, 128, play_once=True)
                            except Exception:
                                pass
                            knight.resize(200, 200)
                            if knight.hp <= 0:
                                lives -= 1
                                hearts.remove(hearts[-1])
                                knight.hp = 100
                                if lives == 0:
                                    knight.die(character)

                    if getattr(enemy, 'play_once_done', False):
                        knight.took_damage = False
                
                else:
                    enemy.move(knight.rect.x)

            if getattr(knight, 'dead', False) and getattr(knight, 'play_once_done', False):
                is_home = None
                is_home = game_over(window)
                if is_home != None and not is_home:
                    game_reset()

    display.update()
    clock.tick(60)
