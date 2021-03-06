#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import interface as api
import utils as u
# import algorithms as algo

IAName = "Improved closest"
(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = api.initGame(IAName)
coinsNumber = len(coins) + 1
route = []

best_weight = float("inf")
best_path = []
currentcoin = "gfdsf"


def get_n_shortest(n, coins, playerLocation, dist_matrix):
    sorted(coins, key=lambda x: dist_matrix[playerLocation][x])
    return coins[:n]


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


def exhau(left, node, path, best_path, weight, best_weight, coin_graph):
    if len(left) == 0:
        if weight < best_weight:
            best_weight = weight
            best_path[:] = path

    else:
        for i in left:
            new_left = []
            new_left[:] = left
            new_left.remove(i)
            exhaustive(new_left, i, path + coins_graph[0][node][i], path, weight + coins_graph[1][node][i], weight, coins_graph)

acc = 0
def determineNextMove(playerLocation, opponentLocation, coins):
    
    global route, currentcoin, acc
    u.update_dists_from_each(dist_matrix, route_matrix, playerLocation, mazeMap, coins)
    if currentcoin == playerLocation:
        best_weight = float("inf")
        best_path = []
        coins_to_search = get_n_shortest(7, coins, playerLocation, dist_matrix)
        if playerLocation in coin_to_search:
            api.debug(coin_to_search)
            api.debug(playerLocation)
        meta_route = exhaustive(coins_to_search, playerLocation, [] ,0 ,dist_matrix)
        route = u.location_list_to_route(meta_route, route_matrix)
        currentcoin = meta_route[0]
        #if currentcoin == playerLocation:
            #api.debug(meta_route)
            #api.debug(route)
            #acc+=1
            #api.debug(acc)
    return u.direction(playerLocation, route.pop(0))

dist_matrix, route_matrix = u.dists_from_each(coins + [playerLocation], mazeMap)

api.startGameMainLoop(determineNextMove)
