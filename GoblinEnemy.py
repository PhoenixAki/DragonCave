import arcade

CHARACTER_FRAME_WIDTH = 64
CHARACTER_FRAME_HEIGHT = 64


class GoblinEnemy(arcade.AnimatedWalkingSprite):
    def __init__(self, scale: float, center_x: float, center_y: float):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)


def setup_goblin_enemy(sprite_sheet_path, scl, cent_x, cent_y):
    goblin = GoblinEnemy(scale=scl, center_x=cent_x, center_y=cent_y)

    # character standing left/right frames setup
    frame = arcade.load_texture(str(sprite_sheet_path), 0, CHARACTER_FRAME_HEIGHT * 9,
                                height=CHARACTER_FRAME_HEIGHT,
                                width=CHARACTER_FRAME_WIDTH)
    goblin.stand_left_textures = []
    goblin.stand_left_textures.append(frame)

    frame = arcade.load_texture(str(sprite_sheet_path), 0, CHARACTER_FRAME_HEIGHT * 11,
                                height=CHARACTER_FRAME_HEIGHT,
                                width=CHARACTER_FRAME_WIDTH)
    goblin.stand_right_textures = []
    goblin.stand_right_textures.append(frame)

    # no stand up and stand down textures??

    # setup main character textures
    goblin.texture = frame

    goblin.walk_left_textures = []
    goblin.walk_right_textures = []
    goblin.walk_down_textures = []
    goblin.walk_up_textures = []

    for image_num in range(11):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 2, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        goblin.walk_up_textures.append(frame)
    for image_num in range(11):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 3, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        goblin.walk_left_textures.append(frame)
    for image_num in range(11):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 0, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        goblin.walk_down_textures.append(frame)
    for image_num in range(11):
        frame = arcade.load_texture(str(sprite_sheet_path), image_num * CHARACTER_FRAME_WIDTH,
                                    CHARACTER_FRAME_HEIGHT * 1, height=CHARACTER_FRAME_HEIGHT,
                                    width=CHARACTER_FRAME_WIDTH)
        goblin.walk_right_textures.append(frame)

    return goblin
