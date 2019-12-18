import math
import pathlib
from typing import List

import arcade
from arcade.draw_commands import Texture

from Enemy import Enemy


class WyvernEnemy(Enemy):
    """One of the 2 enemy types that appear in Cave 1. Has 2 health and deals 1 damage to the player."""
    def __init__(self, scale: float, center_x: float, center_y: float, health: int, init_range: int, change_x, change_y, speed: int):
        super().__init__(scale, center_x, center_y, health, init_range, change_x, change_y, speed)

        self.walking_x = 0
        self.walking_y = 0

        self.cur_texture_index = 0
        self.drop = None
        self.attacking = False

    def update_animation(self, delta_time=1/30):
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
        if self.change_x < 0 < len(self.walk_left_textures) and self.state != self.FACE_LEFT:
            self.state = self.FACE_LEFT
        elif self.change_x > 0 < len(self.walk_right_textures) and self.state != self.FACE_RIGHT:
            self.state = self.FACE_RIGHT
        elif self.change_y < 0 < len(self.walk_down_textures) and self.state != self.FACE_DOWN:
            self.state = self.FACE_DOWN
        elif self.change_y > 0 < len(self.walk_up_textures) and self.state != self.FACE_UP:
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
                raise RuntimeError("error loading walk animations in wyvern update_animation")

            # check if done playing the texture
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0

            self.texture = texture_list[self.cur_texture_index]


def setup_wyvern(scl, cent_x, cent_y, drop, health, init_range, change_x, change_y, speed):
    wyvern = WyvernEnemy(scl, cent_x, cent_y, health, init_range, change_x, change_y, speed)
    
    # get sprite sheet paths
    left_textures_path = pathlib.Path.cwd() / 'Assets' / 'Enemies' / 'Wyvern' / 'reddragonfly_l.png'
    right_textures_path = pathlib.Path.cwd() / 'Assets' / 'Enemies' / 'Wyvern' / 'reddragonfly_r.png'
    up_textures_path = pathlib.Path.cwd() / 'Assets' / 'Enemies' / 'Wyvern' / 'reddragonfly_u.png'
    down_textures_path = pathlib.Path.cwd() / 'Assets' / 'Enemies' / 'Wyvern' / 'reddragonfly_d.png'

    wyvern_frame_width = 164
    wyvern_frame_height = 128

    for image_row in range(2):
        for image_col in range(4):
            frame = arcade.load_texture(str(left_textures_path), image_col * wyvern_frame_width,
                                        wyvern_frame_height * image_row, height=wyvern_frame_height,
                                        width=wyvern_frame_width)
            wyvern.walk_left_textures.append(frame)
    
            frame = arcade.load_texture(str(right_textures_path), image_col * wyvern_frame_width,
                                        wyvern_frame_height * image_row, height=wyvern_frame_height,
                                        width=wyvern_frame_width)
            wyvern.walk_right_textures.append(frame)
    
            frame = arcade.load_texture(str(up_textures_path), image_col * wyvern_frame_width,
                                        wyvern_frame_height * image_row, height=wyvern_frame_height,
                                        width=wyvern_frame_width)
            wyvern.walk_up_textures.append(frame)
    
            frame = arcade.load_texture(str(down_textures_path), image_col * wyvern_frame_width,
                                        wyvern_frame_height * image_row, height=wyvern_frame_height,
                                        width=wyvern_frame_width)
            wyvern.walk_down_textures.append(frame)

    wyvern.drop = drop
    return wyvern
