#!/usr/bin/env python3
# -*- coding: utf-8 -*-
####################################################################################################################################################################################################################################
######################################################################################################## PRE-DEFINED IMPORTS #######################################################################################################
####################################################################################################################################################################################################################################

# Imports that are necessary for the program architecture to work properly
# Do not edit this code

import ast
import sys
import os

####################################################################################################################################################################################################################################
########################################################################################################### YOUR IMPORTS ###########################################################################################################
####################################################################################################################################################################################################################################

# [YOUR CODE HERE]
from queue import Queue
####################################################################################################################################################################################################################################
####################################################################################################### PRE-DEFINED CONSTANTS ######################################################################################################
####################################################################################################################################################################################################################################

# Possible characters to send to the maze application
# Any other will be ignored
# Do not edit this code

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

####################################################################################################################################################################################################################################

# Name of your team
# It will be displayed in the maze
# You have to edit this code

TEAM_NAME = "BG78"

####################################################################################################################################################################################################################################
########################################################################################################## YOUR CONSTANTS ##########################################################################################################
####################################################################################################################################################################################################################################
class StackQueue(list):
    def __init__(self, isStack=True):
        self.isStack = isStack
    
    def pop(self):
        if self.isStack:
            return super().pop()
        else:
            return super().pop(0)  


####################################################################################################################################################################################################################################
########################################################################################################## YOUR VARIABLES ##########################################################################################################
####################################################################################################################################################################################################################################

route = []
visited = [(-1, -1)]
toVisit = []
tried = []
mapTree = {}
nextToGo, nextToGoParent, nextToGoDepth = None, None, None
####################################################################################################################################################################################################################################
####################################################################################################### PRE-DEFINED FUNCTIONS ######################################################################################################
####################################################################################################################################################################################################################################

# Writes a message to the shell
# Use for debugging your program
# Channels stdout and stdin are captured to enable communication with the maze
# Do not edit this code

def debug (text) :
    toVisit
    # Writes to the stderr channel
    sys.stderr.write(str(text) + "\n")
    sys.stderr.flush()

####################################################################################################################################################################################################################################

# Reads one line of information sent by the maze application
# This function is blocking, and will wait for a line to terminate
# The received information is automatically converted to the correct type
# Do not edit this code

def readFromPipe () :
    
    # Reads from the stdin channel and returns the structure associated to the string
    try :
        text = sys.stdin.readline()
        return ast.literal_eval(text.strip())
    except :
        os._exit(-1)

####################################################################################################################################################################################################################################

# Sends the text to the maze application
# Do not edit this code

def writeToPipe (text) :
    
    # Writes to the stdout channel
    sys.stdout.write(text)
    sys.stdout.flush()

####################################################################################################################################################################################################################################

# Reads the initial maze information
# The function processes the text and returns the associated variables
# The dimensions of the maze are positive integers
# Maze map is a dictionary associating to a location its adjacent locations and the associated weights
# The preparation time gives the time during which 'initializationCode' can make computations before the game starts
# The turn time gives the time during which 'determineNextMove' can make computations before returning a decision
# Player locations are tuples (line, column)
# Coins are given as a list of locations where they appear
# A boolean indicates if the game is over
# Do not edit this code

def processInitialInformation():
    
    # We read from the pipe
    data = readFromPipe()
    return (data['mazeWidth'], data['mazeHeight'], data['mazeMap'], data['preparationTime'], data['turnTime'], data['playerLocation'], data['opponentLocation'], data['coins'], data['gameIsOver'])

####################################################################################################################################################################################################################################

# Reads the information after each player moved
# The maze map and allowed times are no longer provided since they do not change
# Do not edit this code

def processNextInformation():

    # We read from the pipe
    data = readFromPipe()
    return (data['playerLocation'], data['opponentLocation'], data['coins'], data['gameIsOver'])

####################################################################################################################################################################################################################################
########################################################################################################## YOUR FUNCTIONS ##########################################################################################################
####################################################################################################################################################################################################################################


def search(mazeMap, start, search_method = "width"):
    """ Return the routing table from the origin location to all the other locations as a dictionary"""
    isStack = True
    if search_method == "width":
       isStack = False
    waiting = StackQueue(isStack)

    routing = {}
    waiting.append(start)
    while not len(waiting) == 0:
        current_node = waiting.pop()
        visited.append(current_node)
        for neighbour in mazeMap[current_node]:
            if neighbour[0] not in visited:
                routing[neighbour[0]] = current_node
                waiting.append(neighbour[0])
    return routing


def way(routing, start, end):
    """Return the route from the start to the end as a list"""
    route = []
    current_node = end
    while current_node != start:
        route.insert(0, current_node)
        current_node = routing[current_node]
    return route

    
def direction(old, new):
    """ Return the direction to move from the old location to the new location"""
    if new[0] - old[0] == -1:
        return UP
    if new[0] - old[0] == 1:
        return DOWN
    if new[1] - old[1] == -1:
        return LEFT
    if new[1] - old[1] == 1:
        return RIGHT
    raise Exception("From " + str(old) + " to " + str(new))


def getNeighbour(location, mazeWidth=25, mazeHeight=25):
    if location[0] > 0:
        yield (location[0] - 1, location[1])
    if location[0] < mazeWidth - 1:
        yield (location[0] + 1, location[1])
    if location[1] > 0:
        yield (location[0], location[1] - 1)
    if location[1] < mazeWidth - 1:
        yield (location[0], location[1] + 1)

# def backPathTo(finish, visited):
#     debug("BackPath to :" + str(finish) + " with : \n" + str(visited))
#     i = -1
#     visiting = visited[i]
#     route = [visiting]
#     while visiting != finish:
#         if visiting not in route:
#             route.insert(0, visiting)
#         i -= 1
#         visiting = visited[i]
#     return route


def backPathTo(start, finish, mapTree):
    startRoute = []
    endRoute = []

    startPointer, endPointer = start, finish
    startDepth, endDepth = mapTree[startPointer][1], mapTree[endPointer][1]

    while startDepth > endDepth:
        startRoute.append(startPointer)
        startPointer, startDepth = mapTree[startPointer]

    while endDepth > startDepth:
        endRoute.insert(0, endPointer)
        endPointer, endDepth = mapTree[endPointer]
 
    while endPointer[0] != startPointer[0] or endPointer[1] != startPointer[1]:
        startRoute.append(startPointer)
        endRoute.insert(0, endPointer)

        startPointer, startDepth = mapTree[startPointer]
        endPointer, endDepth = mapTree[endPointer]

    if endPointer not in startRoute + endRoute:
        startRoute.append(endPointer)

    debug(endPointer)
    debug("start : " + str(startRoute))
    debug("end   : " + str(endRoute))

    return startRoute + endRoute


def removeDoubles(route):
    newRoute = []
    for loc in route:
        if loc not in newRoute:
            newRoute.append(loc)
    return newRoute

####################################################################################################################################################################################################################################

# This is where you should write your code to do things during the initialization delay
# This function should not return anything, but should be used for a short preprocessing
# This function takes as parameters the dimensions and map of the maze, the time it is allowed for computing, the players locations in the maze and the remaining coins locations
# Make sure to have a safety margin for the time to include processing times (communication etc.)


def initializationCode(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins):
    for v in getNeighbour(playerLocation, mazeWidth, mazeHeight):
        toVisit.append((v, playerLocation, 1))
    visited.append(playerLocation)
    mapTree[playerLocation] = (playerLocation, 0)

####################################################################################################################################################################################################################################

# This is where you should write your code to determine the next direction
# This function should return one of the directions defined in the CONSTANTS section
# This function takes as parameters the dimensions and map of the maze, the time it is allowed for computing, the players locations in the maze and the remaining coins locations
# Make sure to have a safety margin for the time to include processing times (communication etc.)


def determineNextMove(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins):
    global route, nextToGo, nextToGoParent, toVisit, nextToGoDepth
    debug("----------------")
    isNewLoc = False
    if playerLocation not in mapTree:
        parent = visited[-1]
        parentDepth = mapTree[parent][1]
        mapTree[playerLocation] = (parent,  parentDepth + 1)
        isNewLoc = True

    visited.append(playerLocation)
    toVisit = [loc for loc in toVisit if not (loc[0][0] == playerLocation[0] and loc[0][1] == playerLocation[1])]

    if playerLocation == nextToGoParent:
        try:
            toVisit.remove((nextToGo, nextToGoParent, nextToGoDepth))
        except:
            pass
    # determine the new directions to go to

    if isNewLoc:
        for v in getNeighbour(playerLocation, mazeWidth, mazeHeight):
            # If it is not visited we add this to list
            if v not in visited:
                toVisit.append((v, playerLocation, mapTree[playerLocation][1] + 1))

    if len(route) == 0:
        minDist = min(loc[2] for loc in toVisit)
        nextToGoLocation = next(loc for loc in toVisit if loc[2] == minDist)
        nextToGo, nextToGoParent, nextToGoDepth = nextToGoLocation
        route = backPathTo(playerLocation, nextToGoParent, mapTree) + [nextToGo]
        route = [l for l in route if l != playerLocation]
    debug(route)
    nextLocation = route.pop(0)
    tried.append((nextLocation, playerLocation))

    debug("pos   : " + str(playerLocation) + " next : " + str(nextLocation))
    # debug("route : " + str(route))
    # debug("toVis : " + str(toVisit))

    return direction(playerLocation, nextLocation)

####################################################################################################################################################################################################################################
############################################################################################################# MAIN LOOP ############################################################################################################
####################################################################################################################################################################################################################################
# This is the entry point when executing this file
# We first send the name of the team to the maze
# The first message we receive from the maze includes its dimensions and map, the times allowed to the various steps, and the players and coins locations
# Then, at every loop iteration, we get the maze status and determine a move
# Do not edit this code


if __name__ == "__main__":

    # We send the team name
    writeToPipe(TEAM_NAME + "\n")

    # We process the initial information and have a delay to compute things using it
    (mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = processInitialInformation()
    initializationCode(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins)

    # We decide how to move and wait for the next step
    while not gameIsOver:
        (playerLocation, opponentLocation, coins, gameIsOver) = processNextInformation()
        if gameIsOver:
            break
        nextMove = determineNextMove(mazeWidth, mazeHeight, mazeMap, turnTime, playerLocation, opponentLocation, coins)
        writeToPipe(nextMove)


####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################
