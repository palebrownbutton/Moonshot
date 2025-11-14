from pygame import *
from AnimatedSprite import *
import json

class Knight(AnimatedSprite):

    def __init__(self, sprite_sheet, x, y, w, h, knight_number):
        super().__init__(sprite_sheet, x, y, w, h)
        self.knight_number = knight_number

        with open ("upgrades.json", "r") as file:
            attributes = json.load(file)[0]

        self.velocity_y = 0
        self.on_ground = True
        self.attacking = False
        self.defending = False
        self.hp = attributes["hp"]
        self.strength = attributes["strength"]
        self.dead = False
        self.took_damage = False

    def get_hitbox(self):

        hb_w = 128
        hb_h = 128
        hb_x = self.rect.centerx - hb_w // 2
        hb_y = self.rect.y
        return Rect(hb_x, hb_y, hb_w, hb_h)

    def die(self, character):
        if getattr(self, "dead", False):
            return
        self.dead = True
        self.attacking = False
        self.defending = False
        self.play_once = True
        self.play_once_done = False

        try:
            self.change_animation(f"{character}/Dead.png", 128, 128, play_once=True)
        except Exception:
            pass
        try:
            if getattr(self, "scale_w", None) is not None:
                self.resize(self.scale_w, self.scale_h)
        except Exception:
            pass

    def update(self):
        gravity = 0.5
        self.velocity_y += gravity
        self.rect.y += self.velocity_y
        ground_level = 590

        if self.rect.y >= ground_level:
            self.rect.y = ground_level
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        if getattr(self, "attacking", False) and getattr(self, "play_once_done", False):
            self.attacking = False
            self.play_once = False
            self.play_once_done = False

    def move_left(self, knight_number):

        if self.direction != "left":
            self.direction = "left"
            self.rect.x -= 110

        if self.rect.x > -117:
            self.rect.x -= 7
        if not getattr(self, "attacking", False):
            self.change_animation(f"{knight_number}/Run.png", 128, 128)

    def move_right(self, knight_number):

        if self.direction != "right":
            self.direction = "right"
            self.rect.x += 110

        if self.rect.x < 710:
            self.rect.x += 7
        if not getattr(self, "attacking", False):
            self.change_animation(f"{knight_number}/Run.png", 128, 128)

    def jump(self, knight_number):

        if getattr(self, "attacking", False):
            self.attacking = False
            self.play_once = False
            self.play_once_done = False

        self.change_animation(f"{knight_number}/Jump.png", 128, 128)
        self.velocity_y = -10
        self.on_ground = False

    def attack_stationary(self, knight_number, attack_type):

        if getattr(self, "attacking", False):
            return

        self.change_animation(f"{knight_number}/Attack {attack_type}.png", 128, 128, play_once=True)
        self.attacking = True

    def attack_moving(self, knight_number):

        if getattr(self, "attacking", False):
            return

        self.change_animation(f"{knight_number}/Run+Attack.png", 128, 128, play_once=True)
        self.attacking = True

    def defend(self, knight_number):

        if getattr(self, "attacking", False):
            return

        self.change_animation(f"{knight_number}/Protect.png", 128, 128, play_once=True)
        self.attacking = True

    def defend_start(self, knight_number):

        if getattr(self, "attacking", False):
            return

        self.defending = True
        self.change_animation(f"{knight_number}/Protect.png", 128, 128, play_once=False)

    def defend_stop(self, knight_number):

        if not getattr(self, "defending", False):
            return

        self.defending = False
        self.change_animation(f"{knight_number}/Idle.png", 128, 128)