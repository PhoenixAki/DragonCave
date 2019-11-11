from arcade.geometry import check_for_collision_with_list
from arcade.sprite import Sprite
from arcade.sprite_list import SpriteList


# template borrowed from Arcade graphics package
class EnemyEngineSimple:
    """
    This class will move everything, and take care of collisions.
    """

    def __init__(self, enemy_sprite: Sprite, walls: SpriteList):
        """
        Constructor.
        """
        assert (isinstance(enemy_sprite, Sprite))
        assert (isinstance(walls, SpriteList))
        self.enemy_sprite = enemy_sprite
        self.walls = walls

    def update(self):
        """
        Move everything and resolve collisions.
        """
        # --- Move in the x direction
        self.enemy_sprite.center_x += self.enemy_sprite.change_x

        # Check for wall hit
        hit_list = \
            check_for_collision_with_list(self.enemy_sprite,
                                          self.walls)

        # If we hit a wall, move so the edges are at the same point
        if len(hit_list) > 0:
            if self.enemy_sprite.change_x > 0:
                for item in hit_list:
                    self.enemy_sprite.right = min(item.left,
                                                   self.enemy_sprite.right)
                self.enemy_sprite.change_x = self.enemy_sprite.change_x * -1
            elif self.enemy_sprite.change_x < 0:
                for item in hit_list:
                    self.enemy_sprite.left = max(item.right,
                                                  self.enemy_sprite.left)
                self.enemy_sprite.change_x = self.enemy_sprite.change_x * -1
            else:
                print("Error, collision while player wasn't moving.")

        # --- Move in the y direction
        self.enemy_sprite.center_y += self.enemy_sprite.change_y

        # Check for wall hit
        hit_list = \
            check_for_collision_with_list(self.enemy_sprite,
                                          self.walls)

        # If we hit a wall, move so the edges are at the same point
        if len(hit_list) > 0:
            if self.enemy_sprite.change_y > 0:
                for item in hit_list:
                    self.enemy_sprite.top = min(item.bottom,
                                                 self.enemy_sprite.top)
                self.enemy_sprite.change_y = self.enemy_sprite.change_y * -1
            elif self.enemy_sprite.change_y < 0:
                for item in hit_list:
                    self.enemy_sprite.bottom = max(item.top,
                                                    self.enemy_sprite.bottom)
                self.enemy_sprite.change_y = self.enemy_sprite.change_y * -1
            else:
                print("Error, collision while player wasn't moving.")
