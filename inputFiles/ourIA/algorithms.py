# -*- coding:utf-8 -*-
#
# DORNIER Martin, CHICHPORTICH Jeremy, CARR Loïc
#
# File containing all the useful algorithms of our AI
import utils as u


def pathWidth(mazeMap, start, data_struct=None):
    """ Return the routing table from the origin location to 
        all the other locations as a dictionary using path width algorithm"""
    waiting = data_struct()
    visited = []
    routing = {}
    waiting.append(start)
    while not len(waiting) == 0:
        current_node = waiting.pop()
        visited.append(current_node)
        for neighbour in mazeMap[current_node]:
            if neighbour[0] not in visited and neighbour not in waiting:
                routing[neighbour[0]] = current_node
                waiting.append(neighbour[0])
    return routing

def dijkstra(mazeMap, start):
    """ Return the routing table from the origin location to 
    all the other locations as a dictionary using Dijkstra algorithm"""
    waiting = u.MinStack()
    routing = {}
    waiting.add(start,0)
    distances = u.filledStack(mazeMap)
    while not waiting.empty():
        current_node, distance = waiting.remove()
        for neighbour in mazeMap[current_node]:
            dist_by_current = distance + neighbour[1]
            if distances[neighbour[0]] > dist_by_current:
                distances[neighbour[0]] = dist_by_current
                waiting.add(neighbour[0], dist_by_current)                    
                routing[neighbour[0]] = current_node
    return routing, distances

def royWarshall(mazeMap):
    """ Return the routing table from any point to any point
    using Roy-Warshall algorithm"""
    distances, routing = u.create_distances_routing_roy(mazeMap)
    for k in mazeMap:
        for i in mazeMap:
            for j in mazeMap:
                alt_distance = distances[i][k] + distances[k][j]
                if alt_distance < distances[i][j]:
                    distances[i][j] = alt_distance
                    if k in [v[0] for v in mazeMap[i]]:
                        routing[i][j] = k
                    else :
                        routing[i][j]=routing[i][k]
    return routing
