from collections import deque

import arcade

import PlayerCharacter
from Main import Node


class Enemy(arcade.AnimatedWalkingSprite):
    """
    Base class that all enemies inherit from. Mostly used to save code repetition to save space.

    Notable Parameters:
        **state** - ROAMING and ATTACKING are used to determine whether to calculate paths to the player or not.

        **range** - Determines how close to the enemy a player should get before switching to ATTACK state.

        **health** - Tracks health of Enemy (goblins start with 1, wyverns have 2, and golem boss has 3)

        **player_loc** - Used to determine if the player has moved to a new location or not.
    """
    def __init__(self, scale, center_x, center_y, health, init_range):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.state = None  # can be ROAMING or ATTACKING
        self.range = init_range

        # all enemies have walking textures
        self.walk_left_textures = []
        self.walk_right_textures = []
        self.walk_down_textures = []
        self.walk_up_textures = []

        # all enemies have health (goblins have 1, wyverns have 2, golems have 3)
        self.health = health

        self.FACE_LEFT = 0
        self.FACE_RIGHT = 1
        self.FACE_UP = 2
        self.FACE_DOWN = 3

        self.player_loc = None  # only updates path if player is in a different node than previously known

    def move(self, character: PlayerCharacter, graph):
        """Manages state, calculates paths to the player, and moves the enemy according to said paths."""
        if arcade.get_distance_between_sprites(self, character) <= self.range:
            self.state = "ATTACKING"
        elif arcade.get_distance_between_sprites(self, character) > self.range:
            self.state = "ROAMING"

        # if attacking, move according to path
        if self.state is "ATTACKING":
            char_node_x = int(character.center_x / 64)
            char_node_y = int((960-character.center_y) / 64)
            cur_player_loc = (char_node_x, char_node_y)

            # if no search in progress and player has moved, re-calculate path
            if cur_player_loc != self.player_loc:
                self.find_path(graph, char_node_x, char_node_y)

            # if player is in different location, update it
            if cur_player_loc != self.player_loc:
                self.player_loc = cur_player_loc

            # TODO implement movement along path
        # if roaming, move in random directions
        elif self.state is "ROAMING":
            pass
            # TODO implement random movement

    def find_path(self, graph, player_node_x: int, player_node_y: int):
        """Setup & preparation for building a path to the player."""
        cur_node: Node = graph[int((960-self.center_y) / 64)][int(self.center_x / 64)]
        player_node: Node = graph[player_node_y][player_node_x]
        queue: deque = deque()
        queue.appendleft(cur_node)  # starting node is the enemy's current node

        path = build_path(queue, cur_node, player_node)

        # TODO remove this print block once testing is done
        builder = ""
        for y in graph:
            for x in y:
                if x is not None:
                    if x in path:
                        if path[0] is x:
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
        print(builder)


def build_path(queue: deque, start, end: Node):
    """Uses Breadth First Search to find the shortest path to the player."""
    explored = [False] * 225  # tracks whether a given node has been explored yet
    explored[start.ID] = True
    previous = [None] * 225  # tracks the previous node we came from, used for building path after exploration

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

    path = deque()
    current = end

    # build the path by following the previous list
    while current is not None:
        path.appendleft(current)
        current = previous[current.ID]

    return path
