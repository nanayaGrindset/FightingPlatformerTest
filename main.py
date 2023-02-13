import pygame
import os
import sys
import threading
import random
import time
import importlib
import pytweening as tween

sys.path.insert(0, "UNIVERSAL FUNCTIONS")
sys.path.insert(0, "UNIVERSAL FUNCTIONS/FRAME DATA")

# UNIVERSAL MODULES
import globalProcesses
from globalProcesses import get_processes
from fxHandler import FX
from colorInverter import invert_color
from hitboxHandler import Hitbox
from frameData import get_movedata

# CHARACTER MOVESET MODULES
import jotaro
import thug
from jotaro import new_attack
import thug
from thug import new_attack as thug_attack
import vampire
from vampire import new_attack as vamp_attack

# GLOBAL PROCESSES
processes = get_processes() # i ended up using classes to access lists from different files
hitbox_group = processes.hitbox_group
vfx_group = processes.vfx_group
stand_group = processes.stand_group

# intitialize pygame features
pygame.mixer.init()
pygame.font.init()
tile_rects = []

# universal hit sounds
hit_l = pygame.mixer.Sound("SOUND/COMBAT/hit_l.wav")
hit_b = pygame.mixer.Sound("SOUND/COMBAT/hit_b.wav")
hit_r = pygame.mixer.Sound("SOUND/COMBAT/hit_r.wav")
hit_l.set_volume(0.1)
hit_b.set_volume(0.1)
hit_r.set_volume(0.1)

# in-game images
street_tile = pygame.image.load("IMAGES/MAPS/CITY/TILES/resized.png")
player_stats_black = pygame.image.load("IMAGES/GAME UI/PLAYER/player_stats_black.png")
player_stats_white = pygame.image.load("IMAGES/GAME UI/PLAYER/player_stats_white.png")
player_stats = pygame.image.load("IMAGES/GAME UI/PLAYER/player_stats.png")
green_health = pygame.image.load("IMAGES/GAME UI/PLAYER/green_health.png")
rage_bar = pygame.image.load("IMAGES/GAME UI/PLAYER/rage_bar.png")
green_health = pygame.image.load("IMAGES/GAME UI/PLAYER/green_health.png")
rage_heat = pygame.image.load("IMAGES/GAME UI/PLAYER/rage_heat.png")
enemy_health = pygame.image.load("IMAGES/GAME UI/enemy_health.png")
timer_img = pygame.image.load("IMAGES/GAME UI/PLAYER/timer.png")
timer_cracked = pygame.image.load("IMAGES/GAME UI/PLAYER/timer_cracked.png")
pause_img = pygame.image.load("IMAGES/GAME UI/PLAYER/pause.png")
timestop_img = pygame.image.load("IMAGES/GAME UI/PLAYER/timestop.png")
frame_img = pygame.image.load("IMAGES/GAME UI/PLAYER/frame.png")
pause_menu = pygame.image.load("IMAGES/GAME UI/PLAYER/pause_menu.png")
menu_button = pygame.image.load("IMAGES/GAME UI/PLAYER/menu_button.png")

timer_font = pygame.font.Font("MISC/baron.ttf", 45)
timer_rect = timer_img.get_rect()
timer_rect.center = (1100, 100)
pause_rect = pause_img.get_rect()
pause_rect.center = (60, 60)

# initializing pygame
clock = pygame.time.Clock()
pygame.init()

# screen settings
GRAVITY = 0.75
JUMP_POWER = -15
TERMINAL_FALL_VEL = 10

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = street_tile.get_width()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# title images
title_art = pygame.image.load("IMAGES/GAME UI/TITLE_SCREEN/title_art.png")
play_button = pygame.image.load("IMAGES/GAME UI/TITLE_SCREEN/play_button.png")
play_button_hover = pygame.image.load("IMAGES/GAME UI/TITLE_SCREEN/play_button_hover.png")
PLAY_BUTTON_RECT = play_button.get_rect()
PLAY_BUTTON_RECT.center = (1075, 450)

controls_button = pygame.image.load("IMAGES/GAME UI/TITLE_SCREEN/controls_button.png")
controls_button_hover = pygame.image.load("IMAGES/GAME UI/TITLE_SCREEN/controls_button_hover.png")
CONTROLS_BUTTON_RECT = play_button.get_rect()
CONTROLS_BUTTON_RECT.center = (1030, 600)

control_display = pygame.image.load("IMAGES/GAME UI/TITLE_SCREEN/controls.png")
CONTROLS_RECT = control_display.get_rect()
CONTROLS_RECT.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 600)

# title screen settings
showing_controls = False
changing_control_key = False
selected_move = ""
controls_tween_index = 0
black_screen_tween_index = 0

# keybind customization for the player, where the first element in the list is the key for each move
controls_map = {
    "weak": [pygame.K_h, pygame.Rect(300, 295, 100, 50)],
    "barrage": [pygame.K_j, pygame.Rect(300, 340, 100, 50)],
    "launchers": [pygame.K_k, pygame.Rect(300, 385, 100, 50)],
    "star_finger": [pygame.K_l, pygame.Rect(300, 430, 100, 50)],
    "ground_slam": [pygame.K_u, pygame.Rect(650, 295, 100, 50)],
    "rage_mode": [pygame.K_v, pygame.Rect(650, 340, 100, 50)],
    "timestop": [pygame.K_t, pygame.Rect(650, 385, 100, 50)],
    "dash": [pygame.K_q, pygame.Rect(650, 430, 100, 50)]
}

# controlled player specific variables
moving_left = False
moving_right = False
rage_mode = False
rage_indicator_transparency = 0
timestop_indicator_transparency = 0
RAGE_DRAIN_RATE = 0.2
RAGE_DAMAGE_MULTIPLIER = 1.3
RAGE_WALKSPEED = 10
timestop = False
pausing = False
timestop_timer_count = 0
timestop_ticks_passed = 0
timer_seconds = 60
frame_count = 0
background_objects = []

# list of all characters on screen
char_list = []

# general combat sounds dictionary
combat_sounds_dict = {}

# puts the name of the sound as the key with the directory for easy access
for sound in os.listdir(f"SOUND/COMBAT"):
    # checks if file type in name, which means it's a sound
    if not ".DS_Store" in sound and "." in sound:
        sound_name = sound.split(".")
        sound_name = sound_name[0]
        file = pygame.mixer.Sound(f"SOUND/COMBAT/{sound}")
        combat_sounds_dict[sound_name] = file

# define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# scroll (parallax) variables
true_scroll = [0,0]

# waves
current_wave = 0

# GAME FUNCTIONS
def load_map(map_type, map_number):
    file = open(f"MISC/MAP_INFO/{map_type}/{str(map_number)}_levelfile.rtf", "r")
    data = file.read()
    file.close()
    # erases \n, which signifies new line
    data = data.split("\n")
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

def sort_by_fourth_index(a):
    # i need this for the "key" argument, which is index 3 (dont ask)
	return a[3]

def load_background(map_type):

    # returns all layers for background
    directory_contents = os.listdir(f"IMAGES/MAPS/{map_type}/BACKGROUND")
    background_data = []

    for item in directory_contents:
        splitted = item.split("_")
        order = splitted[1]
        order = order.replace(".png", "")
        # depending on the name will decide the speed which the layer will move

        if splitted[0] == "superfast":
            background_speed = "superfast"
        elif splitted[0] == "fast":
            background_speed = "fast"
        elif splitted[0] == "medium":
            background_speed = "medium"
        elif splitted[0] == "slow":
            background_speed = "slow"
        elif splitted[0] == "stationary":
            background_speed = "stationary"

        img = pygame.image.load(f"IMAGES/MAPS/{map_type}/BACKGROUND/{item}")
        img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        background_data.append([background_speed, img, pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT), order])

    # the "order" variable indicates the order to be blitted: eg. "5" is blitted on top of the previous four
    background_data.sort(key = sort_by_fourth_index)
    return background_data

game_map = load_map("CITY", 1)
game_background = load_background("CITY")
print(game_background)

def draw_bg(scroll):

    for object_data in game_background:
        obj_image = object_data[1]
        distance_multiplier = object_data[0]
        # once again, setting the keyword to an appropiate speed
        if distance_multiplier == "superfast":
            distance_multiplier = 0.12
        elif distance_multiplier == "fast":
            distance_multiplier = 0.1
        elif distance_multiplier == "medium":
            distance_multiplier = 0.08
        elif distance_multiplier == "slow":
            distance_multiplier = 0.04
        elif distance_multiplier == "stationary":
            distance_multiplier = 0

        obj_rect = pygame.Rect(object_data[2].left - scroll[0] * distance_multiplier, object_data[2].top - scroll[1] * distance_multiplier, SCREEN_WIDTH, SCREEN_HEIGHT)
        screen.blit(obj_image, obj_rect)

def play_sound(directory, volume):
    # plays sound given directory and volume
    sound = pygame.mixer.Sound(directory)
    sound.set_volume(volume)
    sound.play()

def stop_sound(directory):
    # stops a sound given the directory
    sound = pygame.mixer.Sound(directory)
    sound.stop()

def play_sound_in_dict(name, volume, looped=False):
    # for sounds in the COMBAT folder where they are used frequently
    sound = combat_sounds_dict[name]
    sound.set_volume(volume)
    if looped == False:
        sound.play()
    else:
        sound.play(-1)

# load jotaro's theme
play_sound_in_dict("MUSIC", 0.05, True)

# returns an "inbetween" from one value to another given the current step, goal value and all steps
def tween_value(current_step, goal_value, all_steps):
    return tween.easeOutSine(current_step / all_steps) * goal_value

# used for player death, creates a new surface to use transparency
def fade_to_black(current_step, goal_value, all_steps):
    black_transparency = 0 + tween_value(current_step, goal_value, all_steps)
    print(black_transparency)
    black_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    black_screen.set_alpha(black_transparency)  # alpha level
    black_screen.fill((0, 0, 0))  # fills entire surface
    screen.blit(black_screen, (0, 0))

def tween_rage_indicator():
    # amount of frames it takes to tween back and forth
    IMAGE_TWEEN_SPEED = 1000
    global rage_indicator_transparency

    if rage_mode == True:
        initial_transparency = 0
        # i don't know why but I have to expand the range loop for tweening by one to the desired amount

        for current_tick in range(0, 255 + 1):
            rage_indicator_transparency = initial_transparency + tween_value(current_tick, 255, 255)
            # resets to opaque if over 255 alpha
            if rage_indicator_transparency >= 255:
                rage_indicator_transparency = 255
                break
            dt = clock.tick(IMAGE_TWEEN_SPEED)

    else:

        initial_transparency = 255
        for current_tick in range(0, 255 + 1):
            rage_indicator_transparency = initial_transparency - tween_value(current_tick, 255, initial_transparency)
            # resets to transparent if under 0 alpha

            if rage_indicator_transparency <= 0:
                rage_indicator_transparency = 0
                break
            dt = clock.tick(IMAGE_TWEEN_SPEED)

def tween_timestop_indicator():
    # amount of frames it takes to tween back and forth
    IMAGE_TWEEN_SPEED = 1000
    global timestop_indicator_transparency

    if timestop == True:
        initial_transparency = 0

        # i don't know why but I have to expand the range loop for tweening to the desired amount
        for current_tick in range(0, 255 + 1):
            timestop_indicator_transparency = initial_transparency + tween_value(current_tick, 255, 255)
            # resets to opaque if over 255 alpha
            if timestop_indicator_transparency >= 255:
                timestop_indicator_transparency = 255
                break
            dt = clock.tick(IMAGE_TWEEN_SPEED)

    else:

        initial_transparency = 255
        for current_tick in range(0, 255 + 1):
            timestop_indicator_transparency = initial_transparency - tween_value(current_tick, 255, initial_transparency)
            # resets to transparent if under 0 alpha
            if timestop_indicator_transparency <= 0:
                rage_indicator_transparency = 0
                break
            dt = clock.tick(IMAGE_TWEEN_SPEED)

def grayscale_image(surf):
    # used for timestop, takes in a surface and returns the surface with inverted pixel colours
    width, height = surf.get_size()
    for x in range(width):

        for y in range(height):
            red, green, blue, alpha = surf.get_at((x, y))
            L = 0.3 * red + 0.59 * green + 0.11 * blue
            gs_color = (L, L, L, alpha)
            surf.set_at((x, y), gs_color)

    return surf

class Player(pygame.sprite.Sprite):

    def __init__(self, char_type, x, y, scale, speed, id, health):
        pygame.sprite.Sprite.__init__(self)
        char_list.append(self)

        # basic character settings
        self.alive = True
        self.char_type = char_type
        print("appended: ", self.char_type)
        self.id = id
        self.speed = speed

        # movement variables
        self.prev_x = 0
        self.prev_y = 0
        self.X_KNOCKBACK_RESISTANCE = 2
        self.vel_y = 0
        self.vel_x = 0
        self.movement = [0,0]
        self.forward_x_movement = 0
        self.air_suspend = 0

        # health bar variables (player)
        self.current_health = health
        self.target_health = health
        self.max_health = health
        self.player_healthbar_length = 183
        self.player_healthbar_ratio = self.max_health / self.player_healthbar_length
        self.HEALTH_CHANGE_SPEED = 5

        # health bar variables (enemy)
        self.enemy_healthbar_length = 100
        self.enemy_healthbar_ratio = self.max_health / self.enemy_healthbar_length

        # rage bar varaibles (player)
        self.ragebar_length = 325
        self.rage_percent = 0
        self.RAGEBAR_RATIO = 100 / self.ragebar_length

        # attack variables
        self.invincible = False
        self.stun_frames = 0
        self.attack_cooldown = 0
        self.direction = 1
        self.scale = scale
        self.jump = False
        self.in_air = True
        self.flip = False
        self.doing_move = False
        self.barrage_held = False
        self.playing_attack_anim = False
        self.light_at_counter = 0
        self.heavy_at_counter = 0
        self.air_at_counter = 0

        # animation variables
        self.animation_list = {}
        self.frame_index = 1
        self.action = "IDLE"
        self.animation_cooldown = 150
        self.current_animation_looped = True

        # freezing frames
        self.frame_to_freeze = None
        self.freeze_duration = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []

        #create ai varaibles
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 700, 200)
        self.attack_vision = pygame.Rect(0, 0, 200, 20)
        self.idling = False
        self.idling_counter = 0

        # load character sprites
        directory_contents = os.listdir(f"IMAGES/{self.char_type}")
        for item in directory_contents:
            dir_path = os.path.join(f"IMAGES/{self.char_type}", item)
            if os.path.isdir(dir_path) and item != "STAND":
                for i in range(0, len(os.listdir(f"IMAGES/{self.char_type}/{item}"))):
                    img = pygame.image.load(f"IMAGES/{self.char_type}/{item}/{i}_{str(item)}_.png")
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                # list of lists of animations
                self.animation_list[item] = temp_list
                temp_list = []

        # character image variables
        self.has_outline = False
        self.afterimage_list = []
        self.afterimage_update_time = pygame.time.get_ticks()
        self.outline_colour = (208, 108, 230)
        self.image = self.animation_list[self.action][self.frame_index]

        # establishing character hitbox
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hitbox = self.rect
        self.hitbox.center = (x, y)

    def collision_test(self, tiles):
        # used to get all touching tiles for other functions to filter out certain tiles to prevent weird behavoir
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def check_for_top_tile(self, tile):
        # if a tile exists above the parameter tile, return false
        is_top = True
        for test in tile_rects:
            if test.centerx == tile.centerx and test.centery == (tile.centery - TILE_SIZE):
                is_top = False
        return is_top

    def handle_tile_collision(self):
        hit_list = self.collision_test(tile_rects)
        tiles_on_right = []
        tiles_on_left = []

        for tile in hit_list:
            # checks for tiles in the hit_list above the player on either side
            if self.rect.right > tile.left and self.rect.bottom > tile.centery and self.rect.centerx < tile.centerx:
                tiles_on_right.append(tile)
            if self.rect.left < tile.right and self.rect.bottom > tile.centery and self.rect.centerx > tile.centerx:
                tiles_on_left.append(tile)

        for tile in tiles_on_right:
            # detects collision between two lines; the top of the character's rect and the bottom of the tiles on the right or left
            # however, both lines are slightly smaller than their rectangles to differentiate between top and side collision
            bottom_tile_line = pygame.Rect(tile.left + 5, tile.bottom + 1, TILE_SIZE - 10, 1)
            top_char_line = pygame.Rect(self.rect.left + 1, self.rect.top - 1, (self.rect.width - 2), 50)
            # pygame.draw.rect(screen, RED, bottom_tile_line, 1)
            # pygame.draw.rect(screen, (0, 0, 255), top_char_line, 1)

            if bottom_tile_line.colliderect(top_char_line) and abs(self.forward_x_movement) < 5 and abs(self.vel_x) < 5:
                tiles_on_right.remove(tile)
                self.rect.top = tile.bottom

        for tile in tiles_on_left:
            # detects collision between two lines; the top of the character's rect and the bottom of the tiles on the right or left
            # however, both lines are slightly smaller than their rectangles to differentiate between top and side collision
            bottom_tile_line = pygame.Rect(tile.left + 5, tile.bottom + 1, TILE_SIZE - 10, 1)
            top_char_line = pygame.Rect(self.rect.left + 1, self.rect.top - 1, (self.rect.width - 2), 50)
            # pygame.draw.rect(screen, RED, bottom_tile_line, 1)
            # pygame.draw.rect(screen, (0, 0, 255), top_char_line, 1)

            if bottom_tile_line.colliderect(top_char_line) and abs(self.forward_x_movement) < 5 and abs(self.vel_x) < 5:
                tiles_on_left.remove(tile)
                self.rect.top = tile.bottom

        # the remaining tiles after removals from the left and right lists are the tiles below the character
        if len(hit_list) > 0:
            if len(tiles_on_right) > 0:
                for tile in tiles_on_right:
                    self.rect.right = tile.left

            if len(tiles_on_left) > 0:
                for tile in tiles_on_left:
                    self.rect.left = tile.right


        for tile in hit_list:

            # any tiles above the character should force them down
            if self.rect.bottom > tile.top and tile.centery > self.rect.centery and self.movement[1] <= 11.75 and (not tile in tiles_on_right and not tile in tiles_on_left):
                self.rect.bottom = tile.top

                # landing vfx
                if self.in_air == True:
                    landing = FX(screen, "LANDING", self.rect.centerx, (self.rect.centery - 25), 1, 20, 200, self.flip)
                    vfx_group.append(landing)
                self.in_air = False

        self.prev_y = self.rect.y
        self.movement[0] = 0
        self.movement[1] = 0

    def manage_afterimages(self):
        # afterimage constants
        NEXT_AFTERIMAGE_COOLDOWN = 60
        AFTERIMAGE_FADETICKS = 120
        AFTERIMAGE_TRANSPARENCY = 200

        # waits for the cooldown before adding another image to the afterimage_list
        if pygame.time.get_ticks() - self.afterimage_update_time > NEXT_AFTERIMAGE_COOLDOWN:
            self.afterimage_update_time = pygame.time.get_ticks()
            afterimage_data = [self.image.copy(), self.rect, 0, AFTERIMAGE_TRANSPARENCY, self.flip]
            self.afterimage_list.append(afterimage_data)

        # tweens each afterimage in the list independently
        for afterimage_sublist in self.afterimage_list:
            afterimage_sublist[3] -= tween_value(afterimage_sublist[2], AFTERIMAGE_TRANSPARENCY, AFTERIMAGE_FADETICKS)
            afterimage_sublist[2] += 1

            # removes once the max fadeticks have been reached
            if afterimage_sublist[3] <= 0 and afterimage_sublist[2] >= 0:
                self.afterimage_list.remove(afterimage_sublist)

            # blits afterimage adjusted for camera movement (scroll)
            else:
                afterimage_sublist[0].set_alpha(afterimage_sublist[3])
                adjusted_rect = pygame.Rect(afterimage_sublist[1].x - scroll[0], afterimage_sublist[1].y - scroll[1], afterimage_sublist[1].width, afterimage_sublist[1].height)
                screen.blit(pygame.transform.flip(afterimage_sublist[0], afterimage_sublist[4], False), adjusted_rect)

    def tween_player_health(self):
        transition_width = 0
        transition_color = (255, 0, 0)

        # health changes gradually by self.HEALTH_CHANGE_SPEED
        # transition to lower health
        if self.current_health < self.target_health:
            self.current_health += self.HEALTH_CHANGE_SPEED
            if self.current_health > self.target_health:
                self.current_health = self.target_health
            if self.current_health >= self.max_health:

                # sets health to max health if over max health
                self.current_health = self.max_health
                self.target_health = self.max_health

            transition_width = int((self.target_health - self.current_health) / self.player_healthbar_ratio)
            transition_color = (0, 255, 0)

        # transition to higher health
        if self.current_health > self.target_health:
            self.current_health -= self.HEALTH_CHANGE_SPEED
            if self.current_health < self.target_health:
                self.current_health = self.target_health

            if self.current_health <= 0:
                # sets health to 0 if under 0
                self.current_health = 0
                self.target_health = 0

        # If the player character, the main healthbar should be made
        if self.id == 0:
            healthbar_width = int(self.current_health / self.player_healthbar_ratio)
            healthbar = pygame.Rect(223, 89, healthbar_width, 27)
            transition_bar = pygame.Rect(healthbar.right, 89, transition_width, 27)

            pygame.draw.rect(screen, (201, 226, 101), healthbar)
            pygame.draw.rect(screen, transition_color, transition_bar)
        else:
            # Mini healthbar for enemies
            healthbar_width = int(self.current_health / self.enemy_healthbar_ratio)
            enemy_healthbar_frame = enemy_health.get_rect()
            enemy_healthbar_frame.centerx = self.hitbox.centerx
            enemy_healthbar_frame.centery = self.hitbox.top - 30
            healthbar = pygame.Rect(enemy_healthbar_frame.left + 50, enemy_healthbar_frame.top + 44, healthbar_width, 12)
            transition_bar = pygame.Rect(healthbar.right, enemy_healthbar_frame.top + 44, transition_width, 12)

            if self.alive == True:
                # draws the enemy healthbar if alive
                screen.blit(enemy_health, enemy_healthbar_frame)
                pygame.draw.rect(screen, (201, 226, 101), healthbar, 10)
                pygame.draw.rect(screen, (201, 226, 101), healthbar)
                pygame.draw.rect(screen, transition_color, transition_bar)

    def handle_rage_bar(self):
        global rage_mode

        # ratio for percentage of rage for rage bar
        ragebar_width = int(self.rage_percent / self.RAGEBAR_RATIO)

        # Any rage over 100% is floored
        if self.rage_percent >= 100:
            self.rage_percent = 100
            ragebar_width = self.ragebar_length

        if rage_mode == True:
            # Rage bar drains in rage mode until reaching zero
            self.rage_percent -= RAGE_DRAIN_RATE
            # regeneration
            self.target_health += 2

            if self.rage_percent <= 0:
                self.rage_percent = 0
                rage_mode = False
                self.has_outline = False
                threading.Thread(target=tween_rage_indicator).start()

        # Timestop removes rage buffs
        if timestop == True:
            self.rage_percent = 0

        pygame.draw.rect(screen, (203, 108, 230), (111,136,ragebar_width,8))

    def update(self):
        self.update_animation()
        print("stun frames: ", self.stun_frames)
        self.check_alive()
        self.draw()

        for plr in enemy_list:
            plr.tween_player_health()

        if self.has_outline == True:
            # Jotaro has distinct outlines for timestop and rage, unlike enemies
            if self.id == 0:
                self.outline_colour = (208, 108, 230)
                if timestop == True:
                    self.outline_colour = (255, 215, 0)
            self.create_outline()
            self.manage_afterimages()
        else:
            # Outlines usually come with afterimages
            self.afterimage_list = []

        # handle frames for self stun and attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.stun_frames > 0:
            self.stun_frames -= 1

        # apply knockback if exists
        if self.vel_x > 0:
            self.rect.x += self.vel_x * -self.direction
            self.movement[0] += self.vel_x * -self.direction
            self.vel_x -= self.X_KNOCKBACK_RESISTANCE

            # to prevent weird behavoir for knockback
            if self.vel_x < 0:
                self.vel_x = 0

        elif self.vel_x < 0:
            self.rect.x += self.vel_x * -self.direction
            self.movement[0] += self.vel_x * -self.direction
            # knockback resistance works against knockback as a dampener
            self.vel_x += self.X_KNOCKBACK_RESISTANCE

            if self.vel_x > 0:
                self.vel_x = 0
        else:
            self.vel_x = 0

        # air suspension frames
        if self.air_suspend > 0:
            self.air_suspend -= 1
        # another external for similar to vel_x
        if self.forward_x_movement > 0:
            self.rect.x += self.forward_x_movement * self.direction
            self.movement[0] += self.forward_x_movement * self.direction
            self.forward_x_movement -= self.X_KNOCKBACK_RESISTANCE

            if self.forward_x_movement < 0:
                self.forward_x_movement = 0

        elif self.forward_x_movement < 0:
            self.rect.x += self.forward_x_movement * self.direction
            self.movement[0] += self.forward_x_movement * self.direction
            self.forward_x_movement += self.X_KNOCKBACK_RESISTANCE

            if self.forward_x_movement > 0:
                self.forward_x_movement = 0
        else:
            self.forward_x_movement = 0
        # handle tile collision AFTER all positions have been changed
        self.handle_tile_collision()

    def move(self, moving_left, moving_right):

        # reset movement variables
        if self.air_suspend == 0:
            dx = 0
            dy = 0
            # net movement of zero for aerial attacks
            if self.doing_move == False and self.stun_frames == 0:
                # If not attacking or stunned, player is able to walk
                if moving_left:
                    dx = - self.speed
                    self.direction = -1
                    self.flip = True
                if moving_right:
                    dx = self.speed
                    self.direction = 1
                    self.flip = False

                if self.jump == True and self.in_air == False:
                    self.vel_y = JUMP_POWER  # negative appears to go up
                    self.jump = False
                    self.in_air = True

            # apply gravity
            self.vel_y += GRAVITY
            dy += self.vel_y

            # to prevent extreme y velocities, the vel_y is automatically capped
            if self.vel_y > TERMINAL_FALL_VEL:
                self.vel_y = TERMINAL_FALL_VEL + 1

            self.rect.x += dx
            self.rect.y += dy
            self.movement[0] += dx
            self.movement[1] += dy

    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        # Checks current frame with frame to freeze
        if self.frame_index != self.frame_to_freeze:

            if (pygame.time.get_ticks() - self.update_time > self.animation_cooldown):
                self.update_time = pygame.time.get_ticks()
                if self.alive == True:
                    # if alive and animation cooldown has passed, go to next animation frame
                    self.frame_index += 1

                elif self.alive == False:
                    # death animation stops on the last frame
                    if self.frame_index != len(self.animation_list[self.action]) - 1:
                        self.frame_index += 1


            if self.frame_index >= len(self.animation_list[self.action]):
                if self.current_animation_looped == True:

                    # if died, don't loop the death animation
                    if self.action == "DIED":
                        self.frame_index = len(self.animation_list[self.action])
                    else:
                        self.frame_index = 0
                else:

                    # if not in combat, do default movement animation
                    self.playing_attack_anim = False

                    if self.in_air and self.vel_y < 0:
                        self.update_action("JUMP_FALLING", 150, True)
                    elif self.in_air and self.vel_y >= 0:
                        player.update_action("JUMP_RISING", 150, True)
                    elif moving_left or moving_right:
                        self.update_action("WALK", 75, True)
                    elif self.stun_frames > 0:
                        self.update_action("GOT_HIT", 150, True)
                    else:
                        self.update_action("IDLE", 150, True)

        else:
            # check if custom anim is playing to freeze
            if self.playing_attack_anim != False:
                self.freeze_duration -= 1
                if self.freeze_duration == 0:
                    self.frame_to_freeze = None

        # aligns the hitbox and rect to each other
        self.hitbox = self.image.get_rect()
        self.hitbox.center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = self.hitbox.center

    def update_action(self, new_action, new_anim_speed, looped):

        #check if new action is different to previous
        if new_action != self.action:
            self.action = new_action
            self.animation_cooldown = new_anim_speed
            self.current_animation_looped = looped

            # reset animation index
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.current_health <= 0:
            if self.alive == True and self.id == 0:
                # play death sound only for player
                play_sound("SOUND/COMBAT/jotaro_death.wav", 0.3)

            # immobilize the player
            self.speed = 0
            self.alive = False
            self.update_action("DIED", 150, False)


    def draw(self):
        # draws the player at an adjusted position depending on scroll
        adjusted_rect = pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), adjusted_rect)
        self.hitbox = adjusted_rect

    def ai(self):
        if self.alive and player.alive:
            ai_moving_right = False
            ai_moving_left = False

            # slim chance to idle
            if self.char_type == "THUG":
                if random.randint(1, 200) == 1 and self.idling == False:
                    self.update_action("IDLE", 150, True)
                    self.idling = True
                    self.idling_counter = 50

                # check if player in attack vision (smaller than movement vision)
                if self.attack_vision.colliderect(player.hitbox):
                    # randomize between strong swings and regular
                    if random.randint(1, 3) == 1:
                        thug_attack(self, screen, "J_attack")
                    else:
                        thug_attack(self, screen, "H_attack")

                if self.playing_attack_anim != False:
                    self.update_action(self.playing_attack_anim, 75, False)
                else:
                    # if the player is in vision, move towards the player
                    if self.vision.colliderect(player.hitbox):
                        if self.hitbox.x > player.hitbox.x:
                            ai_moving_left = True
                        elif self.hitbox.x < player.hitbox.x:
                            ai_moving_left = False
                        ai_moving_right = not ai_moving_left
                        self.update_action("WALK", 150, True)

                    elif self.idling == False:
                        # normal walking
                        if self.direction == 1:
                            ai_moving_right = True
                        else:
                            ai_moving_right = False
                        ai_moving_left = not ai_moving_right
                        self.update_action("WALK", 150, True)
                        self.move_counter += 1

                        # if the ai has travelled a single tile, switch directions
                        if self.move_counter > TILE_SIZE:
                            self.direction *= -1
                            original_left = ai_moving_left
                            ai_moving_left = not ai_moving_right
                            ai_moving_right = original_left
                            self.move_counter *= -1

                    else:
                        # count down idle before walking again
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self.idling = False

                # stun frames override all other states
                if self.stun_frames > 0:
                    self.update_action("GOT_HIT", 150, True)

                # update ai vision
                self.vision.center = (self.rect.centerx + 75 * self.direction - scroll[0], self.rect.centery - scroll[1])
                self.attack_vision.center = (self.rect.centerx + 75 * self.direction - scroll[0], self.rect.centery - scroll[1])
                # pygame.draw.rect(screen, BLUE, self.vision, 2)
                # pygame.draw.rect(screen, RED, self.attack_vision, 2)
                self.move(ai_moving_left, ai_moving_right)

            elif self.char_type == "VAMPIRE":
                # mostly the same as the thug ai
                if self.alive and player.alive:

                    ai_moving_right = False
                    ai_moving_left = False

                    if self.char_type == "VAMPIRE":
                        if random.randint(1, 200) == 1 and self.idling == False:
                            self.update_action("IDLE", 150, True)
                            self.idling = True
                            self.idling_counter = 50

                        if self.attack_vision.colliderect(player.hitbox):
                            if random.randint(1, 3) == 1:
                                vamp_attack(self, screen, "J_attack")
                            else:
                                vamp_attack(self, screen, "H_attack")

                        if self.playing_attack_anim != False:
                            self.update_action(self.playing_attack_anim, 75, False)

                        else:
                            if self.vision.colliderect(player.hitbox):
                                if self.hitbox.x > player.hitbox.x:
                                    ai_moving_left = True
                                elif self.hitbox.x < player.hitbox.x:
                                    ai_moving_left = False
                                ai_moving_right = not ai_moving_left
                                self.update_action("WALK", 150, True)

                            elif self.idling == False:
                                if self.direction == 1:
                                    ai_moving_right = True
                                else:
                                    ai_moving_right = False

                                ai_moving_left = not ai_moving_right
                                self.update_action("WALK", 150, True)
                                self.move_counter += 1

                                if self.move_counter > TILE_SIZE:
                                    self.direction *= -1
                                    original_left = ai_moving_left
                                    ai_moving_left = not ai_moving_right
                                    ai_moving_right = original_left
                                    self.move_counter *= -1

                            else:
                                self.idling_counter -= 1
                                if self.idling_counter <= 0:
                                    self.idling = False

                        if self.stun_frames > 0:
                            self.update_action("GOT_HIT", 150, True)

                        # update ai vision
                        self.vision.center = (self.rect.centerx + 75 * self.direction - scroll[0], self.rect.centery - scroll[1])
                        self.attack_vision.center = (self.rect.centerx + 75 * self.direction - scroll[0], self.rect.centery - scroll[1])
                        # pygame.draw.rect(screen, BLUE, self.vision, 2)
                        # pygame.draw.rect(screen, RED, self.attack_vision, 2)
                        self.move(ai_moving_left, ai_moving_right)

    def create_outline(self):
        # creates a mask of the current sprite
        mask = pygame.mask.from_surface(self.image)
        if self.direction == -1:
            mask = pygame.mask.from_surface(pygame.transform.flip(self.image, self.flip, False))

        # mask outline and seperate surface for outline
        loc = self.hitbox.topleft
        mask_outline = mask.outline()
        mask_surf = pygame.Surface(self.image.get_size())

        # sets all pixels in mask to the outline colour
        for pixel in mask_outline:
            mask_surf.set_at(pixel, self.outline_colour)

        mask_surf.set_colorkey((0, 0, 0))
        screen.blit(mask_surf, (loc[0] - 1, loc[1]))
        screen.blit(mask_surf, (loc[0] + 1, loc[1]))
        screen.blit(mask_surf, (loc[0], loc[1] - 1))
        screen.blit(mask_surf, (loc[0], loc[1] + 1))

    def dash(self):
        if self.attack_cooldown == 0 and self.doing_move == False and self.stun_frames == 0:

            # dash has no recovery, meaning the momentum can be cancelled into other moves
            self.forward_x_movement = 25
            self.playing_attack_anim = "DASH"
            self.frame_to_freeze = 1
            self.freeze_duration = 8
            play_sound(f"SOUND/COMBAT/dash.wav", 0.1)
            # invincibility during dash
            self.invincible = True
            dash_fx2 = FX(screen, "DASH_2", (self.rect.centerx + 10 * self.direction), self.rect.centery + 30, 1.5, 25, 200, self.flip)
            vfx_group.append(dash_fx2)

            for i in range(9):
                if i == 2:
                    # on the second frame, create the dash vfx
                    dash_fx = FX(screen, "DASH", self.rect.centerx, self.rect.centery, 0.3, 50, 150, self.flip)
                    vfx_group.append(dash_fx)
                # no vel_y makes sure dash goes straight
                self.vel_y = 0
                pygame.time.delay(30)
            self.invincible = False

    def player_timestop(self):
        global rage_mode
        global timestop
        global timestop_timer_count

        if self.attack_cooldown == 0 and self.doing_move == False and self.stun_frames == 0:

            stop_sound("SOUND/COMBAT/MUSIC.mp3")
            self.doing_move = True
            TIMESTOP_SECONDS = 5
            # timestop startup animation
            self.playing_attack_anim = "TIMESTOP"
            self.attack_cooldown = 60
            self.frame_to_freeze = 3
            self.freeze_duration = 50

            # the """hitbox""" is just to keep track of frame data, it has 0 size
            box = Hitbox(screen, self, get_movedata(self.char_type,"timestop"), self.direction)
            hitbox_group.append(box)
            sys.stdout.flush()

            pygame.time.delay(30)
            timestop = True
            rage_mode = False
            # tween rage indicator to disappear and time indicator to appear
            threading.Thread(target=tween_timestop_indicator).start()
            threading.Thread(target=tween_rage_indicator).start()
            timestop_timer_count = TIMESTOP_SECONDS
            play_sound_in_dict("timestop", 0.2)
            play_sound_in_dict("timer_shatter", 0.3)
            sys.stdout.flush()


player = Player("JOTARO", 200, 200, 2, 5, 0, 1000)
enemy_list = []

def reset_game():
    global player
    global enemy_list
    global moving_left
    global moving_right
    global rage_indicator_transparency
    global rage_mode
    global timestop
    global pausing
    global timestop_timer_count
    global timestop_ticks_passed
    global timestop_indicator_transparency
    global timer_seconds
    global frame_count
    global true_scroll
    global current_wave

    # reset all player-influenced variables, clear all global processes and char list
    moving_left = False
    moving_right = False
    rage_mode = False
    rage_indicator_transparency = 0
    timestop_indicator_transparency = 0
    timestop = False
    pausing = False
    timestop_timer_count = 0
    timestop_ticks_passed = 0
    timer_seconds = 60
    frame_count = 0
    enemy_list.clear()
    char_list.clear()
    true_scroll = [0,0]
    current_wave = 0
    hitbox_group.clear()
    stand_group.clear()
    vfx_group.clear()
    # create new player in char_list
    player = Player("JOTARO", 200, 200, 2, 5, 0, 1000)

def manageHitboxes():
    if len(hitbox_group) > 0:
        garbage_hitboxes = []
        ordered_garbage_hitboxes = []

        for index in range(len(hitbox_group)):
            hitbox_group[index].hitbox_group_index = index
            check = hitbox_group[index].updateFrame()
            hitbox_group[index].draw(scroll)
            collided_char = hitbox_group[index].activate(char_list, scroll)
            # collided_char will equal the character hit if it exists

            if collided_char and collided_char.invincible == False and collided_char.alive == True:
                # do vfx on character position
                collided_char.stun_frames = hitbox_group[index].move_data["hitstun"]
                collided_char.doing_move = False
                collided_char.direction = hitbox_group[index].owner.direction * -1

                # delete all collided_char hitboxes
                for index in range(len(hitbox_group)):
                    if hitbox_group[index].owner.id == collided_char.id:
                        garbage_hitboxes.append(hitbox_group[index])

                # knockback and damage from framedata
                if "x_pushback" in hitbox_group[index].move_data:
                    collided_char.vel_x += hitbox_group[index].move_data["x_pushback"]
                if "y_pushback" in hitbox_group[index].move_data:
                    collided_char.vel_y -= hitbox_group[index].move_data["y_pushback"]
                if "damage" in hitbox_group[index].move_data:
                    if hitbox_group[index].owner.char_type == "JOTARO" and rage_mode == True:
                        collided_char.target_health -= hitbox_group[index].move_data["damage"] * RAGE_DAMAGE_MULTIPLIER
                    else:
                        collided_char.target_health -= hitbox_group[index].move_data["damage"]

                # if the hitbox was by the player (jotaro), increase the player's rage bar
                if hitbox_group[index].owner.char_type == "JOTARO":
                    if "ragebar_increase" in hitbox_group[index].move_data:
                        player.rage_percent += hitbox_group[index].move_data["ragebar_increase"]

                if random.randint(1,2) == 1:
                    # random damage sounds
                    play_sound(f"SOUND/COMBAT/{(collided_char.char_type).upper()}/damaged_{random.randint(1,3)}.wav", 0.3)

                hitEffect = FX(screen, hitbox_group[index].move_data["effect_type"], collided_char.rect.centerx, collided_char.rect.centery, hitbox_group[index].move_data["effect_size"], hitbox_group[index].move_data["fx_tick_speed"], hitbox_group[index].move_data["effect_transparency"])
                vfx_group.append(hitEffect)
                if hitbox_group[index].move_data["effect_type"] == "light":
                    hit_l.play()
                elif hitbox_group[index].move_data["effect_type"] == "barrage":
                    hit_b.play()
                elif hitbox_group[index].move_data["effect_type"] == "heavy":
                    hit_r.play()

            # if hitbox should still exist, draw it
            if check == True:
                # check move data if doing move should still be active
                # no for barrage
                if hitbox_group[index].move_data["reset_doing_move"] == True:
                    hitbox_group[index].owner.doing_move = False
                # if ended, add to debris list
                garbage_hitboxes.append(hitbox_group[index])

        # delete all items in debris list
        # starting from here may be the suspect code
        if len(garbage_hitboxes) > 0:
            maximum = garbage_hitboxes[0]  # arbitrary number in list
            for item in garbage_hitboxes:
                if item.hitbox_group_index > maximum.hitbox_group_index:
                    maximum = item
            ordered_garbage_hitboxes.append(maximum)
            garbage_hitboxes.remove(maximum)

        for debris in ordered_garbage_hitboxes:
                del hitbox_group[debris.hitbox_group_index]  # fix when index deleted shifting all other elements

def manageVFX():
    if len(vfx_group) != 0:
        # garbage_vfx for vfx that are finished playing, and ordered_garbage_vfx to order deletion
        garbage_vfx = []
        ordered_garbage_vfx = []


        for index in range(0, len(vfx_group)):
            vfx_group[index].vfx_group_index = index
            check = vfx_group[index].update(true_scroll)
            # if vfx should end, add to garbage_vfx
            if check == True or vfx_group[index].end_early == True:
                garbage_vfx.append(vfx_group[index])

        if len(garbage_vfx) > 0:
            maximum = garbage_vfx[0]  # arbitrary number in list
            for item in garbage_vfx:
                if item.vfx_group_index > maximum.vfx_group_index:
                    maximum = item

            ordered_garbage_vfx.append(maximum)
            garbage_vfx.remove(maximum)

        # after ordering by vfx_group_index, all garbage_vfx are deleted in order
        for debris in ordered_garbage_vfx:
            del vfx_group[debris.vfx_group_index]

run = True
game_state = "title"

while run:
    # title screen
    if game_state == "title":
        # blit title images
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(title_art, (0,0))
        screen.blit(play_button, PLAY_BUTTON_RECT)
        screen.blit(controls_button, CONTROLS_BUTTON_RECT)
        screen.blit(control_display, CONTROLS_RECT)

        # blit hover variant of button over actual button
        if PLAY_BUTTON_RECT.collidepoint(mouse_pos) and showing_controls == False:
            screen.blit(play_button_hover, PLAY_BUTTON_RECT)
        if CONTROLS_BUTTON_RECT.collidepoint(mouse_pos) and showing_controls == False:
            screen.blit(controls_button_hover, CONTROLS_BUTTON_RECT)

        # tween controls gui
        if showing_controls == True:
            if controls_tween_index <= 100:
                CONTROLS_RECT.centery = ((SCREEN_HEIGHT / 2) + 600) - tween_value(controls_tween_index, 600, 100)
                controls_tween_index += 1

            # display keybind buttons when tween is complete
            if controls_tween_index >= 100:
                for move_name in controls_map:
                    key_text = timer_font.render(pygame.key.name(controls_map[move_name][0]), True, WHITE)
                    text_rect = key_text.get_rect(center=(controls_map[move_name][1].centerx, controls_map[move_name][1].centery))
                    screen.blit(key_text, text_rect)

        else:
            # reverse the tween gui
            if controls_tween_index <= 100:
                CONTROLS_RECT.centery = ((SCREEN_HEIGHT / 2)) + tween_value(controls_tween_index, 600, 100)
                controls_tween_index += 1

        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                # switch to gameplay when play button clicked
                if PLAY_BUTTON_RECT.collidepoint(mouse_pos) and showing_controls == False:
                    game_state = "gameplay"
                    play_sound_in_dict("rage_heat", 0.2)
                # start controls ui tween when controls button clicked
                if CONTROLS_BUTTON_RECT.collidepoint(mouse_pos) and showing_controls == False:
                    showing_controls = True
                    controls_tween_index = 0

                for key in controls_map.keys():
                    # select the clicked keybind in the controls ui
                    if controls_map[key][1].collidepoint(mouse_pos) and showing_controls == True:
                        selected_move = key
                        play_sound_in_dict("keybind_select", 0.2)
                        changing_control_key = True

            if event.type == pygame.KEYDOWN:
                # close control sui
                if event.key == pygame.K_e and changing_control_key == False and showing_controls == True:
                    showing_controls = False
                    controls_tween_index = 0

                if changing_control_key == True:
                    # check if any other keybind shares the same key with the currently pressed key during the keybind configuration
                    already_matching_keybind = False
                    for key in controls_map.keys():
                        if controls_map[key][0] == event.key:
                            already_matching_keybind = True
                    # if not, change the keybind and deselect the selected keybind
                    if already_matching_keybind == False:
                        controls_map[selected_move][0] = event.key
                        changing_control_key = False
                        play_sound_in_dict("keybind_change", 0.2)
                        selected_move = ""

    elif game_state == "gameplay":
        draw_bg(true_scroll)
        true_scroll[0] += (player.rect.centerx - true_scroll[0] - ((SCREEN_WIDTH / 2))) / 20
        true_scroll[1] += (player.rect.centery - true_scroll[1] - ((SCREEN_HEIGHT / 2))) / 20
        # scroll is to ensure that tiles are positioned by integers
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        # once all tiles on the x axis are iterated through, add one tile unit to y
        tile_rects = []
        y_tile_units = 0

        for row in game_map:
            x_tile_units = 0
            for tile in row:
                if tile == "1":
                    # create street tile
                    screen.blit(street_tile, (x_tile_units * TILE_SIZE - scroll[0], y_tile_units * TILE_SIZE - scroll[1]))
                if tile != "0":
                    tile_rects.append(pygame.Rect(x_tile_units * TILE_SIZE, y_tile_units * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                x_tile_units += 1
            y_tile_units += 1

        if pausing == False:
            # update player
            player.update()

            all_enemies_dead = True
            for enemy in enemy_list:
                if enemy.alive == True:
                    all_enemies_dead = False

            # if no enemies remain, move to next wave and spawn enemies
            if all_enemies_dead == True:
                enemy_list.clear()
                timer_seconds = 60
                current_wave += 1
                if current_wave >= 4:
                    timer_seconds = 120
                if current_wave >= 8:
                    timer_seconds = 360

                # wave number is # of enemies
                for i in range(current_wave):
                    rand_enemy = random.randint(1, 2)
                    rand_position = random.randint(-500, 500)
                    rand_position = rand_position - scroll[0]
                    # randomize thug or vampire
                    if rand_enemy == 1:
                        new_enemy = Player("THUG", rand_position, 250, 2.3, 6, random.randint(1,1000), 200 * current_wave)
                        enemy_list.append(new_enemy)
                    elif rand_enemy == 2:
                        new_enemy = Player("VAMPIRE", rand_position, 250, 2, 6, random.randint(1,1000), 200 * current_wave)
                        enemy_list.append(new_enemy)

            # if timestop false, update all enemy positions
            if timestop == False:
                for enemy in enemy_list:
                    enemy.update()
                    enemy.ai()
                    if (enemy.rect.centery) > (1000):
                        enemy.rect.centery = (100)
                        rand_x = random.randint(100,700)
                        enemy.rect.centerx = (rand_x - scroll[1])
            else:
                # if timestop true, only draw the enemies in place
                for enemy in enemy_list:
                    enemy.draw()

            if timestop == True:
                # start timestop counter until reaches zero
                if timestop_timer_count > -1:
                    if timestop_ticks_passed % 60 == 0:
                        play_sound_in_dict("second_tick", 0.5)
                        timestop_timer_count -= 1
                    timestop_ticks_passed += 1
                else:
                    play_sound_in_dict("timestop_resume", 0.2)
                    timestop = False
                    threading.Thread(target=tween_timestop_indicator).start()
                    player.has_outline = False

            # update hitboxes and vfx every frame
            manageHitboxes()
            manageVFX()

            if player.alive:

                # if player alive, check conditions for basic movement states
                if player.playing_attack_anim != False:
                    player.update_action(player.playing_attack_anim, 50, False)
                elif player.in_air and player.vel_y < 0:
                    player.update_action("JUMP_FALLING", 150, True)
                elif player.in_air and player.vel_y >= 0:
                    player.update_action("JUMP_RISING", 150, True)
                elif moving_left or moving_right and player.stun_frames == 0:
                    player.update_action("WALK", 75, True)
                elif player.stun_frames > 0:
                    player.update_action("GOT_HIT", 150, True)
                else:
                    player.update_action("IDLE", 150, True)

                player.move(moving_left, moving_right)
                # if falling in the void, kill player (skill issue lol)
                if (player.rect.centery - scroll[1]) > (1500 - scroll[1]):
                    player.target_health = 0

            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN and player.stun_frames == 0:
                    if event.key == pygame.K_a:
                        moving_left = True
                    if event.key == pygame.K_d:
                        moving_right = True

                    # load moves triggered from controls map
                    if event.key == controls_map["weak"][0]:
                        new_attack(player, screen, "H_attack")
                    if event.key == controls_map["barrage"][0]:
                        player.barrage_held = True
                        new_attack(player, screen, "J_attack")
                    if event.key == controls_map["launchers"][0]:
                        new_attack(player, screen, "K_attack")
                    if event.key == controls_map["rage_mode"][0]:
                        if player.rage_percent == 100 and rage_mode == False:
                            # enter rage mode
                            rage_mode = True
                            player.has_outline = True
                            play_sound_in_dict("rage_heat", 0.1)
                            play_sound_in_dict("jotaro_yare", 0.3)
                            threading.Thread(target=tween_rage_indicator).start()

                    # the rest of the moves trigged from controls map
                    if event.key == controls_map["star_finger"][0]:
                        new_attack(player, screen, "L_attack")
                    if event.key == controls_map["ground_slam"][0]:
                        new_attack(player, screen, "U_attack")
                    if event.key == controls_map["dash"][0]:
                        threading.Thread(target=player.dash).start()
                    if event.key == controls_map["timestop"][0]:
                        if rage_mode == True and timestop == False:
                            stop_sound("SOUND/COMBAT/MUSIC.mp3")
                            threading.Thread(target=player.player_timestop).start()

                    if event.key == pygame.K_w and player.alive:
                        player.jump = True

                    if event.key == pygame.K_ESCAPE:
                        run = False

                # pause game when pause button pressed
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if pause_rect.collidepoint(mouse_pos):
                        pausing = True
                        moving_left = False
                        moving_right = False

                if event.type == pygame.KEYUP and player.stun_frames == 0:
                    if event.key == pygame.K_a:
                        moving_left = False
                    if event.key == pygame.K_d:
                        moving_right = False
                    # stop currently active barrage when key is lifted (more dynamic)
                    if event.key == controls_map["barrage"][0]:
                        player.barrage_held = False

                # stop walking if stunned
                if player.stun_frames > 0:
                    moving_left = False
                    moving_right = False

            # count down timer
            if (frame_count / 60).is_integer():
                if timer_seconds > 0:
                    timer_seconds -= 1
                else:
                    # kill player at zero
                    timer_seconds = 0
                    player.target_health = 0

        else:
            # (when pausing is true)
            # only draw players
            player.draw()
            for enemy in enemy_list:
                enemy.draw()

            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    menu_button_rect = menu_button.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                    # if the main menu button is clicked in the pause menu, go back to title screen and restart game
                    if menu_button_rect.collidepoint(mouse_pos):
                        reset_game()
                        game_state = "title"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        # unpause game
                        pausing = False

        if timestop == False:
            # display regular timer
            screen.blit(timer_img, timer_rect)
        else:
            # returns a surface with inverted colors
            inverted_screen = invert_color(screen, mask=None, rel_pos=(0, 0), color=(255, 255, 255))
            screen.blit(inverted_screen, (0, 0))
            # display cracked version of timer
            screen.blit(timer_cracked, timer_rect)
        minutes, seconds = divmod(timer_seconds, 60)
        minutes = str(minutes)
        seconds = str(seconds)

        # ensures that seconds place is two digits to improve timer look
        if len(seconds) == 1:
            seconds = "0" + str(seconds)
        timer_text = timer_font.render(minutes + ":" + seconds, True, WHITE)
        screen.blit(timer_text, (timer_rect.centerx + 12, timer_rect.centery - 20))

        # display current wave
        wave_text = timer_font.render("CURRENT WAVE: " + str(current_wave), True, WHITE)
        screen.blit(wave_text, (100, 600))

        # player profile and stats
        screen.blit(frame_img, (0, 0))
        screen.blit(player_stats, (80, -10))
        screen.blit(pause_img, pause_rect)
        player.tween_player_health()
        player.handle_rage_bar()

        # display rage and timestop indicators
        rage_heat.set_alpha(rage_indicator_transparency)
        screen.blit(rage_heat, (0, 200))
        timestop_img.set_alpha(timestop_indicator_transparency)
        screen.blit(timestop_img, (0, 250))

        if player.alive == False:
            # fade scren to black upon death
            black_screen_tween_index += 1
            if black_screen_tween_index >= 150:
                black_screen_tween_index = 0
                reset_game()
                # back to title screen
                game_state = "title"
            else:
                fade_to_black(black_screen_tween_index, 255, 150)

        if timestop == False and pausing == False:
            frame_count += 1

        # display pause button and menu if pausing active
        if pausing == True:
            screen.blit(pause_menu, pause_menu.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
            screen.blit(menu_button, menu_button.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
    pygame.display.flip()
    dt = clock.tick(60)
