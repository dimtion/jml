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

# Multithreading
# To be able to have the control window in a separate thread

import threading

####################################################################################################################################################################################################################################

# Graphics and key events
# For the window to give decisions

import tkinter
from tkinter import font

####################################################################################################################################################################################################################################

# Time management
# For the time to elapse before we take a decision

import time

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

TEAM_NAME = "Human player"

####################################################################################################################################################################################################################################
########################################################################################################## YOUR CONSTANTS ##########################################################################################################
####################################################################################################################################################################################################################################

# Set to true to repeat the last move until a new one is provided
# If false, a missed timing will cause the token to do nothing

REPEAT_LAST_MOVE = False;

####################################################################################################################################################################################################################################

# Ratio of the time allowed after which we must return a decision (used only in the mode in which we repeat the last move)
RATIO_OF_TIME_ALLOWED = 0.95;

####################################################################################################################################################################################################################################
########################################################################################################## YOUR VARIABLES ##########################################################################################################
####################################################################################################################################################################################################################################

# Global variable shared by the player thread and the interface thread to enable taking decisions
# A mutex is associated to the shared variable to ensure synchronization among threads

decision = 'X'
decisionMutex = threading.Lock()

####################################################################################################################################################################################################################################
####################################################################################################### PRE-DEFINED FUNCTIONS ######################################################################################################
####################################################################################################################################################################################################################################

# Writes a message to the shell
# Use for debugging your program
# Channels stdout and stdin are captured to enable communication with the maze
# Do not edit this code

def debug (text) :
    
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

def processInitialInformation () :
    
    # We read from the pipe
    data = readFromPipe()
    return (data['mazeWidth'], data['mazeHeight'], data['mazeMap'], data['preparationTime'], data['turnTime'], data['playerLocation'], data['opponentLocation'], data['coins'], data['gameIsOver'])

####################################################################################################################################################################################################################################

# Reads the information after each player moved
# The maze map and allowed times are no longer provided since they do not change
# Do not edit this code

def processNextInformation () :

    # We read from the pipe
    data = readFromPipe()
    return (data['playerLocation'], data['opponentLocation'], data['coins'], data['gameIsOver'])

####################################################################################################################################################################################################################################
########################################################################################################## YOUR FUNCTIONS ##########################################################################################################
####################################################################################################################################################################################################################################

# Callback for when the user takes a decision
# Unblocks the function that determines the next move to send the decision to the maze application

def callback (key) :
    
    # If we are in the mode in which we repeat the last move, we directly update the decision
    global decision
    global decisionMutex
    if REPEAT_LAST_MOVE :
        decisionMutex.acquire()
        decision = key
        decisionMutex.release()
        
    # Otherwise, we set the decision and allow the player to process the decision (the test avoids long key press)
    elif decisionMutex.locked() :
        decision = key
        decisionMutex.release()

####################################################################################################################################################################################################################################

# Thread in which the interface runs
# Starts the interface, binds the buttons to keys, and waits for events

def interfaceThread () :
    
    # Frame
    frame = tkinter.Tk()
    frame["bg"] = "black"
    frame.title(TEAM_NAME)

    # Buttons
    biggerFont = font.Font(size=30)
    topButton = tkinter.Button(frame, text="▲", height=1, width=2, font=biggerFont, command=(lambda : callback(UP)))
    topButton.grid(row=0, column=1)
    leftButton = tkinter.Button(frame, text="◀", height=1, width=2, font=biggerFont, command=(lambda : callback(LEFT)))
    leftButton.grid(row=1, column=0)
    bottomButton = tkinter.Button(frame, text="▼", height=1, width=2, font=biggerFont, command=(lambda : callback(DOWN)))
    bottomButton.grid(row=1, column=1)
    rightButton = tkinter.Button(frame, text="▶", height=1, width=2, font=biggerFont, command=(lambda : callback(RIGHT)))
    rightButton.grid(row=1, column=2)
    
    # Keys
    frame.bind("<Up>", lambda event : callback(UP))
    frame.bind("<Left>", lambda event : callback(LEFT))
    frame.bind("<Down>", lambda event : callback(DOWN))
    frame.bind("<Right>", lambda event : callback(RIGHT))
    
    # Go
    frame.mainloop()

####################################################################################################################################################################################################################################

# This is where you should write your code to do things during the initialization delay
# This function should not return anything, but should be used for a short preprocessing
# This function takes as parameters the dimensions and map of the maze, the time it is allowed for computing, the players locations in the maze and the remaining coins locations
# Make sure to have a safety margin for the time to include processing times (communication etc.)

def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    
    # We start the interface allowing the user to press keys
    thread = threading.Thread(target=interfaceThread)
    thread.start()
    
    # We start with the mutex already locked if not in the mode in which we repeat the last move
    global decisionMutex
    if not REPEAT_LAST_MOVE :
        decisionMutex.acquire()
    
####################################################################################################################################################################################################################################

# This is where you should write your code to determine the next direction
# This function should return one of the directions defined in the CONSTANTS section
# This function takes as parameters the dimensions and map of the maze, the time it is allowed for computing, the players locations in the maze and the remaining coins locations
# Make sure to have a safety margin for the time to include processing times (communication etc.)

def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    
    # If we are in the mode in which we repeat the last move, we wait until the very end to return the decision
    global decisionMutex
    if REPEAT_LAST_MOVE :
        time.sleep(RATIO_OF_TIME_ALLOWED * timeAllowed)
        decisionMutex.acquire()
        decisionToReturn = decision
        decisionMutex.release()
        return decisionToReturn
    
    # Otherwise, we return the decision when it is available
    else :
        decisionMutex.acquire()
        return decision

####################################################################################################################################################################################################################################
############################################################################################################# MAIN LOOP ############################################################################################################
####################################################################################################################################################################################################################################

# This is the entry point when executing this file
# We first send the name of the team to the maze
# The first message we receive from the maze includes its dimensions and map, the times allowed to the various steps, and the players and coins locations
# Then, at every loop iteration, we get the maze status and determine a move
# Do not edit this code

if __name__ == "__main__" :
    
    # We send the team name
    writeToPipe(TEAM_NAME + "\n")
    
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

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################