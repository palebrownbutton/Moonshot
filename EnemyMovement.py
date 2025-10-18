from pygame import *
from AnimatedSprite import *
from StillImage import StillImage
import random

class Enemy(AnimatedSprite):

    def __init__(self, sprite_sheet, x, y, w, h):
        super().__init__(sprite_sheet, x, y, w, h)

        self.hp = 50
        self.strenght = 5

    def spawn(self):
        
        side = random.choice(["left", "right"])
        if side == "left":
            self.rect.x = random.randint(-600, -200)
            self.direction = "right"
        else:
            self.rect.x = random.randint(670, 1070)
            self.direction = "left"
        self.rect.y = 590

    def move(self, player_x):

        if self.direction == "right":
             
            self.rect.x += 2
            if not getattr(self, 'attacking', False):
                self.change_animation("Skeleton_Spearman/Run.png", 128, 128)
        
        if self.direction == "left":

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
       
        if getattr(self, 'attacking', False) and getattr(self, 'play_once_done', False):
            self.attacking = False
            self.play_once = False
            self.play_once_done = False
            self.change_animation("Skeleton_Spearman/Run.png", 128, 128)
