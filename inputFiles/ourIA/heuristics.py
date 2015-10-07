#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import interface as api
import utils as u
import algorithms as algo

from time import time
from random import randrange

IAName = "OPT OPTIMISATION"
(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = api.initGame(IAName)
coinsNumber = len(coins) + 1
route = []
old_coins = [playerLocation]


def dists_from_each(locations, maze_map):
    """ Return the dists and routes from each locations
    TODO :
    - Cache routes and dists
    """
    dists_matrix = {l: {} for l in locations}
    routes_matrix = {l: {} for l in locations}

    for i in range(len(locations)):
        l1 = locations[i]
        routing_table, dists_table = algo.dijkstra(maze_map, l1)

        for j in range(i + 1, len(locations)):
            l2 = locations[j]
            route = u.way_width(routing_table, l1, l2)

            dists_matrix[l1][l2] = dists_table[l2]
            routes_matrix[l1][l2] = route

            dists_matrix[l2][l1] = dists_table[l2]
            routes_matrix[l2][l1] = [l for l in reversed(route[:-1])] + [l1]

    return dists_matrix, routes_matrix


def update_dists_from_each(dists_matrix, routes_matrix, new_location, maze_map, coins):
    routing_table, dists_table = algo.dijkstra(maze_map, new_location)
    dists_matrix[new_location] = {}
    routes_matrix[new_location] = {}
    for loc in coins:
        route = u.way_width(routing_table, new_location, loc)

        dists_matrix[new_location][loc] = dists_table[loc]
        routes_matrix[new_location][loc] = route

        dists_matrix[loc][new_location] = dists_table[loc]
        routes_matrix[loc][new_location] = [l for l in reversed(route[:-1])] + [new_location]
    return dists_matrix, routes_matrix


def get_shortest(location, coins_list, remaining_coins):
    dists_list = coins_list[location]
    min_dist = float('inf')
    min_loc = (0, 0)
    for loc in remaining_coins:
        if dists_list[loc] < min_dist:
            min_dist = dists_list[loc]
            min_loc = loc
    return min_loc, min_dist


def path_from_nearest(playerLocation, opponentLocation, coins, all_dists):
    # remaining_coins = [c for c in coins if all_dists[c][playerLocation] < all_dists[c][opponentLocation]]  # ne marche pas très bien
    # avg = sum(all_dists[playerLocation][c] for c in coins) / len(coins)
    # remaining_coins = [c for c in coins if all_dists[c][playerLocation] < avg + 1]
    # if len(remaining_coins) < 5:
    remaining_coins = coins[:]

    coins_route = [playerLocation]
    coins_length = 0
    while len(remaining_coins) > 0:
        next_loc, next_dist = get_shortest(coins_route[-1], all_dists, remaining_coins)
        coins_route.append(next_loc)
        coins_length += next_dist
        remaining_coins.remove(next_loc)
    return coins_route, coins_length


def location_list_to_route(locations, routes_list):
    route = []
    for i in range(len(locations) - 1):
        l1, l2 = locations[i], locations[i+1]
        route += routes_list[l1][l2]
    return route


def evaluate_route(route, coins_dists):
    route_score = 0
    for i in range(len(route) - 1):
        l1, l2 = route[i], route[i+1]
        route_score += coins_dists[l1][l2]
    return route_score


#### OPTIMISATION
def opt_algorithm(route, route_len, all_dists):
    key1 = randrange(0, len(route) - 1)
    key2 = randrange(key1 + 1, len(route))
    part1 = route[:key1]
    part2 = route[key1:key2]
    part3 = route[key2:]

    new_route = part1 + [k for k in reversed(part2)] + part3
    # api.debug(key)
    # api.debug(route)
    new_route_len = evaluate_route(new_route, all_dists)
    if route_len > new_route_len:
        api.debug("FROM " + str(route_len) + " TO " + str(new_route_len))
        return new_route, new_route_len
    else:
        return route, route_len


def determineNextMove(playerLocation, opponentLocation, coins):
    global route, currentcoin, old_coins, meta_route, meta_route_len, next_coin
    # api.debug("Update routes...")
    t = time()
    t0 = t
    # update for our location
    update_dists_from_each(dists_matrix, routes_matrix, playerLocation, mazeMap, coins)
    # update the oponent location
    try:
        update_dists_from_each(dists_matrix, routes_matrix, opponentLocation, mazeMap, coins)
    except:
        pass
    # api.debug("Time : " + str(time() - t))
    meta_route = [c for c in meta_route if c in coins]
    # api.debug("Calc init route...")
    t = time()
    if playerLocation in old_coins:
        next_coin = meta_route.pop(0)
        route = location_list_to_route([playerLocation, next_coin], routes_matrix)
    # api.debug("Time : " + str(time() - t))  

    next_move = route.pop(0)  # Discard the first element to avoid back and forth

    for _ in range(3000):
        if len(meta_route) > 2:
            meta_route_len, meta_route_len = opt_algorithm(meta_route, meta_route_len, dists_matrix)

    t_tot = time() - t0
    # api.debug("TOTAL TIME : " + str(t_tot))
    if t_tot > .1:
        api.debug("/!\OVER_SHOT : +" + str(t_tot - .1))
    old_coins = coins
    return u.direction(playerLocation, next_move)

########
######## EXECUTION
########

api.debug("Calc all dists...")
t = time()
t0 = t
locs = [playerLocation] + coins
if opponentLocation != (-1, -1):
    locs.append(opponentLocation)

dists_matrix, routes_matrix = dists_from_each(locs, mazeMap)
api.debug("Time : " + str(time() - t))

api.debug("Calc init route...")
t = time()
meta_route, meta_route_len = path_from_nearest(playerLocation, opponentLocation,  coins, dists_matrix)
next_coin = meta_route.pop(0)

api.debug("Time : " + str(time() - t))
api.debug(meta_route_len)

api.debug("Optimising route...")
t = time()
for _ in range(100000):
    meta_route, meta_route_len = opt_algorithm(meta_route, meta_route_len, dists_matrix)
api.debug("Time : " + str(time() - t))

api.debug("\nTotal : " + str(time() - t0))
api.debug("GO")

api.startGameMainLoop(determineNextMove)
