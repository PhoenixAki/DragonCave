import math
import pathlib
from typing import List

import arcade
from arcade.draw_commands import Texture

FACE_LEFT = 0
FACE_RIGHT = 1
FACE_UP = 2
FACE_DOWN = 3


class PlayerCharacter(arcade.AnimatedWalkingSprite):
    def __init__(self, scale: float, center_x: float, center_y: float):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.attacking = False
        self.temp_invincibility = False
        self.invincibility_timer = 0
        self.health = 3
        self.money = 50
        self.arrows = 0
        self.boots = False
        self.magic_book = False
        self.chest_key = False
        self.crystal = False

        self.cur_texture_index = 0
        self.state = FACE_UP

        self.node_x = None
        self.node_y = None

        # walking textures
        self.walk_left_textures = []
        self.walk_right_textures = []
        self.walk_down_textures = []
        self.walk_up_textures = []

        # attack textures
        self.spear_left_textures = []
        self.spear_right_textures = []
        self.spear_down_textures = []
        self.spear_up_textures = []

        self.hurt_sound_path = pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'player_hurt.wav'
        self.hurt_sound = arcade.Sound(str(self.hurt_sound_path))

    def update_health(self, health):
        """
        **health:** value to update character's health to \n
        *example: pass in character.health-1 to subtract 1, or character.health+1 to add 1*

        **temp_invincibility:** enabled upon taking damage, and prevents more damage from being taken for 3 seconds.
        """
        old_health = self.health

        if self.temp_invincibility is False:
            self.health = health
            print("Health reduced from ", old_health, " to ", self.health)
            self.hurt_sound.play()

        if health < old_health and self.temp_invincibility is False:
            self.temp_invincibility = True
            print("Enabling invincibility.")  # this will print even if the player is about to die due to 0 health

    def update(self):
        if self.temp_invincibility is True:
            self.invincibility_timer += 1

        if self.invincibility_timer >= 60:  # 2 seconds at 30fps
            self.invincibility_timer = 0
            self.temp_invincibility = False
            print("Disabling invincibility.")

    def update_animation(self, delta_time: float = 1/30):
        """
        Logic for selecting the proper texture to use.
        """

        texture_list: List[Texture] = []

        if self.attacking:
            if self.state == FACE_LEFT:
                texture_list = self.spear_left_textures
            elif self.state == FACE_RIGHT:
                texture_list = self.spear_right_textures
            elif self.state == FACE_UP:
                texture_list = self.spear_up_textures
            elif self.state == FACE_DOWN:
                texture_list = self.spear_down_textures

            if len(texture_list) == 0:
                raise RuntimeError("error loading attack textures in player update_animation")

            # check if done playing the texture
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0
                self.attacking = False

            self.texture = texture_list[self.cur_texture_index]

        else:
            x1 = self.center_x
            x2 = self.last_texture_change_center_x
            y1 = self.center_y
            y2 = self.last_texture_change_center_y
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            change_direction = True
            if self.change_x < 0 < len(self.walk_left_textures) and self.state != FACE_LEFT:
                self.state = FACE_LEFT
            elif self.change_x > 0 < len(self.walk_right_textures) and self.state != FACE_RIGHT:
                self.state = FACE_RIGHT
            elif self.change_y < 0 < len(self.walk_down_textures) and self.state != FACE_DOWN:
                self.state = FACE_DOWN
            elif self.change_y > 0 < len(self.walk_up_textures) and self.state != FACE_UP:
                self.state = FACE_UP
            else:
                change_direction = False

            # if not moving, load first texture from walk textures (in place of standing textures)
            if self.change_x == 0 and self.change_y == 0:
                if self.state == FACE_LEFT:
                    self.texture = self.walk_left_textures[0]
                elif self.state == FACE_RIGHT:
                    self.texture = self.walk_right_textures[0]
                elif self.state == FACE_UP:
                    self.texture = self.walk_up_textures[0]
                elif self.state == FACE_DOWN:
                    self.texture = self.walk_down_textures[0]

            elif change_direction or distance >= self.texture_change_distance:
                self.last_texture_change_center_x = self.center_x
                self.last_texture_change_center_y = self.center_y

                if self.state == FACE_LEFT:
                    texture_list = self.walk_left_textures
                elif self.state == FACE_RIGHT:
                    texture_list = self.walk_right_textures
                elif self.state == FACE_UP:
                    texture_list = self.walk_up_textures
                elif self.state == FACE_DOWN:
                    texture_list = self.walk_down_textures

                if len(texture_list) == 0:
                    raise RuntimeError("error loading walk animations in player update_animation")

                # check if done playing the texture
                self.cur_texture_index += 1
                if self.cur_texture_index >= len(texture_list):
                    self.cur_texture_index = 0

                self.texture = texture_list[self.cur_texture_index]


# use this function to setup a Player Character
def setup_character(scl, cent_x, cent_y) -> PlayerCharacter:
    character = PlayerCharacter(scale=scl, center_x=cent_x, center_y=cent_y)

    # get sprite sheet path
    sprite_sheet_path = pathlib.Path.cwd() / 'Assets' / 'Characters' / 'hero_character_1.png'

    character_frame_width = 64
    character_frame_height = 64

    # load walking textures
    for image_num in range(9):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * character_frame_width,
                                    character_frame_height * 8, height=character_frame_height,
                                    width=character_frame_width)
        character.walk_up_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * character_frame_width,
                                    character_frame_height * 9, height=character_frame_height,
                                    width=character_frame_width)
        character.walk_left_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * character_frame_width,
                                    character_frame_height * 10, height=character_frame_height,
                                    width=character_frame_width)
        character.walk_down_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * character_frame_width,
                                    character_frame_height * 11, height=character_frame_height,
                                    width=character_frame_width)
        character.walk_right_textures.append(frame)

    # load attack textures
    for image_num in range(13):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * character_frame_width,
                                    character_frame_height * 16, height=character_frame_height,
                                    width=character_frame_width)
        character.spear_up_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * character_frame_width,
                                    character_frame_height * 17, height=character_frame_height,
                                    width=character_frame_width)
        character.spear_left_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * character_frame_width,
                                    character_frame_height * 18, height=character_frame_height,
                                    width=character_frame_width)
        character.spear_down_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * character_frame_width,
                                    character_frame_height * 19, height=character_frame_height,
                                    width=character_frame_width)
        character.spear_right_textures.append(frame)

    return character
