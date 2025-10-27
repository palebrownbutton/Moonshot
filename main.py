from pygame import *
import random
from AnimatedSprite import *
from StillImage import StillImage
from KnightMovement import Knight
from CharacterSelect import *
import StartScreen
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

skeletons = []
max_skeletons = 3
for i in range(max_skeletons):
    skelton = Enemy("Skeleton_Spearman/Idle.png", -200, 590, 128, 128)
    skelton.spawn()
    skelton.resize(200, 200)
    skeletons.append(skelton)

archers = []
max_archers = 2
for i in range(max_archers):
    pass

background = StillImage(0, 0, 800, 800, "background1.png")

def game_reset():
    global knight, character, skeletons, prev_space, prev_down, ignore_return, scorenum, max_skeletons, hearts, lives

    knight = Knight("Knight_1/Idle.png", 350, 590, 128, 128, "Knight_1")
    knight.resize(200, 200)
    character = None
    prev_space = False
    prev_down = False
    ignore_return = False
    scorenum = 0

    skeletons = []
    max_skeletons = 3
    for i in range(max_skeletons):
        skelton = Enemy("Skeleton_Spearman/Idle.png", -200, 590, 128, 128)
        skelton.spawn()
        skelton.resize(200, 200)
        skeletons.append(skelton)

    lives = 5
    hearts = []
    xheart = 135
    for i in range(5):
        heart = StillImage(xheart, 0, 45, 45, "hearts.png")
        hearts.append(heart)
        xheart += 50

is_home = True

lives_image = StillImage(5, -40, 128, 128, "lives.png")
lives = 5
hearts = []
xheart = 135
for i in range(5):
    heart = StillImage(xheart, 0, 45, 45, "hearts.png")
    hearts.append(heart)
    xheart += 50

scorenum = 0
scorenumtxt = font.SysFont("Arial", 45)
scorepic = StillImage(0, 10, 140, 140, "score.png")

spawn_cooldown = 20000
last_spawn_time = time.get_ticks()

while True:

    for e in event.get():
        if e.type == QUIT:
            exit()

    if is_home == True or StartScreen.instructions_open == True:

        is_home = StartScreen.start_screen(window)
        if is_home == False and StartScreen.instructions_open == False:
            ignore_return = True
        
    else:
    
        if character == None:
            pressed_any = key.get_pressed()
            if ignore_return and not pressed_any[K_RETURN]:
                ignore_return = False
            character = select_character(window, ignore_return)
        else:

            current_time = time.get_ticks()

            if current_time - last_spawn_time > 20000:
                last_spawn_time = current_time
                max_skeletons += 1
                skelton = Enemy("Skeleton_Spearman/Idle.png", -200, 590, 128, 128)
                skelton.spawn()
                skelton.resize(200, 200)
                skeletons.append(skelton)

            if current_time - last_spawn_time > 90000:

                pass
                # once we get the spaceships to work add spereate section here
                # however i'm now thinking that maybe archer skeltons would be cooler

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

                    for skeleton in skeletons:
                        if skeleton.rect.x < knight.rect.x:
                            distance = knight.rect.x - skeleton.rect.x
                        else:
                            distance = skeleton.rect.x - knight.rect.x

                        if knight.rect.colliderect(skeleton.rect) >= distance:
                            
                            skeleton.hp -= 20 
                            if skeleton.hp <= 0:
                                scorenum += 100
                                skeleton.die()
                                skeletons.remove(skeleton)

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
            scorepic.draw(window)
            font.rendered_score = scorenumtxt.render(f"{scorenum}", True, (3, 41, 153))
            window.blit(font.rendered_score, (135, 53 ))
            
            for heart in hearts:
                heart.draw(window)
            
            for skeleton in skeletons:
                
                skeleton.update()
                skeleton.draw(window)
                skeleton.resize(200, 200)

                if skeleton.rect.x < knight.rect.x:
                    distance = (knight.rect.x - skeleton.rect.x) - 30
                else:
                    distance = skeleton.rect.x - knight.rect.x

                if distance <= 60:
            
                    if not getattr(skeleton, 'attacking', False):
                        skeleton.attack()
                        skeleton.resize(200, 200)

                    if getattr(skeleton, 'attacking', False) and not getattr(skeleton, 'play_once_done', False):
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

                    if getattr(skeleton, 'play_once_done', False):
                        knight.took_damage = False
                
                else:
                    skeleton.move(knight.rect.centerx)

            if getattr(knight, 'dead', False) and getattr(knight, 'play_once_done', False):
                ignore_return = True
                is_home = None
                StartScreen.ignore_return_local = True
                StartScreen.ignore_until = time.get_ticks() + 300
                is_home = StartScreen.game_over(window)
                if is_home != None and not is_home:
                    game_reset()
            
            if len(skeletons) == 0:
                for i in range(max_skeletons - 2):
                    skelton = Enemy("Skeleton_Spearman/Idle.png", -200, 590, 128, 128)
                    skelton.spawn()
                    skelton.resize(200, 200)
                    skeletons.append(skelton)

    display.update()
    clock.tick(60)

