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
        if self.in_air == False:
            self.light_at_counter += 1
            self.attack_cooldown = 30
            box = Hitbox(screen, self, get_movedata(self.char_type, "lightAttack"), self.direction)

            if self.light_at_counter == 1:
                self.playing_attack_anim = "LIGHT_1"
                play_sound(f"SOUND/COMBAT/{self.char_type}/light_1.wav", 0.1)
                self.forward_x_movement = 5

            elif self.light_at_counter == 2:
                self.playing_attack_anim = "LIGHT_2"
                play_sound(f"SOUND/COMBAT/{self.char_type}/light_2.wav", 0.1)
                self.forward_x_movement = 5

            elif self.light_at_counter == 3:
                self.playing_attack_anim = "LIGHT_3"
                play_sound(f"SOUND/COMBAT/{self.char_type}/light_3.wav", 0.1)
                self.forward_x_movement = 10

            elif self.light_at_counter == 4:
                self.playing_attack_anim = "LIGHT_4"
                self.light_at_counter = 0
                play_sound(f"SOUND/COMBAT/{self.char_type}/light_4.wav", 0.1)
                self.forward_x_movement = 3
                box = Hitbox(screen, self, get_movedata(self.char_type, "lightAttackEnder"), self.direction)
                self.attack_cooldown = 100
            hitbox_group.append(box)

def strong_swing(self, screen):
    if self.attack_cooldown == 0 and self.doing_move == False and self.stun_frames == 0 and self.in_air == False:
        self.doing_move = True
        self.frame_to_freeze = 0
        self.freeze_duration = 40
        self.playing_attack_anim = "STRONG_SWING"
        self.has_outline = True
        self.outline_colour = (255, 0, 0)
        play_sound(f"SOUND/COMBAT/{self.char_type}/strong_swing_voice.wav", 0.1)
        time.sleep(0.2)
        play_sound(f"SOUND/COMBAT/{self.char_type}/bat_charge.wav", 0.1)
        time.sleep(0.2)
        self.has_outline = False
        self.forward_x_movement = 25
        self.frame_to_freeze = 2
        self.freeze_duration = 40
        box = Hitbox(screen, self, get_movedata(self.char_type, "strong_swing"), self.direction)
        hitbox_group.append(box)

moves = {
    "H_attack": attack,
    "J_attack": strong_swing,
    "K_attack": None,
    "L_attack": None,
    "U_attack": None
}

def new_attack(player, screen, move_key):
    for key in moves:
        if move_key == key:
            threading.Thread(target=moves[move_key], args=(player, screen)).start()