import pygame
import os
import random
import sys
import os

sys.path.insert(0, "UNIVERSAL FUNCTIONS/MOVE DATA")

from standData import get_stand_anim

def play_sound(directory, volume):
    sound = pygame.mixer.Sound(directory)
    sound.set_volume(volume)
    sound.play()

def clean_directory(directory):
    new_directory = []
    for item in os.listdir(directory):
        if item.endswith(".png"):
            new_directory.append(item)
    return new_directory

class FX(pygame.sprite.Sprite):
    def __init__(self, screen, type, x, y, scale, animation_cooldown, transparency, flip=False, char_stand=False):
        pygame.sprite.Sprite.__init__(self)
        # basic settings
        self.screen = screen
        self.animation_cooldown = animation_cooldown
        self.type = type
        self.scale = scale
        self.flip = flip
        self.frame_index = 0
        self.hitbox_group_index = ""
        self.sprite_list = []

        # specific actions for stand animations
        self.stand_move_anim_data = None
        self.stand_anim_action_index = 0

        # freezing frames
        self.frame_to_freeze = None
        self.freeze_duration = 0

        # looping frames
        self.frame_loop_range = None
        self.frame_loop_count = 0

        # end early
        self.end_early = False
        self.update_time = pygame.time.get_ticks()

        if char_stand == False:
            self.fx_directory = f"IMAGES/VFX/{self.type}"
        else:
            # if the vfx is a stand, get the anim_data and play the stand summon
            self.fx_directory = f"IMAGES/VFX/{char_stand}/{self.type}"
            self.stand_move_anim_data = get_stand_anim(char_stand, self.type)
            self.stand_anim_action = 0
            play_sound(f"SOUND/COMBAT/{char_stand}/stand_summon.wav", 0.1)

        # annoying ass .DStore in random directories
        cleaned_dir = clean_directory(self.fx_directory)
        for i in range(0, len(cleaned_dir)):
            # create sprite list of images and append to self.sprite_list
            img = pygame.image.load(f"{self.fx_directory}/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            img.set_alpha(transparency)
            self.sprite_list.append(img)

        self.image = self.sprite_list[self.frame_index]

        # f and curly brackets allows concentation with variables easier
        # get the rect from the image and set the center
        self.rect = self.image.get_rect()
        self.image_rect = self.rect
        self.rect.center = (x, y)

        # used to randomize barrage vfx position
        if self.type == "barrage":
            self.rect.center = ((random.randint(x - 30, x + 30)), (random.randint(y - 30, y + 30)))

    def update(self, true_scroll):
        check_if_ended = self.checkIfEnded()
        if check_if_ended != True:
            self.updateFrame()
            # move vfx for scrolling
            self.draw(true_scroll)
        return check_if_ended

    def updateFrame(self):
        self.image = self.sprite_list[self.frame_index]
        # if the vfx is a stand, iterate through the stand anim data for freeze or loop events
        if self.stand_move_anim_data != None:
            if self.stand_anim_action_index < len(self.stand_move_anim_data) and self.freeze_duration == 0:
                anim_action_data = self.stand_move_anim_data[self.stand_anim_action_index]
                # if current action is freeze, set the frame to freeze in the instance
                if anim_action_data[0] == "freeze_frame_action":
                    self.frame_to_freeze = anim_action_data[1]
                    self.freeze_duration = anim_action_data[2]
                    print(anim_action_data[0])
                # similar for looping frames here
                if anim_action_data[0] == "loop_frames_action":
                    self.frame_loop_range = [anim_action_data[2], anim_action_data[3]]
                    self.frame_loop_count = anim_action_data[1]

                self.stand_anim_action_index += 1

        if self.frame_index != self.frame_to_freeze:
            if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
                self.image_rect = self.image.get_rect()

                # align the rect of the image to the bottom right of the image's first frame
                if not self.frame_index > len(self.sprite_list) - 1:
                    if self.flip == True:
                        self.image_rect.bottomright = self.rect.bottomright
                    elif self.flip == False:
                        self.image_rect.bottomleft = self.rect.bottomleft

                # if the next action is looking a set of frames, go back to the minimum range of the loop
                self.update_time = pygame.time.get_ticks()
                if self.frame_loop_range != None and self.frame_loop_count > 0:
                    if self.frame_loop_range[1] == self.frame_index:
                        self.frame_index = self.frame_loop_range[0] - 1
                        self.frame_loop_count -= 1
                self.frame_index += 1

        else:
            # check if custom anim is playing to freeze
            self.freeze_duration -= 1
            if self.freeze_duration == 0:
                self.frame_to_freeze = None

    def checkIfEnded(self):
        # check if the frame index is equal to or bigger than the amount of frames
        if self.frame_index >= len(clean_directory(self.fx_directory)):
            return True

    def draw(self, scroll):
        adjusted_rect = pygame.Rect(self.image_rect.x - scroll[0], self.image_rect.y - scroll[1], self.image_rect.width, self.image_rect.height)
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), adjusted_rect)
        # pygame.draw.rect(self.screen, (0, 255, 255), self.image_rect, 2)
        # pygame.draw.aaline(self.screen, (255, 0, 0), (self.image_rect.right, 0), (self.image_rect.right, 720))
        # pygame.draw.aaline(self.screen, (255, 0, 0), (self.image_rect.left, 0), (self.image_rect.left, 720))














