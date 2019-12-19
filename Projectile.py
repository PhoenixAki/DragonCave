import arcade


class Projectile(arcade.Sprite):
    """Represents the arrows that the player buys and shoots as weapon."""
    def __init__(self, img_path: str, speed: int, direction: int, game_window):
        super().__init__(img_path)
        self.speed = speed
        self.direction = direction
        self.game = game_window

        self.FACE_LEFT = 0
        self.FACE_RIGHT = 1
        self.FACE_UP = 2
        self.FACE_DOWN = 3

    def update(self):
        if self.direction == self.FACE_UP:
            self.center_y += self.speed
        elif self.direction == self.FACE_DOWN:
            self.center_y -= self.speed
        elif self.direction == self.FACE_LEFT:
            self.center_x -= self.speed
        elif self.direction == self.FACE_RIGHT:
            self.center_x += self.speed
