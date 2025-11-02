from pygame import *
from AnimatedSprite import *
from StillImage import StillImage
import random

arrows = []
can_shoot = False

class Enemy(AnimatedSprite):

    def __init__(self, sprite_sheet, x, y, w, h, enemy_type, hp):
        super().__init__(sprite_sheet, x, y, w, h)

        self.hp = hp
        self.strenght = 5
        self.dead = False

    def spawn(self, enemy_type):

        self.resize(200, 200)
        
        side = random.choice(["left", "right"]) 
        if side == "left":
            self.rect.x = random.randint(-600, -200)
            self.direction = "right"
        else:
            self.rect.x = random.randint(670, 1070)
            self.direction = "left"

        self.hp = 60
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

    def die(self, enemy_type):
        if getattr(self, 'dead', False):
            return
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

class Archer(Enemy):

    def __init__(self, sprite_sheet, x, y, w, h, enemy_type, hp=80):
        super().__init__(sprite_sheet, x, y, w, h, enemy_type, hp)

        self.shoot_cooldown = 0

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

        self.attacking = True
        try:
            self.change_animation(f"{enemy_type}/Shot_1.png", 128, 128, play_once=True)
        except Exception:
            pass

        arrow = Arrows(self.rect.x + 50, self.rect.y + 90, 83, 100, "arrow.png", direction=self.direction)
        arrows.append(arrow)

class Arrows(StillImage):

    def __init__(self, x, y, w, h, filename, direction='right'):
        super().__init__(x, y, w, h, filename)

        self.direction = direction

    def update(self):
        if getattr(self, 'direction', 'right') == "left":
            self.rect.x -= 10
        else:
            self.rect.x += 10
        return self.rect.right < 0 or self.rect.left > 800
    
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
