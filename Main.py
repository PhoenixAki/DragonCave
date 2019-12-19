import pathlib
import xml.etree.ElementTree
import arcade
import RPG_Map

CUR_ID = 1  # global to avoid bug with incrementing it in recursive context


class Node:
    """
    Used for flood filling cave 1 and 2 for enemy traversal.

    Notable Parameters:
        **ID** - Distinct ID for this node.

        **neighbors** - List of up to 4 neighbor nodes on a graph.

        **x_node_loc & y_node_loc** - X and Y locations among the node graph (left->right and up->down).

        **x_pixel_loc & y_pixel_loc** - Center of X and Y locations among the pixel graph (left->right and down->up).
    """
    def __init__(self, x_node_loc: int, y_node_loc: int, x_pixel_loc: int, y_pixel_loc: int):
        self.ID = CUR_ID
        self.neighbors = [None, None, None, None]  # left, right, top bottom for indexes 0 1 2 3
        self.x_node_loc = x_node_loc
        self.y_node_loc = y_node_loc
        self.x_pixel_loc = x_pixel_loc
        self.y_pixel_loc = y_pixel_loc


def graph_setup():
    """Sets up the graph for Cave 1 & 2 using flood filling."""
    graph, layer_map = process_xml('Cave_1.tmx')
    initial_node: Node = Node(1, 1, 96, 864)
    graph[1][1] = initial_node
    cave_1 = flood_fill(initial_node, graph, layer_map)
    graph, layer_map = process_xml('Cave_2.tmx')
    initial_node = Node(1, 1, 96, 864)  # make new copy to not repeat the first one
    graph[1][1] = initial_node
    cave_2 = flood_fill(initial_node, graph, layer_map)

    return cave_1, cave_2


def process_xml(path):
    """Loads and processes the xml files for Cave 1 & 2."""
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
        # split based on comma to get each element, and append to matrix
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
    """Checks all 4 directions for walls, empty spaces, or other nodes to connect to. Returns the filled in graph."""
    global CUR_ID

    # look left
    if node.x_node_loc > 0 and layer_map[node.y_node_loc][node.x_node_loc - 1] != 0:
        if graph[node.y_node_loc][node.x_node_loc - 1] is None:
            # if there isn't a node here, create one and connect it
            CUR_ID += 1
            new_node = Node(node.x_node_loc - 1, node.y_node_loc, node.x_pixel_loc - 64, node.y_pixel_loc)
            node.neighbors[0] = new_node
            graph[new_node.y_node_loc][new_node.x_node_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.neighbors[0] is None:
            # connect to the existing node
            node.neighbors[0] = graph[node.y_node_loc][node.x_node_loc - 1]
    # look right
    if node.x_node_loc < 14 and layer_map[node.y_node_loc][node.x_node_loc + 1] != 0:
        if graph[node.y_node_loc][node.x_node_loc + 1] is None:
            # if there isn't a node here, create one and connect it
            CUR_ID += 1
            new_node = Node(node.x_node_loc + 1, node.y_node_loc, node.x_pixel_loc + 64, node.y_pixel_loc)
            node.neighbors[1] = new_node
            graph[new_node.y_node_loc][new_node.x_node_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.neighbors[1] is None:
            # connect to the existing node
            node.neighbors[1] = graph[node.y_node_loc][node.x_node_loc + 1]
    # check up
    if node.y_node_loc > 0 and layer_map[node.y_node_loc - 1][node.x_node_loc] != 0:
        if graph[node.y_node_loc - 1][node.x_node_loc] is None:
            # if there isn't a node here, create one and connect it
            CUR_ID += 1
            new_node = Node(node.x_node_loc, node.y_node_loc - 1, node.x_pixel_loc, node.y_pixel_loc + 64)
            node.neighbors[2] = new_node
            graph[new_node.y_node_loc][new_node.x_node_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.neighbors[2] is None:
            # connect to the existing node
            node.neighbors[2] = graph[node.y_node_loc - 1][node.x_node_loc]
    # check down
    if node.y_node_loc < 14 and layer_map[node.y_node_loc + 1][node.x_node_loc] != 0:
        if graph[node.y_node_loc + 1][node.x_node_loc] is None:
            # if there isn't a node here, create one and connect it
            CUR_ID += 1
            new_node = Node(node.x_node_loc, node.y_node_loc + 1, node.x_pixel_loc, node.y_pixel_loc - 64)
            node.neighbors[3] = new_node
            graph[new_node.y_node_loc][new_node.x_node_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.neighbors[3] is None:
            # connect to the existing node
            node.neighbors[3] = graph[node.y_node_loc + 1][node.x_node_loc]
    else:
        return  # end the recursive chaining when all directions have been checked

    return graph


def main():
    cave_1_graph, cave_2_graph = graph_setup()

    # TODO uncomment these print blocks to display the 2 graphs with node IDs
    '''builder = ""
    for y in cave_1_graph:
        for x in y:
            if x is not None:
                if x.ID < 10:
                    builder += str(x.ID) + "   "
                elif 10 <= x.ID < 100:
                    builder += str(x.ID) + "  "
                elif x.ID >= 100:
                    builder += str(x.ID) + " "
            else:
                builder += "x   "
        builder += "\n"
    print(builder)

    builder = ""
    for y in cave_2_graph:
        for x in y:
            if x is not None:
                if x.ID < 10:
                    builder += str(x.ID) + "   "
                elif 10 <= x.ID < 100:
                    builder += str(x.ID) + "  "
                elif x.ID >= 100:
                    builder += str(x.ID) + " "
            else:
                builder += "x   "
        builder += "\n"
    print(builder)'''

    window: RPG_Map.Map = RPG_Map.Map(cave_1_graph, cave_2_graph)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
