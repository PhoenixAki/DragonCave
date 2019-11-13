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
        self.cave_1_open = pathlib.Path.cwd() / 'Assets' / 'Cave_1_open.tmx'
        self.cave_2_map = pathlib.Path.cwd() / 'Assets' / 'Cave_2.tmx'
        self.close_chest_path = pathlib.Path.cwd() / 'Assets' / 'Item_Drops' / 'Chest' / 'Treasure_Chest_closed.png'
        self.open_chest_path = pathlib.Path.cwd() / 'Assets' / 'Item_Drops' / 'Chest' / 'Treasure_Chest_open.png'
        self.coin_sound_path = pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'coin_collect.wav'
        self.coin_sound = arcade.Sound(str(self.coin_sound_path))
        self.ruby_sound_path = pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'ruby_collect.wav'
        self.ruby_sound = arcade.Sound(str(self.ruby_sound_path))
        # -----------
        self.boss_damage_sound_path = pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'boss_damage_0.wav'
        self.boss_damage_sound = arcade.Sound(str(self.boss_damage_sound_path))

        self.chest_open_sound_path = pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'chest_open.wav'
        self.chest_open_sound = arcade.Sound(str(self.chest_open_sound_path))

        self.collect_crystal_sound_path = pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'collect_crystal.wav'
        self.collect_crystal_sound = arcade.Sound(str(self.collect_crystal_sound_path))

        self.collect_key_sound_path = pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'collect_key.wav'
        self.collect_key_sound = arcade.Sound(str(self.collect_key_sound_path))

        self.end_game_sound_path = pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'end_game.wav'
        self.end_game_sound = arcade.Sound(str(self.end_game_sound_path))

        self.golem_attack_sound_path = pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'golem_attack.wav'
        self.golem_attack_sound = arcade.Sound(str(self.golem_attack_sound_path))

        self.regular_arrow_shoot_sound_path = pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'regular_arrow_shoot.wav'
        self.regular_arrow_shoot_sound = arcade.Sound(str(self.regular_arrow_shoot_sound_path))

        self.sell_buy_item_sound_path = pathlib.Path.cwd() / 'Assets' / 'Sounds' / 'sell_buy_item.wav'
        self.sell_buy_item_sound = arcade.Sound(str(self.sell_buy_item_sound_path))

        self.current_map = None
        self.current_map_tmx = None
        self.floor_list = None
        self.wall_list = None

        # booleans triggers + strings
        self.HUD = False
        self.chest_opened = False
        self.display_message = False
        self.item_list = ""

        # sprites
        self.up_arrow_sprite_path = None
        self.down_arrow_sprite_path = None
        self.left_arrow_sprite_path = None
        self.right_arrow_sprite_path = None
        self.arrow_sprites = None
        self.animated_key = None
        self.chest = None
        self.opened_chest_texture = None
        self.animated_crystal = None

        # character + enemies
        self.character = None
        self.char_list = None
        self.character_projectile_list = None
        self.character_speed = 3
        self.cave_1_enemies = None
        self.golem_boss = None
        self.golem_list = None
        self.enemy_drop_list = None

        # initialize physics engine + framerate
        self.simple_Physics = None
        self.frame_time = 0

        self.end_game_flag = False

    def setup(self):
        # setup players and enemies
        self.setup_character()
        self.cave_1_enemies = arcade.SpriteList()
        self.setup_cave_1()
        self.enemy_drop_list = arcade.SpriteList()

        # set current map
        self.current_map = self.forest_map
        self.process_map()

        # setup golem boss
        self.golem_boss = GolemEnemy.setup_golem(1.7, 0, 0, (64 * 5) + 32, 485)
        self.golem_list = arcade.SpriteList()
        self.golem_list.append(self.golem_boss)

        # setup boss room textures/animations
        self.chest = arcade.Sprite(str(self.close_chest_path), center_x=64 * 13 + 32, center_y=64 * 13 + 32)
        self.opened_chest_texture = arcade.load_texture(str(self.open_chest_path))
        self.chest.append_texture(self.opened_chest_texture)
        self.setup_boss_key()
        self.setup_animated_crystal()
        self.setup_projectiles()

        # setup physics engine
        self.simple_Physics = arcade.PhysicsEngineSimple(self.character, self.wall_list)

    def on_update(self, delta_time: float):

        # FOREST MAP UPDATES ------------
        if self.current_map == self.forest_map:
            self.forest_update()

        # CAVE 1 MAP UPDATES --------------
        elif self.current_map == self.cave_1_map:
            self.cave_1_update()

        # CAVE 1 OPEN DOOR MAP UPDATES -----------
        elif self.current_map == self.cave_1_open:
            self.cave_1_open_update()

        # CAVE 2 MAP UPDATES ------------
        elif self.current_map == self.cave_2_map:
            self.cave_2_update()

        # ****** BELOW: UPDATES THAT HAPPEN ON EVERY MAP *************
        # these have to happen every time to avoid "Exception: Error: Attempt to draw a sprite without a texture set."
        if self.current_map == self.cave_1_map:
            self.cave_1_enemies.update()
            self.cave_1_enemies.update_animation()
            self.enemy_drop_list.update_animation()
        elif self.current_map == self.cave_1_open:
            self.enemy_drop_list.update_animation()
        elif self.current_map == self.cave_2_map:
            self.golem_list.update()
            self.golem_list.update_animation()

        # update animations using frame rate
        self.frame_time += delta_time
        if self.frame_time > 1/30:  # 30fps for now?
            self.frame_time = 0
            self.char_list.update()
            self.char_list.update_animation()

        # update key animation if boss dead
        if len(self.golem_list) <= 0 and not self.character.chest_key:
            self.animated_key.update_animation()
        if self.chest_opened:
            self.animated_crystal.update_animation()

        # *********************************************************

        self.simple_Physics.update()

        # projectiles
        self.character_projectile_list.update()
        [proj.kill() for proj in self.character_projectile_list
         if arcade.check_for_collision_with_list(proj, self.wall_list)]

        # check if player is dead
        if self.character.health <= 0:
            self.character.kill()
            print("You lose.")
            exit()

    def on_draw(self):
        arcade.start_render()
        self.floor_list.draw()
        self.wall_list.draw()

        # projectiles
        if len(self.character_projectile_list) > 0:
            self.character_projectile_list.draw()

        # forest
        if self.current_map == self.forest_map:
            if self.display_message:
                if not self.character.crystal:
                    output = "DEFEAT THE EVIL GOLEM.\nGET HIS KEY.\nRETRIEVE THE SCARED CRYSTAL!"
                    arcade.draw_text(output, 10, 510, arcade.color.WHITE, 20)
                else:
                    output = "YOU RETRIEVED THE SACRED CRYSTAL!\nWE ARE SAFE AGAIN, THANK YOU!"
                    arcade.draw_text(output, 10, 510, arcade.color.WHITE, 20)
                    if self.end_game_flag is False:
                        self.end_game_sound.play()
                        self.end_game_flag = True

            output = "  50               350            150"
            arcade.draw_text(output, 650, 370, arcade.color.WHITE, 12)
        # cave 1
        elif self.current_map == self.cave_1_map:
            self.cave_1_enemies.draw()
            self.enemy_drop_list.draw()
        # cave 1 open
        elif self.current_map == self.cave_1_open:
            self.enemy_drop_list.draw()
        # cave 2
        elif self.current_map == self.cave_2_map:
            self.chest.draw()
            if len(self.golem_list) > 0:
                self.golem_list.draw()
            if len(self.golem_list) <= 0 and not self.character.chest_key:
                self.animated_key.draw()
            if self.chest_opened and not self.character.crystal:
                self.animated_crystal.draw()

        self.char_list.draw()
        if self.HUD is True:
            arcade.draw_rectangle_filled(150, 875, 185, 135, arcade.color.DAVY_GREY)
            arcade.draw_text("HEALTH: " + str(self.character.health), 80, 920, arcade.color.BLACK, 15)
            arcade.draw_text("MONEY: " + str(self.character.money), 80, 890, arcade.color.BLACK, 15)
            arcade.draw_text("ARROWS: " + str(self.character.arrows), 80, 860, arcade.color.BLACK, 15)
            arcade.draw_text("ITEMS: " + self.item_list, 80, 830, arcade.color.BLACK, 12)

    def on_key_press(self, key: int, modifiers: int):
        # character movement
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
                if self.character.arrows < 1:
                    print("Out of arrows!")
                else:
                    self.character.change_x = 0
                    self.character.change_y = 0
                    self.character.attacking = True
                    self.shoot_arrow()
                    self.regular_arrow_shoot_sound.play()

        # miscellaneous keyboard inputs
        if key == arcade.key.ENTER and self.character.state == FACE_UP:
            if self.current_map == self.forest_map:
                    self.npc_interactions()
            elif self.current_map == self.cave_2_map:
                if 64 * 14 >= self.character.center_x >= 64 * 13 >= self.character.center_y >= 64 * 12 \
                        and self.character.chest_key:
                    self.chest.set_texture(1)
                    self.chest_opened = True
                    self.chest_open_sound.play()

        if key == arcade.key.ESCAPE:
            self.close()
        if key == arcade.key.TAB:
            self.HUD = not self.HUD  # toggle HUD display for player stats

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
            self.character.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
            self.character.change_x = 0

# ######################## Utility functions #############################
    def setup_character(self):
        hero_sprite_sheet_path = pathlib.Path.cwd() / 'Assets' / 'Characters' / 'hero_character_1.png'
        self.character = PlayerCharacter.setup_character(hero_sprite_sheet_path, 1, 64 * 11 + 32, 64 * 3 + 32)
        self.char_list = arcade.SpriteList()
        self.char_list.append(self.character)
        self.character_projectile_list = arcade.SpriteList()

    def setup_boss_key(self):
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

    def process_map(self):
        self.current_map_tmx = arcade.tilemap.read_tmx(str(self.current_map))
        self.floor_list = arcade.tilemap.process_layer(self.current_map_tmx, "floor_layer", 1)
        self.wall_list = arcade.tilemap.process_layer(self.current_map_tmx, "walls_layer", 1)
        self.simple_Physics = arcade.PhysicsEngineSimple(self.character, self.wall_list)

    def shoot_arrow(self):
        new_arrow_sprite = Projectile(self.arrow_sprites[self.character.state], speed=10,
                                      direction=self.character.state, game_window=self)
        new_arrow_sprite.center_y = self.character.center_y
        new_arrow_sprite.center_x = self.character.center_x
        self.character_projectile_list.append(new_arrow_sprite)
        self.character.arrows -= 1

    def setup_cave_1(self):
        goblin1 = GoblinEnemy.setup_goblin(self.goblin_path, 1, 1.5, 0, 700, 200, "coin")
        goblin2 = GoblinEnemy.setup_goblin(self.goblin_path, 1, -1.5, 0, 600, 300, "coin")
        goblin3 = GoblinEnemy.setup_goblin(self.goblin_path, 1, 0, 1.5, 500, 400, "coin")
        goblin4 = GoblinEnemy.setup_goblin(self.goblin_path, 1, 0, -1.5, 400, 500, "coin")
        wyvern1 = WyvernEnemy.setup_wyvern(.9, 3, 0, 750, 250, "ruby")
        wyvern2 = WyvernEnemy.setup_wyvern(.9, -3, 0, 650, 600, "ruby")
        wyvern3 = WyvernEnemy.setup_wyvern(.9, 0, 3, 750, 450, "ruby")
        wyvern4 = WyvernEnemy.setup_wyvern(.9, 0, -3, 200, 550, "ruby")
        self.cave_1_enemies.append(goblin1)
        self.cave_1_enemies.append(goblin2)
        self.cave_1_enemies.append(goblin3)
        self.cave_1_enemies.append(goblin4)
        self.cave_1_enemies.append(wyvern1)
        self.cave_1_enemies.append(wyvern2)
        self.cave_1_enemies.append(wyvern3)
        self.cave_1_enemies.append(wyvern4)

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
    def forest_update(self):
        if (64 * 7) + 5 <= self.character.center_x <= (64 * 7) + 59 and self.character.center_y >= (64 * 13) + 20:
            # set character to opening of cave_1 and update physics engine
            self.current_map = self.cave_1_map
            self.character.center_y = 40
            self.character.center_x = (64 * 7) + 32
            self.process_map()
            if len(self.cave_1_enemies) == 0:
                self.setup_cave_1()

        if self.character.center_y < 64 * 6:
            self.display_message = False

    def cave_1_update(self):
        self.cave_1_enemies.update()
        self.cave_1_enemies.update_animation()
        # check for collision between projectiles and enemies
        for proj in self.character_projectile_list:
            collisions = arcade.check_for_collision_with_list(proj, self.cave_1_enemies)
            if len(collisions) > 0:
                collisions[0].health -= 1
                proj.kill()

                if collisions[0].health == 0:
                    collisions[0].kill()

                    if collisions[0].drop == "coin":
                        coin = create_coin_drop(collisions[0].center_x, collisions[0].center_y)
                        self.enemy_drop_list.append(coin)
                    elif collisions[0].drop == "ruby":
                        ruby = create_ruby_drop(collisions[0].center_x, collisions[0].center_y)
                        self.enemy_drop_list.append(ruby)

        # check for collision between character and enemies
        enemy_collisions = arcade.check_for_collision_with_list(self.character, self.cave_1_enemies)
        if len(enemy_collisions) > 0:
            self.character.update_health(self.character.health - 1)

        # open door when all enemies are dead
        if len(self.cave_1_enemies) == 0:
            # update map to cave_1_wall_open and update physics engine
            self.current_map = self.cave_1_open
            self.process_map()

        # check if player is returning to forest
        if self.character.center_y <= -10 and (64 * 6 <= self.character.center_x <= 64 * 9):
            self.current_map = self.forest_map
            self.process_map()
            # set character to opening of forest
            self.character.center_y = (64 * 12) + 42
            self.character.center_x = (64 * 7) + 32

        # pick up coins and rubies
        self.pickup_drops()

        for enemy in self.cave_1_enemies:
            if arcade.get_distance_between_sprites(self.character, enemy) < enemy.range:
                enemy.change_x = 0
                enemy.change_y = 0
            else:
                enemy.change_x = enemy.walking_x
                enemy.change_y = enemy.walking_y

    def cave_1_open_update(self):
        # check if player is entering cave 2
        if self.character.center_x >= 64 * 15 and (64 * 6 <= self.character.center_y <= 64 * 9):
            self.current_map = self.cave_2_map
            self.process_map()
            # set character to opening of cave 2
            self.character.center_y = (64 * 7) + 32
            self.character.center_x = 32
        elif self.character.center_y <= -10 and (64 * 6 <= self.character.center_x <= 64 * 9):
            self.current_map = self.forest_map
            self.process_map()
            # set character to opening of forest
            self.character.center_y = (64 * 12) + 42
            self.character.center_x = (64 * 7) + 32

        # pick up coins and rubies
        self.pickup_drops()

        # ***opening chest happens in key press detection***
        # pick up crystal here
        if 64 * 12 <= self.character.center_x <= 64 * 13 <= self.character.center_y <= 64 * 14 and self.chest_opened:
            self.character.crystal = True

    def cave_2_update(self):
        # ROOM EXITING
        if self.character.center_x <= -10 and (64 * 6 <= self.character.center_y <= 64 * 9):
            self.current_map = self.cave_1_open
            self.process_map()
            # set character to opening of cave_1
            self.character.center_y = (64 * 7) + 32
            self.character.center_x = (64 * 14) + 32
        # BOSS INTERACTION ***
        if arcade.get_distance_between_sprites(self.character, self.golem_boss) <= 300.0 and len(self.golem_list) > 0:
            self.golem_boss.character_x_loc = self.character.center_x
            self.golem_boss.character_y_loc = self.character.center_y
            if self.golem_boss.move_state is not ATTACK:
                self.golem_boss.move_state = ATTACK
                self.golem_attack_sound.play()
        else:
            self.golem_boss.move_state = ROAM

        if len(self.golem_list) > 0:
            boss_collisions = arcade.check_for_collision_with_list(self.character, self.golem_list)
            if len(boss_collisions) > 0:
                self.character.update_health(self.character.health - 1)

        # If player has magic arrows, can kill the golem
        for proj in self.character_projectile_list:
            if arcade.check_for_collision(proj, self.golem_boss) and self.character.magic_book:
                proj.kill()
                self.golem_boss.health -= 1
                self.boss_damage_sound.play()

                if self.golem_boss.health == 0:
                    self.golem_boss.kill()

        # pick up key
        if len(self.golem_list) <= 0 and 64 * 11 <= self.character.center_x <= 64 * 12 and \
                64 * 6 <= self.character.center_y <= 64 * 7:
            if not self.character.chest_key:
                self.collect_key_sound.play()
            self.character.chest_key = True

        # ***opening chest happens in key press detection***
        # pick up crystal here
        if 64 * 12 <= self.character.center_x <= 64 * 13 <= self.character.center_y <= 64 * 14 and self.chest_opened:
            if not self.character.crystal:
                self.collect_crystal_sound.play()
            self.character.crystal = True

    # -----------------
    def upgrade_to_magic_fire_arrows(self):
        self.left_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'left_fire_arrow.png'
        self.right_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'right_fire_arrow.png'
        self.up_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'up_fire_arrow.png'
        self.down_arrow_sprite_path = pathlib.Path.cwd() / 'Assets' / 'Projectiles' / 'down_fire_arrow.png'
        self.arrow_sprites = [self.left_arrow_sprite_path, self.right_arrow_sprite_path,
                              self.up_arrow_sprite_path, self.down_arrow_sprite_path]

    def pickup_drops(self):
        collisions = arcade.check_for_collision_with_list(self.character, self.enemy_drop_list)
        if len(collisions) > 0 and self.character.money < 600:
            if len(collisions[0].textures) == 7:  # rubies
                self.ruby_sound.play()
                self.character.money += 50
                collisions[0].kill()
            elif len(collisions[0].textures) == 9:  # coins
                self.coin_sound.play()
                self.character.money += 25
                collisions[0].kill()

        if self.character.money > 600:
            self.character.money = 600

    def npc_interactions(self):
        if 64 <= self.character.center_x <= 64 * 2 and 64 * 6 <= self.character.center_y <= 64 * 7:
            self.display_message = True
        elif 64 * 10 < self.character.center_x < 64 * 11 and 64 * 4 < self.character.center_y < 64 * 5:
            if self.character.money >= 50 and self.character.arrows < 45:
                self.character.money -= 50
                self.character.arrows += 15
                self.sell_buy_item_sound.play()

                if self.character.arrows > 45:
                    self.character.arrows = 45
        elif 64 * 11 <= self.character.center_x <= 64 * 12 and 64 * 4 <= self.character.center_y <= 64 * 5:
            if self.character.money >= 350 and not self.character.magic_book:
                self.character.magic_book = True
                self.character.money -= 350
                self.sell_buy_item_sound.play()
                if self.item_list == "":
                    self.item_list = "Magic Book, "
                else:
                    self.item_list = self.item_list + "Magic Book"
                self.upgrade_to_magic_fire_arrows()
        elif 64 * 12 <= self.character.center_x <= 64 * 13 and 64 * 4 <= self.character.center_y <= 64 * 5:
            if self.character.money >= 150 and not self.character.boots:
                self.character.boots = True
                self.character.money -= 150
                self.sell_buy_item_sound.play()
                if self.item_list == "":
                    self.item_list = "Boots, "
                else:
                    self.item_list = self.item_list + "Boots"
                # player's speed has increased
                self.character_speed = 5


def create_coin_drop(x, y):
    path = pathlib.Path.cwd() / 'Assets' / 'Item_Drops' / 'Coin'
    coin = arcade.AnimatedTimeSprite(1, center_x=x, center_y=y)
    all_files = path.glob('*.png')  # return a generator with all the qualified paths to all png files in dir
    textures = []
    for file_path in all_files:
        frame = arcade.load_texture(str(file_path))
        frame.height = frame.height  # * 0.5
        frame.width = frame.width  # * 0.5
        textures.append(frame)
    coin.textures = textures
    return coin


def create_ruby_drop(x, y):
    path = pathlib.Path.cwd() / 'Assets' / 'Item_Drops' / 'Ruby' / 'ruby2.png'
    ruby = arcade.AnimatedTimeSprite(1, center_x=x, center_y=y)
    ruby_frames = []
    for col in range(7):
        frame = arcade.load_texture(str(path), x=col * 24, y=0, width=24, height=24)
        ruby_frames.append(frame)
    ruby.textures = ruby_frames
    return ruby
