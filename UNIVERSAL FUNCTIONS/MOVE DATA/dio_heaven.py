# SCRAPPED IDEA

import pygame
import os
import sys
import threading
import random
import time

from fxHandler import FX
from colorInverter import invert_color
from hitboxHandler import Hitbox
from frameData import get_movedata

import globalProcesses
from globalProcesses import get_processes

processes = get_processes()
hitbox_group = processes.hitbox_group
vfx_group = processes.vfx_group
stand_group = processes.stand_group

def play_sound(directory, volume):
    sound = pygame.mixer.Sound(directory)
    sound.set_volume(volume)
    sound.play()

def attack(self, screen):
    if self.attack_cooldown == 0 and self.doing_move == False and self.stun_frames == 0:
        self.doing_move = True
        self.light_at_counter += 1
        self.attack_cooldown = 20
        box = Hitbox(screen, self, get_movedata(self.char_type, "lightAttack"), self.direction)

        if self.light_at_counter == 1:
            self.playing_attack_anim = "LIGHT_1"
            self.forward_x_movement = 5

        elif self.light_at_counter == 2:
            self.playing_attack_anim = "LIGHT_2"
            self.forward_x_movement = 5

        elif self.light_at_counter == 3:
            self.playing_attack_anim = "LIGHT_3"
            self.forward_x_movement = 10

        elif self.light_at_counter == 4:
            self.playing_attack_anim = "LIGHT_4"
            self.light_at_counter = 0
            self.frame_to_freeze = 0
            self.freeze_duration = 50
            self.forward_x_movement = 3
            box = Hitbox(screen, self, get_movedata(self.char_type, "lightAttackEnder"), self.direction)
            stand = FX(screen, self.playing_attack_anim, (self.rect.centerx + 75 * self.direction), self.rect.centery, self.scale, 100, 255, self.flip, self.char_type)
            vfx_group.append(stand)
        hitbox_group.append(box)

def heavy(self, screen):
    if self.attack_cooldown == 0 and self.doing_move == False and self.stun_frames == 0 and self.in_air == False:
        self.heavy_at_counter += 1
        self.doing_move = True
        self.attack_cooldown = 12
        box = Hitbox(screen, self, get_movedata(self.char_type,"heavyAttack"), self.direction)
        self.playing_attack_anim = "SUMMON_STAND"
        self.frame_to_freeze = 2
        self.freeze_duration = 10

        if self.heavy_at_counter == 1:
            # play_sound(f"SOUND/COMBAT/{self.char_type}/light_1.wav", 0.1)
            # self.forward_x_movement = 5
            # print("ran 1")
            stand = FX(screen, "HEAVY_1", (self.rect.centerx + 75 * self.direction), self.rect.centery, self.scale, 50, 255, self.flip, self.char_type)
            play_sound(f"SOUND/COMBAT/{self.char_type}/light_2.wav", 0.1)

        elif self.heavy_at_counter == 2:
            # play_sound(f"SOUND/COMBAT/{self.char_type}/light_2.wav", 0.1)
            # self.forward_x_movement = 5
            # print("ran 2")
            stand = FX(screen, "HEAVY_2", (self.rect.centerx + 75 * self.direction), self.rect.centery, self.scale, 50, 255, self.flip, self.char_type)
            play_sound(f"SOUND/COMBAT/{self.char_type}/light_1.wav", 0.1)

        elif self.heavy_at_counter == 3:
            # play_sound(f"SOUND/COMBAT/{self.char_type}/light_3.wav", 0.1)
            # self.forward_x_movement = 10
            print("ran 3")
            stand = FX(screen, "HEAVY_3", (self.rect.centerx + 100 * self.direction), self.rect.centery, self.scale,50, 255, self.flip, self.char_type)
            box = Hitbox(screen, self, get_movedata(self.char_type,"heavyAttackEnder"), self.direction)
            play_sound(f"SOUND/COMBAT/{self.char_type}/light_4.wav", 0.1)
            self.heavy_at_counter = 0
        vfx_group.append(stand)
        hitbox_group.append(box)

moves = {
    "H_attack": attack,
    "J_attack": barrage,
    "K_attack": heavy,
    "L_attack": star_finger,
    "U_attack": ora_smash
}

def new_attack(player, screen, move_key):
    for key in moves:
        if move_key == key:
            threading.Thread(target=moves[move_key], args=(player, screen)).start()