import pathlib
import arcade
import math
from typing import List
from arcade.draw_commands import Texture

FACE_LEFT = 0
FACE_RIGHT = 1
FACE_UP = 2
FACE_DOWN = 3

ROAM = 1
ATTACK = 2

GOLEM_FRAME_WIDTH = 64
GOLEM_FRAME_HEIGHT = 64


class GolemEnemy(arcade.AnimatedWalkingSprite):
    def __init__(self, scale: float, center_x: float, center_y: float):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.move_state = ROAM
        self.health = 3

        self.walk_left_textures = []
        self.walk_right_textures = []
        self.walk_down_textures = []
        self.walk_up_textures = []

        self.character_x_loc = 0
        self.character_y_loc = 0
        
        self.attacking_textures = []

        self.state = FACE_LEFT
        self.cur_texture_index = 0

    def update(self):
        if self.move_state == ROAM:
            if self.state == FACE_LEFT:
                self.change_x = -1
            elif self.state == FACE_RIGHT:
                self.change_x = 1
            elif self.state == FACE_UP:
                self.change_y = 1
            elif self.state == FACE_DOWN:
                self.change_y = -1
            if self.center_x < 64 or self.center_x > 64 * 14:
                self.change_x *= -1
            elif self.center_y < 64 or self.center_y > 64 * 14:
                self.change_y *= -1
        elif self.move_state == ATTACK:
            if self.center_x != self.character_x_loc:
                self.change_y = 0
                if self.center_x < self.character_x_loc:
                    self.change_x = 2
                elif self.center_x > self.character_x_loc:
                    self.change_x = -2
            else:
                self.change_x = 0
                if self.center_y < self.character_y_loc:
                    self.change_y = 2
                elif self.center_y >= self.character_y_loc:
                    self.change_y = -2

        self.center_x += self.change_x
        self.center_y += self.change_y

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
            
            
def setup_golem(scl, change_x, change_y, cent_x, cent_y):
    golem = GolemEnemy(scale=scl, center_x=cent_x, center_y=cent_y)
    
    walking_sprite_sheet = pathlib.Path.cwd() / 'Assets' / 'Enemies' / 'Golem' / 'golem-walk.png'

    for image_num in range(1, 7, 1):
        frame = arcade.load_texture(str(walking_sprite_sheet), image_num * GOLEM_FRAME_WIDTH,
                                    GOLEM_FRAME_HEIGHT * 0, height=GOLEM_FRAME_HEIGHT,
                                    width=GOLEM_FRAME_WIDTH)
        frame.width = frame.width * scl
        frame.height = frame.height * scl
        # print(f'scaled: {image_num}')
        golem.walk_up_textures.append(frame)

        frame = arcade.load_texture(str(walking_sprite_sheet), image_num * GOLEM_FRAME_WIDTH,
                                    GOLEM_FRAME_HEIGHT * 1, height=GOLEM_FRAME_HEIGHT,
                                    width=GOLEM_FRAME_WIDTH)
        frame.width = frame.width * scl
        frame.height = frame.height * scl
        # print(f'scaled: {image_num}')
        golem.walk_left_textures.append(frame)

        frame = arcade.load_texture(str(walking_sprite_sheet), image_num * GOLEM_FRAME_WIDTH,
                                    GOLEM_FRAME_HEIGHT * 2, height=GOLEM_FRAME_HEIGHT,
                                    width=GOLEM_FRAME_WIDTH)
        frame.width = frame.width * scl
        frame.height = frame.height * scl
        # print(f'scaled: {image_num}')
        golem.walk_down_textures.append(frame)

        frame = arcade.load_texture(str(walking_sprite_sheet), image_num * GOLEM_FRAME_WIDTH,
                                    GOLEM_FRAME_HEIGHT * 3, height=GOLEM_FRAME_HEIGHT,
                                    width=GOLEM_FRAME_WIDTH)
        frame.width = frame.width * scl
        frame.height = frame.height * scl
        # print(f'scaled: {image_num}')
        golem.walk_right_textures.append(frame)

    golem.change_x = change_x
    golem.change_y = change_y
    return golem
