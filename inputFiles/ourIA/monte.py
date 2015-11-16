#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lib.interface as interface
import lib.utils as u
import lib.algorithms as algo


IAName = "closest"

(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = interface.initGame(IAName)
route = []
mazeMap[(-1,-1)] = ()
def next_way(playerLocation, coins):
    candidates = algo.dijkstra(mazeMap, playerLocation)
    dist = float("inf")
    coin = (-1,-1)
    for c in coins:
        if candidates[1][c] < dist:
            dist = candidates[1][c]
            coin = c
    coins.remove(coin)
    return u.way_width(candidates[0], playerLocation, coin)


def initialisationTurn (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    global route
    route = next_way(playerLocation, coins)


def determineNextMove(playerLocation, opponentLocation, coins):
    global route
    if len(route) == 0:
        route = next_way(playerLocation, coins)
    else: 
        ennemy_dists = algo.dijkstra(mazeMap, opponentLocation)
        if ennemy_dists[1][route[-1]] < len(route):
            route = next_way(playerLocation, coins)
    next_pos = route.pop(0)
    return u.direction(playerLocation, next_pos)

# Init our AI
initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins)

# Starts the game
interface.startGameMainLoop(determineNextMove)
x