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
            print(get_movedata(self.char_type, "lightAttack"))
            print(self.char_type)
            box = Hitbox(screen, self, get_movedata(self.char_type, "lightAttack"), self.direction)

            if self.light_at_counter == 1:
                self.frame_to_freeze = 3
                self.freeze_duration = 10
                self.playing_attack_anim = "LIGHT_1"
                play_sound(f"SOUND/COMBAT/{self.char_type}/first_hit.wav", 0.1)
                self.forward_x_movement = 5

            elif self.light_at_counter == 2:
                self.frame_to_freeze = 3
                self.freeze_duration = 10
                self.playing_attack_anim = "LIGHT_2"
                play_sound(f"SOUND/COMBAT/{self.char_type}/second_hit.wav", 0.1)
                self.forward_x_movement = 5

            elif self.light_at_counter == 3:
                self.frame_to_freeze = 4
                self.freeze_duration = 10
                self.playing_attack_anim = "LIGHT_3"
                play_sound(f"SOUND/COMBAT/{self.char_type}/third_hit.wav", 0.1)
                self.forward_x_movement = 5

            elif self.light_at_counter == 4:
                self.frame_to_freeze = 3
                self.freeze_duration = 10
                self.playing_attack_anim = "LIGHT_4"
                self.light_at_counter = 0
                self.forward_x_movement = 10
                play_sound(f"SOUND/COMBAT/{self.char_type}/fourth_hit.wav", 0.1)
                box = Hitbox(screen, self, get_movedata(self.char_type, "lightAttackEnder"), self.direction)
                self.attack_cooldown = 100

            hitbox_group.append(box)

def dbz_combo(self, screen):
    if self.attack_cooldown == 0 and self.doing_move == False and self.stun_frames == 0 and self.in_air == False:
        self.doing_move = True
        self.frame_to_freeze = 0
        self.freeze_duration = 40
        self.playing_attack_anim = "DBZ_1"
        self.has_outline = True
        self.outline_colour = (255, 0, 0)
        play_sound(f"SOUND/COMBAT/{self.char_type}/dbz_charge.wav", 0.1)
        time.sleep(0.66)
        if self.stun_frames == 0:
            play_sound(f"SOUND/COMBAT/{self.char_type}/dbz_voice.wav", 0.1)
            self.frame_to_freeze = 5
            self.freeze_duration = 20
            self.forward_x_movement = 30
            box = Hitbox(screen, self, get_movedata(self.char_type, "dbz_combo_1"), self.direction)
            hitbox_group.append(box)
            time.sleep(0.35)
        if self.stun_frames == 0:
            play_sound(f"SOUND/COMBAT/{self.char_type}/dbz_teleport.mp3", 0.4)
            self.forward_x_movement = 20
            self.vel_y -= 60
            time.sleep(0.1)
        # reverse direction, second atack
        # checking stun every attack (it works i guess)
            self.air_suspend = 50
            self.vel_y = 0
            self.direction *= -1
            self.flip = not self.flip
            self.frame_to_freeze = 0
            self.freeze_duration = 20
            self.playing_attack_anim = "DBZ_2"
            time.sleep(0.33)
            box = Hitbox(screen, self, get_movedata(self.char_type, "dbz_combo_2"), self.direction)
            hitbox_group.append(box)
        else:
            self.has_outline = False

        # # third attack

        if self.stun_frames == 0:
            time.sleep(0.55)
            play_sound(f"SOUND/COMBAT/{self.char_type}/dbz_teleport.mp3", 0.4)
            self.vel_y -= 30
            self.forward_x_movement = -25
            self.direction *= -1
            self.flip = not self.flip
            time.sleep(0.1)
            self.air_suspend = 50
            self.frame_to_freeze = 0
            self.freeze_duration = 40
            self.playing_attack_anim = "DBZ_3"
            time.sleep(0.33)
            self.vel_y = 0
            box = Hitbox(screen, self, get_movedata(self.char_type, "dbz_combo_3"), self.direction)
            hitbox_group.append(box)
            self.has_outline = False
        else:
            self.has_outline = False

moves = {
    "H_attack": attack,
    "J_attack": dbz_combo,
    "K_attack": None,
    "L_attack": None,
    "U_attack": None
}

def new_attack(player, screen, move_key):
    for key in moves:
        if move_key == key:
            threading.Thread(target=moves[move_key], args=(player, screen)).start()