import arcade
import pathlib
import PlayerCharacter
import GoblinEnemy
import WyvernEnemy
import GolemEnemy
from Projectile import Projectile

FACE_LEFT = 0
FACE_RIGHT = 1
FACE_UP = 2
FACE_DOWN = 3

ROAM = 1
ATTACK = 2


class Map(arcade.Window):
    def __init__(self):
        super().__init__(960, 960, "Dragoncave")
        # initialize tile maps and paths
        self.goblin_path = pathlib.Path.cwd() / 'Assets' / 'Enemies' / 'goblinsword.png'
        self.forest_map = pathlib.Path.cwd() / 'Assets' / 'Forest.tmx'
        self.cave_1_map = pathlib.Path.cwd() / 'Assets' / 'Cave_1.tmx'
        self.cave_1_wall_open_map = pathlib.Path.cwd() / 'Assets' / 'Cave_1_wall_open.tmx'
        self.cave_2_map = pathlib.Path.cwd() / 'Assets' / 'Cave_2.tmx'
        self.close_chest_path = pathlib.Path.cwd() / 'Assets' / 'Item_Drops' / 'Chest' / 'Treasure_Chest_closed.png'
        self.open_chest_path = pathlib.Path.cwd() / 'Assets' / 'Item_Drops' / 'Chest' / 'Treasure_Chest_open.png'
        self.current_map = None
        self.current_map_tmx = None
        self.floor_list = None
        self.wall_list = None
        self.entering_cave_1 = False

        # initialize sprites
        self.up_arrow_sprite_path = None
        self.down_arrow_sprite_path = None
        self.left_arrow_sprite_path = None
        self.right_arrow_sprite_path = None
        self.arrow_sprites = None
        self.animated_key = None
        self.chest = None
        self.chest_opened = False
        self.opened_chest_texture = None
        self.animated_crystal = None

        # initialize character + lists
        self.character = None
        self.char_list = None
        self.character_projectile_list = None
        self.character_speed = 2
        self.cave_1_enemy_list = None
        self.goblin_kill_count = 0
        self.golem_list = None

        # dragon boss
        # self.dragonboss = None

        # golem boss
        self.golem_boss = None

        # initialize physics engines
        self.simple_Physics = None
        self.enemy_Physics = None

        # timer to control framerate
        self.frame_time = 0

        # message to print on the screen
        self.display_message = False

    def setup(self):
        self.setup_character()

        # setup tile maps
        self.current_map = self.forest_map
        # read map and process current layers
        self.process_current_tmx_and_layers()

        # setup goblins in cave 1
        self.cave_1_enemy_list = arcade.SpriteList()
        self.setup_cave_1()

        # setup golem boss
        self.golem_list = arcade.SpriteList()
        self.golem_boss = GolemEnemy.setup_golem(1.7, 0, 0, (64 * 7) + 32, 485)
        self.golem_list.append(self.golem_boss)

        self.chest = arcade.Sprite(str(self.close_chest_path), center_x=64 * 13 + 32, center_y=64 * 13 + 32)
        self.opened_chest_texture = arcade.load_texture(str(self.open_chest_path))
        self.chest.append_texture(self.opened_chest_texture)

        self.setup_boss_key()

        self.setup_animated_crystal()

        self.setup_projectiles()

        # setup physics engines
        self.simple_Physics = arcade.PhysicsEngineSimple(self.character, self.wall_list)
        # self.enemy_Physics = EnemyPhysics.EnemyEngineSimple(self.golem_boss, self.wall_list)

    def on_update(self, delta_time: float):

        # FOREST MAP UPDATES ------------
        if self.current_map == self.forest_map:
            self.do_forest_map_updates()

        # CAVE 1 MAP UPDATES --------------
        elif self.current_map == self.cave_1_map:
            self.do_cave1_map_updates()

        # CAVE 1 OPEN DOOR MAP UPDATES -----------
        elif self.current_map == self.cave_1_wall_open_map:
            self.do_cave1_open_door_updates()

        # CAVE 2 MAP UPDATES ------------
        elif self.current_map == self.cave_2_map:
            self.do_cave2_map_updates()

        # ****** BELOW: UPDATES THAT HAPPEN ON EVERY MAP *************
        # these have to happen every time to avoid "Exception: Error: Attempt to draw a sprite without a texture set."
        if self.current_map == self.cave_1_map:
            self.cave_1_enemy_list.update()
            self.cave_1_enemy_list.update_animation()
        elif self.current_map == self.cave_2_map:
            self.golem_list.update()
            self.golem_list.update_animation()
        # update animations using frame rate
        self.frame_time += delta_time
        if self.frame_time > 1 / 30:  # 30fps for now?
            # reset frame timer
            self.frame_time = 0
            # update character
            self.char_list.update()
            self.char_list.update_animation()
        # update key animation if boss dead
        if len(self.golem_list) <= 0 and not self.character.chest_key:
            self.animated_key.update_animation()
        if self.chest_opened:
            self.animated_crystal.update_animation()

        # *********************************************************

        self.simple_Physics.update()

        self.projectile_updates()

        # check if player is dead
        if self.character.health <= 0:
            self.character.kill()
            print("You lose.")
            exit()

    def on_draw(self):
        arcade.start_render()
        self.floor_list.draw()
        self.wall_list.draw()
        self.char_list.draw()

        # draw projectiles
        if len(self.character_projectile_list) > 0:
            self.character_projectile_list.draw()
        # draw forest stuff
        if self.current_map == self.forest_map:
            if self.display_message:
                output = "DEFEAT THE EVIL GOLEM.\nGET HIS KEY.\nRETRIEVE THE SCARED CRYSTAL!"
                arcade.draw_text(output, 10, 510, arcade.color.WHITE, 20)
            output = "  100              500            250"
            arcade.draw_text(output, 650, 370, arcade.color.WHITE, 12)
        # draw cave 1 stuff
        elif self.current_map == self.cave_1_map:
            self.cave_1_enemy_list.draw()
        # draw cave 1 (open door) stuff
        elif self.current_map == self.cave_1_wall_open_map:
            pass
        # draw cave 2 stuff
        elif self.current_map == self.cave_2_map:
            self.chest.draw()
            if len(self.golem_list) > 0:
                self.golem_list.draw()
            if len(self.golem_list) <= 0 and not self.character.chest_key:
                self.animated_key.draw()
            if self.chest_opened and not self.character.crystal:
                self.animated_crystal.draw()

    def on_key_press(self, key: int, modifiers: int):
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
            if self.current_map == self.forest_map:
                if key == arcade.key.ENTER:
                    if self.character.state == FACE_UP:
                        self.handle_npc_and_store_interactions()
            elif self.current_map == self.cave_2_map:
                if key == arcade.key.ENTER:
                    if self.character.state == FACE_UP:
                        if 64 * 14 >= self.character.center_x >= 64 * 13 >= self.character.center_y >= 64 * 12 and \
                                self.character.chest_key:
                            self.chest.set_texture(1)
                            self.chest_opened = True
            if key == arcade.key.ESCAPE:
                self.close()

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
            self.character.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
            self.character.change_x = 0

# ######################## Utility functions #############################
    def setup_character(self):
        # setup character + lists
        hero_sprite_sheet_path = pathlib.Path.cwd() / 'Assets' / 'Characters' / 'hero_character_1.png'
        self.character = PlayerCharacter.setup_character(hero_sprite_sheet_path, 1, 64 * 11 + 32, 64 * 3 + 32)
        self.char_list = arcade.SpriteList()
        self.char_list.append(self.character)
        self.character_projectile_list = arcade.SpriteList()

    def setup_boss_key(self):
        # boss key
        path = pathlib.Path.cwd() / 'Assets' / 'Item_Drops' / 'Keys'
        self.animated_key = arcade.AnimatedTimeSprite(1, center_x=64 * 11 + 32, center_y=64 * 6 + 32)
        all_files = path.glob('*.png')  # return a generator with all the qualified paths to all png files in dir
        textures = []
        for file_path in all_files:
            frame = arcade.load_texture(str(file_path))  # we want the whole image
            frame.height = frame.height * 0.5
            frame.width = frame.width * 0.5
            textures.append(frame)
        self.animated_key.textures = textures

    def setup_projectiles(self):
        # setup projectiles
        self.left_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'left_arrow.png'
        self.right_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'right_arrow.png'
        self.up_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'up_arrow.png'
        self.down_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'down_arrow.png'
        self.arrow_sprites = [self.left_arrow_sprite_path, self.right_arrow_sprite_path,
                              self.up_arrow_sprite_path, self.down_arrow_sprite_path]

    def process_current_tmx_and_layers(self):
        self.current_map_tmx = arcade.tilemap.read_tmx(str(self.current_map))
        self.floor_list = arcade.tilemap.process_layer(self.current_map_tmx, "floor_layer", 1)
        self.wall_list = arcade.tilemap.process_layer(self.current_map_tmx, "walls_layer", 1)
        self.simple_Physics = arcade.PhysicsEngineSimple(self.character, self.wall_list)

    def character_arrow_shoot(self):
        new_arrow_sprite = Projectile(self.arrow_sprites[self.character.state], speed=10,
                                      direction=self.character.state, game_window=self)
        new_arrow_sprite.center_y = self.character.center_y
        new_arrow_sprite.center_x = self.character.center_x
        self.character_projectile_list.append(new_arrow_sprite)

    def setup_cave_1(self):
        goblin1 = GoblinEnemy.setup_goblin(self.goblin_path, 1, 2, 0, 700, 200)
        goblin2 = GoblinEnemy.setup_goblin(self.goblin_path, 1, -2, 0, 600, 300)
        goblin3 = GoblinEnemy.setup_goblin(self.goblin_path, 1, 0, 2, 500, 400)
        goblin4 = GoblinEnemy.setup_goblin(self.goblin_path, 1, 0, -2, 400, 500)
        wyvern1 = WyvernEnemy.setup_wyvern(0.9, 4, 0, 750, 250)
        wyvern2 = WyvernEnemy.setup_wyvern(0.9, -4, 0, 650, 600)
        wyvern3 = WyvernEnemy.setup_wyvern(0.9, 0, 4, 750, 450)
        wyvern4 = WyvernEnemy.setup_wyvern(0.9, 0, -4, 200, 550)
        self.cave_1_enemy_list.append(goblin1)
        self.cave_1_enemy_list.append(goblin2)
        self.cave_1_enemy_list.append(goblin3)
        self.cave_1_enemy_list.append(goblin4)
        self.cave_1_enemy_list.append(wyvern1)
        self.cave_1_enemy_list.append(wyvern2)
        self.cave_1_enemy_list.append(wyvern3)
        self.cave_1_enemy_list.append(wyvern4)

    def setup_animated_crystal(self):
        path = pathlib.Path.cwd() / 'Assets' / 'Item_Drops' / 'Crystal' / 'crystal.png'
        self.animated_crystal = arcade.AnimatedTimeSprite(1, center_x=64 * 12 + 32, center_y=64 * 13 + 32)
        crystal_frames = []
        for col in range(8):
            frame = arcade.load_texture(str(path), x=col * 32, y=0,
                                        width=32, height=32)
            crystal_frames.append(frame)
        self.animated_crystal.textures = crystal_frames

    # ----UPDATE FUNCTIONS----
    def do_forest_map_updates(self):
        # check if entering cave_1
        if (64 * 7) + 5 <= self.character.center_x <= (64 * 7) + 59 and self.character.center_y >= (64 * 13) + 20:
            # set character to opening of cave_1 and update physics engine
            self.current_map = self.cave_1_map
            self.character.center_y = 40
            self.character.center_x = (64 * 7) + 32
            self.process_current_tmx_and_layers()
        # ************** TODO: RESPAWN ENEMIES FOR CAVE ROOM 1 if cave room 1 enemy list is empty**************
            # going into cave_1 - setup enemies if enemy list empty
            # update wyvern list
            # update other stuff for room
        if self.character.center_y < 64 * 6:
            self.display_message = False

    def do_cave1_map_updates(self):
        self.cave_1_enemy_list.update()
        self.cave_1_enemy_list.update_animation()
        # check for collision between projectiles and enemies
        for proj in self.character_projectile_list:
            collisions = arcade.check_for_collision_with_list(proj, self.cave_1_enemy_list)
            if len(collisions) > 0:
                collisions[0].kill()
                proj.kill()

        # check for collision between character and enemies
        enemy_collisions = arcade.check_for_collision_with_list(self.character, self.cave_1_enemy_list)
        if len(enemy_collisions) > 0:
            self.character.update_health(self.character.health - 1)

        # open door when all enemies are dead
        if len(self.cave_1_enemy_list) <= 0:
            # update map to cave_1_wall_open and update physics engine
            self.current_map = self.cave_1_wall_open_map
            self.process_current_tmx_and_layers()

        # check if player is returning to forest
        if self.character.center_y <= -10 and (64 * 6 <= self.character.center_x <= 64 * 9):
            self.current_map = self.forest_map
            # set character to opening of forest
            self.character.center_y = (64 * 12) + 42
            self.character.center_x = (64 * 7) + 32
            # setup new map and update physics engine
            self.process_current_tmx_and_layers()

    def do_cave1_open_door_updates(self):
        # check if player is entering cave 2
        if self.character.center_x >= 64 * 15 and (64 * 6 <= self.character.center_y <= 64 * 9):
            self.current_map = self.cave_2_map
            # set character to opening of cave 2
            self.character.center_y = (64 * 7) + 32
            self.character.center_x = 32
            # setup new map and update physics engine
            self.process_current_tmx_and_layers()
        elif self.character.center_y <= -10 and (64 * 6 <= self.character.center_x <= 64 * 9):
            self.current_map = self.forest_map
            # set character to opening of forest
            self.character.center_y = (64 * 12) + 42
            self.character.center_x = (64 * 7) + 32
            # setup new map and update physics engine
            self.process_current_tmx_and_layers()

    def do_cave2_map_updates(self):
        # ROOM EXITING
        if self.character.center_x <= -10 and (64 * 6 <= self.character.center_y <= 64 * 9):
            self.current_map = self.cave_1_wall_open_map
            # set character to opening of cave_1
            self.character.center_y = (64 * 7) + 32
            self.character.center_x = (64 * 14) + 32
            # setup new map and layers
            self.process_current_tmx_and_layers()
        # BOSS INTERACTION ***
        if arcade.get_distance_between_sprites(self.character, self.golem_boss) <= 200.0:
            self.golem_boss.character_x_loc = self.character.center_x
            self.golem_boss.character_y_loc = self.character.center_y
            self.golem_boss.move_state = ATTACK
        else:
            self.golem_boss.move_state = ROAM

        if len(self.golem_list) > 0:
            boss_collisions = arcade.check_for_collision_with_list(self.character, self.golem_list)
            if len(boss_collisions) > 0:
                self.character.update_health(self.character.health - 1)

        # If player has magic arrows, can kill the golem
        if self.character.magic_book:
            [gol.kill() for gol in self.golem_list if
             arcade.check_for_collision_with_list(gol, self.character_projectile_list)]

        [proj.kill() for proj in self.character_projectile_list
         if arcade.check_for_collision_with_list(proj, self.golem_list)]

        # pick up key
        if len(self.golem_list) <= 0 and 64 * 11 <= self.character.center_x <= 64 * 12 and \
                64 * 6 <= self.character.center_y <= 64 * 7:
            self.character.chest_key = True

        # ***opening chest happens in key press detection***
        # pick up crystal here
        if 64 * 12 <= self.character.center_x <= 64 * 13 <= self.character.center_y <= 64 * 14 and self.chest_opened:
            self.character.crystal = True

    def projectile_updates(self):
        # move player projectiles
        for character_projectile in self.character_projectile_list:
            character_projectile.move()
        # check for projectile collisions with "wall_layer" and off screen
        [proj.kill() for proj in self.character_projectile_list
         if arcade.check_for_collision_with_list(proj, self.wall_list)]

    # -----------------
    def upgrade_to_magic_fire_arrows(self):
        self.left_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'left_fire_arrow.png'
        self.right_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'right_fire_arrow.png'
        self.up_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'up_fire_arrow.png'
        self.down_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'down_fire_arrow.png'
        self.arrow_sprites = [self.left_arrow_sprite_path, self.right_arrow_sprite_path,
                              self.up_arrow_sprite_path, self.down_arrow_sprite_path]

    def handle_npc_and_store_interactions(self):
        if 64 <= self.character.center_x <= 64 * 2 and 64 * 6 <= self.character.center_y <= 64 * 7:
            self.display_message = True
        elif 64 * 10 < self.character.center_x < 64 * 11 and 64 * 4 < self.character.center_y < 64 * 5:
            if self.character.money >= 100:
                self.character.money -= 100
                self.character.arrows += 10
                print(self.character.money)
                print(self.character.arrows)
        elif 64 * 11 <= self.character.center_x <= 64 * 12 and 64 * 4 <= self.character.center_y <= 64 * 5:
            if self.character.money >= 500:
                self.character.magic_book = True
                self.character.money -= 500
                print(self.character.money)
                print(self.character.magic_book)
                # player now has magic fire arrows
                self.upgrade_to_magic_fire_arrows()
        elif 64 * 12 <= self.character.center_x <= 64 * 13 and 64 * 4 <= self.character.center_y <= 64 * 5:
            if self.character.money >= 250:
                self.character.boots = True
                self.character.money -= 250
                print(self.character.money)
                print(self.character.boots)
                # player's speed has increased
                self.character_speed = 4