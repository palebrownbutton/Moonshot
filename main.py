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

home = True

while True:

    for e in event.get():
        if e.type == QUIT:
            exit()

    if home == True:

        home = start_screen(window)
        if home == False:
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

            prev_space = current_space

            if pressed_keys[K_UP] and knight.on_ground:
                knight.jump(character)
                knight.resize(200, 200)
                moved = True

            down = pressed_keys[K_DOWN]
            if down and not prev_down and knight.on_ground:
                knight.defend_start(character)
                knight.resize(200, 200)
            if not down and prev_down:
                knight.defend_stop(character)
                knight.resize(200, 200)

            if not moved and knight.on_ground and not knight.attacking and not knight.defending:
                knight.change_animation(f"{character}/Idle.png", 128, 128)
                knight.resize(200, 200)
            prev_down = down

            knight.update()
            window.fill((0, 0, 0))
            background.draw(window)
            knight.draw(window)

            for enemy in enemies:
                enemy.move(knight.rect.x)
                enemy.draw(window)
                enemy.resize(200, 200)
                enemy.update()

                if enemy.rect.colliderect(knight.rect):
                    
                    if not getattr(enemy, 'attacking', False):
                        enemy.attack()
                        enemy.resize(200, 200)

    display.update()
    clock.tick(60)
