from enum import Enum, auto
import arcade
import pathlib
import PlayerCharacter
import GoblinEnemy
from Projectile import Projectile

FACE_LEFT = 0
FACE_RIGHT = 1
FACE_UP = 2
FACE_DOWN = 3


class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Map(arcade.Window):
    def __init__ (self):
        super().__init__(960, 960, "Dragoncave")
        # initialize tile maps
        self.map_location = pathlib.Path.cwd() / 'Assets' / 'Forest.tmx'
        self.floor_list = None
        self.wall_list = None

        # initialize sprites
        self.up_arrow_sprite_path = None
        self.down_arrow_sprite_path = None
        self.left_arrow_sprite_path = None
        self.right_arrow_sprite_path = None
        self.arrow_sprites = None

        # initialize character
        self.character = None
        self.char_list = None
        self.character_projectile_list = None
        self.character_speed = 2

        # initialize physics engine
        self.simple_Physics = None

        # timer to control framerate
        self.frame_time = 0

    def setup (self):
        # setup tile maps
        sample__map = arcade.tilemap.read_tmx(str(self.map_location))
        self.floor_list = arcade.tilemap.process_layer(sample__map, "floor_layer", 1)
        self.wall_list = arcade.tilemap.process_layer(sample__map, "walls_layer", 1)

        # setup character
        hero_sprite_sheet_path = pathlib.Path.cwd() / 'Assets' / 'Characters' / 'hero_character_1.png'
        self.character = PlayerCharacter.setup_character(hero_sprite_sheet_path, 1, 200, 150)
        self.char_list = arcade.SpriteList()
        self.char_list.append(self.character)
        self.character_projectile_list = arcade.SpriteList()

        # setup projectiles
        self.left_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'left_arrow.png'
        self.right_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'right_arrow.png'
        self.up_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'up_arrow.png'
        self.down_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'down_arrow.png'
        self.arrow_sprites = [ self.left_arrow_sprite_path, self.right_arrow_sprite_path,
                               self.up_arrow_sprite_path, self.down_arrow_sprite_path ]

        # setup physics engine
        self.simple_Physics = arcade.PhysicsEngineSimple(self.character, self.wall_list)

        # test goblins
        goblin_sheet_path = pathlib.Path.cwd() / 'Assets' / 'Enemies' / 'goblinsword.png'
        self.goblin_1 = GoblinEnemy.setup_goblin(goblin_sheet_path, 1, 200, 400)
        self.goblin_2 = GoblinEnemy.setup_goblin(goblin_sheet_path, 1, 300, 600)
        self.goblin_3 = GoblinEnemy.setup_goblin(goblin_sheet_path, 1, 400, 600)
        self.goblin_4 = GoblinEnemy.setup_goblin(goblin_sheet_path, 1, 500, 600)
        self.goblin_1.change_x = 2
        self.goblin_2.change_y = -2
        self.goblin_3.change_x = -2
        self.goblin_4.change_y = 2
        self.goblin_list = arcade.SpriteList()
        self.goblin_list.append(self.goblin_1)
        self.goblin_list.append(self.goblin_2)
        self.goblin_list.append(self.goblin_3)
        self.goblin_list.append(self.goblin_4)

    def on_update (self, delta_time: float):

        self.frame_time += delta_time
        if self.frame_time > 1 / 30:  # 30fps for now?
            self.char_list.update()
            self.char_list.update_animation()

            if self.map_location == pathlib.Path.cwd() / 'Assets' / 'Forest.tmx':
                pass
                # -- Sethia do stuff here
                # -- if character is on cave entrance:
                # --set self.map_location to opening_map.txp and change location of character to the entrance of the
                # dungeon
            # self.character.center_x = 480 * (64[ 0 ] * 0.50) + 64 / 2
            # self.character.center_y = (960 - 480 - 1) * (
            # 64[ 1 ] * 0.50) + 64 / 2
            # self.character_list.update()
            # refer to the block comment at the end of the code :)

            elif self.map_location == pathlib.Path.cwd() / 'Assets' / 'opening_map.tmx':
                self.goblin_list.update()
                self.goblin_list.update_animation()

            self.frame_time = 0

        # check for collisions
        self.simple_Physics.update()

        # move player projectiles
        for character_projectile in self.character_projectile_list:
            character_projectile.move()

        # check for projectile collisions with "wall_layer" and off screen
        # @@@@@@@@@@@@@@@@MAKE THIS GENERIC TO HOLD ANY PROJECTILE LIST@@@@@@@@@@@@
        [ proj.kill() for proj in self.character_projectile_list
          if arcade.check_for_collision_with_list(proj, self.wall_list) ]
        [ proj.kill() for proj in self.character_projectile_list
          if proj.center_x < -50 or proj.center_x > 1010 or proj.center_y < -50 or proj.center_y > 1010 ]

        # check for room-specific stuff

    def on_draw (self):
        arcade.start_render()
        self.floor_list.draw()
        self.wall_list.draw()
        self.char_list.draw()
        self.character_projectile_list.draw()

        if self.map_location == pathlib.Path.cwd() / 'Assets' / 'Forest.tmx':
            pass
            # sethia do stuff here



        elif self.map_location == pathlib.Path.cwd() / 'Assets' / 'opening_map.tmx':
            self.goblin_list.draw()

    def on_key_press (self, key: int, modifiers: int):
        if not self.character.attacking:
            if key == arcade.key.UP or key == arcade.key.W:
                self.character.change_y = self.character_speed
                self.character.change_x = 0
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.character.change_y = -self.character_speed
                self.character.change_x = 0
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.character.change_x = -self.character_speed
                self.character.change_y = 0
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.character.change_x = self.character_speed
                self.character.change_y = 0
            elif key == arcade.key.SPACE:
                self.character.change_x = 0
                self.character.change_y = 0
                self.character.attacking = True
                self.character_arrow_shoot()
            elif key == arcade.key.ESCAPE:
                self.close()

    def on_key_release (self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
            self.character.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
            self.character.change_x = 0

    # ---------------------Window Class Utility Functions ---------------------------

    def character_arrow_shoot (self):

        new_arrow_sprite = Projectile(self.arrow_sprites[ self.character.state ], speed=10,
                                      direction=self.character.state, game_window=self)
        new_arrow_sprite.center_y = self.character.center_y
        new_arrow_sprite.center_x = self.character.center_x
        self.character_projectile_list.append(new_arrow_sprite)


'''
    def get_money (self):

        new_balance = PlayerCharacter.money + 50
        return new_balance

    def get_current_money(self):

        return PlayerCharacter.money

    def get_arrows(self):

        return PlayerCharacter.arrows

    # should be a dialogue that asks if player wants to buy an item or not. If yest, then perform actions.

    def buy_item (self):
        if(player chooses arrow):
            new_arrow_count = PlayerCharacter.arrows + 5
            get_current_money() - 25
        elif(current_money < 0): # if money goes below 0
            print("You do not have enough money. Go work.")
        else:
            print("You currently have" + str(PlayerCharacter.arrows() + "arrows"))

    def magic_boot_gain(self):
        if(PlayerCharacter.magic_book == 3):
            "You have reached the max number of books you can carry!"

        elif(If get_current_money() < 0):
            print("You do not have enough money. Go work.")

        # purchasing the book
        else:
            PlayerCharacter.magic_book + 1
            get_current_money() - 10

        return PlayerCharacter.magic_book

class DialogueBox:
    def __init__(self, x, y, width, height, color=None, theme=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = False
        self.button_list = []
        self.text_list = []
        self.theme = theme
        if self.theme:
            self.texture = self.theme.dialogue_box_texture

    def on_draw(self):
        if self.active:
            if self.theme:
                arcade.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.texture)
            else:
                arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)
            for button in self.button_list:
                button.draw()
            for text in self.text_list:
                text.draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        for button in self.button_list:
            button.check_mouse_press(x, y)

    def on_mouse_release(self, x, y, _button, _modifiers):
        for button in self.button_list:
            button.check_mouse_release(x, y)


-----
'''
