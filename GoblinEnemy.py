import math
import pathlib
from typing import List

import arcade
from arcade.draw_commands import Texture

from Enemy import Enemy


class GoblinEnemy(Enemy):
    """One of the 2 enemy types that appear in Cave 1. Has 1 health and deals 1 damage to the player."""
    def __init__(self, scale, center_x, center_y, health, init_range, change_x, change_y):
        super().__init__(scale, center_x, center_y, health, init_range, change_x, change_y)

    def update_animation(self, delta_time=1/10):
        """
        Logic for selecting the proper texture to use.
        """

        texture_list: List[Texture] = []

        x1 = self.center_x
        x2 = self.last_texture_change_center_x
        y1 = self.center_y
        y2 = self.last_texture_change_center_y
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        change_direction = True
        if self.direction == self.MOVING_LEFT and 0 < len(self.walk_left_textures) and self.state != self.FACE_LEFT:
            self.state = self.FACE_LEFT
        elif self.direction == self.MOVING_RIGHT and 0 < len(self.walk_right_textures) and self.state != self.FACE_RIGHT:
            self.state = self.FACE_RIGHT
        elif self.direction == self.MOVING_DOWN and 0 < len(self.walk_down_textures) and self.state != self.FACE_DOWN:
            self.state = self.FACE_DOWN
        elif self.direction == self.MOVING_UP and 0 < len(self.walk_up_textures) and self.state != self.FACE_UP:
            self.state = self.FACE_UP
        else:
            change_direction = False

        # if not moving, load first texture from walk textures (in place of standing textures)
        if self.change_x == 0 and self.change_y == 0:
            if self.state == self.FACE_LEFT:
                self.texture = self.walk_left_textures[0]
            elif self.state == self.FACE_RIGHT:
                self.texture = self.walk_right_textures[0]
            elif self.state == self.FACE_UP:
                self.texture = self.walk_up_textures[0]
            elif self.state == self.FACE_DOWN:
                self.texture = self.walk_down_textures[0]

        elif change_direction or distance >= self.texture_change_distance:
            self.last_texture_change_center_x = self.center_x
            self.last_texture_change_center_y = self.center_y

            if self.state == self.FACE_LEFT:
                texture_list = self.walk_left_textures
            elif self.state == self.FACE_RIGHT:
                texture_list = self.walk_right_textures
            elif self.state == self.FACE_UP:
                texture_list = self.walk_up_textures
            elif self.state == self.FACE_DOWN:
                texture_list = self.walk_down_textures

            if len(texture_list) == 0:
                raise RuntimeError("error loading walk animations in goblin update_animation")

            # check if done playing the texture
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0

            self.texture = texture_list[self.cur_texture_index]


def setup_goblin(scl, cent_x, cent_y, drop, health, init_range, change_x, change_y):
    goblin = GoblinEnemy(scl, cent_x, cent_y, health, init_range, change_x, change_y)

    # get sprite sheet path
    sprite_sheet_path = pathlib.Path.cwd() / 'Assets' / 'Enemies' / 'goblinsword.png'

    goblin_frame_width = 64
    goblin_frame_height = 64

    for image_num in range(7):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * goblin_frame_width,
                                    goblin_frame_height * 3, height=goblin_frame_height,
                                    width=goblin_frame_width)
        goblin.walk_left_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * goblin_frame_width,
                                    goblin_frame_height * 1, height=goblin_frame_height,
                                    width=goblin_frame_width)
        goblin.walk_right_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * goblin_frame_width,
                                    goblin_frame_height * 2, height=goblin_frame_height,
                                    width=goblin_frame_width)
        goblin.walk_up_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * goblin_frame_width,
                                    goblin_frame_height * 0, height=goblin_frame_height,
                                    width=goblin_frame_width)
        goblin.walk_down_textures.append(frame)

    goblin.drops[0] = drop
    goblin.texture = goblin.walk_left_textures[0]
    return goblin
