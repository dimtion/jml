# -*- coding:utf-8 -*-
#
# DORNIER Martin, CHICHPORTICH Jeremy, CARR Loïc
#
# File containing all the usefull functions and classes for our AI

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

####################################################
############# Data structures ######################
####################################################
import lib.interface as api
import lib.algorithms as algo
from lib.structs import *

####################################################
############# Utils Functions ######################
####################################################


def direction(old, new):
    """ Return the direction to move from the old location to the new location"""
    if new[0] - old[0] == -1:
        return UP
    elif new[0] - old[0] == 1:
        return DOWN 
    elif new[1] - old[1] == -1:
        return LEFT 
    elif new[1] - old[1] == 1:
        return RIGHT
    else:
        raise RuntimeError("direction: old: " + str(old) + " new: " + str(new))


def way_roy(routing, start, end):
    """Return the route from the start to the end as a list for the Roy-Warshall algorithm"""
    route = []
    current_node = start
    while current_node != end:
        route.append(current_node)
        current_node = routing[current_node][end]  # Follow the routing matrix
    route.append(end)
    return route

def way_width(routing, start, end):
    """Return the route from the start to the end as a list"""
    route = []
    current_node = end
    while current_node != start:
        route.insert(0, current_node)
        current_node = routing[current_node]  # Follow the fathers

    return route

def create_distances_routing_roy(mazeMap):
    """ Initialize the routing table and the distance table for the Roy-Warshall algorithm"""
  
    dist = {}
    route = {}
    for i in mazeMap:
        dist[i] = {k: float("inf") for k in mazeMap}
        route[i] = {k: (-1,-1) for k in mazeMap}
        # Initialize the neighbours to their real distance
        for j in mazeMap[i]:
            dist[i][j[0]] = j[1]
            route[i][j[0]] = j[0]
        route[i][i] = i
        dist[i][i] = float("inf")
    return dist, route


#### Calc all dists
def dists_from_each(locations, maze_map):
    """ Return the dists and routes from each locations
    TODO :
    - Cache routes and dists
    """
    dists_matrix = {l: {} for l in locations}
    routes_matrix = {l: {} for l in locations}

    for i in range(len(locations)):
        l1 = locations[i]
        routing_table, dists_table = algo.dijkstra(maze_map, l1)

        for j in range(0, len(locations)):
            l2 = locations[j]
            route = way_width(routing_table, l1, l2)

            dists_matrix[l1][l2] = dists_table[l2]
            routes_matrix[l1][l2] = route

            dists_matrix[l2][l1] = dists_table[l2]
            routes_matrix[l2][l1] = [l for l in reversed(route[:-1])] + [l1]

    return dists_matrix, routes_matrix


def update_dists_from_each(dists_matrix, routes_matrix, new_location, maze_map, coins):
    """Update dists_matrix, routes_matrix taking into account the player_location"""
    routing_table, dists_table = algo.dijkstra(maze_map, new_location)
    dists_matrix[new_location] = {}
    routes_matrix[new_location] = {}
    for loc in coins:
        route = way_width(routing_table, new_location, loc)

        dists_matrix[new_location][loc] = dists_table[loc]
        routes_matrix[new_location][loc] = route

        dists_matrix[loc][new_location] = dists_table[loc]
        routes_matrix[loc][new_location] = [l for l in reversed(route[:-1])] + [new_location]
    return dists_matrix, routes_matrix


def get_shortest(location, coins_list, remaining_coins):
    """ Return the nearest remaining_coins from location"""
    dists_list = coins_list[location]
    min_dist = float('inf')
    min_loc = (0, 0)
    for loc in remaining_coins:
        if dists_list[loc] < min_dist:
            min_dist = dists_list[loc]
            min_loc = loc
    return min_loc, min_dist


def location_list_to_route(locations, routes_list):
    """Convert a location list to a real route"""
    route = []
    for i in range(len(locations) - 1):
        l1, l2 = locations[i], locations[i+1]
        route += routes_list[l1][l2]

    return route
