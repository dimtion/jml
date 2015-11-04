#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils as u
import algorithms as algo
import interface as api
import math 
#import statistics as stats

IAName = "packagev2"

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
            if weight + coins_graph[1][node][i] > best_weight:
                break
            exhaustive(new_left, i, path + coins_graph[0][node][i], weight + coins_graph[1][node][i], coins_graph)

def fill_packages(coins, mazeMap):
    """fill packages, also create the route table from any coin to any coin """
    global packages, route_table, dists
    used = []
    dists, route_table = u.dists_from_each(coins + [playerLocation], mazeMap)
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
                    left_coins.remove(c)
                    visited.append(c)
                    
    packages = [packages[p] for p in packages]
    packages = list(reversed(sorted(packages, key=lambda x: (len(x)+1)/min([dists[playerLocation][c] for c in x]))))
    for k in range(len(packages)):
        n = len(packages[k])
        if n > 5:
            p1 = packages[k][:n//2]
            p2 = packages[k][n//2:]
            if len(p1)> 5:
                p1prime = p1[:len(p1)//2]
                p1sec = p1[len(p1)//2:]
                p2prime = p2[:len(p2)//2]
                p2sec = p2[len(p2)//2:]
                packages[k] = p1prime
                packages.insert(k+1,p1sec)
                packages.insert(k+2,p2prime)
                packages.insert(k+3,p2sec)   
            else:
                packages[k] = p1
                packages.insert(k+1,p2)              

def find_players(packages, opponentLocation, playerLocation):
    """Check if opponent is in packages"""
    i1,i2 = (-1,-1)
    j1,j2 = (-1,-1)
    acc = 0
    for i in range(len(packages)):
        for k in range(len(packages[i])):
                if opponentLocation == packages[i][k]:
                    i1, i2 = i, k
                    acc = acc +1
                elif playerLocation == packages[i][k]:
                    j1, j2 = i, k
                    acc = acc +1
                if acc > 1:
                    break
    return i1,i2,j1,j2
    

def initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins) :
    """Function called once at the begining of the game"""
    global route_table, packages, best_weight, best_path, current_package, dists
    fill_packages(coins, mazeMap)
    current_package = packages.pop(0)
    exhaustive(current_package, playerLocation, [], 0, (route_table, dists))


def determineNextMove(playerLocation, opponentLocation, coins):
    """Function called at each turn, must return the next move of the player"""
    global packages, dists, route_table, best_path, best_weight, current_package
    
    if playerLocation in current_package:
        current_package.remove(playerLocation)
        
    i1,i2,j1,j2  = find_players(packages, opponentLocation, playerLocation)
    if i1 >= 0:
        packages[i1].remove(packages[i1][i2])
        if len(packages[i1]) == 0:
            packages.remove(packages[i1])
    if j1 >= 0 and opponentLocation != playerLocation:
        packages[j1].remove(packages[j1][j2])
        if len(packages[j1]) == 0:
            packages.remove(packages[j1])
                           
    if opponentLocation in current_package:
        dists, route_table = u.update_dists_from_each(dists, route_table, playerLocation, mazeMap, coins)
        if len(current_package) > 1:
            current_package.remove(opponentLocation)
        else:
            current_package = packages.pop(0)
        best_weight = float("inf")
        best_path = []
        exhaustive(current_package, playerLocation, [], 0, (route_table, dists))
           
    if len(best_path) == 0:
        packages = list(reversed(sorted(packages, key=lambda x: (len(x)+1)/min([dists[playerLocation][c] for c in x]))))
        best_weight = float("inf")
        best_path = []
        current_package = packages.pop(0)
        if len(current_package) == 1 and packages != []:
            current_package = current_package + packages.pop(0)
        exhaustive(current_package, playerLocation, [], 0, (route_table, dists))
    return u.direction(playerLocation, best_path.pop(0))    

    

# Init our AI
initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins)

# Starts the game
api.startGameMainLoop(determineNextMove)
                   
