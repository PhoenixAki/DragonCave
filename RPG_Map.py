from enum import Enum, auto
import arcade
import pathlib

CHARACTER_FRAME_WIDTH = 64
CHARACTER_FRAME_HEIGHT = 64

class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Map2(arcade.Window):
    def __init__(self):
        super().__init__(960, 960, "Dragoncave")
        self.map_location = pathlib.Path.cwd() / 'Assets' / 'opening_map.tmx'
        self.maplist = None
        self.wall_list = None
        # self.player = None
        # self.playerList = None
        self.simple_Physics = None

        # : arcade.AnimatedWalkingSprite
        self.character = None
        # : arcade.SpriteList
        self.char_list = None
        self.moveSpeed = 2

    def setup(self):
        sample__map = arcade.tilemap.read_tmx(str(self.map_location))
        self.maplist = arcade.tilemap.process_layer(sample__map, "floor_layer", 1)
        self.wall_list = arcade.tilemap.process_layer(sample__map, "walls_layer", 1)
        # self.player = arcade.Sprite(str(pathlib.Path.cwd() / 'Assets' / 'orc2.png'))
        # self.player.center_x = 160  # in the middle of the second tile
        # self.player.center_y = 224  # middle of the forth tile up
        # self.playerList = arcade.SpriteList()
        # self.playerList.append(self.player)

        # character setup
        path = pathlib.Path.cwd() / 'Assets' / 'Characters' / 'hero_character_1.png'
        self.character = arcade.AnimatedWalkingSprite(scale=1, center_x=200, center_y=150)

        frame = arcade.load_texture(str(path), 0, CHARACTER_FRAME_HEIGHT * 9, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        self.character.stand_left_textures = []
        self.character.stand_left_textures.append(frame)

        frame = arcade.load_texture(str(path), 0, CHARACTER_FRAME_HEIGHT * 11, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        self.character.stand_right_textures = []
        self.character.stand_right_textures.append(frame)

        # no stand up and stand down textures??

        self.character.texture = frame
        self.character.walk_left_textures = []
        self.character.walk_right_textures = []
        self.character.walk_down_textures = []
        self.character.walk_up_textures = []

        for image_num in range(9):
            frame = arcade.load_texture(str(path), image_num * CHARACTER_FRAME_WIDTH, CHARACTER_FRAME_HEIGHT * 8,
                                        height=CHARACTER_FRAME_HEIGHT, width=CHARACTER_FRAME_WIDTH)
            self.character.walk_up_textures.append(frame)
        for image_num in range(9):
            frame = arcade.load_texture(str(path), image_num * CHARACTER_FRAME_WIDTH, CHARACTER_FRAME_HEIGHT * 9,
                                        height=CHARACTER_FRAME_HEIGHT, width=CHARACTER_FRAME_WIDTH)
            self.character.walk_left_textures.append(frame)
        for image_num in range(9):
            frame = arcade.load_texture(str(path), image_num * CHARACTER_FRAME_WIDTH, CHARACTER_FRAME_HEIGHT * 10,
                                        height=CHARACTER_FRAME_HEIGHT, width=CHARACTER_FRAME_WIDTH)
            self.character.walk_down_textures.append(frame)
        for image_num in range(9):
            frame = arcade.load_texture(str(path), image_num * CHARACTER_FRAME_WIDTH, CHARACTER_FRAME_HEIGHT * 11,
                                        height=CHARACTER_FRAME_HEIGHT, width=CHARACTER_FRAME_WIDTH)
            self.character.walk_right_textures.append(frame)

        self.char_list = arcade.SpriteList()
        self.char_list.append(self.character)

        # setup physics engine
        self.simple_Physics = arcade.PhysicsEngineSimple(self.character, self.wall_list)

    def on_update(self, delta_time: float):
        # character
        self.char_list.update()
        self.char_list.update_animation()

        self.simple_Physics.update()

    def on_draw(self):
        arcade.start_render()
        self.maplist.draw()
        self.wall_list.draw()
        # self.playerList.draw()

        self.char_list.draw()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.W:
            self.character.change_y = self.moveSpeed
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.character.change_y = -self.moveSpeed
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.character.change_x = -self.moveSpeed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.character.change_x = self.moveSpeed

    def on_key_release(self, key: int, modifiers: int):
        if self.character.change_y > 0 and (key == arcade.key.UP or key == arcade.key.W):
            self.character.change_y = 0
        elif self.character.change_y < 0 and (key == arcade.key.DOWN or key == arcade.key.S):
            self.character.change_y = 0
        elif self.character.change_x < 0 and (key == arcade.key.LEFT or key == arcade.key.A):
            self.character.change_x = 0
        elif self.character.change_x > 0 and (key == arcade.key.RIGHT or key == arcade.key.D):
            self.character.change_x = 0
