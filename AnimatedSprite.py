from pygame import *

class AnimatedSprite(sprite.Sprite):

    def __init__(self, sprite_sheet, x, y, w, h, knight_number=None):
        super().__init__()

        self.direction = 'right'
        self.action = 'idle'
        self.frame_now = 0
        self.animation_time = 0
        self.frame_duration = 5

        self.change_animation(sprite_sheet, w, h)

        self.play_once = False
        self.play_once_done = False

        self.rect = self.sprite_sheet.get_rect()
        self.rect.h = h
        self.rect.w = w
        self.rect.x = x
        self.rect.y = y
        # persistent draw size (None = use raw frame size)
        self.scale_w = None
        self.scale_h = None

    def change_animation(self, sprite_sheet, w, h, play_once=False):

        new_action = sprite_sheet.split(".")[0]
        if self.action != new_action:
            self.frame_now = 0
            self.animation_time = 0
            self.action = new_action
            self.play_once = play_once
            self.play_once_done = False

        self.sprite_sheet = image.load(sprite_sheet)
        self.totalFrames = self.sprite_sheet.get_width() // w
        self.frames = []

        for i in range(self.totalFrames):
            frame_surface = Surface((w, h), SRCALPHA)
            frame_surface.blit(self.sprite_sheet, (0, 0), Rect(i * w, 0, w, h))
            self.frames.append(frame_surface)
        
        if self.direction == "left":
            self.flip()
        # If a persistent scale is set (via resize), apply it to the newly created frames
        if getattr(self, 'scale_w', None) is not None and getattr(self, 'scale_h', None) is not None:
            for i in range(len(self.frames)):
                self.frames[i] = transform.scale(self.frames[i], (self.scale_w, self.scale_h))
            # keep rect dimensions in sync with drawn size
            if hasattr(self, 'rect'):
                self.rect.w = self.scale_w
                self.rect.h = self.scale_h

    def draw(self, window):

        self.animation_time += 1
        if self.animation_time >= self.frame_duration:
            self.animation_time = 0
            if self.play_once:
                if self.frame_now < self.totalFrames - 1:
                    self.frame_now += 1
                else:
                    self.play_once_done = True
            else:
                self.frame_now = (self.frame_now + 1) % self.totalFrames

        window.blit(self.frames[self.frame_now], (self.rect.x, self.rect.y))

    def resize(self, w, h):
        # remember the requested draw size so future change_animation calls
        # will recreate frames at the source size and then scale them back
        # to this size (prevents being overridden by change_animation).
        self.scale_w = w
        self.scale_h = h
        for i in range(len(self.frames)):
            self.frames[i] = transform.scale(self.frames[i], (w, h))
        # update rect size used for positioning
        if hasattr(self, 'rect'):
            self.rect.w = w
            self.rect.h = h
    
    def flip(self):
        for i in range(len(self.frames)):
            self.frames[i] = transform.flip(self.frames[i], True, False)
            