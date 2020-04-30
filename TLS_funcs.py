def find_node(node_position, neighbor_tracking, graph):
    ''' (tuple, dict, igraph) -> tuple

    This function identifies a node to associate with.
    1) First, it looks for neighbors for a selected node position.
    2) Then, it checks to see if that node has degree < 4
    3) If these conditions are met, then the function returns a node to bind to
    4) If there are more than 1 available nodes to bind to, a node is randomly selected

    # test for no neighbors
    >>> neighbor_dic = { (1, 2): [(1, 3)], (5, 5): 'NaN', (1, 3): [(1, 2), (1, 4)], (1, 4): [(1, 3)] }
    >>> G = Graph()
    >>> G.add_vertices(4)
    >>> G.vs['name'] = ['(1, 2)', '(1, 3)', '(1, 4)', '(5, 5)']

    >>> np = (5, 5)
    >>> find_node(np, neighbor_dic, G)
    (5, 5)

    # test for finding a node with one neighbor
    >>> np = (1, 2)
    >>> find_node(np, neighbor_dic, G)
    (1, 3)

    '''
    list_of_neighbors = neighbor_tracking[(node_position)]

    #check to see which node has degree < 4
    if list_of_neighbors != 'NaN':

        node_names = []

        for node in list_of_neighbors:
            node_degrees = graph.vs.find(name= str(node) ).degree()

            if node_degrees < 4:
                node_names.append(node)

        selected_node = random.choice(node_names)
        return selected_node

    # if there aren't any available neighbors, return the node in question's position
    if list_of_neighbors == 'NaN':
        return node_position



def bind(node_position, neighbor_position, g):
    ''' (tuple, tuple, g) -> NoneType

    Add an edge between two nodes.

    '''

    node_1 = g.vs['name'].index( str(node_position) )
    node_2 = g.vs['name'].index( str(neighbor_position) )

    g.add_edge(node_1, node_2)

def update_graph_position(g, layout_old):
    ''' (graph, dict) -> NoneType

    This function updates the positions (name attribute) in the graph.
    It adds new positions from a layout, such as layout_old.

    NOTE: This function may cause problems because I am not updating the positions by MATCHING the values
    I am simply adding new attributes to each node. Will see if this works well to continue forward
    and will update accordingly if it breaks or doesn't work the way I want it to


    '''

    i = 0
    for key, value in layout_old.iteritems():
        g.vs[i]['name'] = str(key)
        g.vs[i]['position'] = key
        g.vs[i]['index'] = value
        i = i + 1


def possible_associations(position, layout):
    ''' (tuple, dict, graph, dict, bool) -> NoneType

    This function identifies ALL possible node neigbors for EACH node.
    This positional information is stored in a dict called: neighbor_tracking

    # test for node with one neighbor

    >>> layout_dict = {(1, 2): 1, (10, 12): 10, (2, 2): 20, (100, 12): 12}
    >>> x = (1, 2)
    >>> output = possible_associations(position=x, layout=layout_dict)
    >>> output
    [(2, 2)]


    # test for node with no neighbors
    >>> layout_dict = {(1, 2): 1, (10, 12): 10, (2, 2): 20, (100, 12): 12}
    >>> x = (100, 12)
    >>> output = possible_associations(x, layout_dict)
    >>> output
    'NaN'


    '''
    posit = numpy.array([[1,0], [0,1], [-1, 0], [0,-1] ])
    new_posit = posit + position


    new_list = []
    for i in new_posit:
        b = tuple(i)

        if b in layout:
            new_list.append(b)
            #neighbors[position] = new_list

    # deal with no neighbors next to node of interest
    if len(new_list) == 0:
        #neighbors[position] = 'NaN'
        new_list = 'NaN'

    return new_list

import doctest
doctest.testmod(verbose=True)
