#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import interface as i
import utils as u
import algorithms as algo
IAName = "Collect All Simple"
(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = i.initGame(IAName)
coinsNumber = len(coins) + 1
route = []

def determineNextMove(playerLocation, opponentLocation, coins):
    global route, currentcoin
    if coinsNumber != len(coins):
        routingTable = algo.dijkstra(mazeMap, playerLocation)
        route = u.way_width(routingTable, playerLocation, coins[0])
    return u.direction(playerLocation, route.pop(0))
    
i.startGameMainLoop(determineNextMove)
