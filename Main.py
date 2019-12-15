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

        **x_loc & y_loc** - X and Y locations among the node graph.

    """
    def __init__(self, x_loc: int, y_loc: int):
        self.ID = CUR_ID
        self.neighbors = [None, None, None, None]  # left, right, top bottom for indexes 0 1 2 3
        self.x_loc = x_loc
        self.y_loc = y_loc


def graph_setup():
    """Sets up the graph for Cave 1 & 2 using flood filling."""
    graph, layer_map = process_xml('Cave_1.tmx')
    graph[1][1] = Node(1, 1)
    cave_1 = flood_fill(Node(1, 1), graph, layer_map)
    graph, layer_map = process_xml('Cave_2.tmx')
    graph[1][1] = Node(1, 1)
    cave_2 = flood_fill(Node(1, 1), graph, layer_map)

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
    if node.x_loc > 0 and layer_map[node.y_loc][node.x_loc - 1] != 0:
        if graph[node.y_loc][node.x_loc - 1] is None:
            # if there isn't a node here, create one and connect it
            CUR_ID += 1
            new_node = Node(node.x_loc - 1, node.y_loc)
            node.neighbors[0] = new_node
            graph[new_node.y_loc][new_node.x_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.neighbors[0] is None:
            # connect to the existing node
            node.neighbors[0] = graph[node.y_loc][node.x_loc - 1]
    # look right
    if node.x_loc < len(graph[0]) - 1 and layer_map[node.y_loc][node.x_loc + 1] != 0:
        if graph[node.y_loc][node.x_loc + 1] is None:
            # if there isn't a node here, create one and connect it
            CUR_ID += 1
            new_node = Node(node.x_loc + 1, node.y_loc)
            node.neighbors[1] = new_node
            graph[new_node.y_loc][new_node.x_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.neighbors[1] is None:
            # connect to the existing node
            node.neighbors[1] = graph[node.y_loc][node.x_loc + 1]
    # check up
    if node.y_loc > 0 and layer_map[node.y_loc - 1][node.x_loc] != 0:
        if graph[node.y_loc - 1][node.x_loc] is None:
            # if there isn't a node here, create one and connect it
            CUR_ID += 1
            new_node = Node(node.x_loc, node.y_loc - 1)
            node.neighbors[2] = new_node
            graph[new_node.y_loc][new_node.x_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.neighbors[2] is None:
            # connect to the existing node
            node.neighbors[2] = graph[node.y_loc - 1][node.x_loc]
    # check down
    if node.y_loc < len(graph) - 1 and layer_map[node.y_loc + 1][node.x_loc] != 0:
        if graph[node.y_loc + 1][node.x_loc] is None:
            # if there isn't a node here, create one and connect it
            CUR_ID += 1
            new_node = Node(node.x_loc, node.y_loc + 1)
            node.neighbors[3] = new_node
            graph[new_node.y_loc][new_node.x_loc] = new_node

            # recursively call the new node
            flood_fill(new_node, graph, layer_map)
        elif node.neighbors[3] is None:
            # connect to the existing node
            node.neighbors[3] = graph[node.y_loc + 1][node.x_loc]
    else:
        return  # end the recursive chaining when all directions have been checked

    return graph


def main():
    cave_1_graph, cave_2_graph = graph_setup()

    # TODO remove this print block once testing is done
    builder = ""
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

    window: RPG_Map.Map = RPG_Map.Map(cave_1_graph, cave_2_graph)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
