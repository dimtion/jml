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

def fill_packages(coins,mazeMap):
    """fill packages, also create the route table from any coin to any coin """
    global packages, route_table, dists
    used = []
    dists, route_table = u.dists_from_each(coins+[playerLocation], mazeMap)
    dists_list = sorted([d for di in dists for d in di])
    quart_dist = dists_list[len(dists_list)//4]
    api.debug(quart_dist)
    visited =[coins[0]]
    left_coins = coins[:]
    while len(left_coins) != 0:
        meta_current_node = left_coins.pop(0)
        packages[meta_current_node] = [meta_current_node]
        visited.append(meta_current_node) 
        while len(visited) !=0:
            current_node = visited.pop(0)
            for c in left_coins:
                if dists[c][current_node] < quart_dist:
                    packages[meta_current_node].append(c)
                    #   api.debug(packages)
                    left_coins.remove(c)
                    visited.append(c)
                    api.debug(left_coins)
        
       
                
            
            
               
    """used = []
    index_dict = {}
    dead_list = []
    for c in coins:
        for k in coins:
            if dists[c][k] < quart_dist and k != c:
                if k not in used and c not in used:
                    used.append(c)
                    used.append(k)
                    index_dict[k] = c
                    packages[c] = [c]
                    packages[c].append(k)
                else:
                    packages[c] = packages[c] + packages[index_dict[k]]
                    dead_list.append[index_dict[k]]
    for d in dead_list:
        del packages[d]    
    for c in coins:
        if c not in used:
            packages[c] = [c]"""
    api.debug(packages)
    packages = [packages[p] for p in packages]
    
    packages = list(reversed(sorted(packages, key=lambda x: len(x)/dists[playerLocation][x[0]])))
    api.debug(packages)
    api.debug(len(coins))
    api.debug(len([c for p in packages for c in p]))
                

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
  

def find_opponent(packages,opponentLocation):
    i1,i2 = (-1,-1)
    for i in range(len(packages)):
        for k in range(len(packages[i])):
            if opponentLocation == packages[i][k]:
                i1, i2 = i, k
                return i1,i2
    return i1,i2
    


def initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins) :
    """Function called once at the begining of the game"""
    global route_table, packages, best_weight, best_path, current_package
    fill_packages(coins,mazeMap)
    current_package = packages.pop(0)
    exhaustive(current_package, playerLocation, [], 0, (route_table,dists))
    #api.debug(best_path)
    #api.debug(packages)

def determineNextMove(playerLocation, opponentLocation, coins):
    """Function called at each turn, must return the next move of the player"""
    global packages, route_table, best_path, best_weight, current_package
    if playerLocation in current_package:
        current_package.remove(playerLocation)
    i1,i2 = find_opponent(packages, opponentLocation)
    if i1 >= 0:
        packages[i1].remove(packages[i1][i2])
                    
    if opponentLocation in current_package:
        current_package.remove(opponentLocation)
        best_weight = float("inf")
        best_path = []
        exhaustive(current_package, playerLocation, [], 0, (route_table,dists))
        
    if len(best_path) == 0:
        best_weight = float("inf")
        best_path = []
        current_package = packages.pop(0)
        exhaustive(current_package, playerLocation, [], 0, (route_table,dists))
        #api.debug(best_path)
    return u.direction(playerLocation, best_path.pop(0))    

    

# Init our AI
initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins)

# Starts the game
api.startGameMainLoop(determineNextMove)
                   
