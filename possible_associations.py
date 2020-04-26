def possible_associations(x, layout_old, neighbor_tracking):
    ''' (tuple, dict, dict) -> NoneType

    This function identifies ALL possible node neigbors for EACH node.
    This positional information is stored in a dict called: neighbor_tracking

    '''
    posit = numpy.array([[1,0], [0,1], [-1, 0], [0,-1] ])

    new_posit = posit + x
    new_list = []
    for i in new_posit:
        b = tuple(i)
        if b in layout_old:
            new_list.append(b)
            neighbor_tracking[x] = new_list
