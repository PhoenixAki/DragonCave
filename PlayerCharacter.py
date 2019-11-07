import arcade
import math
from typing import List
from arcade.draw_commands import Texture

FACE_LEFT = 0
FACE_RIGHT = 1
FACE_UP = 2
FACE_DOWN = 3

CHARACTER_FRAME_WIDTH = 64
CHARACTER_FRAME_HEIGHT = 64


class PlayerCharacter(arcade.AnimatedWalkingSprite):
    def __init__(self, scale: float, center_x: float, center_y: float):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.attacking = False

        self.money = 0
        self.arrows = 20
        self.boots = False
        self.magic_book = False

        self.cur_texture_index = 0
        self.state = FACE_UP

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
def setup_character(sprite_sheet_path, scl, cent_x, cent_y) -> PlayerCharacter:
    character = PlayerCharacter(scale=scl, center_x=cent_x, center_y=cent_y)

    # load walking textures
    for image_num in range(9):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 8, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.walk_up_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 9, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.walk_left_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 10, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.walk_down_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 11, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.walk_right_textures.append(frame)

    # load attack textures
    for image_num in range(13):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 16, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.spear_up_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 17, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.spear_left_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 18, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.spear_down_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 19, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.spear_right_textures.append(frame)

    return character

