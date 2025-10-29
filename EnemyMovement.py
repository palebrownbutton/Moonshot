from pygame import *
from AnimatedSprite import *
from StillImage import StillImage
import random

arrows = []
can_shoot = False

class Enemy(AnimatedSprite):

    def __init__(self, sprite_sheet, x, y, w, h, enemy_type):
        super().__init__(sprite_sheet, x, y, w, h)

        self.hp = 50
        self.strenght = 5
        self.dead = False

    def spawn(self, enemy_type):
        
        side = random.choice(["left", "right"]) 
        if side == "left":
            self.rect.x = random.randint(-600, -200)
            self.direction = "right"
        else:
            self.rect.x = random.randint(670, 1070)
            self.direction = "left"
        self.rect.y = 590

        self.hp = 50
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

    def __init__(self, sprite_sheet, x, y, w, h, enemy_type):
        super().__init__(sprite_sheet, x, y, w, h, enemy_type)

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

class Archer(Enemy):

    def __init__(self, sprite_sheet, x, y, w, h, enemy_type):
        super().__init__(sprite_sheet, x, y, w, h, enemy_type)

        self.shoot_cooldown = 0

    def move(self, player_x, enemy_type):
        global can_shoot

        if getattr(self, 'attacking', False):
            return

        if self.rect.x < -75 or self.rect.x < player_x - 350:
            self.rect.x += 2
            try:
                self.change_animation(f"{enemy_type}/Run.png", 128, 128)
            except Exception:
                pass
            return

        elif self.rect.x > 800 or self.rect.x > player_x + 350:
            self.rect.x -= 1.3
            try:
                self.change_animation(f"{enemy_type}/Run.png", 128, 128)
            except Exception:
                pass
            return
        
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