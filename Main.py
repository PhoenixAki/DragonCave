import pathlib
import xml.etree.ElementTree
import arcade
import RPG_Map


# flood filling uses nodes to fill graph
class Node:
    def __init__(self, x_loc, y_loc):
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.x_loc = x_loc
        self.y_loc = y_loc


def graph_setup():
    graph, layer_map = process_xml('Cave_1.tmx')
    cave_1 = flood_fill(Node(1, 1), graph, layer_map)
    graph, layer_map = process_xml('Cave_2.tmx')
    cave_2 = flood_fill(Node(1, 1), graph, layer_map)

    return cave_1, cave_2


def process_xml(path):
    # load and process XML file
    map_path = pathlib.Path.cwd() / 'Assets' / path
    # parse the layers
    tree = xml.etree.ElementTree.parse(map_path)
    layers = tree.findall('layer')

    # look for 'floor_layer'
    floor_layer = None
    for layer in layers:
        if layer.attrib['name'] == 'floor_layer':
            floor_layer = layer
            break

    # parse matrix data of newline characters and turn into a list
    tile_matrix_raw_text = floor_layer.find('data').text
    tile_matrix_raw_text = tile_matrix_raw_text.strip()
    tile_matrix_row_list = tile_matrix_raw_text.split('\n')
    layer_matrix = []

    for row_data in tile_matrix_row_list:
        # split based on , to get each element, and append to matrix
        row = row_data.split(',')
        clean_row = [int(i) for i in row if i is not '']
        layer_matrix.append(clean_row)

    graph = []
    for _ in range(int(floor_layer.attrib['height'])):
        new_row = []
        for _ in range(int(floor_layer.attrib['width'])):
            new_row.append(None)
        graph.append(new_row)

    return graph, layer_matrix


def flood_fill(node: Node, graph, layer_map):
    # look left
    if node.x_loc > 0 and layer_map[node.y_loc][node.x_loc - 1] != 0:
        if graph[node.y_loc][node.x_loc - 1] is None:
            # if there isn't a node here, create one and connect it
            new_node = Node(x_loc=node.x_loc-1, y_loc=node.y_loc)
            node.left = new_node
            graph[new_node.y_loc][new_node.x_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.left is None:
            # connect to the existing node
            node.left = graph[node.y_loc][node.x_loc - 1]
    # look right
    if node.x_loc < len(graph[0]) - 1 and layer_map[node.y_loc][node.x_loc + 1] != 0:
        if graph[node.y_loc][node.x_loc + 1] is None:
            # if there isn't a node here, create one and connect it
            new_node = Node(x_loc=node.x_loc + 1, y_loc=node.y_loc)
            node.right = new_node
            graph[new_node.y_loc][new_node.x_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.right is None:
            # connect to the existing node
            node.right = graph[node.y_loc][node.x_loc + 1]
    # check up
    if node.y_loc > 0 and layer_map[node.y_loc - 1][node.x_loc] != 0:
        if graph[node.y_loc - 1][node.x_loc] is None:
            # if there isn't a node here, create one and connect it
            new_node = Node(x_loc=node.x_loc, y_loc=node.y_loc - 1)
            node.up = new_node
            graph[new_node.y_loc][new_node.x_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.top is None:
            # connect to the existing node
            node.top = graph[node.y_loc - 1][node.x_loc]
    # check down
    if node.y_loc < len(graph) - 1 and layer_map[node.y_loc + 1][node.x_loc] != 0:
        if graph[node.y_loc + 1][node.x_loc] is None:
            # if there isn't a node here, create one and connect it
            new_node = Node(x_loc=node.x_loc, y_loc=node.y_loc + 1)
            node.bottom = new_node
            graph[new_node.y_loc][new_node.x_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.bottom is None:
            # connect to the existing node
            node.bottom = graph[node.y_loc + 1][node.x_loc]
    else:
        return  # end the recursive chaining when all directions have been checked

    return graph


def main():
    cave_1_graph, cave_2_graph = graph_setup()
    window: RPG_Map.Map = RPG_Map.Map(cave_1_graph, cave_2_graph)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
