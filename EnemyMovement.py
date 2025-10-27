from pygame import *
from AnimatedSprite import *
from StillImage import StillImage
import random

class Enemy(AnimatedSprite):

    def __init__(self, sprite_sheet, x, y, w, h):
        super().__init__(sprite_sheet, x, y, w, h)

        self.hp = 50
        self.strenght = 5
        self.dead = False

    def spawn(self):
        
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

        self.change_animation("Skeleton_Spearman/Run.png", 128, 128)

    def move(self, player_x):

        if self.direction == "right" and not getattr(self, "attacking", False):
             
            if player_x + 100 < self.rect.x:
                self.direction = "left"
                self.rect.x -= 2
                if not getattr(self, 'attacking', False):
                    self.change_animation("Skeleton_Spearman/Run.png", 128, 128)
            else:
                self.rect.x += 2
                if not getattr(self, 'attacking', False):
                    self.change_animation("Skeleton_Spearman/Run.png", 128, 128)
        
        if self.direction == "left" and not getattr(self, "attacking", False):

            if player_x - 100 > self.rect.x:
                self.direction = "right"
                self.rect.x += 2
                if not getattr(self, 'attacking', False):
                    self.change_animation("Skeleton_Spearman/Run.png", 128, 128)
            else:
                self.rect.x -= 2
                if not getattr(self, 'attacking', False):
                    self.change_animation("Skeleton_Spearman/Run.png", 128, 128)
            
    def attack(self):
        
        self.attacking = True
        attack_type = random.randint(1, 2)
        if attack_type == 1:
            self.change_animation("Skeleton_Spearman/Attack_1.png", 128, 128, play_once=True)
        else:
            self.change_animation("Skeleton_Spearman/Attack_2.png", 128, 128, play_once=True)

    def update(self):

        if getattr(self, 'hp', 0) <= 0 and not getattr(self, 'dead', False):
            self.die()

        if getattr(self, 'attacking', False) and getattr(self, 'play_once_done', False):
            self.attacking = False
            self.play_once = False
            self.play_once_done = False
            try:
                self.change_animation("Skeleton_Spearman/Run.png", 128, 128)
            except Exception:
                pass

        if getattr(self, 'dead', False) and getattr(self, 'play_once_done', False):

            self.play_once = False
            self.play_once_done = False
            self.remove = True
            return

    def die(self):
        if getattr(self, 'dead', False):
            return
        self.dead = True
        self.attacking = False
        self.play_once = True
        self.play_once_done = False
        self.death_timer = 0

        try:
            self.change_animation(f"Skeleton_Spearman/Dead.png", 128, 128, play_once=True)
        except Exception:
            pass
        try:
            if getattr(self, 'scale_w', None) is not None:
                self.resize(self.scale_w, self.scale_h)
        except Exception:
            pass