#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import interface as api
import utils as u
import algorithms as algo

import random
from functools import lru_cache
import heapq
import time

IAName = "Collect All Simple"
(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = api.initGame(IAName)
coinsNumber = len(coins) + 1
route = []


def generate_population(playerLocation, coins, coins_dists, pop_size=100):
    """Generate a random population of routes
    TODO :
    - make something smarter
    """
    population = []
    heapq.heapify(population)
    for _ in range(pop_size):
        route = [playerLocation]
        coins_left = coins[:]
        for i in range(len(coins)):
            route.append(pick_good_coin(route[-1], coins_left, coins_dists))
            coins_left.remove(route[-1])
        # random.shuffle(coins)
        # route = [playerLocation] + coins
        score = evaluate_route(route, coins_dists)
        heapq.heappush(population, (score, route))

    return population


def pick_good_coin(init_loc, coins, coins_dists):
    normalisation = sum( (1. / coins_dists[init_loc][c])**2 for c in coins)
    seed = random.random()
    i = 0.
    for c in coins:
        i += (1. / coins_dists[init_loc][c])**2 
        if i > seed * normalisation:
            coin = c
            break

    return coin


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


# @lru_cache(maxsize=None)
def evaluate_route(route, coins_dists):
    route_score = 0
    for i in range(len(route) - 1):
        l1, l2 = route[i], route[i+1]
        if l1 == l2:
            api.debug(route)
        route_score += coins_dists[l1][l2]
    return route_score


def update_pop(population, coins, coins_dists, selection=5, new=50):
    bests = heapq.nlargest(selection, population)
    n = len(population) - selection - new
    population = population[:selection]

    for i in range(n):
        f_score, father = random.choice(bests)
        m_score, mother = random.choice(bests)
        son = []
        for f, m in zip(father, mother):
            e = random.choice((f, m))
            if e not in son:
                son.append(e)

        son_score = evaluate_route(son, coins_dists)
        heapq.heappush(population, (son_score, son))

    new_genes = generate_population(son[0], coins, coins_dists, pop_size=new)
    population = [i for i in heapq.merge(population, new_genes)]

    return population


def init_game(mazeWidth, mazeHeight, maze_map, preparationTime, turnTime, playerLocation, opponentLocation, coins):
    TURNS = 1

    api.debug("Distances...")
    t = time.time()
    all_good_dists, all_good_routes = dists_from_each(coins + [playerLocation], maze_map)
    api.debug(time.time() - t)
    api.debug("Population...")
    population = generate_population(playerLocation, coins, all_good_dists)
    for i in range(TURNS + 1):
        population = update_pop(population, coins, all_good_dists)
        score, route = population[0]
        if i % 100 == 0:
            api.debug("%s : %s" % (i, score))
    api.debug("Start...")
    # return location_list_to_route(route, all_good_routes)


def location_list_to_route(locations, routes_list):
    route = []
    for i in range(len(locations) - 1):
        l1, l2 = locations[i], locations[i+1]
        route += routes_list[l1][l2]
    return route


def determineNextMove(playerLocation, opponentLocation, coins):
    global route
    if len(route) == 0:
        pick_good_coin(playerLocation, coins, coins_dists)
    return u.direction(playerLocation, route.pop(0))

route = init_game(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins)
# route.pop(0)
api.startGameMainLoop(determineNextMove)
