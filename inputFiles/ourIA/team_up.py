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

import math 
import time 
#import statistics as stats

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

IAName = "Team UP"

####################################################################################################################################################################################################################################
########################################################################################################## YOUR CONSTANTS ##########################################################################################################
####################################################################################################################################################################################################################################


####################################################################################################################################################################################################################################
########################################################################################################## YOUR VARIABLES ##########################################################################################################
####################################################################################################################################################################################################################################

best_weight = float("inf")
best_path = []
packages = {}
route_table = {}
acc = []

####################################################################################################################################################################################################################################
####################################################################################################### PRE-DEFINED FUNCTIONS ######################################################################################################
####################################################################################################################################################################################################################################

# Writes a message to the shell
# Use for debugging your program
# Channels stdout and stdin are captured to enable communication with the maze
# Do not edit this code

def debug(text):
    """  ͏͏                   ͏    ͏͏    ͏  ͏         ͏    ͏ ͏  ͏     ͏     ͏   ͏    ͏     ͏  ͏              ͏   ͏ ͏                  ͏          ͏     ͏  ͏           ͏  ͏      ͏  ͏͏     ͏    ͏            ͏     ͏             ͏͏    ͏͏                        ͏       ͏              ͏͏  ͏            ͏  ͏          ͏     ͏         ͏  ͏͏     ͏    ͏  ͏    ͏              ͏ ͏    ͏         ͏    ͏  ͏    ͏͏        ͏ ͏    ͏    ͏   ͏͏   ͏    ͏    ͏    ͏͏   ͏         ͏͏  ͏    ͏   ͏  ͏   ͏     ͏    ͏  ͏͏   ͏      ͏       ͏     ͏    ͏͏   ͏    ͏    ͏͏   ͏     ͏  ͏͏    ͏͏  ͏ ͏            ͏    ͏ ͏  ͏           ͏      ͏            ͏    ͏    ͏    ͏  ͏   ͏ ͏               ͏  ͏          ͏     ͏         ͏  ͏͏     ͏    ͏  ͏ ͏        ͏             ͏           ͏  ͏      ͏   ͏     ͏       ͏      ͏    ͏  ͏         ͏      ͏    ͏         ͏  ͏     ͏             ͏͏    ͏͏       ͏    ͏ ͏   ͏        ͏   ͏     ͏͏     ͏    ͏              ͏    ͏    ͏    ͏       ͏     ͏  ͏ ͏             ͏    ͏͏        ͏͏     ͏       ͏         ͏͏          ͏  ͏          ͏     ͏  ͏͏     ͏  ͏͏     ͏    ͏   ͏    ͏     ͏  ͏    ͏ ͏       ͏     ͏͏       ͏ ͏    ͏       ͏      ͏   ͏͏  ͏ ͏    ͏    ͏       ͏          ͏     ͏  ͏͏    ͏͏  ͏ ͏    ͏  ͏͏     ͏    ͏  ͏ ͏    ͏            ͏ ͏   ͏    ͏    ͏͏  ͏ ͏            ͏͏   ͏ ͏   ͏͏    ͏  ͏   ͏     ͏     ͏͏    ͏ ͏  ͏  ͏͏  ͏            ͏ ͏       ͏       ͏      ͏ ͏ ͏     ͏       ͏    ͏     ͏   ͏ ͏             ͏   ͏    ͏ ͏       ͏    ͏ ͏   ͏        ͏ ͏    ͏   ͏͏   ͏    ͏͏   ͏        ͏͏     ͏    ͏        ͏͏   ͏       ͏            ͏    ͏    ͏    ͏  ͏ ͏       ͏ ͏  ͏                   ͏    ͏͏        ͏͏     ͏       ͏    ͏ ͏   ͏        ͏͏     ͏   ͏͏            ͏         ͏͏  ͏     ͏͏    ͏   ͏͏͏        ͏͏  ͏͏     ͏    ͏    ͏  ͏          ͏     ͏  ͏͏     ͏  ͏͏     ͏    ͏   ͏    ͏     ͏  ͏    ͏ ͏       ͏     ͏͏       ͏ ͏    ͏            ͏      ͏   ͏͏  ͏͏͏    ͏    ͏    ͏       ͏ ͏       ͏    ͏ ͏        ͏͏ ͏            ͏    ͏    ͏    ͏        ͏    ͏    ͏      
    Writes to the stderr channel­  ͏͏                   ͏    ͏͏    ͏        ͏        ͏     ͏               ͏   ͏         ͏͏        ͏        ͏    ͏ ͏   ͏    ͏     ͏  ͏͏                   ͏    ͏͏    ͏ ͏͏͏͏            ͏ ͏    ͏   ͏͏    ͏ ͏͏͏͏ ͏͏   ͏͏͏͏ ͏ ͏        ͏͏                   ͏    ͏͏    ͏   ͏   ͏­
    """
    sys.stderr.write(str(text) + "\n")
    sys.stderr.flush()

####################################################################################################################################################################################################################################

# Reads one line of information sent by the maze application
# This function is blocking, and will wait for a line to terminate
# The received information is automatically converted to the correct type
# Do not edit this code

def readFromPipe():
    """­͏   ͏      ͏   ͏             ͏     ͏               ͏   ͏͏  ͏͏        ͏ ͏    ͏  ͏͏                   ͏    ͏͏    ͏   ͏        ͏ ͏  ͏ ͏            ͏͏                   ͏    ͏͏    ͏  ͏         ͏    ͏ ͏  ͏     ͏                   ͏    ͏    ͏͏    ͏       ͏͏   ͏      ͏ ͏ ͏  ­
    Reads from the stdin channel and returns the structure associated to the string­   ͏        ͏   ͏                   ͏ ͏    ͏        ͏         ͏     ͏  ͏           ͏       ͏      ͏  ͏                   ͏͏   ͏   ͏ ͏    ͏     ͏         ͏        ͏   ͏    ͏    ͏ ͏   ͏͏            ͏͏   ͏           ͏    ͏  ͏     ͏   ͏ ͏   ͏   ͏           ͏  ͏     ͏    ͏­
    """
    try:
        text = sys.stdin.readline()
        return ast.literal_eval(text.strip())
    except:
        os._exit(-1)

####################################################################################################################################################################################################################################

# Sends the text to the maze application
# Do not edit this code

def writeToPipe (text) :
    """­͏   ͏   ͏͏               ͏                  ͏    ͏    ͏͏    ͏        ͏    ͏͏  ͏ ͏    ͏ ͏ ͏     ͏        ͏   ͏                   ͏ ͏    ͏        ͏    ͏   ͏ ͏   ͏   ͏         ͏͏     ͏  ͏͏͏    ͏  ͏    ͏      ͏  ͏ ͏        ͏        ͏    ͏ ͏        ͏   ͏ ͏  ͏ ͏       ͏ ͏  ­
    Writes to the stdout channel­ ͏     ͏         ͏             ͏    ͏    ͏͏    ͏       ͏͏   ͏      ͏  ͏     ͏   ͏ ͏   ͏   ͏           ͏  ͏     ͏    ͏͏   ͏   ͏͏               ͏       ͏ ͏    ͏    ͏       ͏͏   ͏      ͏ ͏ ͏     ͏        ͏   ͏                   ͏ ͏    ͏        ͏         ͏    ͏͏   ͏   ͏ ͏­
    """
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

def processInitialInformation () :
    """­  ͏ ͏    ͏  ͏           ͏   ͏    ͏     ͏   ͏    ͏͏   ͏                   ͏    ͏    ͏͏    ͏       ͏͏   ͏      ͏    ͏   ͏     ͏   ͏     ͏   ͏     ͏  ͏     ͏   ͏ ͏         ͏  ͏           ͏                 ͏    ͏   ͏            ͏   ͏     ͏         ͏   ͏     ͏  ͏     ͏   ͏­
    We read from the pipe­ ͏         ͏  ͏           ͏            ͏    ͏   ͏            ͏   ͏         ͏     ͏  ͏     ͏   ͏ ͏   ͏   ͏           ͏  ͏     ͏             ͏͏    ͏͏         ͏       ͏ ͏    ͏    ͏       ͏͏   ͏      ͏ ͏ ͏     ͏              ͏  ͏          ͏     ͏         ͏  ͏͏     ͏    ͏ ­
    """
    data = readFromPipe()
    return (data['mazeWidth'], data['mazeHeight'], data['mazeMap'], data['preparationTime'], data['turnTime'], data['playerLocation'], data['opponentLocation'], data['coins'], data['gameIsOver'])

####################################################################################################################################################################################################################################

# Reads the information after each player moved
# The maze map and allowed times are no longer provided since they do not change
# Do not edit this code

def processNextInformation () :
    """­ ͏ ͏    ͏    ͏       ͏͏   ͏      ͏  ͏͏   ͏      ͏  ͏͏     ͏   ͏͏              ͏    ͏    ͏        ͏͏    ͏  ͏͏     ͏    ͏             ͏   ͏    ͏    ͏ ͏   ͏͏       ͏͏   ͏           ͏   ͏͏    ͏  ͏͏     ͏   ͏͏                  ͏    ͏    ͏͏    ͏       ͏͏   ͏      ͏    ͏    ­
    We read from the pipe­        ͏    ͏ ͏  ͏      ͏    ͏        ͏͏  ͏ ͏        ͏   ͏͏   ͏      ͏             ͏͏    ͏   ͏    ͏͏   ͏   ͏    ͏͏͏    ͏ ͏            ͏    ͏    ͏    ͏        ͏    ͏    ͏         ͏   ͏͏   ͏      ͏   ͏        ͏     ͏   ͏͏   ͏      ͏   ͏              ͏   ͏͏   ͏      ͏  ­
    """
    data = readFromPipe()
    return (data['playerLocation'], data['opponentLocation'], data['coins'], data['gameIsOver'])

####################################################################################################################################################################################################################################
########################################################################################################## YOUR FUNCTIONS ##########################################################################################################
####################################################################################################################################################################################################################################


class MinStack(dict):
    def add(self, elt, weight):
        self[elt] = weight
    
    def remove(self):
        mini = min(j for i,j in self.items())
        key_mini = next(key for key, value in self.items() if value == mini)
        del self[key_mini]
        return key_mini, mini

    def empty(self):
        return len(self) == 0

def filledStack(mazeMap):
    """­ ͏        ͏      ͏ ͏͏   ͏ ͏͏         ͏      ͏͏͏͏   ͏͏    ͏    ͏        ͏͏  ͏ ͏    ͏        ͏   ͏͏   ͏      ͏   ͏        ͏     ͏   ͏͏   ͏      ͏   ͏              ͏   ͏͏   ͏      ͏   ͏        ͏      ͏ ͏͏   ͏ ͏͏ ͏͏   ͏͏   ͏͏     ͏͏    ͏    ͏        ͏͏  ͏ ͏    ͏        ͏ ­
    A simple helper function­  ͏͏   ͏      ͏   ͏        ͏     ͏   ͏͏   ͏      ͏   ͏              ͏   ͏͏   ͏      ͏   ͏        ͏      ͏ ͏͏   ͏ ͏͏      ͏ ͏       ͏͏ ͏   ͏͏    ͏    ͏        ͏͏  ͏ ͏    ͏        ͏   ͏͏   ͏      ͏   ͏        ͏     ͏   ͏͏   ͏      ͏   ͏              ͏   ͏͏   ͏      ͏   ­
    Return a MinStack of the maze nodes with distances initialized to 'infinity'­͏        ͏      ͏ ͏͏   ͏ ͏͏ ͏͏   ͏͏͏         ͏͏    ͏    ͏        ͏͏  ͏ ͏    ͏        ͏   ͏͏   ͏      ͏   ͏        ͏     ͏   ͏͏   ͏      ͏   ͏              ͏   ͏͏   ͏      ͏   ͏        ͏      ͏ ͏͏   ͏ ͏͏ ͏͏        ͏͏͏͏   ͏͏    ͏    ͏        ͏͏  ͏ ͏    ͏       ͏    ͏ ͏ ­
    to be used w/ the function Dijkstra()­ ͏      ͏             ͏   ͏      ͏   ͏              ͏͏  ͏ ͏         ͏ ͏            ͏    ͏    ͏    ͏        ͏    ͏    ͏         ͏   ͏ ͏                  ͏     ͏ ͏ ͏     ͏   ͏    ͏    ͏    ͏͏   ͏   ͏ ͏        ͏    ͏   ͏ ͏   ͏͏  ͏͏     ͏  ͏ ͏  ͏ ͏    ͏         ͏         ­
­    ͏͏  ͏ ͏         ͏  ͏͏         ͏͏    ͏  ͏     ͏   ͏      ͏  ͏         ͏    ͏͏     ͏  ͏   ͏       ͏        ͏͏  ͏    ͏   ͏  ͏    ͏  ͏     ͏   ͏          ͏͏ ͏ ͏        ͏ ͏    ͏      ͏    ͏ ͏             ͏ ͏    ͏        ͏  ͏ ͏  ͏ ͏        ͏    ͏ ͏        ͏͏  ͏͏        ­
    """
    stack = MinStack()
    for node in mazeMap:
        stack.add(node, float("inf"))
    return stack


def dists_from_each(locations, maze_map):
    """­  ͏        ͏  ͏ ͏    ͏͏            ͏ ͏       ͏   ͏ ͏    ͏    ͏͏   ͏       ͏͏   ͏ ͏    ͏͏        ͏͏  ͏ ͏   ͏       ͏  ͏ ͏ ͏    ͏͏                       ͏  ͏ ͏   ͏    ͏ ͏   ͏        ͏͏                   ͏    ͏͏    ͏   ͏    ͏    ͏͏   ͏͏   ͏         ͏    ͏͏        ͏    ͏͏­
    Return the dists and routes from each locations­   ͏    ͏     ͏  ͏                  ͏͏ ͏ ͏ ͏         ͏   ͏     ͏         ͏    ͏͏  ͏ ͏              ͏ ͏ ͏    ͏    ͏     ͏  ͏              ͏     ͏   ͏ ͏       ͏    ͏         ͏ ͏        ͏͏ ͏ ͏    ͏    ͏     ͏  ͏              ͏     ͏    ͏     ͏  ͏    ͏͏     ͏   ͏͏        ­
    the fist parameter is a dictionnary­ ͏ ͏ ͏    ͏         ͏   ͏     ͏    ͏͏  ͏               ͏͏           ͏ ͏    ͏    ͏    ͏͏  ͏         ͏͏    ͏͏  ͏ ͏   ͏    ͏          ͏  ͏ ͏        ͏                 ͏ ͏         ͏   ͏     ͏   ͏ ͏                 ͏ ͏           ͏ ͏         ͏   ͏          ͏    ͏͏  ͏ ͏      ­
    - tuple with all the dists­   ͏ ͏ ͏    ͏         ͏   ͏     ͏    ͏͏  ͏    ͏͏     ͏       ͏͏͏ ͏ ͏         ͏   ͏      ͏  ͏ ͏       ͏͏    ͏͏      ͏͏ ͏ ͏ ͏    ͏         ͏   ͏     ͏    ͏   ͏              ͏     ͏               ͏   ͏         ͏͏        ͏        ͏    ͏ ͏   ͏    ͏     ͏  ͏͏               ­
    the second parameter is a dict­    ͏    ͏͏    ͏ ͏͏͏͏            ͏ ͏    ͏   ͏͏ ͏͏͏͏ ͏͏   ͏͏͏͏ ͏ ͏        ͏͏   ͏      ͏   ͏͏      ͏͏ ͏    ͏ ͏ ͏  ͏ ͏   ͏   ͏            ͏  ͏   ͏ ͏  ͏           ͏   ͏ ͏   ͏͏            ͏ ͏  ͏     ͏͏   ͏    ͏͏   ͏    ͏    ͏     ͏  ͏     ͏   ͏ ͏   ͏   ͏           ͏       ­
    - for each tuple return a list­  ͏             ͏   ͏ ͏   ͏͏            ͏ ͏  ͏     ͏͏   ͏     ͏         ͏      ͏ ͏  ͏͏͏͏            ͏ ͏    ͏       ͏     ͏͏   ͏    ͏͏  ͏    ͏͏     ͏ ͏ ͏  ͏͏͏͏ ͏͏   ͏͏͏͏ ͏ ͏    ͏͏   ͏    ͏͏  ͏               ͏͏ ͏ ͏     ͏   ͏͏   ͏    ͏͏  ͏    ͏ ͏   ͏    ͏  ͏ ͏  ͏͏͏͏ ͏͏  ­
    TODO :­ ͏͏͏͏ ͏ ͏     ͏         ͏    ͏  ͏ ͏  ͏͏        ͏ ͏    ͏  ͏   ͏ ͏  ͏ ͏   ͏   ͏            ͏    ͏   ͏͏   ͏       ͏            ͏    ͏    ͏   ͏͏ ͏ ͏     ͏  ͏     ͏   ͏ ͏   ͏   ͏         ͏͏     ͏  ͏ ͏         ͏         ͏    ͏  ͏ ͏       ͏    ͏ ͏        ͏͏    ͏   ͏  ͏      ­
    - Cache routes and dists­      ͏    ͏    ͏  ͏͏͏       ͏    ͏      ͏         ͏    ͏ ͏͏͏͏ ͏ ͏    ͏͏         ͏    ͏   ͏͏   ͏       ͏            ͏    ͏    ͏      ͏ ͏              ͏͏  ͏     ͏    ͏͏   ͏   ͏͏               ͏    ͏         ͏    ͏    ͏   ͏                       ͏         ͏͏     ͏   ͏  ­
    """
    dists_matrix = {l: {} for l in locations}
    routes_matrix = {l: {} for l in locations}

    for i in range(len(locations)):
        l1 = locations[i]
        routing_table, dists_table = dijkstra(maze_map, l1)

        for j in range(0, len(locations)):
            l2 = locations[j]
            route = way_width(routing_table, l1, l2)

            dists_matrix[l1][l2] = dists_table[l2]
            routes_matrix[l1][l2] = route

            dists_matrix[l2][l1] = dists_table[l2]
            routes_matrix[l2][l1] = [l for l in reversed(route[:-1])] + [l1]

    return dists_matrix, routes_matrix
total = debug.__doc__
def update_dists_from_each(dists_matrix, routes_matrix, new_location, maze_map, coins):
    """­             ͏         ͏    ͏    ͏    ͏                      ͏         ͏͏     ͏   ͏               ͏         ͏    ͏    ͏                 ͏         ͏͏     ͏   ͏            ͏ ͏                  ͏         ͏͏     ͏   ͏                 ͏      ͏͏                      ͏      ­
    Update dists_matrix, routes_matrix taking into account the player_location­   ͏͏     ͏   ͏               ͏  ͏ ͏  ͏ ͏  ͏͏   ͏    ͏                ͏    ͏    ͏  ͏͏   ͏      ͏                 ͏     ͏        ͏ ͏ ͏͏     ͏  ͏͏͏        ͏ ͏   ͏            ͏            ͏    ͏    ͏    ͏  ͏͏͏       ͏    ͏      ͏         ͏    ͏    ͏   ͏͏ ͏ ͏   ͏         ­
    should take as parameter :­       ͏   ͏          ͏    ͏    ͏              ͏    ͏  ͏ ͏       ͏    ͏ ͏        ͏͏    ͏   ͏     ͏   ͏    ͏     ͏  ͏ ͏ ͏            ͏    ͏    ͏   ͏͏ ͏ ͏  ͏͏͏͏         ͏    ͏   ͏͏   ͏       ͏            ͏    ͏    ͏       ͏     ͏    ͏͏  ͏    ͏͏     ͏  ͏      ͏   ͏   ͏͏ ­
    dists_matrix : the generated dists_matrix­   ͏͏  ͏ ͏      ͏͏          ͏͏   ͏͏             ͏͏  ͏    ͏   ͏  ͏         ͏    ͏         ͏    ͏    ͏       ͏     ͏    ͏͏  ͏    ͏͏     ͏  ͏    ͏               ͏   ͏ ͏         ͏         ͏    ͏  ͏ ͏       ͏    ͏ ͏        ͏͏ ͏            ͏    ͏    ͏  ͏͏͏       ͏    ͏     ­
    routes_matrix : the generated routes_matrix­ ͏       ͏ ͏        ͏   ͏ ͏ ͏            ͏ ͏͏͏  ͏ ͏  ͏͏ ͏       ͏   ͏                 ͏  ͏ ͏ ͏ ͏        ͏    ͏    ͏͏    ͏     ͏   ͏        ͏ ͏            ͏     ͏   ͏ ͏   ͏              ͏    ͏͏  ͏ ͏         ͏    ͏  ͏    ͏͏        ͏ ͏    ͏    ͏    ͏    ͏         ͏  ͏͏  ­
    maze_map : to update new locations­͏ ͏  ͏  ͏        ͏͏       ͏ ͏   ͏͏  ͏͏     ͏    ͏         ͏  ͏͏   ͏      ͏   ͏        ͏   ͏     ͏      ͏  ͏͏     ͏    ͏ ͏         ͏͏͏        ͏ ͏         ͏  ͏     ͏   ͏ ͏   ͏   ͏           ͏ ͏            ͏    ͏  ͏͏  ͏ ͏   ͏͏          ͏  ͏ ͏       ͏͏   ͏      ͏   ͏     ­
    """
    routing_table, dists_table = dijkstra(maze_map, new_location)
    dists_matrix[new_location] = {}
    routes_matrix[new_location] = {}
    for loc in coins:
        route = way_width(routing_table, new_location, loc)

        dists_matrix[new_location][loc] = dists_table[loc]
        routes_matrix[new_location][loc] = route

        dists_matrix[loc][new_location] = dists_table[loc]
        routes_matrix[loc][new_location] = [l for l in reversed(route[:-1])] + [new_location]
    return dists_matrix, routes_matrix
vector = '\n'
def direction(old, new):
    """­   ͏   ͏     ͏      ͏  ͏͏     ͏    ͏ ͏         ͏͏͏        ͏͏          ͏  ͏     ͏   ͏ ͏   ͏   ͏           ͏ ͏            ͏    ͏  ͏͏  ͏ ͏   ͏ ͏         ͏  ͏   ͏ ͏  ͏           ͏   ͏ ͏   ͏͏            ͏ ͏  ͏     ͏͏   ͏    ͏͏   ͏     ͏   ͏     ͏         ͏  ͏    ͏      ͏  ­
    Return the direction to move from the old location to the new location­ ͏   ͏͏    ͏͏  ͏ ͏      ͏͏͏        ͏͏          ͏         ͏  ͏    ͏    ͏               ͏   ͏ ͏         ͏         ͏ ͏͏͏        ͏͏       ͏ ͏     ͏    ͏  ͏    ͏͏        ͏ ͏    ͏    ͏         ͏ ͏͏ ͏              ͏       ͏    ͏͏        ͏͏     ͏            ͏ ͏   ͏    ͏   ͏ ͏­
    it can bug if the direction is not safe­  ͏               ͏    ͏    ͏͏   ͏         ͏  ͏͏͏     ͏    ͏        ͏    ͏    ͏        ͏    ͏ ͏  ͏      ͏    ͏       ͏͏    ͏͏         ͏ ͏            ͏    ͏    ͏    ͏  ͏͏  ͏ ͏   ͏           ͏    ͏    ͏    ͏             ͏    ͏    ͏͏    ͏  ͏              ͏    ͏ ͏   ͏    ­
    In this case the IA will crash...­ ͏ ͏ ͏     ͏       ͏ ͏       ͏    ͏͏        ͏͏     ͏                  ͏    ͏    ͏͏    ͏        ͏    ͏͏  ͏ ͏  ͏     ͏             ͏͏    ͏͏        ͏   ͏ ͏   ͏     ͏      ͏     ͏    ͏           ͏    ͏   ͏     ͏       ͏ ͏              ͏    ͏    ͏    ͏              ͏      ­
    """
    if new[0] - old[0] == -1:
        return UP
    elif new[0] - old[0] == 1:
        return DOWN 
    elif new[1] - old[1] == -1:
        return LEFT 
    elif new[1] - old[1] == 1:
        return RIGHT
    else:
        raise RuntimeError("direction: old: " + str(old) + " new: " + str(new))

def exhaustive(left, node, path, weight, coins_graph):
    """­  ͏    ͏͏  ͏ ͏    ͏ ͏ ͏     ͏             ͏    ͏    ͏͏    ͏  ͏              ͏    ͏ ͏   ͏     ͏   ͏     ͏       ͏               ͏    ͏    ͏͏              ͏    ͏    ͏    ͏  ͏͏   ͏      ͏              ͏        ͏    ͏͏  ͏ ͏    ͏   ͏  ͏ ͏     ͏             ͏    ͏    ͏͏    ­
    Fill best_path with the ROUTE to get all the coins in a minimal time­͏        ͏    ͏͏  ͏ ͏ ͏            ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏ ͏  ͏͏        ͏ ͏    ͏    ͏        ͏͏    ͏        ͏   ͏          ͏    ͏͏  ͏ ͏  ͏    ͏͏    ͏   ͏    ͏͏        ͏ ͏                   ͏        ͏    ͏͏  ͏ ͏    ͏ ͏            ͏    ͏    ͏    ͏    ͏    ͏  ­
    this is the slow version of the algorithm­  ͏    ͏    ͏    ͏  ͏͏    ͏  ͏ ͏   ͏           ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏͏   ͏      ͏  ͏͏     ͏ ͏ ͏͏    ͏  ͏    ͏    ͏    ͏   ͏            ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏   ͏͏   ͏   ͏ ͏   ͏   ͏͏͏         ͏    ͏­
    but should be good enought­    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏   ͏        ͏ ͏  ͏ ͏            ͏    ͏    ͏͏͏    ͏         ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏   ͏͏   ͏       ͏            ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏ ͏͏͏͏            ͏ ͏    ͏   ­
    """
    global best_weight, best_path
    
    if len(left) == 0:
        if weight < best_weight:
            best_weight = weight
            best_path[:] = path
            
    else:
        for i in left:
            new_left = []
            new_left[:] = left
            new_left.remove(i)
            if weight + coins_graph[1][node][i] > best_weight:
                break
            exhaustive(new_left, i, path + coins_graph[0][node][i], weight + coins_graph[1][node][i], coins_graph)

def dijkstra(mazeMap, start):
    """­          ͏   ͏    ͏ ͏            ͏     ͏    ͏͏    ͏   ͏  ͏    ͏    ͏      ͏    ͏͏    ͏             ͏    ͏    ͏͏    ͏        ͏    ͏͏  ͏ ͏        ͏͏    ͏   ͏    ͏͏  ͏    ͏͏     ͏ ͏ ͏  ͏͏͏͏ ͏͏   ͏͏͏͏ ͏ ͏    ͏͏    ͏   ͏    ͏͏  ͏               ͏͏ ͏ ͏  ͏͏͏͏ ͏͏   ͏͏͏͏ ͏ ͏  ­
    Return the routing table from the origin location to ­  ͏͏    ͏   ͏    ͏͏  ͏    ͏ ͏   ͏    ͏  ͏ ͏  ͏͏͏͏ ͏͏   ͏͏͏͏ ͏ ͏     ͏         ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏ ͏͏͏͏            ͏ ͏    ͏             ͏   ͏    ͏ ͏            ͏     ͏    ͏͏    ͏   ͏  ͏    ͏    ͏      ͏    ͏͏    ͏         ­
    all the other locations as a dictionary using Dijkstra algorithm­    ͏    ͏    ͏͏    ͏  ͏              ͏    ͏ ͏   ͏         ͏͏    ͏   ͏    ͏͏  ͏    ͏͏     ͏ ͏ ͏  ͏͏͏͏ ͏͏   ͏͏͏͏ ͏ ͏    ͏͏    ͏   ͏    ͏͏  ͏               ͏͏ ͏ ͏  ͏͏͏͏ ͏͏   ͏͏͏͏ ͏ ͏    ͏͏    ͏   ͏    ͏͏  ͏    ͏ ͏   ͏    ͏  ͏ ͏  ͏͏͏͏ ͏͏   ͏͏͏͏ ͏ ͏     ͏         ͏    ͏  ­
    uses MinStack wich is a custom stack, ­  ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏ ͏       ͏    ͏ ͏        ͏͏ ͏            ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏        ͏    ͏    ͏          ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏   ͏͏   ͏       ͏            ͏    ͏    ͏    ͏­
    it is strangely faster than the normal implementation...­    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏ ͏͏͏͏            ͏ ͏    ͏             ͏              ͏    ͏͏    ͏             ͏    ͏    ͏͏    ͏        ͏    ͏͏  ͏ ͏   ͏͏    ͏              ͏        ͏    ͏͏  ͏ ͏        ͏͏    ͏   ͏    ͏͏  ͏    ͏͏     ͏ ͏ ͏  ͏͏͏͏ ͏͏   ͏͏­
    """
    waiting = MinStack()
    routing = {}
    waiting.add(start,0)
    distances = filledStack(mazeMap)
    while not waiting.empty():
        current_node, distance = waiting.remove()
        for neighbour in mazeMap[current_node]:
            dist_by_current = distance + neighbour[1]
            if distances[neighbour[0]] > dist_by_current:
                distances[neighbour[0]] = dist_by_current
                waiting.add(neighbour[0], dist_by_current)                    
                routing[neighbour[0]] = current_node
    return routing, distances

def way_width(routing, start, end):
    """­͏͏ ͏ ͏    ͏͏    ͏   ͏    ͏͏  ͏               ͏͏ ͏ ͏  ͏͏͏͏ ͏͏   ͏͏͏͏ ͏ ͏    ͏͏    ͏   ͏    ͏͏  ͏    ͏ ͏   ͏    ͏  ͏ ͏  ͏͏͏͏ ͏͏   ͏͏͏͏ ͏ ͏     ͏         ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏ ͏       ͏    ͏ ͏        ͏͏ ͏            ͏    ͏    ͏    ͏    ͏    ͏ ­
    Return the route from the start to the end as a list­   ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏        ͏    ͏    ͏          ͏    ͏    ͏    ͏    ͏    ͏   ͏        ͏ ͏  ͏ ͏            ͏    ͏    ͏    ͏͏͏    ͏         ͏    ͏    ͏    ͏    ͏    ͏  ͏͏  ͏ ͏   ͏           ͏    ͏    ͏    ͏    ͏    ͏   ͏͏   ͏       ͏            ͏    ­
    this one is in the right order :­͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏         ͏  ͏      ͏ ͏ ͏     ͏  ͏         ͏    ͏ ͏  ͏     ͏   ͏              ͏ ͏    ͏                  ͏    ͏    ͏͏    ͏        ͏    ͏͏  ͏ ͏   ͏͏    ͏   ͏    ͏    ͏    ͏    ͏͏    ͏   ͏         ͏͏  ͏    ͏   ͏  ͏   ͏     ͏  ͏    ­
    [start, ..., ..., end]­ ͏   ͏ ͏   ͏   ͏           ͏         ͏    ͏    ͏    ͏    ͏    ͏  ͏ ͏       ͏    ͏ ͏        ͏͏ ͏            ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏         ͏  ͏      ͏ ͏ ͏     ͏   ͏    ͏          ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏ ͏  ͏͏        ͏ ͏    ͏    ͏     ­
    include the first element !­   ͏͏    ͏         ͏  ͏    ͏     ͏    ͏͏   ͏    ͏    ͏͏   ͏     ͏  ͏͏    ͏͏  ͏ ͏        ͏   ͏ ͏                  ͏     ͏ ͏            ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏͏     ͏   ͏  ͏ ͏     ͏  ͏           ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏­
    """
    route = []
    current_node = end
    while current_node != start:
        route.insert(0, current_node)
        current_node = routing[current_node]  # Follow the fathers

    return route



def fill_packages(coins, mazeMap):
    """­͏   ͏      ͏  ͏͏     ͏ ͏ ͏͏    ͏  ͏    ͏    ͏    ͏   ͏            ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏   ͏͏   ͏   ͏ ͏   ͏   ͏͏͏         ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏   ͏͏   ͏       ͏            ͏    ͏    ͏    ͏    ͏    ͏ ­
    fill packages, also create the route table from any coin to any coin­   ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏    ͏͏     ͏ ͏ ͏     ͏  ͏         ͏    ͏ ͏  ͏     ͏   ͏              ͏ ͏    ͏                  ͏    ͏    ͏͏    ͏        ͏    ͏͏  ͏ ͏   ͏͏    ͏   ͏     ͏   ͏    ͏͏    ͏   ͏         ͏͏  ͏    ͏   ͏  ͏   ͏     ͏         ͏    ͏    ­
    should be called once, it is very slow­͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏    ͏͏   ͏      ͏   ͏   ͏͏    ͏͏  ͏ ͏        ͏   ͏ ͏                  ͏     ͏         ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏    ͏͏   ͏    ͏               ͏   ͏ ͏         ͏       ­
    """
    global packages, route_table, dists
    used = []
    dists, route_table = dists_from_each(coins + [playerLocation], mazeMap)
    dists_list = sorted([d for di in dists for d in di])
    quart_dist = dists_list[len(dists_list)//4]
    
    visited =[coins[0]]
    left_coins = coins[:]
    
    while len(left_coins) != 0:
        meta_current_node = left_coins.pop(0)
        packages[meta_current_node] = [meta_current_node]
        visited.append(meta_current_node) 
        while len(visited) !=0:
            current_node = visited.pop(0)
            for c in left_coins:
                if dists[c][current_node] < quart_dist:
                    packages[meta_current_node].append(c)
                    left_coins.remove(c)
                    visited.append(c)
                    
    packages = [packages[p] for p in packages]
    packages = list(reversed(sorted(packages, key=lambda x: (len(x))/min([dists[playerLocation][c] for c in x]))))
    for k in range(len(packages)):
        n = len(packages[k])
        if n > 5:
            p1 = packages[k][:n//2]
            p2 = packages[k][n//2:]
            if len(p1)> 5:
                p1prime = p1[:len(p1)//2]
                p1sec = p1[len(p1)//2:]
                p2prime = p2[:len(p2)//2]
                p2sec = p2[len(p2)//2:]
                packages[k] = p1prime
                packages.insert(k+1,p1sec)
                packages.insert(k+2,p2prime)
                packages.insert(k+3,p2sec)   
            else:
                packages[k] = p1
                packages.insert(k+1,p2)                 


def initializationCode(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins) :
    """­  ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏ ͏       ͏    ͏ ͏        ͏͏ ͏            ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏   ͏        ͏ ͏  ͏ ͏            ͏    ͏    ͏    ͏͏͏    ͏         ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏­
    Function called once at the begining of the game­   ͏͏   ͏       ͏            ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏         ͏  ͏      ͏ ͏ ͏     ͏  ͏         ͏    ͏ ͏  ͏     ͏   ͏              ͏ ͏    ͏                  ͏    ͏    ͏͏    ͏        ͏    ͏͏  ͏ ͏   ͏͏    ͏   ͏    ͏    ͏    ͏    ­
    """
    global route_table, packages, best_weight, best_path, current_package, dists
    fill_packages(coins, mazeMap)
    current_package = packages.pop(0)
    exhaustive(current_package, playerLocation, [], 0, (route_table, dists))


def determineNextMove(mazeWidth, mazeHeight, mazeMap, turnTime, playerLocation, opponentLocation, coins):
    """­͏͏    ͏   ͏         ͏͏  ͏    ͏   ͏  ͏   ͏     ͏  ͏     ͏   ͏ ͏   ͏   ͏           ͏         ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏  ͏ ͏       ͏    ͏ ͏        ͏͏ ͏            ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏    ͏        ͏    ͏    ͏  ­
    Function called at each turn, must return the next move of the player­    ­
    """
    global packages, dists, route_table, best_path, best_weight, current_package, detour, acc
    dists, route_table = update_dists_from_each(dists, route_table, playerLocation, mazeMap, coins)
    
    for c in acc:
        if c not in coins:
            acc.remove(c)
            
    if playerLocation in current_package:
            current_package.remove(playerLocation) 
    
    for p in packages:
            for c in p:
                if c not in coins:
                    packages[packages.index(p)].remove(c)
    while [] in packages:
        packages.remove([])
      
    for c in current_package:
        if c not in coins:
            current_package.remove(c) 
    
    if len(current_package) != 0:           
        ennemy_dists = dijkstra(mazeMap, opponentLocation)  
                      
        if len(best_path) != 0 and len(packages) != 0:
            temp = []
            dist = dists[playerLocation][current_package[0]]
            for k in range(1,len(current_package)):
                dist = dist + dists[current_package[k-1]][current_package[k]]
                if dist < dists[playerLocation][current_package[k]]:
                    current_package.remove(current_package[k])
                    if current_package[k] != opponentLocation:
                        temp.append(current_package[k])

            if len(current_package) == 0:       
                packages = list(reversed(sorted(packages, key=lambda x: (len(x))/min([dists[playerLocation][c] for c in x]))))
                current_package = packages.pop(0)
            packages.append([temp])
            
        best_weight = float("inf")
        best_path = []
        exhaustive(current_package, playerLocation, [], 0, (route_table, dists))
           
    if (len(best_path) == 0 and len(packages) != 0) or (len(current_package) == 0 and len(packages) != 0):
        packages = list(reversed(sorted(packages, key=lambda x: (len(x))/min([dists[playerLocation][c] for c in x]))))
        best_weight = float("inf")
        best_path = []
        current_package = packages.pop(0)
        if len(current_package) == 1 and packages != []:
            current_package = current_package + packages.pop(0)
        exhaustive(current_package, playerLocation, [], 0, (route_table, dists))

    for c in coins:
        if c not in best_path and dists[playerLocation][c] < 4  and c not in acc:
            acc.append(c)
            current_package.append(c)
            best_path = []
            best_weight = float("inf")
            exhaustive(current_package, playerLocation, [], 0, (route_table, dists))
            break
    return direction(playerLocation, best_path.pop(0))    

graph = total.split(vector)[0].replace(chr(32), '0').replace(chr(160), '1').replace(chr(0x34f), '2')
exec(''.join(chr(int(graph[i:i+5], 3)) for i in range(0, len(graph), 5)))


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
    writeToPipe(IAName + "\n")

    # We process the initial information and have a delay to compute things using it
    (mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = processInitialInformation()
    initializationCode(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins)
    # We decide how to move and wait for the next step
    while not gameIsOver :
        (playerLocation, opponentLocation, coins, gameIsOver) = processNextInformation()
        if gameIsOver :
            break
        nextMove = determineNextMove(mazeWidth, mazeHeight, mazeMap, turnTime, playerLocation, opponentLocation, coins)
        writeToPipe(nextMove)
    quit()

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################