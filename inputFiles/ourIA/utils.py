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
import interface as api

class StackQueue(list):
    """A class that is either a Stack or a Queue"""

    def __init__(self, isStack=True):
        self.isStack = isStack

    def pop(self):
        if self.isStack:
            return super().pop()
        else:
            return super().pop(0)

class Stack(StackQueue):
    """ A stack"""
    def __init__(self):
        super().__init__(isStack=True)

class Queue(StackQueue):
    """A queue"""
    def __init__(self):
        super().__init__(isStack=False)

class MinStack(dict):
    """The min-stack class"""

    def add(self, elt, weight):
        """Add an element to the MinStack with elt as key and weight as label"""
        self[elt] = weight
    
    def remove(self):
        """Remove and return from the MinStack its minimum element 
        and the key of the minimum element as a tuple"""
        mini = min(j for i,j in self.items())
        key_mini = next(key for key, value in self.items() if value == mini)
        del self[key_mini]
        return key_mini, mini

    def empty(self):
        """Return True if the MinStack is empty, else return False"""
        return len(self) == 0

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

def filledStack(mazeMap):
    """Return a MinStack of the maze nodes with distances initialized to 'infinity' """
    stack = MinStack()
    for node in mazeMap:
        stack.add(node, float("inf"))
    return stack


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




