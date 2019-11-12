import arcade
import math
from typing import List
from arcade.draw_commands import Texture

FACE_LEFT = 0
FACE_RIGHT = 1
FACE_UP = 2
FACE_DOWN = 3

GOBLIN_FRAME_WIDTH = 64
GOBLIN_FRAME_HEIGHT = 64


class GoblinEnemy(arcade.AnimatedWalkingSprite):
    def __init__(self, scale: float, center_x: float, center_y: float):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.walk_left_textures = []
        self.walk_right_textures = []
        self.walk_down_textures = []
        self.walk_up_textures = []

        self.attack_left_textures = []
        self.attack_right_textures = []
        self.attack_up_textures = []
        self.attack_down_textures = []

        self.walking_x = 0
        self.walking_y = 0

        self.health = 1
        self.state = None
        self.cur_texture_index = 0
        self.texture_list = None
        self.drop = None

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 65 or self.right > 895:
            self.change_x *= -1
            self.walking_x = self.change_x
        elif self.top > 895 or self.bottom < 65:
            self.change_y *= -1
            self.walking_y = self.change_y

    def update_animation(self, delta_time: float = 1/30):
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
                raise RuntimeError("error loading walk animations in goblin update_animation")

            # check if done playing the texture
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0

            self.texture = texture_list[self.cur_texture_index]


def setup_goblin(sprite_sheet_path, scl, change_x, change_y, cent_x, cent_y, drop):
    goblin = GoblinEnemy(scale=scl, center_x=cent_x, center_y=cent_y)

    for image_num in range(7):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * GOBLIN_FRAME_WIDTH,
                                    GOBLIN_FRAME_HEIGHT * 3, height=GOBLIN_FRAME_HEIGHT,
                                    width=GOBLIN_FRAME_WIDTH)
        goblin.walk_left_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * GOBLIN_FRAME_WIDTH,
                                    GOBLIN_FRAME_HEIGHT * 1, height=GOBLIN_FRAME_HEIGHT,
                                    width=GOBLIN_FRAME_WIDTH)
        goblin.walk_right_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * GOBLIN_FRAME_WIDTH,
                                    GOBLIN_FRAME_HEIGHT * 2, height=GOBLIN_FRAME_HEIGHT,
                                    width=GOBLIN_FRAME_WIDTH)
        goblin.walk_up_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * GOBLIN_FRAME_WIDTH,
                                    GOBLIN_FRAME_HEIGHT * 0, height=GOBLIN_FRAME_HEIGHT,
                                    width=GOBLIN_FRAME_WIDTH)
        goblin.walk_down_textures.append(frame)

    for num in range(4):
        image_num = num + 7

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * GOBLIN_FRAME_WIDTH,
                                    GOBLIN_FRAME_HEIGHT * 3, height=GOBLIN_FRAME_HEIGHT,
                                    width=GOBLIN_FRAME_WIDTH)
        goblin.attack_left_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * GOBLIN_FRAME_WIDTH,
                                    GOBLIN_FRAME_HEIGHT * 1, height=GOBLIN_FRAME_HEIGHT,
                                    width=GOBLIN_FRAME_WIDTH)
        goblin.attack_right_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * GOBLIN_FRAME_WIDTH,
                                    GOBLIN_FRAME_HEIGHT * 2, height=GOBLIN_FRAME_HEIGHT,
                                    width=GOBLIN_FRAME_WIDTH)
        goblin.attack_up_textures.append(frame)

        frame = arcade.load_texture(str(sprite_sheet_path), image_num * GOBLIN_FRAME_WIDTH,
                                    GOBLIN_FRAME_HEIGHT * 0, height=GOBLIN_FRAME_HEIGHT,
                                    width=GOBLIN_FRAME_WIDTH)
        goblin.attack_down_textures.append(frame)

    goblin.change_x = change_x
    goblin.walking_x = change_x
    goblin.change_y = change_y
    goblin.walking_y = change_y
    goblin.drop = drop
    goblin.texture = goblin.walk_left_textures[0]
    return goblin
