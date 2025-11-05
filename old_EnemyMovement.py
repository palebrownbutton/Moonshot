from pygame import *
from AnimatedSprite import *
from StillImage import StillImage
import random
import math
import math as pymath

arrows = []
can_shoot = False

class Enemy(AnimatedSprite):

    def __init__(self, sprite_sheet, x, y, w, h, enemy_type, hp):
        super().__init__(sprite_sheet, x, y, w, h)

        self.hp = hp
        self.dead = False

    def spawn(self, enemy_type, hp):

        self.resize(200, 200)
        
        side = random.choice(["left", "right"]) 
        if side == "left":
            self.rect.x = random.randint(-600, -200)
            self.direction = "right"
        else:
            self.rect.x = random.randint(670, 1070)
            self.direction = "left"

        self.hp = hp
        self.dead = False
        self.attacking = False
        self.play_once = False
        self.play_once_done = False
        self.death_timer = 0

        try:
            self.change_animation(f"{enemy_type}/Run.png", 128, 128)
        except Exception:
            pass

    def update(self, enemy_type):

        if getattr(self, 'hp', 0) <= 0 and not getattr(self, 'dead', False):
            self.die(enemy_type)

        if getattr(self, 'attacking', False) and getattr(self, 'play_once_done', False):
            self.attacking = False
            self.play_once = False
            self.play_once_done = False
            try:
                self.change_animation(f"{enemy_type}/Run.png", 128, 128)
            except Exception:
                pass

        if getattr(self, 'dead', False) and getattr(self, 'play_once_done', False):
            self.play_once = False
            self.play_once_done = False
            self.remove = True
            return

    def get_hitbox(self):
        """Return a consistent 128x128 hitbox for small enemies, centered
        horizontally on the enemy's rect and aligned to its top.
        """
        hb_w = 128
        hb_h = 128
        hb_x = self.rect.centerx - hb_w // 2
        hb_y = self.rect.y
        return Rect(hb_x, hb_y, hb_w, hb_h)

    def die(self, enemy_type):

        if getattr(self, 'dead', False):
            return

        self.hp = max(0, self.hp)

        self.dead = True
        self.attacking = False
        self.play_once = True
        self.play_once_done = False
        self.death_timer = 0

        try:
            self.change_animation(f"{enemy_type}/Dead.png", 128, 128, play_once=True)
        except Exception:
            pass
        try:
            if getattr(self, 'scale_w', None) is not None:
                self.resize(self.scale_w, self.scale_h)
        except Exception:
            pass

class Skeleton(Enemy):

    def __init__(self, sprite_sheet, x, y, w, h, enemy_type, hp=50):
        super().__init__(sprite_sheet, x, y, w, h, enemy_type, hp)

    def move(self, player_x, enemy_type):

        if self.direction == "right" and not getattr(self, "attacking", False):
            if player_x + 100 < self.rect.x:
                self.direction = "left"
                self.rect.x -= 2
                if not getattr(self, 'attacking', False):
                    try:
                        self.change_animation(f"{enemy_type}/Run.png", 128, 128)
                    except Exception:
                        pass
            else:
                self.rect.x += 2
                if not getattr(self, 'attacking', False):
                    try:
                        self.change_animation(f"{enemy_type}/Run.png", 128, 128)
                    except Exception:
                        pass
        
        if self.direction == "left" and not getattr(self, "attacking", False):

            if player_x - 100 > self.rect.x:
                self.direction = "right"
                self.rect.x += 2
                if not getattr(self, 'attacking', False):
                    try:
                        self.change_animation(f"{enemy_type}/Run.png", 128, 128)
                    except Exception:
                        pass
            else:
                self.rect.x -= 2
                if not getattr(self, 'attacking', False):
                    try:
                        self.change_animation(f"{enemy_type}/Run.png", 128, 128)
                    except Exception:
                        pass
                
    def attack(self, enemy_type):
        
        self.attacking = True
        attack_type = random.randint(1, 2)
        if attack_type == 1:
            try:
                self.change_animation(f"{enemy_type}/Attack_1.png", 128, 128, play_once=True)
            except Exception:
                pass
        else:
            try:
                self.change_animation(f"{enemy_type}/Attack_2.png", 128, 128, play_once=True)
            except Exception:
                pass

class BossSkeleton(Enemy):

    def __init__(self, sprite_sheet, x, y, w, h, enemy_type, hp=150):
        super().__init__(sprite_sheet, x, y, w, h, enemy_type, hp)

    def move(self, player_x):

        if getattr(self, "attacking", False):
            return 

        attack_range = 170  

        if self.rect.centerx < player_x - attack_range:
            self.rect.x += 2
            self.direction = "right"
            try:
                self.change_animation("Skeleton_Spearman/Run.png", 128, 128)
            except Exception:
                pass
        elif self.rect.centerx > player_x + attack_range:
            self.rect.x -= 2
            self.direction = "left"
            try:
                self.change_animation("Skeleton_Spearman/Run.png", 128, 128)
            except Exception:
                pass
        else:
            self.attack()

    def attack(self):
        
        self.attacking = True
        try:
            self.change_animation("Skeleton_Spearman/Attack_1.png", 128, 128, play_once=True)
        except Exception:
            pass

    def get_hitbox(self):

        hb_w = 400
        hb_h = 400
        hb_x = self.rect.centerx - hb_w // 2
        hb_y = self.rect.y
        return Rect(hb_x, hb_y, hb_w, hb_h)

class Archer(Enemy):

    def __init__(self, sprite_sheet, x, y, w, h, enemy_type, hp=80):
        super().__init__(sprite_sheet, x, y, w, h, enemy_type, hp)

        self.shoot_cooldown = 0
        self.arrow_timer = None
        self.arrow_fired = False

    def move(self, player_x, enemy_type):
        global can_shoot

        if getattr(self, 'attacking', False):
            return

        STOP_DISTANCE = 320

        if self.rect.x < -75:
            self.rect.x += 2
            try:
                self.change_animation(f"{enemy_type}/Run.png", 128, 128)
            except Exception:
                pass
            return
        if self.rect.x > 880:
            self.rect.x -= 2
            try:
                self.change_animation(f"{enemy_type}/Run.png", 128, 128)
            except Exception:
                pass
            return

        dist = abs(self.rect.x - player_x)

        if dist > STOP_DISTANCE:
            if self.rect.x < player_x:
                self.rect.x += 2
                self.direction = 'right'
            else:
                self.rect.x -= 2
                self.direction = 'left'
            try:
                self.change_animation(f"{enemy_type}/Run.png", 128, 128)
            except Exception:
                pass
            return
        
        if self.rect.x < player_x:
            self.direction = 'right'
        else:
            self.direction = 'left'

        try:
            self.change_animation(f"{enemy_type}/Run.png", 128, 128)
        except Exception:
            pass
        
    def attack(self, enemy_type):
        global arrows

        # start the attack animation and schedule an arrow spawn in update()
        self.attacking = True
        self.arrow_fired = False
        self.arrow_timer = time.get_ticks() + 400
        # allow a caller (main) to set a target position by setting
        # self.target_pos before the timer expires
        self.target_pos = getattr(self, 'target_pos', None)
        try:
            self.change_animation(f"{enemy_type}/Shot_1.png", 128, 128, play_once=True)
        except Exception:
            pass
    
    def update(self, enemy_type):
        super().update(enemy_type)

        # Fire the arrow when the scheduled time arrives
        if self.attacking and not getattr(self, 'arrow_fired', False) and getattr(self, 'arrow_timer', None) and time.get_ticks() >= self.arrow_timer:
            arrow_w = 83
            arrow_h = 100
            if self.direction == 'right':
                spawn_x = self.rect.right - 10
            else:
                spawn_x = self.rect.left - arrow_w + 10
            spawn_y = self.rect.y + 90
            arrow = Arrows(spawn_x, spawn_y, arrow_w, arrow_h, "arrow.png", direction=self.direction, target_pos=getattr(self, 'target_pos', None))
            arrows.append(arrow)
            self.arrow_fired = True
            self.arrow_fired = True

class BossArcher(Enemy):

    def __init__(self, sprite_sheet, x, y, w, h, enemy_type, hp=250):
        super().__init__(sprite_sheet, x, y, w, h, enemy_type, hp)

    def move(self, player_x):
        global can_shoot

        if getattr(self, 'attacking', False):
            return

        STOP_DISTANCE = 150

        if self.rect.x < -75:
            self.rect.x += 2
            try:
                self.change_animation("Skeleton_Archer/Run.png", 128, 128)
            except Exception:
                pass
            return
        if self.rect.x > 880:
            self.rect.x -= 2
            try:
                self.change_animation("Skeleton_Archer/Run.png", 128, 128)
            except Exception:
                pass
            return

        dist = abs(self.rect.x - player_x)

        if dist > STOP_DISTANCE:
            if self.rect.x < player_x:
                self.rect.x += 2
                self.direction = 'right'
            else:
                self.rect.x -= 2
                self.direction = 'left'
            try:
                self.change_animation("Skeleton_Archer/Run.png", 128, 128)
            except Exception:
                pass
            return
        
        if self.rect.x < player_x:
            self.direction = 'right'
        else:
            self.direction = 'left'

        try:
            self.change_animation("Skeleton_Archer/Run.png", 128, 128)
        except Exception:
            pass

    def attack(self):
        global arrows

        self.attacking = True
        self.arrow_fired = False  
        self.arrow_timer = time.get_ticks() 
        try:
            self.change_animation("Skeleton_Archer/Shot_1.png", 128, 128, play_once=True)
        except Exception:
            pass

    def update(self, enemy_type, knight):
        super().update(enemy_type)
    
        if self.attacking and not self.arrow_fired and self.arrow_timer and time.get_ticks() >= self.arrow_timer:            
            arrow = Arrows(self.rect.x + 50, self.rect.y + 65, 83, 100, "arrow.png", direction=self.direction, target_pos=(knight.rect.centerx, knight.rect.centery))
            arrows.append(arrow)
            self.arrow_fired = True

    def get_hitbox(self):

        hb_w = 400
        hb_h = 400
        hb_x = self.rect.centerx - hb_w // 2
        hb_y = self.rect.y
        return Rect(hb_x, hb_y, hb_w, hb_h)

class Arrows(StillImage):

    def __init__(self, x, y, w, h, filename, direction, target_pos):
        super().__init__(x, y, w, h, filename)

        self.direction = direction
        self.original_image = image.load(filename).convert_alpha()

        speed = 12

        if target_pos is not None:

            target_x, target_y = target_pos[0], target_pos[1] - 70

            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            dist = pymath.hypot(dx, dy)
            if dist == 0:
                dist = 1

            self.vel_x = dx / dist * speed
            self.vel_y = dy / dist * speed

            angle = pymath.degrees(pymath.atan2(dy, dx))
            self.image = transform.rotate(self.original_image, -angle)

            if self.direction == "right":
                rotated = transform.rotate(self.original_image, -angle)

            else:
                self.rect.x -= 400
                flipped = transform.flip(self.original_image, True, False)
                rotated = transform.rotate(flipped, -angle)

            self.image = rotated

        else:

            self.vel_x = speed if direction == "right" else -speed
            self.vel_y = 0
            if self.direction == "right":
                self.image = transform.flip(self.original_image, True, False)
            else:
                self.image = self.original_image

        if self.direction == "right":
            self.image = transform.rotate(self.image, 180)

    def update(self):
        
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        return (self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 800)
    
    def get_hitbox(self):

        hb_w = 400
        hb_h = 100
        hb_x = self.rect.centerx - hb_w // 2
        hb_y = self.rect.y
        return Rect(hb_x, hb_y, hb_w, hb_h)
    
class Healthbars():

    def __init__(self, x, y, w, h):
        
        self.rect = Rect(x, y, w, h)

    def draw(self, window):
        
        draw.rect(window, (201, 2, 2), self.rect)
        fill_rect = Rect(self.rect.x, self.rect.y, self.fill_width, self.rect.h)
        draw.rect(window, (1, 145, 28), fill_rect)
        draw.rect(window, (0, 0, 0), self.rect, 2)

    def update(self, enemy_hp, enemy_x, enemy_y, max_enemy_hp):

        fill_portion = max(0, min(1, enemy_hp / max_enemy_hp))
        self.fill_width = int(self.rect.w * fill_portion)
        self.rect.x = enemy_x + 75
        self.rect.y = enemy_y + 90
