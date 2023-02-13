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
            self.attack_cooldown = 20
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
                self.frame_to_freeze = 2
                self.freeze_duration = 50
                self.forward_x_movement = 3
                box = Hitbox(screen, self, get_movedata(self.char_type, "lightAttackEnder"), self.direction)
                stand = FX(screen, self.playing_attack_anim, (self.rect.centerx + 75 * self.direction),self.rect.centery, self.scale, 100, 255, self.flip, self.char_type)

                vfx_group.append(stand)

            hitbox_group.append(box)
        else:
            self.air_at_counter += 1
            box = Hitbox(screen, self, get_movedata(self.char_type, "lightAttackAir"), self.direction)
            if self.air_at_counter == 1:
                stand = FX(screen, "HEAVY_1", (self.rect.centerx + 75 * self.direction), self.rect.centery, self.scale, 40, 255, self.flip, self.char_type)
                self.air_suspend = 20
                hitbox_group.append(box)
                vfx_group.append(stand)
            elif self.air_at_counter == 2:
                stand = FX(screen, "HEAVY_2", (self.rect.centerx + 75 * self.direction), self.rect.centery, self.scale,
                           40, 255, self.flip, self.char_type)
                self.air_suspend = 20
                play_sound(f"SOUND/COMBAT/{self.char_type}/air_2.wav", 0.1)
                hitbox_group.append(box)
                vfx_group.append(stand)
            elif self.air_at_counter == 3:
                self.air_at_counter = 0
                stand = FX(screen, "AIR_BARRAGE", (self.rect.centerx + 75 * self.direction), self.rect.centery,self.scale, 40, 255, self.flip, self.char_type)
                box = Hitbox(screen, self, get_movedata(self.char_type, "lightAttackAirEnder"), self.direction)
                self.air_suspend = 100
                hitbox_group.append(box)
                vfx_group.append(stand)
                play_sound(f"SOUND/COMBAT/{self.char_type}/air_finisher.wav", 0.2)
                play_sound(f"SOUND/COMBAT/{self.char_type}/air_finisher_stand.wav", 0.1)
                sys.stdout.flush()
                time.sleep(0.5)
                sys.stdout.flush()
                for i in range(15):
                    box = Hitbox(screen, self, get_movedata(self.char_type, "airBarrage"), self.direction)
                    hitbox_group.append(box)
                    pygame.time.wait(70)
                box = Hitbox(screen, self, get_movedata(self.char_type, "airBarrageFinisher"), self.direction)
                stand = FX(screen, "AIR_BARRAGE_FINISHER", (self.rect.centerx + 75 * self.direction), self.rect.centery,
                           self.scale, 40, 255, self.flip, self.char_type)
                hitbox_group.append(box)
                vfx_group.append(stand)
                # self.doing_move = False

def barrage(self, screen):
    if self.attack_cooldown == 0 and self.doing_move == False and self.stun_frames == 0 and self.in_air == False:
        self.doing_move = True
        self.attack_cooldown = 30

        MIN_BARRAGE_COUNT = 10
        MAX_BARRAGE_COUNT = 70
        barrage_count = 0
        barrage_cap = MIN_BARRAGE_COUNT

        play_sound(f"SOUND/COMBAT/{self.char_type}/barrage.wav", 0.1)
        play_sound(f"SOUND/COMBAT/{self.char_type}/barrage_voice.wav", 0.1)

        self.frame_to_freeze = 4
        self.freeze_duration = 130
        self.playing_attack_anim = "BARRAGE"
        stand = FX(screen, self.playing_attack_anim, (self.rect.centerx + 75 * self.direction), self.rect.centery,self.scale, 50, 255, self.flip, self.char_type)
        vfx_group.append(stand)
        finished = False
        while finished == False:
            if self.barrage_held == True and barrage_count < MAX_BARRAGE_COUNT and self.stun_frames == 0:
                box = Hitbox(screen, self, get_movedata(self.char_type,"barrage"), self.direction)
                hitbox_group.append(box)
                barrage_count += 1
            else:
                finished = True
                stand.end_early = True
                self.playing_attack_anim = False
                self.update_action("IDLE", 150, True)
                self.current_animation_looped == True
                self.frame_to_freeze = None
                self.freeze_duration = 0

            barrage_count += 1
            self.attack_cooldown += 1
            pygame.time.wait(70)
        self.doing_move = False

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

def star_finger(self, screen):
    if self.attack_cooldown == 0 and self.doing_move == False and self.stun_frames == 0:
        self.doing_move = True
        self.attack_cooldown = 50
        self.frame_to_freeze = 4
        self.freeze_duration = 20
        self.playing_attack_anim = "BARRAGE"
        stand = FX(screen, "STAR_FINGER", (self.rect.centerx + 80 * self.direction), self.rect.centery, self.scale,50, 255, self.flip, self.char_type)
        impact = FX(screen, "IMPACT", (self.rect.centerx + 180 * self.direction), self.rect.centery, 0.5, 25, 255, self.flip)
        impact2 = FX(screen, "IMPACT", (self.rect.centerx + 230 * self.direction), self.rect.centery, 0.2, 25, 255, self.flip)
        box = Hitbox(screen, self, get_movedata(self.char_type,"starFinger"), self.direction)
        hitbox_group.append(box)
        vfx_group.append(stand)
        vfx_group.append(impact)
        play_sound(f"SOUND/COMBAT/{self.char_type}/star_finger.wav", 0.1)
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.flush()
        play_sound(f"SOUND/COMBAT/{self.char_type}/star_finger_impact.wav", 0.1)
        vfx_group.append(impact2)

def ora_smash(self, screen):
    if self.attack_cooldown == 0 and self.doing_move == False and self.stun_frames == 0 and self.in_air == False:
        self.doing_move = True
        self.frame_to_freeze = 3
        self.freeze_duration = 30
        self.forward_x_movement = -12
        self.playing_attack_anim = "SMASH"
        stand = FX(screen, "SMASH", (self.rect.centerx + 50 * self.direction), self.rect.centery, self.scale, 50, 255, self.flip, self.char_type)
        ground_smash = FX(screen, "GROUND_SMASH", (self.rect.centerx + 130 * self.direction), (self.rect.centery + 60), 1, 50, 255, self.flip)
        explosion = FX(screen, "EXPLOSION", (self.rect.centerx + 130 * self.direction), (self.rect.centery + 10), 0.5, 25, 200, self.flip)
        box = Hitbox(screen, self, get_movedata(self.char_type,"oraSmash"), self.direction)
        hitbox_group.append(box)
        vfx_group.append(stand)
        play_sound(f"SOUND/COMBAT/{self.char_type}/ora_smash.wav", 0.2)
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.flush()
        play_sound(f"SOUND/COMBAT/{self.char_type}/rock_smash.wav", 0.3)
        vfx_group.append(ground_smash)
        vfx_group.append(explosion)

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