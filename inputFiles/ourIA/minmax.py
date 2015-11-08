#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import interface
import utils as u
import algorithms as algo

import sys
# N = 10000
# sys.setrecursionlimit(N)

IAName = "minmax"

(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = interface.initGame(IAName)
route = []
# mazeMap[(-1, -1)] = ()
dists_matrix, route_matrix = [], []
coins_init_num = len(coins)
old_coins = []
playerScore, enemyScore = 0, 0
alpha, beta = float('-inf'), float('inf')


def minmax(coins_left, score_p1, len_path_p1, loc_p1, score_p2, len_path_p2, loc_p2, turn):
    """Recursive search of the winning tree"""
    global alpha, beta
    # At the end of the tree, return the value of the leaf
    if len(coins_left) == 0 or score_p2 - 1 > coins_init_num / 2 or score_p1 - 1 > coins_init_num / 2:
        return - score_p2, None, [], []  # maximizing for p1

    # Update the map data
    u.update_dists_from_each(dists_matrix, route_matrix, loc_p1, mazeMap, coins)
    u.update_dists_from_each(dists_matrix, route_matrix, loc_p2, mazeMap, coins + [loc_p1])

    # pl_won_coin = False
    pl_last_coin, en_last_coin = [], []
    # Calculating the score for each participant
    # if loc_p1 in coins_left:
    #     score_p1 += 1
    #     pl_last_coin = [loc_p1]
    #     new_coins_left.remove(loc_p1)
    #     pl_won_coin = True
    # if loc_p2 in coins_left:
    #     score_p2 += 1
    #     en_last_coin = [loc_p2]
    #     new_coins_left.remove(loc_p2)
    # if pl_won_coin and loc_p1 == loc_p2:
    #     score_p2 += 1
    #     en_last_coin = [loc_p2]

    new_coins_left = coins_left[:]
    # Player1 turn :
    if len_path_p1 <= turn:
        # Check if he is on a coin and increase his score :
        if loc_p1 in coins_left:
            score_p1 += 1
            pl_last_coin = [loc_p1]
            new_coins_left.remove(loc_p1)

        # Player on is playing, MAXIMIZING THE OVERALL SCORE
        best_value = float('-inf')
        best_coin = None

        # Search path in all coins
        for coin in coins_left:
            len_path_p1 += dists_matrix[loc_p1][coin]
            loc_p1 = coin
            node_value, _, en_path, pl_path = minmax(new_coins_left, score_p1, len_path_p1, loc_p1, score_p2, len_path_p2, loc_p2, turn + 1)
            if node_value > best_value:
                best_value = node_value
                best_coin = coin

            if beta <= best_value:  # Algo alpha-beta
                break

        beta = min(best_value, beta)
    elif len_path_p2 <= turn:  # Player2 turn
        # Check if he is on a coin and increase his score :
        if loc_p2 in coins_left:
            score_p2 += 1
            en_last_coin = [loc_p2]
            new_coins_left.remove(loc_p2)

        # Player on is playing, MINIMZING THE OVERALL SCORE
        best_value = float('+inf')
        best_coin = None

        # Search path in all coins
        for coin in coins_left:
            len_path_p2 += dists_matrix[loc_p2][coin]
            loc_p2 = coin  # route_matrix[loc_p1][coin][0]
            # if dists_matrix[loc_p2][coin] < dists_matrix[loc_p2][loc_p1] and dists_matrix[loc_p1][coin] < dists_matrix[loc_p2][loc_p1]:
            # score_p1 += 1 / 2 ** dists_matrix[loc_p1][coin]  # * min(1, dists_matrix[loc_p2][coin] / dists_matrix[loc_p1][coin]) ** 2 # Add a sort of pb
            # else:
            #     score_p1 += 1
            node_value, _, en_path, pl_path = minmax(new_coins_left, score_p1, len_path_p1, loc_p1, score_p2, len_path_p2, loc_p2, turn + 1)
            if node_value < best_value:
                best_value = node_value
                best_coin = coin
            if alpha >= best_value:  # Algo alpha-beta
                break
        alpha = max(best_value, beta)
    else:
        next_turn = min(len_path_p1, len_path_p2)
        best_value, best_coin, en_path, pl_path = minmax(new_coins_left, score_p1, len_path_p1, loc_p1, score_p2, len_path_p2, loc_p2, next_turn)

    pl_path = pl_last_coin + pl_path
    en_path = en_last_coin + en_path
    return best_value, best_coin, en_path, pl_path

    # # Todo : this is not very dynamic, if the enemy goes to the coin I want ?
    # if len_path_p1 <= len_path_p2:  # MAXIMIZING player1 turn
    #     best_value = float('-inf')
    #     best_coin = None

    #     for coin in coins_left:
    #         len_path_p1 += dists_matrix[loc_p1][coin]
    #         loc_p1 = coin  # route_matrix[loc_p1][coin][0]
    #         # if dists_matrix[loc_p2][coin] < dists_matrix[loc_p2][loc_p1] and dists_matrix[loc_p1][coin] < dists_matrix[loc_p2][loc_p1]:
    #         # score_p1 += 1 / 2 ** dists_matrix[loc_p1][coin]  # * min(1, dists_matrix[loc_p2][coin] / dists_matrix[loc_p1][coin]) ** 2 # Add a sort of pb
    #         # else:
    #         #     score_p1 += 1
    #         node_value, _, en_path, pl_path = minmax(new_coins_left, score_p1, len_path_p1, loc_p1, score_p2, len_path_p2, loc_p2)
    #         if node_value > best_value:
    #             best_value = node_value
    #             best_coin = coin

    #         # if beta < best_value:  # Algo alpha-beta
    #         #     break
    #     pl_path = pl_last_coin + pl_path
    #     alpha = min(best_value, beta)

    # else:  # MINIMIZING, player2 turn
    #     best_value = float('inf')
    #     best_coin = None

    #     for coin in coins_left:
    #         len_path_p2 += dists_matrix[loc_p1][coin]
    #         loc_p2 = coin   # route_matrix[loc_p2][coin][0]

    #         # len_path_p2 += dists_matrix[loc_p2][coin]
    #         # score_p2 += 1 / 2 ** dists_matrix[loc_p2][coin]  # Add a sort of pb
    #         node_value, _, en_path, pl_path = minmax(new_coins_left, score_p1, len_path_p1, loc_p1, score_p2, len_path_p2, loc_p2)
    #         if node_value < best_value:
    #             best_value = node_value
    #             best_coin = coin
    #         alpha = max(best_value, alpha)
    #         # if alpha > node_value:  # Algo alpha-beta
    #         #     break

    #     alpha = max(best_value, beta)

    # en_path = en_last_coin + en_path
    # pl_path = pl_last_coin + pl_path
    # return best_value, best_coin, en_path, pl_path


# def next_way(playerLocation, coins):
#     candidates = algo.dijkstra(mazeMap, playerLocation)
#     dist = float("inf")
#     coin = (-1, -1)
#     for c in coins:
#         if candidates[1][c] < dist:
#             dist = candidates[1][c]
#             coin = c
#     coins.remove(coin)
#     return u.way_width(candidates[0], playerLocation, coin)


def coins_close(playerLocation, coins, dists_matrix, limit=3):
    return [coin for coin in coins if dists_matrix[playerLocation][coin] <= limit]


def initialisationTurn(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins):
    global route, dists_matrix, route_matrix
    # route = next_way(playerLocation, coins)
    dists_matrix, route_matrix = u.dists_from_each(coins + [playerLocation, opponentLocation], mazeMap)


def determineNextMove(playerLocation, opponentLocation, coins):
    global route, old_coins, playerScore, enemyScore
    u.update_dists_from_each(dists_matrix, route_matrix, playerLocation, mazeMap, coins)
    u.update_dists_from_each(dists_matrix, route_matrix, opponentLocation, mazeMap, coins + [playerLocation])

    # Calculate our score and en score :
    if playerLocation in old_coins and playerLocation not in coins:
        playerScore += 1
    if playerLocation in old_coins and playerLocation not in coins:
        enemyScore += 1

    if len(route) == 0 or route[-1] not in coins:
        winning_value, next_coin, en_best_path, pl_best_path = minmax(coins, playerScore, 0, playerLocation, enemyScore, 0, opponentLocation, 0)
        interface.debug(pl_best_path)
        interface.debug(en_best_path)
        interface.debug("going to : " + str(next_coin) + " with a probable score of : " + str(winning_value))
        route = route_matrix[playerLocation][next_coin]

    coins_which_are_close = coins_close(playerLocation, coins, dists_matrix, limit=2)
    closest_coin = None
    for coin in coins_which_are_close:
        # If we don't already go there, and the enemy is not going there
        if dists_matrix[playerLocation][coin] < dists_matrix[opponentLocation][coin]:  # TODO : magic number, same : with the enemy
            if closest_coin is None or dists_matrix[playerLocation][coin] < dists_matrix[playerLocation][closest_coin]:
                closest_coin = coin
    if closest_coin is not None:
        pass
        # route = route_matrix[playerLocation][closest_coin]
        # interface.debug("NEAR : " + str(closest_coin))

    old_coins = coins
    next_pos = route.pop(0)
    # input()
    return u.direction(playerLocation, next_pos)

# Init our AI
initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins)

# Starts the game
interface.startGameMainLoop(determineNextMove)
