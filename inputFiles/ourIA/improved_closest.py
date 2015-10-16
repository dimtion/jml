#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import interface as api
import utils as u
import algorithms as algo

IAName = "Improved closest"
(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = api.initGame(IAName)
coinsNumber = len(coins) + 1
route = []

best_weight = float("inf")
best_path = []
currentcoin = playerLocation


def get_n_shortest(n, coins, playerLocation, dist_matrix):
    """Return the n closest coins to the player location"""
    new_coins = coins[:]
    new_coins = sorted(new_coins, key=lambda x: dist_matrix[playerLocation][x])
    return new_coins[:n]


best_weight = float("inf")
best_path = []

def exhaustive(left, node, path, weight, coins_graph):
    """Fill best_path with the best COIN SEQUENCE to get all the coins in a minimal time"""
    global best_weight, best_path

    if len(left) == 0:
        if weight < best_weight:
            best_weight = weight
            best_path = path

    else:
        for i in left:
            new_left = []
            new_left[:] = left
            new_left.remove(i)
            exhaustive(new_left, i, path + [i], weight + coins_graph[node][i], coins_graph)


def determineNextMove(player_location, opponentLocation, coins):
    """Return the next direction"""
    global route, currentcoin, meta_route, best_weight, best_path, coins_to_search
    #the second test prevents the player from going to coins which have been taken by the opponent
    if currentcoin == player_location or opponentLocation in coins_to_search:
        dists_matrix, routes_matrix = u.update_dists_from_each(dist_matrix, route_matrix, player_location, mazeMap, coins)
<<<<<<< HEAD
        coins_to_search = get_n_shortest(3, coins, player_location, dist_matrix)
        ennemy_dists = algo.dijkstra(mazeMap, opponentLocation)
        may_be_lost_coins = []
        # Remove from coins_to_search the first coin which is closer to the opponent than to the player
        for c in coins_to_search:
            if len(coins_to_search) >= 2 and ennemy_dists[1][c] < dists_matrix[player_location][c]:
                may_be_lost_coins.append(c)
        if len(may_be_lost_coins) != 0:
            coins_to_search.remove(may_be_lost_coins[0])    
=======
        coins_to_search = get_n_shortest(2, coins, player_location, dist_matrix)
>>>>>>> bd63da4adad63d55f72a0917276a528fe82eb40c
        best_weight = float("inf")
        best_path = []
        exhaustive(coins_to_search, player_location, [], 0, dist_matrix)
        meta_route = [player_location]+best_path
        route = u.location_list_to_route(meta_route, route_matrix)
        currentcoin = meta_route[1]

    return u.direction(player_location, route.pop(0))

dist_matrix, route_matrix = u.dists_from_each(coins + [playerLocation], mazeMap)
coins_to_search = [opponentLocation]

api.startGameMainLoop(determineNextMove)
