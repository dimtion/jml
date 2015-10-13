#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import interface as api
import utils as u

IAName = "Improved closest"
(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = api.initGame(IAName)
coinsNumber = len(coins) + 1
route = []

best_weight = float("inf")
best_path = []
currentcoin = playerLocation


def get_n_shortest(n, coins, playerLocation, dist_matrix):
    new_coins = coins[:]
    new_coins = sorted(new_coins, key=lambda x: dist_matrix[playerLocation][x])
    return new_coins[:n]


best_weight = float("inf")
best_path = []

def exhaustive(left, node, path, weight, coins_graph):
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
    global route, currentcoin, meta_route, best_weight, best_path, coins_to_search
    if currentcoin == player_location or opponentLocation in coins_to_search:
        dists_matrix, routes_matrix = u.update_dists_from_each(dist_matrix, route_matrix, player_location, mazeMap, coins)
        coins_to_search = get_n_shortest(2, coins, player_location, dist_matrix)
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
