#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils as u
import algorithms as algo
import interface as api
#import statistics as stats

IAName = "package"

(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = api.initGame(IAName)


best_weight = float("inf")
best_path = []
packages = {}
route_table = {}

def exhaustive(left, node, path, weight, coins_graph):
    """Fill best_path with the ROUTE to get all the coins in a minimal time"""
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
    """Fill packages, also create the route table from any coin to any coin """
    global packages, route_table, dists
    used = []
    dists, route_table = u.dists_from_each(coins+[playerLocation], mazeMap)
    dists_list = sorted([d for di in dists for d in di])
    quart_dist = dists_list[len(dists_list)//4]
    for c in coins:
        for k in coins:
            if dists[c][k] < quart_dist and k not in used and c not in used and k != c:
                used.append(c)
                used.append(k)
                packages[c] = [c]
                packages[c].append(k)
    for c in coins:
        if c not in used:
            packages[c] = [c]
    packages = [packages[p] for p in packages]
    packages = sorted(packages, key=lambda x: len(x)/dists[playerLocation][x[0]])
    api.debug(packages)
                

def initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins) :
    """Function called once at the begining of the game"""
    global route_table, packages, best_weight, best_path, route
    fill_packages(coins)
    current_package = packages.pop(0)
    exhaustive(current_package, playerLocation, [], 0, (route_table,dists))
    api.debug(best_path)

def determineNextMove(playerLocation, opponentLocation, coins):
    """Function called at each turn, must return the next move of the player"""
    global packages, route_table, best_path, best_weight, route
    if len(best_path) == 0:
        current_package = packages.pop(0)
        exhaustive(current_package, playerLocation, [], 0, (route_table,dists))
        api.debug(best_path)
    return u.direction(playerLocation, best_path.pop(0))    

    

# Init our AI
initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins)

# Starts the game
api.startGameMainLoop(determineNextMove)
                   
