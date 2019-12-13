import pathlib
import arcade
import RPG_Map
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from time import sleep


def main():

    @dataclass
    class Node:
        top = None
        bottom = None
        left = None
        right = None
        x_loc: int
        y_loc: int

    def flood_fill(node: Node, graph, map):


        #
        # # print graph progress
        # for row in graph:
        #     for i in row:
        #         if i is None:
        #             print(" ", end="")
        #         else:
        #             print("X", end="")
        #     print()

        # print()
        # sleep(.2)
        # check left
        if node.x_loc > 0 and map[node.y_loc][node.x_loc - 1] != 0:
            if graph[node.y_loc][node.x_loc - 1] is None:
                # create a node to the left
                new_node = Node(x_loc=node.x_loc-1, y_loc=node.y_loc)
                # connect to node
                node.left = new_node
                # update graph
                graph[new_node.y_loc][new_node.x_loc] = new_node
                # recursive call
                flood_fill(new_node, graph, map)
            elif node.left is None:
                node.left = graph[node.y_loc][node.x_loc - 1]
        # check right
        if node.x_loc < len(graph[0]) - 1 and map[node.y_loc][node.x_loc + 1] != 0:
            if graph[node.y_loc][node.x_loc + 1] is None:
                # create node to the right
                new_node = Node(x_loc=node.x_loc + 1, y_loc=node.y_loc)
                # connect to node
                node.right = new_node
                # update graph
                graph[new_node.y_loc][new_node.x_loc] = new_node
                # recursive call
                flood_fill(new_node, graph, map)
            elif node.right is None:
                node.right = graph[node.y_loc][node.x_loc + 1]
        # check up
        if node.y_loc > 0 and map[node.y_loc - 1][node.x_loc] != 0:
            if graph[node.y_loc - 1][node.x_loc] is None:
                # create node above
                new_node = Node(x_loc=node.x_loc, y_loc=node.y_loc - 1)
                # connect to node
                node.up = new_node
                # update graph
                graph[new_node.y_loc][new_node.x_loc] = new_node
                # recursive call
                flood_fill(new_node, graph, map)
            elif node.top is None:
                node.top = graph[node.y_loc - 1][node.x_loc]
        # check down
        if node.y_loc < len(graph) - 1 and map[node.y_loc + 1][node.x_loc] != 0:
            if graph[node.y_loc + 1][node.x_loc] is None:
                # create node below
                new_node = Node(x_loc=node.x_loc, y_loc=node.y_loc + 1)
                # connect to node
                node.bottom = new_node
                # update graph
                graph[new_node.y_loc][new_node.x_loc] = new_node
                # recursive call
                flood_fill(new_node, graph, map)
            elif node.bottom is None:
                node.bottom = graph[node.y_loc + 1][node.x_loc]
        else:
            return

    # xml testing stuff
    # get path
    map_path = pathlib.Path.cwd() / 'Assets' / 'Cave_2.tmx'
    # get XML tree
    tree = ET.parse(map_path)
    # get the layers
    layers = tree.findall('layer')
    # print(layers)

    # look for 'floor_layer'
    floor_layer = None
    for layer in layers:
        # print(layer, layer.attrib)
        if layer.attrib['name'] == 'floor_layer':
            floor_layer = layer

    # get the layer matrix data
    tile_matrix_raw_text = floor_layer.find('data').text
    # take new line characters from beginning and end of matrix string
    tile_matrix_raw_text = tile_matrix_raw_text.strip()
    # split on \n to crate separate matrix rows
    tile_matrix_row_list = tile_matrix_raw_text.split('\n')
    layer_matrix = []
    for row_data in tile_matrix_row_list:
        row = ""
        if row_data[len(row_data) - 1] == ',':
            row = row_data[:-1]
        else:
            row = row_data
        row = row.split(',')
        # convert elements from strings to ints
        clean_row = [int(i) for i in row]
        layer_matrix.append(clean_row)

    # for r in layer_matrix:
    #     print(r)

    print()

    graph = []
    for _ in range(int(floor_layer.attrib['height'])):
        new_row = []
        for _ in range(int(floor_layer.attrib['width'])):
            new_row.append(None)
        graph.append(new_row)

    # for row in graph:
    #     print(row)

    print()

    # make an initial node
    initial_node = Node(x_loc=1, y_loc=1)

    flood_fill(initial_node, graph, layer_matrix)

    # print graph progress
    for row in graph:
        for i in row:
            if i is None:
                print(" ", end="")
            else:
                print("X", end="")
        print()

    # print(', '.join("%s: %s" % item for item in vars(node).items()))
    # print(f'TOP: {node.top}')
    # print(f'BOTTOM: {node.bottom}')
    # print(f'LEFT: {node.left}')
    # print(f'RIGHT: {node.right}')

    for row in graph:
        for i in row:
            if i is None:
                print(" ", end="")
            else:
                print(', '.join("%s: %s" % item for item in vars(i).items()))
                print(f'TOP: {i.top}')
                print(f'BOTTOM: {i.bottom}')
                print(f'LEFT: {i.left}')
                print(f'RIGHT: {i.right}')
                print()
        print()

    # for row in graph:
    #     print(row)



    #
    # tile_matrix = tile_matrix.strip().split('\n')
    # for x in tile_matrix:
    #     x.rstrip(',')
    #     print(x)
    # print(tile_matrix)



    window: RPG_Map.Map = RPG_Map.Map()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
