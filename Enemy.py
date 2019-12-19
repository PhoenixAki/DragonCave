from collections import deque
import random
import arcade

import PlayerCharacter
from Main import Node


class Enemy(arcade.AnimatedWalkingSprite):
    """
    Base class that all enemies inherit from. Mostly used to save code repetition to save space.

    Notable Parameters:
        **move_state** - ROAMING and ATTACKING are used to determine whether to calculate paths to the player or not.

        **range** - Determines how close to the enemy a player should get before switching to ATTACK move_state.

        **speed** - How many pixels the Enemy should move each time move_next_node is called (every frame).

        **health** - Tracks health of Enemy (goblins start with 1, wyverns have 2, and golem boss has 3)

        **path** - Filled with the path the Enemy is currently on. Can either be random when ROAMING, or towards
                    the player when ATTACKING.

        **player_loc** - Used to determine if the player has moved to a new location or not.
    """
    def __init__(self, scale, center_x, center_y, health, init_range, change_x, change_y):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.FACE_LEFT = 0
        self.FACE_RIGHT = 1
        self.FACE_UP = 2
        self.FACE_DOWN = 3

        self.MOVING_LEFT = 4
        self.MOVING_RIGHT = 5
        self.MOVING_UP = 6
        self.MOVING_DOWN = 7

        self.move_state = None  # can be ROAMING or ATTACKING
        self.state = None
        self.direction = self.MOVING_LEFT
        self.range = init_range
        self.drops = ["", ""]
        self.drop_index = 0

        self.change_x = change_x
        self.change_y = change_y

        # all enemies have walking textures
        self.walk_left_textures = []
        self.walk_right_textures = []
        self.walk_down_textures = []
        self.walk_up_textures = []
        self.cur_texture_index = 0

        self.health = health  # all enemies have health (goblins have 1, wyverns have 2, golems have 3)

        self.path = deque()  # path can be either randomized or towards a player
        self.player_loc = None  # only updates path if player is in a different node than previously known
        self.build_again = True  # determines if a new random path needs to be created

    def move(self, character: PlayerCharacter, graph):
        """Manages move_state, calculates paths to the player, and moves the enemy according to said paths."""
        # enemy attacks 
        if arcade.get_distance_between_sprites(self, character) <= self.range and not character.temp_invincibility:
            self.move_state = "ATTACKING"
        # elif arcade.get_distance_between_sprites(self, character) > self.range:
        else:
            self.move_state = "ROAMING"

        cur_node_x = int(self.center_x / 64)
        cur_node_y = int((960-self.center_y) / 64)
        if len(self.path) > 0:
            next_node = self.path[-1]
        else:
            next_node = None

        # if attacking, move according to path
        if self.move_state is "ATTACKING":
            char_node_x = int(character.center_x / 64)
            char_node_y = int((960-character.center_y) / 64)
            cur_player_loc = (char_node_x, char_node_y)

            # if player has moved, re-calculate path
            if cur_player_loc != self.player_loc:
                self.build_player_path(graph, char_node_x, char_node_y, cur_node_x, cur_node_y, next_node)

            # if player is in different location, update it
            if cur_player_loc != self.player_loc:
                self.player_loc = cur_player_loc

            if next_node is not None:
                self.move_next_node(next_node)
        # if roaming, move in random directions
        elif self.move_state is "ROAMING":
            if self.build_again is True:
                self.build_random_path(graph[cur_node_y][cur_node_x])
                self.build_again = False

            if next_node is not None:
                self.move_next_node(next_node)

    def move_next_node(self, next_node):
        # check if arrived at the next node in the path
        if self.center_x == next_node.x_pixel_loc and self.center_y == next_node.y_pixel_loc:
            if len(self.path) == 1:
                self.build_again = True
                return
            else:
                next_node: Node = self.path.pop()

        # move towards the next node and bounce back to the center if enemy goes past it
        if self.center_x > next_node.x_pixel_loc:  # left
            self.direction = self.MOVING_LEFT
            if self.center_x - self.change_x < next_node.x_pixel_loc:
                self.center_x = next_node.x_pixel_loc
            else:
                self.center_x -= self.change_x
        elif self.center_x < next_node.x_pixel_loc:  # right
            self.direction = self.MOVING_RIGHT
            if self.center_x + self.change_x > next_node.x_pixel_loc:
                self.center_x = next_node.x_pixel_loc
            else:
                self.center_x += self.change_x
        elif self.center_y > next_node.y_pixel_loc:  # down
            self.direction = self.MOVING_DOWN
            if self.center_y - self.change_y < next_node.y_pixel_loc:
                self.center_y = next_node.y_pixel_loc
            else:
                self.center_y -= self.change_y
        elif self.center_y < next_node.y_pixel_loc:  # up
            self.direction = self.MOVING_UP
            if self.center_y + self.change_y > next_node.y_pixel_loc:
                self.center_y = next_node.y_pixel_loc
            else:
                self.center_y += self.change_y

    def build_player_path(self, graph, player_node_x: int, player_node_y: int, cur_node_x, cur_node_y, next_node):
        """Setup & preparation for building a path to the player."""
        if player_node_x < 0 or player_node_y > 14:  # catches case of leaving cave 1 and 2
            return

        cur_node: Node = graph[cur_node_y][cur_node_x]
        player_node: Node = graph[player_node_y][player_node_x]
        queue: deque = deque()
        queue.appendleft(cur_node)  # starting node is the enemy's current node

        self.player_search(queue, cur_node, player_node, next_node)

        # TODO uncomment this print block to display the new path to the player
        '''builder = ""
        for y in graph:
            for x in y:
                if x is not None:
                    if x in self.path:
                        if self.path[-1] is x:
                            builder += "E   "
                        elif x is player_node:
                            builder += "P   "
                        else:
                            builder += "--- "
                    else:
                        builder += "x   "
                else:
                    builder += "x   "
            builder += "\n"
        print(builder)'''

    def build_random_path(self, cur_node):
        """Builds a randomized path to move around. Generates 3 random nodes in succession to move to."""
        self.path = deque()  # reset any previous path that existed

        while len(self.path) < 3:
            rand_neighbor = random.randint(0, 3)

            while cur_node.neighbors[rand_neighbor] is None:
                rand_neighbor = random.randint(0, 3)

            self.path.appendleft(cur_node.neighbors[rand_neighbor])  # append a random neighbor to path
            cur_node = cur_node.neighbors[rand_neighbor]  # adjust cur_node to the appropriate neighbor

    def player_search(self, queue: deque, start, end: Node, next_node):
        """Uses Breadth First Search to find the shortest path to the player.
            A*/Dijkstra aren't optimal because this is an unweighted graph."""
        explored = [False] * 318  # tracks whether a given node has been explored yet
        explored[start.ID] = True
        previous = [None] * 318  # tracks the previous node we came from, used for building path after exploration

        while len(queue) > 0:
            cur_node = queue.pop()

            # before anything else, break if at the end goal
            if cur_node is end:
                break

            # if not, add all of the current node's unvisited neighbors to the queue to be explored
            for node in cur_node.neighbors:
                if node is not None and explored[node.ID] is False:
                    queue.appendleft(node)
                    explored[node.ID] = True
                    previous[node.ID] = cur_node

        self.path = deque()
        current = end

        # build the path by following the previous list
        while current is not start:
            self.path.append(current)
            current = previous[current.ID]

        if next_node is not None:
            self.path.append(next_node)
