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


    if node_position in neighbor_tracking:
        list_of_neighbors = neighbor_tracking[node_position]

        #check to see which node has degree < 4
        if list_of_neighbors != 'NaN':

            node_names = []

            for node in list_of_neighbors:
                node_degrees = graph.vs.find(name= str(node) ).degree()

                if node_degrees < 4:
                    node_names.append(node)

            selected_node = random.choice(node_names)
            return node_position
            
        # if there aren't any available neighbors, return the node in question's position
        if list_of_neighbors == 'NaN':
            return node_position
    else:
        return node_position


def bind(node_position, neighbor_position, G):
    ''' (tuple, tuple, g) -> NoneType

    Add an edge between two nodes.

    # set up
    >>> G = Graph()
    >>> G.add_vertices(4)
    >>> G.vs['name'] = ['(1, 2)', '(1, 3)', '(1, 4)', '(5, 5)']

    #test for edge binding
    >>> node_position = (1, 2)
    >>> neighbor_position = (1, 3)
    >>> bind(node_position, neighbor_position, G)
    >>> G.degree()
    [1, 1, 0, 0]

    '''

    node_1 = G.vs['name'].index( str(node_position) )
    node_2 = G.vs['name'].index( str(neighbor_position) )

    G.add_edge(node_1, node_2)


def initiate_graph_position(g, layout_old):
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

def update_neighbors(oldPosition, newPosition, layout_dict, neighbors_dict):
    ''' (tuple, tuple, dict, dict) -> NoneType

    This function updates neighbor tracking dict (neighbor_tracking) based on which nodes
    moved in the movement dict (layout_old)


    1) remove node from move_count dict (!!!not updating this for now!!!)
    2) remove it from neighbor_tracking dict
    3) add it back to neighbor_tracking dict with new position by calling the possible_associations function


    >>> oldPosi = (1, 2)
    >>> newPosi = (2, 2)
    >>> n_dict = {(1, 2):'NaN', (3, 2): 'NaN', (5, 5):'NaN', (2, 3): 'NaN'}
    >>> lo_dict = { (1, 2): 19, (3, 2): 22, (5, 5): 100, (2, 2): 340, (2, 3): 120 }

    # test for movement to nearby nodes
    >>> update(oldPosition=oldPosi, newPosition=newPosi, layout_dict=lo_dict, neighbors_dict=n_dict)

    # test updating the neighbor dict (n_dict) with the new neighbors for the node that moved (newPosi)
    >>> n_dict[newPosi]
    [(3, 2), (2, 3)]

    # test updating the NEIGHBORS neigbhor in n_dict. If it updated correctly
    # then n_dict[(3, 2)] = [(2, 2)] instead of 'NaN'
    >>> n_dict[(3, 2)]
    [(2, 2)]

    # test for succesfully updating the neighbors of the neighbors
    >>> n_dict[(2, 2)]
    [(3, 2), (2, 3)]
    '''


    #move_count.pop(oldPosition)
    #neighbors_dict.pop(oldPosition)
    if oldPosition  in neighbor_tracking:
        neighbor_tracking[newPosition] = neighbor_tracking[oldPosition]
        del neighbor_tracking[oldPosition]


        # I don't need to change layout_old because its being done in the Mover function
        #layout_dict.pop(oldPosition)

        # update neighbor_tracking dict with new position and neighbors
        new_neighbor_positions = possible_associations(position=newPosition, layout=layout_dict)

        # update the new node position with the new neighbors
        neighbors_dict[newPosition] = new_neighbor_positions

        # update the position of the NEIGHBORS neighbors: need to fix
        for pos in new_neighbor_positions:
            new_neighbor_position = possible_associations(position=newPosition, layout=layout_dict)
            #print neighbors_dict[pos]
            neighbors_dict[newPosition] = new_neighbor_position
    else:
        pass


def update_graph(G, layout, new_position, old_position):
    ''' (igraph, dict, tuple, tuple) -> NoneType

    Update graph attributes based on the node that has moved.

    This function should run inside the main code.

    The function initiate_graph_position should run at the beginning to initiate the graph attributes

    >>> lo_dict = { (1, 2): 19, (3, 2): 22, (5, 5): 100, (2, 2): 340, (2, 3): 120 }
    >>> old = (5, 5)
    >>> new = (6, 5)
    >>> G = Graph()
    >>> G.add_vertices(5)
    >>> initiate_graph_position(G, lo_dict)

    # "move" a node in the layout dict
    >>> lo_dict[new] = lo_dict.pop(old)

    # get index of position
    >>> old_position_index = G.vs['position'].index(old)

    # check initial values
    >>> G.vs[old_position_index]['position']
    (5, 5)
    >>> G.vs[old_position_index]['name']
    '(5, 5)'
    >>> G.vs[old_position_index]['index']
    100

    # update the attribute using update_graph
    >>> update_graph(G=G, layout=lo_dict, new_position=new, old_position=old)

    # test that I get new position
    >>> G.vs[old_position_index]['position']
    (6, 5)

    # test that I get new name
    >>> G.vs[old_position_index]['name']
    '(6, 5)'

    # test that I get new index
    >>> G.vs[old_position_index]['index']
    100

    '''

    # find the index of the position

    graph_index = G.vs['position'].index(old_position)

    # update each attribute
    G.vs[graph_index]['name'] = str(new_position)
    G.vs[graph_index]['position'] = new_position
    G.vs[graph_index]['index'] = layout[new_position]


def edge_selector(neigh_dict):
    ''' (dict) -> tuple

    Find a node with neighbors.

    The selected node will be interegated for edge binding with its neighbors

    neigh_dict should be the dict where neigbhors are kept



    # test when there are neighbors
    >>> neighbor_dic = { (1, 2): [(1, 3)], (5, 5): 'NaN', (1, 3): [(1, 2), (1, 4)], (1, 4): [(1, 3)] }
    >>> output = edge_selector(neighbor_dic)
    >>> output != 'NaN'
    True

    # test to make sure output is a tuple
    >>> type(output)
    <type 'tuple'>



    # test when there are no neighbors
    >>> neighbor_dic2 = { (1, 2): 'NaN', (5, 5): 'NaN', (1, 3): 'NaN', (1, 4): 'NaN' }
    >>> output = edge_selector(neighbor_dic2)
    >>> output == 'NaN'
    True

    '''

    # set up range to loop through (at worst this function is O(n) )
    index_options = range(0, len(neigh_dict) )
    val = 'NaN'

    for t in index_options:

        # randomly collect matched key value pairs
        key = random.choice(neigh_dict.keys() )
        value = neigh_dict[key]

        # if node contains neighbors (i.e, it's not 'NaN'), then choose the node
        if value != 'NaN':
            val = key
            break
        else:
            pass
    return val







import doctest
doctest.testmod(verbose=True)
