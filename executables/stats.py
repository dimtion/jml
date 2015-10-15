# -*- coding: utf-8 -*-
#####################################################################################
###################################### IMPORTS ######################################
#####################################################################################
 
import os
import time
import subprocess
import ast
 
#####################################################################################
##################################### CONSTANTS #####################################
#####################################################################################
 
# Constants about the programs to test
# Here, we study the execution time and number of moves as a function of the graph walls density
# The mean results are given for 10 graphs
# The result games will be exported in the output directory to be watchable
 
PROGRAMS = ["ourIA/closest.py", "ourIA/improved_closest.py","ourIA/improved_closest_v2.py"]
TESTS_OUTPUT_DIRECTORY = "statistics"
MAZE_DENSITIES = [0.6, 0.7, 0.8, 0.9, 1.0]
NB_TESTS = 10
 
#####################################################################################
 
# Constants defining the maze structure and game mode
# Here, we study mazes of 9x9 cells
# No fences here, and only one coin
 
SINGLE_PLAYER = "true"
SINGLE_COIN = "true"
MAZE_MAP_AVAILABLE = "true"
COINS_LOCATION_AVAILABLE = "true"
MAZE_WIDTH = "9"
MAZE_HEIGHT = "9"
FENCE_PROBABILITY = "0"
 
#####################################################################################
 
# Since we want to measure the time taken by the algorithm, we do not fixed a minimum turn time
# This enables to go as fast as possible
# Also, we do not display the interface to automatize the tests
 
TURN_TIME = "0.0"
PREPARATION_TIME = "0.0"
HIDE_MAZE_INTERFACE = "true"
 
#####################################################################################
 
# Other arguments that are required by the commant line but not important here
 
WAIT_FOR_ALL_PLAYERS = "true"
PLAYER_2_FILE_NAME = "_"
MAZE_FILE_NAME = "_"
COINS_FILE_NAME = "_"
PLAYER_1_STARTING_LOCATION = "_"
OPPONENT_LOCATION_AVAILABLE = "true"
COINS_DISTRIBUTION = "_"
NB_MOVES_TO_CROSS_FENCE = "10"
RANDOM_SEED = "-1"
TRACE_LENGTH = "0"
 
#####################################################################################
##################################### FUNCTIONS #####################################
#####################################################################################
 
# Creates a directory if it does not exist
# Used for archiving the games
 
def createDirectory (directoryPath) :
    
    # We create the directory of not already done
    fullPath = os.path.dirname(directoryPath)
    try :
        os.stat(fullPath)
    except :
        os.mkdir(fullPath) 
 
#####################################################################################
 
# Creates the directories that will store the games
 
def createArchiveStructure () :
    
    # We create the base directories
    statisticsDirectory = "." + os.path.sep + "outputFiles" + os.path.sep + TESTS_OUTPUT_DIRECTORY + os.path.sep
    createDirectory(statisticsDirectory)
    archivesDirectory = statisticsDirectory + "archives" + os.path.sep
    createDirectory(archivesDirectory)
    
    # On the first level, we have the tested programs
    # On the second level, we have the tested densities
    # On the third level, we have the games
    for i in range(len(PROGRAMS)) :
        programDirectory = archivesDirectory + str(PROGRAMS[i]) + os.path.sep
        createDirectory(programDirectory)
        for j in range(len(MAZE_DENSITIES)) :
            densityDirectory = programDirectory + str(MAZE_DENSITIES[j]) + os.path.sep
            createDirectory(densityDirectory)
            for k in range(1, NB_TESTS + 1) :
                testDirectory = densityDirectory + str(k) + os.path.sep
                createDirectory(testDirectory)
    
    # We return the base directory
    return statisticsDirectory
 
#####################################################################################
 
# Creates the file that will store the results
 
def createResultsFile (statisticsDirectory) :
    
    # We create the file that will store the output results
    resultsFileName = statisticsDirectory + "results.csv"
    resultsFile = open(resultsFileName, "w")
    
    # We add the header
    resultsFile.write("Density")
    for testedFile in PROGRAMS :
        resultsFile.write(";" + testedFile + " (moves);" + testedFile + " (missed);" + testedFile + " (time)")
    
    # We return the file handle
    return resultsFile
 
#####################################################################################
 
# Executes PyRat with the given variable arguments
# Here, variable arguments are the player file, the density and the output directory
# This function also measures the time needed by the program to terminate
 
def executePyRat (player1FileName, mazeDensity, outputFilesDirectory) :
    
    # We prepare the command to execute
    command = ("./executables/pyrat" +
               " " + SINGLE_PLAYER +
               " " + PLAYER_1_STARTING_LOCATION +
               " " + player1FileName +
               " " + PLAYER_2_FILE_NAME +
               " " + RANDOM_SEED +
               " " + MAZE_FILE_NAME +
               " " + MAZE_WIDTH +
               " " + MAZE_HEIGHT +
               " " + str(mazeDensity) +
               " " + COINS_FILE_NAME +
               " " + SINGLE_COIN +
               " " + COINS_DISTRIBUTION +
               " " + FENCE_PROBABILITY +
               " " + NB_MOVES_TO_CROSS_FENCE +
               " " + WAIT_FOR_ALL_PLAYERS +
               " " + TURN_TIME +
               " " + PREPARATION_TIME +
               " " + TRACE_LENGTH +
               " " + MAZE_MAP_AVAILABLE +
               " " + OPPONENT_LOCATION_AVAILABLE +
               " " + COINS_LOCATION_AVAILABLE +
               " " + outputFilesDirectory +
               " " + HIDE_MAZE_INTERFACE)
    print("[RUNNING] " + command)
    
    # We execute the program and measure its execution time
    t0 = time.time()
    pyRat = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    rawOutput = str(pyRat.stdout.readline())
    executionTime = time.time() - t0
    print("    [TIME] " + str(executionTime))
    try:
      # We parse PyRat's output
      output = rawOutput[:]
      print(output.strip())
      outputAsStructure = ast.literal_eval(output.strip())
      nbMoves = outputAsStructure["player1"]["moves"]
      nbMissed = outputAsStructure["player1"]["missed"]
      print("    [MOVES] " + str(nbMoves))
      print("    [MISSED] " + str(nbMissed))
    except:
      nbMoves, nbMissed, executionTime = 0, 0, 0 
    # Done
    return (nbMoves, nbMissed, executionTime)
 
#####################################################################################
################################### MAIN FUNCTION ###################################
#####################################################################################
 
# Entry point of the program
# For every configuration to test, we generate a folder in the output directory
# Finally, a CSV file is generated with all the results
 
if __name__ == "__main__" :
    
    # First we create the games archive and the results file
    statisticsDirectory = createArchiveStructure()
    resultsFile = createResultsFile(statisticsDirectory)
    
    # We iterate over the possible densities
    for i in range(len(MAZE_DENSITIES)) :
        
        # We start writing the results file
        resultsFile.write("\n" + str(MAZE_DENSITIES[i]))
        
        # We iterate over the tested programs
        for j in range(len(PROGRAMS)) :
            
            # We make a given number of tests to have mean results
            sumsOfResults = [0, 0, 0]
            for k in range(1, NB_TESTS + 1) :
                
                # File names
                programFileName = "." + os.path.sep + "inputFiles" + os.path.sep + PROGRAMS[j]
                testDirectory = statisticsDirectory + "archives" + os.path.sep + PROGRAMS[j] + os.path.sep + str(MAZE_DENSITIES[i]) + os.path.sep + str(k) + os.path.sep
 
                # We execute PyRat and cumulate the results until the final mean
                (nbMoves, nbMissed, executionTime) = executePyRat(programFileName, MAZE_DENSITIES[i], testDirectory)
                sumsOfResults[0] += nbMoves
                sumsOfResults[1] += nbMissed
                sumsOfResults[2] += executionTime
        
            # We mean the result and export them
            meanResults = [x / NB_TESTS for x in sumsOfResults]
            for result in meanResults :
                resultsFile.write(";" + str(result))
    
    # We close the file
    resultsFile.close()
    
#####################################################################################