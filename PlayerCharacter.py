import arcade
import math
from typing import List
from arcade.draw_commands import Texture

FACE_RIGHT = 0
FACE_LEFT = 1
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

        # attack textures
        self.spear_attack_left_textures = []
        self.spear_attack_right_textures = []
        self.spear_attack_down_textures = []
        self.spear_attack_up_textures = []

    def update_animation(self, delta_time: float = 1 / 60):
        """
        Logic for selecting the proper texture to use.
        """

        texture_list: List[Texture] = []

        if self.attacking:
            if self.state == FACE_LEFT:
                texture_list = self.spear_attack_left_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError("update_animation was called on a sprite that doesn't have a "
                                       "list of walk left textures.")
            elif self.state == FACE_RIGHT:
                texture_list = self.spear_attack_right_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError("update_animation was called on a sprite that doesn't have a list of "
                                       "walk right textures.")
            elif self.state == FACE_UP:
                texture_list = self.spear_attack_up_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError("update_animation was called on a sprite that doesn't have a list of "
                                       "walk up textures.")
            elif self.state == FACE_DOWN:
                texture_list = self.spear_attack_down_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError(
                        "update_animation was called on a sprite that doesn't have a list of walk down textures.")

            self.cur_texture_index += 1
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0
                self.attacking = False

            self.texture = texture_list[self.cur_texture_index]

            if self._texture is None:
                print("Error, no texture set")
            else:
                self.width = self._texture.width * self.scale
                self.height = self._texture.height * self.scale

        else:
            x1 = self.center_x
            x2 = self.last_texture_change_center_x
            y1 = self.center_y
            y2 = self.last_texture_change_center_y
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            change_direction = False
            if self.change_x > 0 \
                    and self.change_y == 0 \
                    and self.state != FACE_RIGHT \
                    and len(self.walk_right_textures) > 0:
                self.state = FACE_RIGHT
                change_direction = True
            elif self.change_x < 0 and self.change_y == 0 and self.state != FACE_LEFT \
                    and len(self.walk_left_textures) > 0:
                self.state = FACE_LEFT
                change_direction = True
            elif self.change_y < 0 and self.change_x == 0 and self.state != FACE_DOWN \
                    and len(self.walk_down_textures) > 0:
                self.state = FACE_DOWN
                change_direction = True
            elif self.change_y > 0 and self.change_x == 0 and self.state != FACE_UP \
                    and len(self.walk_up_textures) > 0:
                self.state = FACE_UP
                change_direction = True

            if self.change_x == 0 and self.change_y == 0:
                if self.state == FACE_LEFT:
                    self.texture = self.stand_left_textures[0]
                elif self.state == FACE_RIGHT:
                    self.texture = self.stand_right_textures[0]
                elif self.state == FACE_UP:
                    self.texture = self.walk_up_textures[0]
                elif self.state == FACE_DOWN:
                    self.texture = self.walk_down_textures[0]

            elif change_direction or distance >= self.texture_change_distance:
                self.last_texture_change_center_x = self.center_x
                self.last_texture_change_center_y = self.center_y

                if self.state == FACE_LEFT:
                    texture_list = self.walk_left_textures
                    if texture_list is None or len(texture_list) == 0:
                        raise RuntimeError("update_animation was called on a sprite that doesn't have a "
                                           "list of walk left textures.")
                elif self.state == FACE_RIGHT:
                    texture_list = self.walk_right_textures
                    if texture_list is None or len(texture_list) == 0:
                        raise RuntimeError("update_animation was called on a sprite that doesn't have a list of "
                                           "walk right textures.")
                elif self.state == FACE_UP:
                    texture_list = self.walk_up_textures
                    if texture_list is None or len(texture_list) == 0:
                        raise RuntimeError("update_animation was called on a sprite that doesn't have a list of "
                                           "walk up textures.")
                elif self.state == FACE_DOWN:
                    texture_list = self.walk_down_textures
                    if texture_list is None or len(texture_list) == 0:
                        raise RuntimeError(
                            "update_animation was called on a sprite that doesn't have a list of walk down textures.")

                self.cur_texture_index += 1
                if self.cur_texture_index >= len(texture_list):
                    self.cur_texture_index = 0

                self.texture = texture_list[self.cur_texture_index]

            if self._texture is None:
                print("Error, no texture set")
            else:
                self.width = self._texture.width * self.scale
                self.height = self._texture.height * self.scale


# use this function to setup a Player Character
def setup_character(sprite_sheet_path, scl, cent_x, cent_y) -> PlayerCharacter:
    character = PlayerCharacter(scale=scl, center_x=cent_x, center_y=cent_y)

    # character standing left/right frames setup
    frame = arcade.load_texture(str(sprite_sheet_path), 0, CHARACTER_FRAME_HEIGHT * 9,
                                height=CHARACTER_FRAME_HEIGHT,
                                width=CHARACTER_FRAME_WIDTH)
    character.stand_left_textures = []
    character.stand_left_textures.append(frame)

    frame = arcade.load_texture(str(sprite_sheet_path), 0, CHARACTER_FRAME_HEIGHT * 11,
                                height=CHARACTER_FRAME_HEIGHT,
                                width=CHARACTER_FRAME_WIDTH)
    character.stand_right_textures = []
    character.stand_right_textures.append(frame)

    # no stand up and stand down textures??

    # setup main character textures
    character.texture = frame

    character.walk_left_textures = []
    character.walk_right_textures = []
    character.walk_down_textures = []
    character.walk_up_textures = []

    character.spear_attack_left_textures = []
    character.spear_attack_right_textures = []
    character.spear_attack_down_textures = []
    character.spear_attack_up_textures = []

    for image_num in range(9):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 8, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.walk_up_textures.append(frame)
    for image_num in range(9):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 9, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.walk_left_textures.append(frame)
    for image_num in range(9):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 10, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.walk_down_textures.append(frame)
    for image_num in range(9):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 11, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.walk_right_textures.append(frame)

    # attacking textures
    for image_num in range(13):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 16, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.spear_attack_up_textures.append(frame)
    for image_num in range(13):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 17, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.spear_attack_left_textures.append(frame)
    for image_num in range(13):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 18, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.spear_attack_down_textures.append(frame)
    for image_num in range(13):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 19, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        character.spear_attack_right_textures.append(frame)

    return character
