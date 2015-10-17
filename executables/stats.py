#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# This statistics file is meant to try each of our program in a more realist way than
# the original one
#

import os
import time
import subprocess
import ast

#
# Editable configuration
# You are welcome to edit this configuration
#

PROGRAMS = ["ourIA/closest.py", "ourIA/improved_closest.py"]
TESTS_OUTPUT_DIRECTORY = "statistics"
NB_TESTS = 5
SINGLE_PLAYER = False
RANDOM_SEED = -1
SAVE_ARCHIVE = False  # Saves the games in case one wants to play them again

# Time configuration
# Warning: if you set this to true, the time could be false
TURN_TIME = "0.1"
PREPARATION_TIME = "3"
HIDE_MAZE_INTERFACE = "true"

################################################
# Static configuration
# Already filled with the competition configuration
################################################

# General configuration
SINGLE_COIN = "false"
WAIT_FOR_ALL_PLAYERS = "false"

# Intelligence configuration
MAZE_MAP_AVAILABLE = "true"
COINS_LOCATION_AVAILABLE = "true"
OPPONENT_LOCATION_AVAILABLE = "true"

# Maze configuration
MAZE_WIDTH = "25"
MAZE_HEIGHT = "25"
FENCE_PROBABILITY = "0.05"
COINS_DISTRIBUTION = "40"
NB_MOVES_TO_CROSS_FENCE = "10"
MAZE_DENSITY = "0.8"


# Other configuration
# PLAYER_2_FILE_NAME = "_"
MAZE_FILE_NAME = "_"
COINS_FILE_NAME = "_"
PLAYER_1_STARTING_LOCATION = "_"
TRACE_LENGTH = "0"

#
# Function utils
#


def createDirectory(directoryPath):
    """Creates a directory if it does not exist
       Used for archiving the games"""
    # We create the directory of not already done
    fullPath = os.path.dirname(directoryPath)
    try:
        os.stat(fullPath)
    except:
        os.mkdir(fullPath)


# def createArchiveStructure(output_directory):
#     # We create the base directories
#     statisticsDirectory = "." + os.path.sep + "outputFiles" + os.path.sep + output_directory + os.path.sep
#     createDirectory(statisticsDirectory)
#     archivesDirectory = statisticsDirectory + "archives" + os.path.sep
#     createDirectory(archivesDirectory)

#     # On the first level, we have the tested programs
#     # On the second level, we have the tested densities
#     # On the third level, we have the games
#     for i in range(len(PROGRAMS)):
#         programDirectory = archivesDirectory + str(PROGRAMS[i]) + os.path.sep
#         createDirectory(programDirectory)
#         for k in range(1, NB_TESTS + 1):
#             testDirectory = programDirectory + str(MAZE_DENSITIES[j]) + os.path.sep + str(k) + os.path.sep
#             createDirectory(testDirectory)

#     # We return the base directory
#     return statisticsDirectory

#####################################################################################

# Creates the file that will store the results


def createResultsFile(statisticsDirectory):

    # We create the file that will store the output results
    resultsFileName = statisticsDirectory + "results-" + str(time.time()) + ".csv"
    resultsFile = open(resultsFileName, "w")

    # We add the header
    resultsFile.write("Configuration; NB_TESTS; RANDOM_SEED; SINGLE_COIN; \n")
    resultsFile.write(str(time.time()) + "; " + str(NB_TESTS) + "; " + str(RANDOM_SEED) + "; " + SINGLE_COIN + "\n")

    # We return the file handle
    return resultsFile


def create_stats_matrix_header(result_file, result_type, opponents):
    result_file.write("\n\n; %s" % result_type)
    for opponent in opponents:
        result_file.write("; %s" % opponent)


def save_results_to_file(result_file, results, opponents):
    results_type = ['score', 'moves', 'missed', 'execution_time']

    for result_type in results_type:
        create_stats_matrix_header(result_file, opponents=opponents, result_type=result_type)
        for program in PROGRAMS:
            result_file.write("\n; %s" % program)
            for opponent in opponents:
                result_file.write("; %s" % results[(program, opponent)]['player1'][result_type])

#####################################################################################


def sum_dicts_values(dict1, dict2):
    """Sums the value between tow dictionnaries (with the same keys) and return the sum"""
    dict = {}
    for k in dict1.keys():
        try:
            dict[k] = int(dict1[k]) + int(dict2[k])
        except:
            dict[k] = int(dict1[k])
    return dict


def executePyRat(outputFilesDirectory, player1FileName, player2FileName="_", is_single_player="true", seed=-1):
    """ Executes PyRat with the given variable arguments
        Here, variable arguments are the player file, the density and the output directory
        This function also measures the time needed by the program to terminate
    """
    single_player = "true" if is_single_player else "false"
    # We prepare the command to execute
    command = ("./executables/pyrat" +
               " " + single_player +
               " " + PLAYER_1_STARTING_LOCATION +
               " " + player1FileName +
               " " + player2FileName +
               " " + str(seed) +
               " " + MAZE_FILE_NAME +
               " " + MAZE_WIDTH +
               " " + MAZE_HEIGHT +
               " " + MAZE_DENSITY +
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
    # print("[RUNNING] " + command)

    # We execute the program and measure its execution time
    t0 = time.time()
    pyRat = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    rawOutput = str(pyRat.stdout.readline())
    executionTime = time.time() - t0
    print(">>>TIME :" + str(executionTime))

    # We parse PyRat's output
    output = rawOutput[:]
    # print(output.strip())

    outputAsStructure = ast.literal_eval(output.strip())
    return outputAsStructure, executionTime

#
# Entry point
#

if __name__ == "__main__":

    # First we create the games archive and the results file
    # statisticsDirectory = createArchiveStructure()
    statisticsDirectory = "." + os.path.sep + "outputFiles" + os.path.sep + TESTS_OUTPUT_DIRECTORY + os.path.sep
    createDirectory(statisticsDirectory)
    resultsFile = createResultsFile(statisticsDirectory)

    all_results = {}
    # We iterate over the tested programs
    if SINGLE_PLAYER:
        OPPONENTS = ["_"]
    else:
        OPPONENTS = PROGRAMS
    for i, player1 in enumerate(PROGRAMS):
        for j, player2 in enumerate(OPPONENTS):
            sumsOfResultsP1 = {
                "moves": 0,
                "missed": 0,
                "execution_time": 0,
                "score": 0,
                "fences": 0
            }
            sumsOfResultsP2 = {
                "moves": 0,
                "missed": 0,
                "execution_time": 0,
                "score": 0,
                "fences": 0
            }

            # We make a given number of tests to have mean results
            for k in range(NB_TESTS):
                print("== STARTS : %s vs %s" % (player1, player2))
                # File names
                programFileName1 = "." + os.path.sep + "inputFiles" + os.path.sep + player1
                if player2 != "_":
                    programFileName2 = "." + os.path.sep + "inputFiles" + os.path.sep + player2
                else:
                    programFileName2 = player2
                # testDirectory = statisticsDirectory + "archives" + os.path.sep + PROGRAMS[j] + os.path.sep + str(MAZE_DENSITIES[i]) + os.path.sep + str(k) + os.path.sep

                # We execute PyRat and cumulate the results until the final mean
                # (nbMoves, nbMissed, executionTime) = executePyRat("./outputFiles/previousGame", programFileName, MAZE_DENSITIES[i])
                seed = RANDOM_SEED if RANDOM_SEED == -1 else RANDOM_SEED + k
                result, executionTime = executePyRat("./outputFiles/previousGame", programFileName1, programFileName2, is_single_player=SINGLE_PLAYER, seed=seed)
                # print("== ENDS : %s vs %s" % (player1, player2))
                result['player1']["execution_time"] = executionTime
                sumsOfResultsP1 = sum_dicts_values(sumsOfResultsP1,  result['player1'])
                if not SINGLE_PLAYER:
                    result['player2']["execution_time"] = executionTime
                    sumsOfResultsP2 = sum_dicts_values(sumsOfResultsP2, result['player2'])
                    print(">>>SCORES : P1  %s | P2 %s" % (result['player1']['score'], result['player2']['score']))
                else:
                    sumsOfResultsP2 = sum_dicts_values(sumsOfResultsP2, {})

            # We mean the result and export them
            meanResults1 = {x: sumsOfResultsP1[x] / NB_TESTS for x in sumsOfResultsP1}
            meanResults2 = {x: sumsOfResultsP2[x] / NB_TESTS for x in sumsOfResultsP2}
            all_results[(player1, player2)] = {'player1': meanResults1, 'player2': meanResults2}

    save_results_to_file(resultsFile, all_results, OPPONENTS)

    # We close the file
    resultsFile.close()
