#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import interface
import utils as u
# import algorithms as algo
import random

# Version 1
# This version is only based on instant distances, doesn't take account 
# for the enemy future movements

IAName = "probas"

(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = interface.initGame(IAName)
route = []
dists_matrix, route_matrix = [], []
coins_probability = {}
coins_to_get = []
best_weight = float('inf')
best_path = []
def closer_probability(player_location, enemy_location, coins, dists_matrix):
    """Return the probability that the player will get a coin based only on
    the player distance to the coin and the enemy distance to the coin
    return a dictionary coin : probability """
    probabilities = {}
    for coin in coins:
        coin_value = dists_matrix[enemy_location][coin] / float(dists_matrix[enemy_location][coin] + dists_matrix[player_location][coin])
        probabilities[coin] = coin_value
    return probabilities


def which_coin_is_next(coins, player_location, enemy_location):
    # filtred = (p for p in probabilities if dists_matrix[enemy_location][p] > dists_matrix[player_location][p])
    best_coin = min(coins, key=probabilities.get)
    return best_coin


def pb_to_get_coin(dist_to_coin):
    return 1. / (2**dist_to_coin)


def generate_random_path(start1, start2, coins, dists_matrix):
    """Generate 2 paths wich are probable the two players gonna take to win"""
    path1, path1L = [start1], 0
    path2, path2L = [start2], 0
    coins_left = coins[:]
    while len(coins_left) > 0:
        if path1L < path2L:
            current_path = path1
        else:
            current_path = path2
        current_location = current_path[-1]
        # On choisi une piece avec une probabilité inversement propotionnelle à la distance
        normalisation = sum(pb_to_get_coin(dists_matrix[current_location][coin]) for coin in coins_left)
        x = random.random() * normalisation
        sum_function = 0
        for coin in coins_left:
            sum_function += pb_to_get_coin(dists_matrix[current_location][coin])
            if sum_function > x:
                next_coin = coin
                break

        # update our lists :
        if current_path == path1:
            path1L += dists_matrix[current_location][coin]
        else:
            path2L += dists_matrix[current_location][coin]
        current_path.append(next_coin)
        coins_left.remove(next_coin)
    return path1, path2


def get_probability_coins(start_player1, start_player2, coins, dists_matrix, tests=10000):
    coins_pb = {}
    for i in range(tests):
        path_player1, path_player2 = generate_random_path(start_player1, start_player2, coins, dists_matrix)
        for coin in path_player1:
            try:
                coins_pb[coin]['player1'] += 1
            except:
                coins_pb[coin] = {'player1': 1, 'player2': 0}
        for coin in path_player2:
            try:
                coins_pb[coin]['player2'] += 1
            except:
                coins_pb[coin] = {'player1': 0, 'player2': 1}
    coins_pb = {coin: {
                        'player1': float(coins_pb[coin]['player1']) / tests,
                        'player2': float(coins_pb[coin]['player2']) / tests}
                for coin in coins_pb}
    return coins_pb


def voyageur_commerce(start_player1, coins, dists_matrix):
    global best_weight, best_path
    best_weight = float('inf')
    best_path = []
    path, _ = exhaustive(coins, [start_player1], 0, dists_matrix)
    path.pop(0)

    return path


def exhaustive(coins_left, path, weight, dists_matrix):
    global best_weight, best_path
    """Fill best_path with the ROUTE to get all the coins in a minimal time"""

    if len(coins_left) == 0:
        return path, weight
    low_weight = weight
    low_weight += len(coins_left) * 2
    if low_weight > best_weight:  # TODO : improve that to to heuristics
        return None, float('inf')

    for coin in coins_left:
        coins_to_pass = coins_left[:]
        coins_to_pass.remove(coin)

        path_to_pass = path + [coin]
        weight_to_pass = weight + dists_matrix[coin][path[-1]]

        returned_path, returned_weight = exhaustive(coins_to_pass, path_to_pass, weight_to_pass, dists_matrix)
        if returned_weight < best_weight and not returned_weight > best_weight:
            best_path, best_weight = returned_path, returned_weight
    return best_path, best_weight


def coins_close(playerLocation, coins, dists_matrix, limit=3):
    return [coin for coin in coins if dists_matrix[playerLocation][coin] <= limit]

#######
# In game general functions
#######


def initialisationTurn(mazeWidth, mazeHeight, maze_map, timeAllowed, playerLocation, opponentLocation, coins):
    global dists_matrix, route_matrix, coins_probability, coins_to_get
    dists_matrix, route_matrix = u.dists_from_each(coins + [playerLocation, opponentLocation], maze_map)
    coins_probability = get_probability_coins(playerLocation, opponentLocation, coins, dists_matrix, tests=100)
    interface.debug(coins_probability)

    # First : we go to the 11 in the middle
    coins_phase1 = [coin for coin in coins if coins_probability[coin]['player1'] > .6]
    sorted(coins_phase1, key=lambda x: coins_probability[x]['player1'], reverse=False)
    coins_to_get = coins_phase1[:10]

    coins_to_get = voyageur_commerce(playerLocation, coins_to_get, dists_matrix)


    # Then we get to the ones close to us :
    # coins_phase2 = coins_phase1[7:16]
    # coins_phase2 = voyageur_commerce(coins_phase1[-1], coins_phase2, dists_matrix)

    # coins_to_get += coins_phase2
    interface.debug(len(coins_to_get))
    interface.debug(coins_to_get)


def determineNextMove(playerLocation, opponentLocation, coins):
    global route, coins_to_get
    # First we update our dists and routes matrix :
    u.update_dists_from_each(dists_matrix, route_matrix, playerLocation, mazeMap, coins)
    u.update_dists_from_each(dists_matrix, route_matrix, opponentLocation, mazeMap, coins)

    if len(route) == 0 or route[-1] not in coins:
        coins_to_get = [c for c in coins_to_get if c in coins]
        sorted(coins_to_get, key=lambda x: dists_matrix[x][playerLocation], reverse=False)
        # probabilities = closer_probability(playerLocation, opponentLocation, coins_to_get, dists_matrix)
        # next_coin = which_coin_is_next(coins_to_get, playerLocation, opponentLocation)

        # Il y a des pièces que l'on pourrait récuperer maintenant ?
        # Une sorte de système de packets
        coins_which_are_close = coins_close(playerLocation, coins, dists_matrix)
        closest_coin = None
        for coin in coins_which_are_close:
            # If we don't already go there, and the enemy is not going there
            if coin not in coins_to_get and dists_matrix[playerLocation][coin] < dists_matrix[opponentLocation][coin]:  # TODO : magic number, we should check that with the enemy
                if closest_coin is None or dists_matrix[playerLocation][coin] < dists_matrix[playerLocation][closest_coin]:
                    closest_coin = coin
        if closest_coin is not None:
            coins_to_get.insert(0, closest_coin)
            interface.debug("Finally go to : " + str(closest_coin))

        try:
            next_coin = coins_to_get.pop(0)
        except:
            interface.debug("PHASE III")
            # Si on a plus rien, on fait un voyageur de commerce sur les pieces qui restent
            sorted(coins, key=lambda coin: dists_matrix[playerLocation][coin])
            coins_to_get = coins[:7]
            coins_to_get = voyageur_commerce(playerLocation, coins_to_get, dists_matrix)
            next_coin = coins_to_get.pop(0)

        interface.debug(coins_to_get)
        # coins_to_get.remove(next_coin)

        route = route_matrix[playerLocation][next_coin]

    # In case we pass not far from a coin :
    # Il y a des pièces que l'on pourrait récuperer maintenant ?
    # Une sorte de système de packets
    coins_which_are_close = coins_close(playerLocation, coins, dists_matrix, limit=2)
    closest_coin = None
    for coin in coins_which_are_close:
        # If we don't already go there, and the enemy is not going there
        if coin not in coins_to_get and dists_matrix[playerLocation][coin] < dists_matrix[opponentLocation][coin]:  # TODO : magic number, same : with the enemy
            if closest_coin is None or dists_matrix[playerLocation][coin] < dists_matrix[playerLocation][closest_coin]:
                closest_coin = coin
    if closest_coin is not None:
        coins_to_get.insert(0, route[-1])
        route = route_matrix[playerLocation][closest_coin]
        interface.debug("Finally go to : " + str(closest_coin))

    next_pos = route.pop(0)
    return u.direction(playerLocation, next_pos)

# Init our AI
initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins)

# Starts the game
interface.startGameMainLoop(determineNextMove)
