from pygame import *
import random
import math
from AnimatedSprite import *
from StillImage import StillImage
from KnightMovement import Knight
from CharacterSelect import *
import StartScreen
from EnemyMovement import *
from ImageEffects import *

init()
font.init()
mixer.init()

window = display.set_mode((800, 800))
clock = time.Clock()

mixer.music.load("game_play.mp3")

wave = 1

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
    skeleton = Skeleton("Skeleton_Spearman/Idle.png", -200, 590, 128, 128, "Skeleton_Spearman")
    skeleton.spawn("Skeleton_Spearman", 60 * wave)
    skeletons.append(skeleton)

archers = []
max_archers = 2
for i in range(max_archers):
    archer = Archer("Skeleton_Archer/Idle.png", -200, 590, 128, 128, "Skeleton_Archer")
    archer.spawn("Skeleton_Archer", 65 * wave)
    archers.append(archer)

skeleton_healthbars = []
for skeleton in skeletons:
    skeleton_healthbar = Healthbars(skeleton.rect.x + 75, skeleton.rect.y + 90, 50, 7)
    skeleton_healthbars.append(skeleton_healthbar)

archer_healthbars = []
for archer in archers:
    archer_healthbar = Healthbars(archer.rect.x + 75, archer.rect.y + 90, 50, 7)
    archer_healthbars.append(archer_healthbar)

boss_skeleton = None
boss_spawned = False
boss_beat = False
boss_battle_text = image.load("boss_battle_text.png").convert_alpha()
boss_battle_text = transform.scale(boss_battle_text, (700, 700))
boss_intro_effect = WavesText(boss_battle_text, (50, 90))
boss_intro_timer = 0
boss_intro_duration = 1000

archers_active = False

background = StillImage(0, 0, 800, 800, "background1.png")
background_switched = False

def game_reset():
    global knight, character, skeletons, prev_space, prev_down, ignore_return, scorenum, max_skeletons, live_skeletons,  hearts, lives, archers, max_archers, archers_active, background, background_switched, game_start_time, highscore_written

    background = StillImage(0, 0, 800, 800, "background1.png")
    background_switched = False
    game_start_time = None

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
        skeleton = Skeleton("Skeleton_Spearman/Idle.png", -200, 590, 128, 128, "Skeleton_Spearman")
        skeleton.spawn("Skeleton_Spearman", 60 * wave)
        skeletons.append(skeleton)

    archers = []
    max_archers = 2
    for i in range(max_archers):
        archer = Archer("Skeleton_Archer/Idle.png", -200, 590, 128, 128, "Skeleton_Archer")
        archer.spawn("Skeleton_Archer", 65 * wave)
        archers.append(archer)

    try:
        arrows.clear()
    except Exception:
        pass

    try:
        collectibles.clear()
    except Exception:
        pass

    archers_active = False

    try:
        highscore_written = False
    except Exception:
        pass

    lives = 5
    hearts = []
    HEART_X_BASE = 135
    HEART_SPACING = 50
    for i in range(5):
        heart = StillImage(HEART_X_BASE + i * HEART_SPACING, 0, 45, 45, "hearts.png")
        hearts.append(heart)

is_home = True

lives_image = StillImage(5, -40, 128, 128, "lives.png")
lives = 5
hearts = []
HEART_X_BASE = 135
HEART_SPACING = 50
for i in range(5):
    heart = StillImage(HEART_X_BASE + i * HEART_SPACING, 0, 45, 45, "hearts.png")
    hearts.append(heart)

collectibles = []

scorenum = 0
scorenumtxt = font.SysFont("Arial", 45)
scorepic = StillImage(0, 10, 140, 140, "score.png")

last_spawn_time = time.get_ticks()
archer_spawn_time = time.get_ticks()
game_start_time = None
heart_spawn_time = time.get_ticks()

try:
    with open("highscore.txt", 'r') as file:
        lines = file.readlines()
        numbers = [int(line.strip()) for line in lines if line.strip().isdigit()]
    highscore = max(numbers) if numbers else 0
except Exception:
    highscore = 0

highscore_written = False

wave1_text = image.load("wave1_text.png").convert_alpha()
wave1_text = transform.scale(wave1_text, (700, 700))
wave1_intro_effect = WavesText(wave1_text, (50, 90))
wave1_intro_timer = 0
wave1_intro_duration = 1000

wave2_text = image.load("wave2_text.png").convert_alpha()
wave2_text = transform.scale(wave2_text, (700, 700))
wave2_intro_effect = WavesText(wave2_text, (50, 90))
wave2_intro_timer = 0
wave2_intro_duration = 1000

paused_game = False
esc_last = 0
esc_delay = 150

while True:

    for e in event.get():
        if e.type == QUIT:
            exit()

    dt = clock.tick(60)
    boss_intro_timer += dt

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

            pressed = key.get_pressed()
            now = time.get_ticks()
            if pressed[K_ESCAPE] and now - esc_last >= esc_delay:
                paused_game = not paused_game
                esc_last = now
            
            if paused_game:
                paused_game, is_home = StartScreen.pause_screen(window)
                display.update()
                clock.tick(60)
                if is_home:
                    is_home = True
                    paused_game = False
                    StartScreen.instructions_open = False
                    StartScreen.ignore_return_local = True
                    StartScreen.ignore_until = time.get_ticks() + 300
                    continue

            if not paused_game:

                if not mixer.music.get_busy():
                    mixer.music.set_volume(0.3)
                    mixer.music.play(-1)

                current_time = time.get_ticks()

                if current_time - heart_spawn_time > 35000 and len(hearts) < 5:
                    heart_spawn_time = current_time
                    new_heart = StillImage(random.randint(-117, 710), random.choice([600, 715]), 45, 45, "hearts.png")
                    collectibles.append({
                        'obj': new_heart,
                        'spawn': current_time
                    })

                if current_time - last_spawn_time > 20000 and len(skeletons) <= 6:
                    last_spawn_time = current_time
                    live_skeletons += 1
                    max_skeletons += 1
                    for i in range(max_skeletons - live_skeletons + 1):
                        if len(skeletons) <= 6:
                            skeleton = Skeleton("Skeleton_Spearman/Idle.png", -200, 590, 128, 128, "Skeleton_Spearman")
                            skeleton.spawn("Skeleton_Spearman", 60 * wave)
                            skeletons.append(skeleton)
                        else:
                            break
                
                if not boss_spawned and game_start_time is not None and current_time - game_start_time > 60000 and boss_beat == False:
                    boss_skeleton = BossSkeleton("Skeleton_Spearman/Idle.png", random.randint(-600, -200), 290, 256, 256, "Skeleton_Spearman")
                    boss_skeleton.spawn("Skeleton_Spearman", 200)
                    boss_skeleton.resize(500, 500)
                    boss_healthbar = Healthbars(boss_skeleton.rect.x + 75, boss_skeleton.rect.y + 100, 200, 20)
                    boss_spawned = True

                if scorenum >= 1000 and boss_beat == True:

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
                                archer.spawn("Skeleton_Archer", 65 * wave)
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

                        if not hasattr(knight, 'damage_dealt'):
                            knight.damage_dealt = False

                        for skeleton in skeletons:
                            if skeleton.rect.x < knight.rect.x:
                                distance = knight.rect.x - skeleton.rect.x
                            else:
                                distance = skeleton.rect.x - knight.rect.x

                            if knight.get_hitbox().colliderect(skeleton.rect) and not knight.damage_dealt:
                                skeleton.hp -= 20
                                knight.damage_dealt = True

                                if skeleton.hp <= 0:
                                    scorenum += 100
                                    skeleton.die("Skeleton_Spearman")

                    if getattr(knight, 'play_once_done', False) and getattr(knight, 'attacking', False):
                        knight.damage_dealt = False
                        knight.attacking = False
                        knight.play_once_done = False

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

                if not moved and knight.on_ground and not knight.attacking and not knight.defending and not getattr(knight, 'dead', False) and not getattr(knight, 'took_damage', False):
                    try:
                        knight.change_animation(f"{character}/Idle.png", 128, 128)
                        knight.resize(200, 200)
                    except Exception:
                        pass

                prev_down = down

                knight.update()
                knight_hitbox = knight.get_hitbox()

                if getattr(knight, 'play_once_done', False) and getattr(knight, 'took_damage', False) and not getattr(knight, 'dead', False):
                    knight.took_damage = False
                    knight.play_once = False
                    knight.play_once_done = False

                background.draw(window)

                if wave1_intro_effect.active and wave == 1:

                    wave1_intro_effect.update(dt)
                    wave1_intro_effect.draw(window)

                if wave2_intro_effect.active and wave == 2:

                    wave2_intro_effect.update(dt)
                    wave2_intro_effect.draw(window)
            
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

                        if knight_hitbox.colliderect(archer.rect) and getattr(knight, 'attacking', True) and not knight.damage_dealt:
                            
                            archer.hp -= 20 
                            if archer.hp <= 0:
                                scorenum += 250
                                archer.die("Skeleton_Archer")

                if boss_skeleton is not None:

                    boss_skeleton.update("Skeleton_Spearman")
                    if getattr(boss_skeleton, 'play_once_done', False) and getattr(boss_skeleton, 'attacking', False):
                        boss_skeleton.attacking = False
                        boss_skeleton.play_once_done = False

                    if not getattr(boss_skeleton, 'music_switched', False):
                        mixer.music.stop()
                        mixer.music.load("boss_fight.mp3")
                        mixer.music.set_volume(0.5)
                        mixer.music.play(-1)
                        boss_skeleton.music_switched = True

                    if boss_intro_effect.active:

                        boss_intro_effect.update(dt)
                        boss_intro_effect.draw(window)

                    else:

                        boss_skeleton.move(knight.rect.centerx)
                        boss_skeleton.draw(window)

                        if boss_skeleton.direction == "right":
                            boss_front_x = boss_skeleton.rect.right
                        else:
                            boss_front_x = boss_skeleton.rect.left

                        distance = abs(knight.rect.centerx - boss_front_x)

                        if not hasattr(boss_skeleton, 'last_attack_time'):
                            boss_skeleton.last_attack_time = 0

                        if not getattr(boss_skeleton, 'attacking', False) and distance <= 30 and current_time - boss_skeleton.last_attack_time > 1200:
                            boss_skeleton.attack()
                            boss_skeleton.damage_dealt = False
                            boss_skeleton.last_attack_time = current_time


                        if getattr(boss_skeleton, 'attacking', False):

                            if not getattr(boss_skeleton, 'play_once_done', False):
                                if not getattr(knight, 'took_damage', False) and not getattr(knight, 'dead', False):
                                    blocked = False
                                    try:
                                        if getattr(knight, 'defending', False):
                                            if getattr(knight, 'direction', None) != getattr(boss_skeleton, 'direction', None):
                                                blocked = True
                                    except Exception:
                                        blocked = False

                                    if not blocked:
                                        knight.hp = max(0, knight.hp - 20)
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
                                        boss_skeleton.damage_dealt = True

                        else:
                            boss_skeleton.attacking = False
                            boss_skeleton.play_once_done = False
                            boss_skeleton.damage_dealt = False
                            knight.took_damage = False

                    if knight.attacking == True:

                        if boss_skeleton.rect.x < knight.rect.x:
                            distance = knight.rect.x - boss_skeleton.rect.x
                        else:
                            distance = boss_skeleton.rect.x - knight.rect.x

                        if knight.get_hitbox().colliderect(boss_skeleton.rect) and not knight.damage_dealt:
                                boss_skeleton.hp -= 20
                                knight.damage_dealt = True

                                if boss_skeleton.hp <= 0:

                                    scorenum += 1000

                                    boss_skeleton.die("Skeleton_Spearman")

                                    mixer.music.stop()
                                    mixer.music.load("game_play.mp3")
                                    mixer.music.set_volume(0.3)
                                    mixer.music.play(-1)

                                    wave = 2

                    if getattr(knight, 'play_once_done', False) and getattr(knight, 'attacking', False):
                        knight.damage_dealt = False
                        knight.attacking = False
                        knight.play_once_done = False


                    if getattr(boss_skeleton, 'dead', False) and getattr(boss_skeleton, 'play_once_done', False):
                        boss_spawned = False
                        boss_beat = True
                        boss_skeleton = None


                COLLECTIBLE_LIFETIME = 10000 
                for item in collectibles[:]:
                    c = item['obj']
                    spawn = item.get('spawn', 0)
                    tick = time.get_ticks() // 500 % 2
                    if tick == 0:
                        c.draw(window)
                    else:
                        ghost_image = c.image.copy()
                        ghost_image.set_alpha(100)
                        window.blit(ghost_image, (c.rect.x, c.rect.y))

                    if c.rect.x < knight.rect.x:
                        distance = knight.rect.x - c.rect.x
                    else:
                        distance = c.rect.x - knight.rect.x

                    if knight_hitbox.colliderect(c.rect):
                        if c.rect.x == 715 and getattr(knight, 'on_ground', True):
                            continue
                        else:
                            if len(hearts) < 5:
                                new_x = HEART_X_BASE + len(hearts) * HEART_SPACING
                                heart = StillImage(new_x, 0, 45, 45, "hearts.png")
                                hearts.append(heart)
                                lives += 1
                        try:
                            collectibles.remove(item)
                        except ValueError:
                            pass
                        continue

                    if current_time - spawn > COLLECTIBLE_LIFETIME:
                        try:
                            collectibles.remove(item)
                        except ValueError:
                            pass

                knight.draw(window)
                lives_image.draw(window)
                scorepic.draw(window)
                font.rendered_score = scorenumtxt.render(f"{scorenum}", True, (3, 41, 153))
                window.blit(font.rendered_score, (135, 53 ))

                for arrow in arrows:
                    prev_x = arrow.rect.x
                    removed = arrow.update()
                    try:
                        collided = arrow.rect.inflate(20, 20).colliderect(knight_hitbox)
                        tunneled = (prev_x > knight_hitbox.right and arrow.rect.x < knight_hitbox.left) or (prev_x < knight_hitbox.left and arrow.rect.x > knight_hitbox.right)
                        if collided or tunneled:

                            blocked = False
                            try:
                                if getattr(knight, 'defending', False):
                                    if getattr(knight, 'direction', None) != getattr(arrow, 'direction', None):
                                        blocked = True
                            except Exception:
                                blocked = False

                            if not blocked:

                                knight.hp = max(0, knight.hp - 10)
                                knight.took_damage = True

                                if not getattr(knight, 'dead', False):
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

                if not boss_spawned:
                
                    for skeleton in skeletons:
                        for skeleton_healthbar in skeleton_healthbars:
                            skeleton_healthbar.update(skeleton.hp, skeleton.rect.x, skeleton.rect.y, 60)
                            skeleton_healthbar.draw(window)

                for skeleton in skeletons[:]:
                    if getattr(skeleton, 'remove', False) and getattr(skeleton, "dead", True):
                        try:
                            skeletons.remove(skeleton)
                            live_skeletons = max(0, live_skeletons - 1)
                        except Exception:
                            pass

                for archer in archers[:]:
                    if getattr(archer, 'remove', False) and getattr(archer, "dead", True):
                        try:
                            archers.remove(archer)
                        except Exception:
                            pass

                for archer in archers:
                    for archer_healthbar in archer_healthbars:
                        archer_healthbar.update(archer.hp, archer.rect.x, archer.rect.y, 80)
                        archer_healthbar.draw(window)

                if boss_skeleton is not None and not getattr(boss_skeleton, 'dead', False):
                    boss_healthbar.update(boss_skeleton.hp, boss_skeleton.rect.x + 75, boss_skeleton.rect.y + 100, 200)
                    boss_healthbar.draw(window)

                if not boss_spawned:
                
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
                    if not highscore_written:
                        try:
                            with open("highscore.txt", 'a') as file:
                                file.write("\n" + str(scorenum))
                        except Exception:
                            pass
                        highscore_written = True
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
                        skeleton = Skeleton("Skeleton_Spearman/Idle.png", -200, 590, 128, 128, "Skeleton_Spearman")
                        skeleton.spawn("Skeleton_Spearman", 60 * wave)
                        skeletons.append(skeleton)
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
                    archer.spawn("Skeleton_Archer", 65 * wave)
                    archers.append(archer)
            
    display.update()
    clock.tick(60)

