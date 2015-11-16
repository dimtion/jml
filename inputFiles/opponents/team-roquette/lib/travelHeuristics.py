#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lib.shortestPaths as sp


def generateMetaGraph (mazeMap, playerLocation, coins):
    """
    Generate a metaGraph from mazeMap, containing all coins and the player.
    This function is built on the  shortestPaths lib.
    """
    nodes = [playerLocation] + coins
    metaGraph = {}
    bestPaths  = {}

    i = len(nodes)-1
    while i >= 0:
        
        routingTable = sp.dijkstra(mazeMap, nodes[i])

        j = 0
        while j < i:

            if nodes[i] not in bestPaths :
                bestPaths[nodes[i]] = {}
                metaGraph[nodes[i]] = {}
                
            if nodes[j] not in bestPaths :
                bestPaths[nodes[j]] = {}
                metaGraph[nodes[j]] = {}

            if not metaGraph[nodes[j]].get(nodes[i], False):
                path = sp.orderPath(routingTable, nodes[i], nodes[j], [])
                distance = routingTable[nodes[j]][1]

                metaGraph[nodes[i]][nodes[j]] = distance
                bestPaths[nodes[i]][nodes[j]] = path

                metaGraph[nodes[j]][nodes[i]] = distance
                bestPaths[nodes[j]][nodes[i]] = path[::-1]

            j += 1
        
        i -= 1            
    
    return metaGraph, bestPaths



bestDistance = float('inf')
bestPaths = []

def auxi(nodeStart, nodes, distance, path):
    global bestDistance
    global bestPaths
    
    if not nodes:
        if distance < bestDistance:
            bestDistance = distance
            bestPaths = path
    else:
        for node in nodes:
            toseeNodes = list(nodes)
            toseeNodes.remove(node)
            auxi(node, toseeNodes, distance + node[1], path+[node[0]])



def travellingSalesman(nodeStart, nodes, distance, path):
    """
    Implementation of the travelling salesman problem algorithm.  
    """
    global bestDistance
    global bestPaths

    bestDistance = float('inf')
    bestPaths = []
                
    auxi(nodeStart, nodes, distance, path)
    return bestDistance, bestPaths



def findNearestCoin(mazeMap, playerLocation, coinsList):
    
    routingTable = sp.dijkstra(mazeMap, playerLocation)
    
    nearest = -1
    distance = float('inf')
    for coin in coinsList:
        if routingTable[coin][1] < distance :
            distance = routingTable[coin][1] < distance
            nearest = coin
    
    return sp.orderPath(routingTable, playerLocation, nearest, [])
