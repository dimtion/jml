#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import interface as api
import utils as u
import algorithms as algo

IAName = "Improved closest v2"
(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = api.initGame(IAName)
coinsNumber = len(coins) + 1
route = []
mazeMap[(-1,-1)] = ()
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

def initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, player_location, opponentLocation, coins) :
    """Initialize some variables during the preparation time"""
    global route, currentcoin, meta_route, best_weight, best_path, coins_to_search, index
	#dists_matrix, routes_matrix = u.dists_from_each(coins + [playerLocation], mazeMap)
    coins_to_search = get_n_shortest(5, coins, player_location, dists_matrix)
    best_weight = float("inf")
    best_path = []
    exhaustive(coins_to_search, player_location, [], 0, dists_matrix)
    meta_route = [player_location] + best_path
    route = u.location_list_to_route(meta_route, routes_matrix)
    index = 1
    currentcoin = meta_route[1]
	
def determineNextMove(player_location, opponentLocation, coins):
    """Return the next direction"""
    global route, currentcoin, meta_route, best_weight, best_path, coins_to_search, index
    if opponentLocation in coins_to_search:
        coins_to_search, meta_route, route = change_way(coins, opponentLocation, player_location)[:3]
        index = 0
    elif currentcoin == player_location: 
        if len(route) != 0:
            old_dist = algo.dijkstra(mazeMap, player_location)[1][meta_route[index+1]]
        coins_to_search2, meta_route2, route2, new_dist = change_way(coins, opponentLocation, player_location)

        #dist_matrix, route_matrix = u.update_dists_from_each(dists_matrix, routes_matrix, player_location, mazeMap, coins)
        #coins_to_search = get_n_shortest(3, coins, player_location, dists_matrix)
    	
        #ennemy_dists = algo.dijkstra(mazeMap, opponentLocation)
        #for c in coins_to_search:
            #if len(coins_to_search) >= 2 and ennemy_dists[1][c] < dists_matrix[player_location][c]:
               # coins_to_search.remove(c)
                #break
        		
        #best_weight = float("inf")
        #best_path = []
        #exhaustive(coins_to_search, player_location, [], 0, dist_matrix)
        #meta_route2 = [player_location] + best_path
        #route2 = u.location_list_to_route(meta_route2, route_matrix)
        #new_dist = dist_matrix[player_location][meta_route2[1]]
		
        if len(route) == 0 or old_dist - new_dist > 3:
            route = route2
            meta_route = meta_route2    
            index = 0
        index += 1
        currentcoin = meta_route[index]
    #api.debug(route)
    return u.direction(player_location, route.pop(0))

def change_way(coins, opponentLocation, player_location):
    """Return the new coin to search, coin sequence, route and the distance from the player to the first coin of the route"""
    global best_weight, best_path
    dist_matrix, route_matrix = u.update_dists_from_each(dists_matrix, routes_matrix, player_location, mazeMap, coins)
    coins_to_search = get_n_shortest(5, coins, player_location, dists_matrix)
    ennemy_dists = algo.dijkstra(mazeMap, opponentLocation)
    for c in coins_to_search:
        if len(coins_to_search) >= 2 and ennemy_dists[1][c] < dists_matrix[player_location][c]:
            coins_to_search.remove(c)
            break
    best_weight = float("inf")
    best_path = []
    api.debug(coins_to_search)
    exhaustive(coins_to_search, player_location, [], 0, dist_matrix)
    meta_route = [player_location] + best_path
    api.debug(meta_route)
    route = u.location_list_to_route(meta_route, route_matrix)
          
    return coins_to_search, meta_route, route, dist_matrix[player_location][meta_route[1]]
 
               
dists_matrix, routes_matrix = u.dists_from_each(coins + [playerLocation], mazeMap)
old_dists = dists_matrix
initialisationTurn(mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins)

api.startGameMainLoop(determineNextMove)
