import pygame

def item_in_list(item, list):
    if item in list:
        return True #list.index(item)
    else:
        return False

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, screen, player, move_data, direction):
        # basic settings
        self.screen = screen
        self.move_data = move_data
        self.owner = player
        self.direction = direction
        self.hitbox_group_index = 0

        # hitbox rect
        player_rect = self.owner.rect
        self.rect = pygame.Rect(player_rect.left, player_rect.top, self.move_data["x_size"], self.move_data["y_size"])
        self.rect.centerx = player_rect.centerx + (self.move_data["x_offset"] * direction)
        self.rect.centery = player_rect.centery + self.move_data["y_offset"]

        # frame data
        self.frame_index = 1
        self.frame_tick_speed = self.move_data["frame_tick_speed"]
        self.state = "startup"
        self.ended = False
        self.frame_data = self.move_data["frame_data"]
        self.effect_type = self.move_data["effect_type"]
        self.stun_frames = self.move_data["hitstun"]
        self.airOK = self.move_data["airOK"]
        self.ignoreList = []
        self.update_time = pygame.time.get_ticks()

    def draw(self, scroll):
        # only used for debugging, allows you to see hitboxes
        if self.state == "active":
            adjusted_rect = pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height)
            pygame.draw.rect(self.screen, (0,255,0), adjusted_rect, 2)
        else:
            adjusted_rect = pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height)
            pygame.draw.rect(self.screen, (255, 0, 0), adjusted_rect, 2)

    def updateFrame(self):
        if not self.ended == True:
            if pygame.time.get_ticks() - self.update_time > self.frame_tick_speed:
                # get type of current frame
                if (self.move_data["frame_data"]["startup"]) <= self.frame_index:
                    self.state = "active"
                if (self.move_data["frame_data"]["startup"] + self.move_data["frame_data"]["active"]) <= self.frame_index:
                    self.state = "recovery"
                if (self.move_data["frame_data"]["startup"] + self.move_data["frame_data"]["active"] + self.move_data["frame_data"]["recovery"]) <= self.frame_index:
                    self.ended = True
                    return True

                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
        else:
            return True

    def activate(self, char_list, scroll):
        if self.state == "active":
            for character in char_list:
                print(character.char_type)
                # for all characters, check if their hurtbox collides with this hitbox and makes sure it diesn't hit twice or hits themself
                if not character.id == self.owner.id and not item_in_list(character, self.ignoreList):
                    adjusted_rect = pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height)
                    if pygame.Rect.colliderect(adjusted_rect, character.hitbox):
                        self.ignoreList.append(character)
                        if self.airOK == True:
                            # keeps enemy in the air for the amount of their stun frames
                            character.air_suspend = self.stun_frames
                        else:
                            character.air_suspend = 0
                        return character









