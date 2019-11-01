import arcade

FACE_RIGHT = 1
FACE_LEFT = 2
FACE_UP = 3
FACE_DOWN = 4


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