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
used_shield = time.get_ticks()

skeletons = []
max_skeletons = 3
live_skeletons = 3
for i in range(live_skeletons):
    skelton = Skeleton("Skeleton_Spearman/Idle.png", -200, 590, 128, 128, "Skeleton_Spearman")
    skelton.spawn("Skeleton_Spearman")
    skeletons.append(skelton)

archers = []
max_archers = 2
for i in range(max_archers):
    archer = Archer("Skeleton_Archer/Idle.png", -200, 590, 128, 128, "Skeleton_Archer")
    archer.spawn("Skeleton_Archer")
    archers.append(archer)

archers_active = False

background = StillImage(0, 0, 800, 800, "background1.png")
background_switched = False

def game_reset():
    global knight, character, skeletons, prev_space, prev_down, ignore_return, scorenum, max_skeletons, live_skeletons,  hearts, lives, archers, max_archers, archers_active

    knight = Knight("Knight_1/Idle.png", 350, 590, 128, 128, "Knight_1")
    knight.resize(200, 200)
    character = None
    prev_space = False
    prev_down = False
    ignore_return = False
    scorenum = 0

    skeletons = []
    live_skeletons = 3
    max_skeletons = 3
    for i in range(live_skeletons):
        skelton = Skeleton("Skeleton_Spearman/Idle.png", -200, 590, 128, 128, "Skeleton_Spearman")
        skelton.spawn("Skeleton_Spearman")
        skeletons.append(skelton)

    archers = []
    max_archers = 2
    for i in range(max_archers):
        archer = Archer("Skeleton_Archer/Idle.png", -200, 590, 128, 128, "Skeleton_Archer")
        archer.spawn("Skeleton_Archer")
        archers.append(archer)

    try:
        arrows.clear()
    except Exception:
        pass

    archers_active = False

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

last_spawn_time = time.get_ticks()
archer_spawn_time = time.get_ticks()
game_start_time = None

while True:

    for e in event.get():
        if e.type == QUIT:
            exit()

    if is_home == True or StartScreen.instructions_open == True:

        is_home = StartScreen.start_screen(window)
        if is_home == False and StartScreen.instructions_open == False:
            ignore_return = True

            now = time.get_ticks()
            try:
                last_spawn_time = now
            except Exception:
                pass
            try:
                archer_spawn_time = now
            except Exception:
                pass
            try:
                game_start_time = now
            except Exception:
                pass
            try:
                archers_active = False
            except Exception:
                pass
            try:
                arrows.clear()
            except Exception:
                pass
        
    else:
    
        if character == None:
            pressed_any = key.get_pressed()
            if ignore_return and not pressed_any[K_RETURN]:
                ignore_return = False
            character = select_character(window, ignore_return)
        else:

            current_time = time.get_ticks()

            if current_time - last_spawn_time > 20000 and len(skeletons) <= 6:
                last_spawn_time = current_time
                live_skeletons += 1
                max_skeletons += 1
                for i in range(max_skeletons - live_skeletons + 1):
                    if len(skeletons) <= 6:
                        skelton = Skeleton("Skeleton_Spearman/Idle.png", -200, 590, 128, 128, "Skeleton_Spearman")
                        skelton.spawn("Skeleton_Spearman")
                        skeletons.append(skelton)
                    else:
                        break

            if game_start_time is not None and current_time - game_start_time > 30000:

                if not background_switched:
                    background = StillImage(0, 0, 800, 800, "background2.png")
                    background_switched = True
                archers_active = True
            
                if current_time - archer_spawn_time > 45000 and len(archers) <= 4:
                    archer_spawn_time = current_time
                    max_archers += 1
                    for i in range(max_archers - 1):
                        if len(archers) <= 4:
                            archer = Archer("Skeleton_Archer/Idle.png", -200, 590, 128, 128, "Archer_Spearman")
                            archer.spawn("Skeleton_Archer")
                            archers.append(archer)
                        else:
                            break

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
                                skeleton.die("Skeleton_Spearman")
                                skeletons.remove(skeleton)
                                live_skeletons -= 1

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
          
            if archers_active:
                for archer in archers:
                    archer.update("Skeleton_Archer")
                    archer.move(knight.rect.centerx, "Skeleton_Archer")
                    archer.draw(window)

                    shoot_current_time = time.get_ticks()
                    if getattr(archer, 'shoot_cooldown', 0) == 0:
                        archer.shoot_cooldown = 0
                    if shoot_current_time - archer.shoot_cooldown > 3000:
                        if abs(archer.rect.x - knight.rect.centerx) <= 350:
                            archer.attack("Skeleton_Archer")
                            archer.shoot_cooldown = shoot_current_time
                
                    if archer.rect.x < knight.rect.x:
                        distance = knight.rect.x - archer.rect.x
                    else:
                        distance = archer.rect.x - knight.rect.x

                    if knight.rect.colliderect(archer.rect) >= distance:
                        
                        archer.hp -= 20 
                        if archer.hp <= 0:
                            scorenum += 250
                            archer.die("Skeleton_Archer")
                            archers.remove(archer)

            knight.draw(window)
            lives_image.draw(window)
            scorepic.draw(window)
            font.rendered_score = scorenumtxt.render(f"{scorenum}", True, (3, 41, 153))
            window.blit(font.rendered_score, (135, 53 ))

            for arrow in arrows:
                prev_x = arrow.rect.x
                removed = arrow.update()
                try:
                    collided = arrow.rect.inflate(20, 20).colliderect(knight.rect)
                    tunneled = (prev_x > knight.rect.right and arrow.rect.x < knight.rect.left) or (prev_x < knight.rect.left and arrow.rect.x > knight.rect.right)
                    if collided or tunneled:
                        
                        locked = False
                        try:
                            if getattr(knight, 'defending', False):
                                if getattr(knight, 'direction', None) != getattr(skeleton, 'direction', None):
                                    blocked = True
                        except Exception:
                            blocked = False

                        if not blocked:

                            knight.hp = max(0, knight.hp - 5)
                            print(knight.hp)
                            knight.took_damage = True
                            try:
                                knight.change_animation(f"{character}/Hurt.png", 128, 128, play_once=True)
                            except Exception:
                                pass
                            knight.resize(200, 200)
                            if knight.hp <= 0:
                                lives -= 1
                                try:
                                    hearts.remove(hearts[-1])
                                except Exception:
                                    pass
                                knight.hp = 100
                                if lives == 0:
                                    knight.die(character)
                            else:
                                knight.took_damage = False
                        try:
                            arrows.remove(arrow)
                        except ValueError:
                            pass
                        continue
                except Exception:
                    pass

                arrow.draw(window)
                if removed:
                    try:
                        arrows.remove(arrow)
                    except ValueError:
                        pass

            for heart in hearts:
                heart.draw(window)
            
            for skeleton in skeletons:
                
                skeleton.update("Skeleton_Spearman")
                skeleton.draw(window)

                if skeleton.rect.x < knight.rect.x:
                    distance = (knight.rect.x - skeleton.rect.x) - 30
                else:
                    distance = skeleton.rect.x - knight.rect.x

                if distance <= 60:
            
                    if not getattr(skeleton, 'attacking', False):
                        skeleton.attack("Skeleton_Spearman")

                    if getattr(skeleton, 'attacking', False) and not getattr(skeleton, 'play_once_done', False):
                        if not getattr(knight, 'took_damage', False) and not getattr(knight, 'dead', False):

                            blocked = False
                            try:
                                if getattr(knight, 'defending', False):
                                    if getattr(knight, 'direction', None) != getattr(skeleton, 'direction', None):
                                        blocked = True
                            except Exception:
                                blocked = False

                            if not blocked:

                                knight.hp = max(0, knight.hp - 5)
                                print(knight.hp)
                                knight.took_damage = True
                                try:
                                    knight.change_animation(f"{character}/Hurt.png", 128, 128, play_once=True)
                                except Exception:
                                    pass
                                knight.resize(200, 200)
                                if knight.hp <= 0:
                                    lives -= 1
                                    try:
                                        hearts.remove(hearts[-1])
                                    except Exception:
                                        pass
                                    knight.hp = 100
                                    if lives == 0:
                                        knight.die(character)
                            else:
                                knight.took_damage = False

                    if getattr(skeleton, 'play_once_done', False):
                        knight.took_damage = False
                
                else:
                    skeleton.move(knight.rect.centerx, "Skeleton_Spearman")

            if getattr(knight, 'dead', False) and getattr(knight, 'play_once_done', False):
                ignore_return = True
                is_home = None
                StartScreen.ignore_return_local = True
                StartScreen.ignore_until = time.get_ticks() + 300
                is_home = StartScreen.game_over(window)
                if is_home != None and not is_home:
                    game_reset()
            
            if len(skeletons) == 0:
                live_skeletons = max_skeletons
                for i in range(max_skeletons):
                    skelton = Skeleton("Skeleton_Spearman/Idle.png", -200, 590, 128, 128, "Skeleton_Spearman")
                    skelton.spawn("Skeleton_Spearman")
                    skeletons.append(skelton)
            if max_skeletons > 6:
                max_skeletons = 6
            while len(skeletons) > max_skeletons:
                try:
                    skeletons.pop()
                    live_skeletons = max(0, live_skeletons - 1)
                except Exception:
                    break

            if len(archers) == 0:
                archer = Archer("Skeleton_Archer/Idle.png", -200, 590, 128, 128, "Skeleton_Archer")
                archer.spawn("Skeleton_Archer")
                archers.append(archer)
            
    display.update()
    clock.tick(60)

