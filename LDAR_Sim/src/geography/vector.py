# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        geography.vector
# Purpose:     Various vector operations
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#

def grid_contains_point(point_coord, grid_list_coord):
    """ Identify if a point is within a grid of coordinates

    Args:
        point_coord ([lat,lon]): Coordinates of a point
        grid_list_coord (list): List of grid centroids

    Returns:
        tuple: (boolean) is contained in point , and an exit message if false
    """
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
