#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# A simple IA that assume that the opponent is a greedy, try to kill him in 100% of the time

import lib.interface as interface
import lib.utils as u
# import lib.algorithms as algo


IAName = "I'll kill you"

(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = interface.initGame(IAName)

dists_matrix, route_matrix = [], []
playerScore, enemyScore = 0, 0
old_coins = []
route = []


def get_closest_coin(player, coins, dists_matrix):
    closest_coin = coins[0]
    closest_coin_dist = dists_matrix[player][closest_coin]
    for coin in coins:
        coin_dist = dists_matrix[player][coin]
        if coin_dist < closest_coin_dist:
            closest_coin = coin
            closest_coin_dist = coin_dist
    return closest_coin, closest_coin_dist


def minmax(coins_left, score_p1, len_path_p1, loc_p1, score_p2, len_path_p2, loc_p2):
    """Recursive search of the winning tree"""
    # At the end of the tree, return the value of the leaf
    if len(coins_left) == 0 or score_p2 > 5 or score_p1 > 5:
        return score_p1, [], []  # maximizing for p1

    pl_last_coin = []
    en_last_coin = []
    best_pl_path = []
    best_en_path = []
    # Update the map data
    u.update_dists_from_each(dists_matrix, route_matrix, loc_p1, mazeMap, coins)
    u.update_dists_from_each(dists_matrix, route_matrix, loc_p2, mazeMap, coins + [loc_p1])

    # Todo : this is not very dynamic, if the enemy goes to the coin I want ?
    if len_path_p1 <= len_path_p2:  # MAXIMIZING player1 turn
        best_value = float('-inf')
        best_coin = get_closest_coin(loc_p1, coins_left, dists_matrix)[0]
        best_pl_path = []
        en_closest_coin, en_closest_coin_dist = get_closest_coin(loc_p2, coins_left, dists_matrix)

        for coin in coins_left:
            new_len_path_p1 = len_path_p1 + dists_matrix[loc_p1][coin]
            loc_p1 = coin
            new_score_p1 = score_p1 + 1
            new_coins_left = coins_left[:]
            new_coins_left.remove(coin)

            node_value, en_path, pl_path = minmax(new_coins_left, new_score_p1, new_len_path_p1, loc_p1, score_p2, len_path_p2, loc_p2)
            if node_value > best_value and (coin != en_closest_coin or dists_matrix[loc_p1][coin] <= en_closest_coin_dist):
                best_value = node_value
                best_coin = coin
                best_pl_path = pl_path
                best_en_path = en_path
        pl_last_coin = [best_coin]

    else:  # MINIMIZING, player 2 is going to the closest coin
        closest_coin, closest_coin_dist = get_closest_coin(loc_p2, coins_left, dists_matrix)

        new_len_path_p2 = len_path_p2 + closest_coin_dist
        loc_p2 = closest_coin
        new_score_p2 = score_p2 + 1
        new_coins_left = coins_left[:]
        new_coins_left.remove(closest_coin)

        node_value, en_path, pl_path = minmax(new_coins_left, score_p1, len_path_p1, loc_p1, new_score_p2, new_len_path_p2, loc_p2)

        best_value = node_value
        best_coin = closest_coin
        best_pl_path = pl_path
        best_en_path = en_path
        en_last_coin = [best_coin]

    en_path = en_last_coin + best_en_path
    pl_path = pl_last_coin + best_pl_path
    return best_value, en_path, pl_path

def minmax2(coins_left, score_p1, )
def initialisationTurn(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins):
    global route, dists_matrix, route_matrix

    dists_matrix, route_matrix = u.dists_from_each(coins + [playerLocation, opponentLocation], mazeMap)


def determineNextMove(playerLocation, opponentLocation, coins):
    global route, old_coins, playerScore, enemyScore
    u.update_dists_from_each(dists_matrix, route_matrix, playerLocation, mazeMap, coins)
    u.update_dists_from_each(dists_matrix, route_matrix, opponentLocation, mazeMap, coins + [playerLocation])

    # Calculate our score and en score :
    if playerLocation in old_coins and playerLocation not in coins:
        playerScore += 1
    if opponentLocation in old_coins and opponentLocation not in coins:
        enemyScore += 1

    if len(route) == 0 or route[-1] not in coins or 1==1:
        winning_value, en_best_path, pl_best_path = minmax(coins, playerScore, 0, playerLocation, enemyScore, 0, opponentLocation)
        interface.debug("------------")
        interface.debug(pl_best_path)
        interface.debug(en_best_path)
        interface.debug("score of : " + str(winning_value))
        route = route_matrix[playerLocation][pl_best_path[0]]

    # coins_which_are_close = coins_close(playerLocation, coins, dists_matrix, limit=2)
    # closest_coin = None
    # for coin in coins_which_are_close:
    #     # If we don't already go there, and the enemy is not going there
    #     if dists_matrix[playerLocation][coin] < dists_matrix[opponentLocation][coin]:  # TODO : magic number, same : with the enemy
    #         if closest_coin is None or dists_matrix[playerLocation][coin] < dists_matrix[playerLocation][closest_coin]:
    #             closest_coin = coin
    # if closest_coin is not None:
    #     pass
    #     # route = route_matrix[playerLocation][closest_coin]
    #     # interface.debug("NEAR : " + str(closest_coin))

    old_coins = coins
    next_pos = route.pop(0)
    return u.direction(playerLocation, next_pos)

# Init our AI
initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins)

# Starts the game
interface.startGameMainLoop(determineNextMove)
