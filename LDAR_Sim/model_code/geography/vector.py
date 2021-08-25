def grid_contains_point(point_coord, grid_list_coord):
    is_contained = True
    exit_msg = None
    if float(point_coord[0]) > max(grid_list_coord[0]):
        exit_msg = 'Simulation terminated: One or more sites is too ' + \
            'far North and is outside the spatial bounds of ' + \
            'your grid data!'
        is_contained = False
    if float(point_coord[0]) < min(grid_list_coord[0]):
        exit_msg = 'Simulation terminated: One or more sites is too ' + \
            'far South and is outside the spatial bounds of ' + \
            'your grid data!'
        is_contained = False
    if float(point_coord[1]) > max(grid_list_coord[1]):
        exit_msg = 'Simulation terminated: One or more sites is too ' + \
            'far East and is outside the spatial bounds of ' + \
            'your grid data!'
        is_contained = False
    if float(point_coord[1]) < min(grid_list_coord[1]):
        exit_msg = 'Simulation terminated: One or more sites is too ' + \
            'far West and is outside the spatial bounds of ' + \
            'your grid data!'
        is_contained = False
    return is_contained, exit_msg
