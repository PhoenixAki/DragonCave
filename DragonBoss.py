import pathlib
import arcade
import math
from typing import List
from arcade.draw_commands import Texture

FACE_LEFT = 0
FACE_RIGHT = 1


class DragonBoss(arcade.AnimatedWalkingSprite):
    def __init__(self, scale: float, center_x: float, center_y: float):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.walk_left_textures = []
        self.walk_right_textures = []
        
        self.bite_attack_textures = []

        self.state = None
        self.cur_texture_index = 0
        
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x < 64 * 6 or self.center_x > 64 * 13:
            self.change_x *= -1

    def update_animation(self, delta_time: float = 1 / 30):
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
        if self.change_x < 0 < len(self.walk_left_textures) and self.state != FACE_LEFT:
            self.state = FACE_LEFT
        elif self.change_x > 0 < len(self.walk_right_textures) and self.state != FACE_RIGHT:
            self.state = FACE_RIGHT
        else:
            change_direction = False

        # if not moving, load first texture from walk textures (in place of standing textures)
        if self.change_x == 0 and self.change_y == 0:
            if self.state == FACE_LEFT:
                self.texture = self.walk_left_textures[0]
            elif self.state == FACE_RIGHT:
                self.texture = self.walk_right_textures[0]

        elif change_direction or distance >= self.texture_change_distance:
            self.last_texture_change_center_x = self.center_x
            self.last_texture_change_center_y = self.center_y

            if self.state == FACE_LEFT:
                texture_list = self.walk_left_textures
            elif self.state == FACE_RIGHT:
                texture_list = self.walk_right_textures

            if len(texture_list) == 0:
                raise RuntimeError("error loading walk animations in goblin update_animation")

            # check if done playing the texture
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0

            self.texture = texture_list[self.cur_texture_index]


def setup_dragon_boss(scl, change_x, change_y, cent_x, cent_y):

    dragon = DragonBoss(scale=scl, center_x=cent_x, center_y=cent_y)

    # setup walking sprites
    path = pathlib.Path.cwd() / 'Assets' / 'Enemies' / 'DragonBoss' / 'Walking_Tiles'
    all_files = path.glob('*.png')  # return a generator with all the qualified paths to all png files in dir
    textures = []
    for file_path in all_files:
        frame = arcade.load_texture(str(file_path))  # we want the whole image
        # scale
        frame.width = frame.width * scl
        frame.height = frame.height * scl
        dragon.walk_left_textures.append(frame)
    # print(textures)
    for file_path in reversed(list(all_files)):
        frame = arcade.load_texture(str(file_path))  # we want the whole image
        # scale
        frame.width = frame.width * scl
        frame.height = frame.height * scl
        dragon.walk_right_textures.append(frame)

    dragon.change_x = change_x
    dragon.change_y = change_y

    return dragon
