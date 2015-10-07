#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils as u
import algorithms as algo
import interface

IAName = "package"

(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = interface.initGame(IAName)


best_weight = float("inf")
best_path = []
packages = {}
route_table = {}

def exhaustive(left, node, path, weight, coins_graph):
    global best_weight, best_path
    
    if len(left) == 0:
        if weight < best_weight:
            best_weight = weight
            best_path[:] = path
            
    else:
        for i in left:
            new_left = []
            new_left[:] = left
            new_left.remove(i)
            exhaustive(new_left, i, path + coins_graph[0][node][i], weight + coins_graph[1][node][i], coins_graph)

def fill_packages(coins):
    """fill packages, also create the route table from any coin to any coin """
    global packages, route_table
    used = []
    route_table = u.coins_graph(mazeMap, coins + [playerLocation])
    for c in coins:
        for k in coins:
            if route_table[1][c][k] < 8 and k not in used and c not in used and k != c:
                used.append(c)
                used.append(k)
                packages[c] = [c]
                packages[c].append(k)
    for c in coins:
        if c not in used:
            packages[c] = [c]
    
                

def mini_pack(packs):
    """used in sorted_pack to sort packages"""
    m = packs[0]
    i = 0
    for k in range(1, len(packs)):
        if len(packs[k])< len(m):
            m = packs[k]
            i = k
    return [m, i]

def sorted_pack():
    """Transform packages in a list and sort it by size of package"""
    global packages
    packages = [packages[p] for p in packages]
    n=len(packages)
    for i in range(n-1,0,-1):
        i_m = mini_pack(packages[:i+1])[1]
        if i_m != i:
            packages[i_m],packages[i] = packages[i],packages[i_m]
  

  
    


def initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins) :
    """Function called once at the begining of the game"""
    global route_table, packages, best_weight, best_path
    fill_packages(coins)
    sorted_pack()
    routes = {}
    dists = {}
    routes[playerLocation] = route_table[0][playerLocation]
    dists[playerLocation] = route_table[1][playerLocation]
    for i in packages[0]:
        routes[i] = route_table[0][i]
        dists[i] = route_table[1][i]
        coinDist = (routes, dists)
    exhaustive(packages[0], playerLocation, [], 0, coinDist)
    interface.debug(best_path)


def determineNextMove(playerLocation, opponentLocation, coins):
    """Function called at each turn, must return the next move of the player"""
    global packages, route_table, best_path, best_weight
    for i in route_table[1][playerLocation]:
        if route_table[1][playerLocation][i]< 4:
            return u.direction(playerLocation, route_table[0][playerLocation][i][0])
    if len(best_path) == 0:
        routes = {}
        dists = {}
        best_weight = float("inf")
        routes[playerLocation] = route_table[0][playerLocation]
        dists[playerLocation] = route_table[1][playerLocation]
        packages = packages[1:]
        interface.debug(packages)
        if playerLocation in packages[0]:
            packages[0].remove(playerLocation)
        for i in packages[0]:
            routes[i] = route_table[0][i]
            dists[i] = route_table[1][i]
        coinDist = (routes, dists)
        exhaustive(packages[0], playerLocation, [], 0, coinDist)
        interface.debug(best_path)
    return u.direction(playerLocation, best_path.pop(0))

# Init our AI
initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins)

# Starts the game
interface.startGameMainLoop(determineNextMove)
                   
