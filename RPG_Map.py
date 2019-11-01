from enum import Enum, auto
import arcade
import pathlib
from PlayerCharacter import setup_character

CHARACTER_FRAME_WIDTH = 64
CHARACTER_FRAME_HEIGHT = 64

FACE_RIGHT = 1
FACE_LEFT = 2
FACE_UP = 3
FACE_DOWN = 4


class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Projectile(arcade.Sprite):
    def __init__(self, img_path: str, speed: int, direction: int, game_window):
        super().__init__(img_path)
        self.speed = speed
        self.direction = direction
        self.game = game_window

    def move(self):
        if self.direction == FACE_UP:
            self.center_y += self.speed
        elif self.direction == FACE_DOWN:
            self.center_y -= self.speed
        elif self.direction == FACE_LEFT:
            self.center_x -= self.speed
        elif self.direction == FACE_RIGHT:
            self.center_x += self.speed
        else:  # should be MoveEnum.NONE
            pass


class Map(arcade.Window):
    def __init__(self):
        super().__init__(960, 960, "Dragoncave")
        self.map_location = pathlib.Path.cwd() / 'Assets' / 'opening_map.tmx'
        self.maplist = None
        self.wall_list = None
        self.simple_Physics = None

        # : arcade.Sprite
        self.up_arrow_sprite_path = None
        self.down_arrow_sprite_path = None
        self.left_arrow_sprite_path = None
        self.right_arrow_sprite_path = None

        # : arcade.AnimatedWalkingSprite
        self.character = None
        # : arcade.SpriteLists
        self.char_list = None
        self.character_projectile_list = None
        self.moveSpeed = 2

        self.frame_time = 0

    def setup(self):
        # tile maps setup ----------
        sample__map = arcade.tilemap.read_tmx(str(self.map_location))
        self.maplist = arcade.tilemap.process_layer(sample__map, "floor_layer", 1)
        self.wall_list = arcade.tilemap.process_layer(sample__map, "walls_layer", 1)

        # character setup ----------
        hero_sprite_sheet_path = pathlib.Path.cwd() / 'Assets' / 'Characters' / 'hero_character_1.png'
        self.character = setup_character(hero_sprite_sheet_path, 1, 200, 150)

        # projectiles setups
        self.up_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'up_arrow.png'
        self.down_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'down_arrow.png'
        self.left_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'left_arrow.png'
        self.right_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'right_arrow.png'

        # setup projectile lists
        self.character_projectile_list = arcade.SpriteList()

        # setup character list
        self.char_list = arcade.SpriteList()
        self.char_list.append(self.character)

        # setup physics engine
        self.simple_Physics = arcade.PhysicsEngineSimple(self.character, self.wall_list)

    def on_update(self, delta_time: float):

        # character projectiles
        if self.character_projectile_list:
            for character_projectile in self.character_projectile_list:
                character_projectile.move()

        # check for projectile collisions with "wall_layer" and off screen
        # @@@@@@@@@@@@@@@@MAKE THIS GENERIC TO HOLD ANY PROJECTILE LIST@@@@@@@@@@@@
        [proj.kill() for proj in self.character_projectile_list
         if arcade.check_for_collision_with_list(proj, self.wall_list)]
        [proj.kill() for proj in self.character_projectile_list
         if proj.center_x < -50 or proj.center_x > 1010 or proj.center_y < -50 or proj.center_y > 1010]

        # character
        self.frame_time += delta_time
        if self.frame_time > 0.035:  # play with this, 20 times per second isn’t totally smooth
            self.char_list.update()
            self.char_list.update_animation()
            self.frame_time = 0

        self.simple_Physics.update()

    def on_draw(self):
        arcade.start_render()
        self.maplist.draw()
        self.wall_list.draw()

        self.char_list.draw()

        self.character_projectile_list.draw()

    def on_key_press(self, key: int, modifiers: int):
        if not self.character.attacking:
            if key == arcade.key.UP or key == arcade.key.W:
                self.character.change_y = self.moveSpeed
                self.character.change_x = 0
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.character.change_y = -self.moveSpeed
                self.character.change_x = 0
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.character.change_x = -self.moveSpeed
                self.character.change_y = 0
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.character.change_x = self.moveSpeed
                self.character.change_y = 0
            elif key == arcade.key.SPACE and self.character.change_x == 0 and self.character.change_y == 0:
                self.character.attacking = True
                # shoot arrow
                # arcade.schedule(self.character_arrow_shoot, 0.5)
                self.character_arrow_shoot()

    def on_key_release(self, key: int, modifiers: int):
        if self.character.change_y > 0 and (key == arcade.key.UP or key == arcade.key.W):
            self.character.change_y = 0
        elif self.character.change_y < 0 and (key == arcade.key.DOWN or key == arcade.key.S):
            self.character.change_y = 0
        elif self.character.change_x < 0 and (key == arcade.key.LEFT or key == arcade.key.A):
            self.character.change_x = 0
        elif self.character.change_x > 0 and (key == arcade.key.RIGHT or key == arcade.key.D):
            self.character.change_x = 0

    # ---------------------Window Class Utility Functions ---------------------------

    def character_arrow_shoot(self):

        if self.character.state == FACE_UP:
            new_arrow_sprite = Projectile(self.up_arrow_sprite_path, speed=10, direction=self.character.state,
                                          game_window=self)
            new_arrow_sprite.center_y = self.character.center_y
            new_arrow_sprite.center_x = self.character.center_x
            self.character_projectile_list.append(new_arrow_sprite)
        elif self.character.state == FACE_DOWN:
            new_arrow_sprite = Projectile(self.down_arrow_sprite_path, speed=10, direction=self.character.state,
                                          game_window=self)
            new_arrow_sprite.center_y = self.character.center_y
            new_arrow_sprite.center_x = self.character.center_x
            self.character_projectile_list.append(new_arrow_sprite)
        elif self.character.state == FACE_LEFT:
            new_arrow_sprite = Projectile(self.left_arrow_sprite_path, speed=10, direction=self.character.state,
                                          game_window=self)
            new_arrow_sprite.center_y = self.character.center_y
            new_arrow_sprite.center_x = self.character.center_x
            self.character_projectile_list.append(new_arrow_sprite)
        elif self.character.state == FACE_RIGHT:
            new_arrow_sprite = Projectile(self.right_arrow_sprite_path, speed=10, direction=self.character.state,
                                          game_window=self)
            new_arrow_sprite.center_y = self.character.center_y
            new_arrow_sprite.center_x = self.character.center_x
            self.character_projectile_list.append(new_arrow_sprite)

# -------- UTILITY FUNCTIONS --------------------


