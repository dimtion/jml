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

#commerce
import time
import heapq
#fincommerce

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
X='X'

####################################################################################################################################################################################################################################

# Name of your team
# It will be displayed in the maze
# You have to edit this code

TEAM_NAME = 'team OTop'

####################################################################################################################################################################################################################################
########################################################################################################## YOUR CONSTANTS ##########################################################################################################
####################################################################################################################################################################################################################################

# [YOUR CODE HERE]

####################################################################################################################################################################################################################################
########################################################################################################## YOUR VARIABLES ##########################################################################################################
####################################################################################################################################################################################################################################

liste_move_op=[]
voisins=[]
#commerce
coins=[]
largeurLabyrinthe =0
directionList = []
visitedCoins = []

class R_barre:
    def __init__(self,num):
        self.num = num
    
    def __add__(self,valueToAdd):
        if self.num == -1 or valueToAdd.num==-1:
            return R_barre(-1)
        else :
            return R_barre(self.num + valueToAdd.num)
    
    def lowerThan(self,valueToCompare):
        if self.num == -1 and valueToCompare.num == -1:
            return False
        elif self.num == -1:
            return False
        elif valueToCompare.num == -1:
            return True
        else:
            a = self.num
            b =valueToCompare.num
            if a < b:
                return True
            else:
                return False
#fin commerce

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

#commerce
def pos_to_int(position):
    global largeurLabyrinthe
    mazeWidth = largeurLabyrinthe
    return position[0] + mazeWidth * position[1]

def int_to_pos(integer):
    global largeurLabyrinthe
    mazeWidth = largeurLabyrinthe
    return (integer%mazeWidth,integer//mazeWidth)


#Parcours d'un graphe en largeur, en profondeur, profondeur limitée

def adjacentWay(previousLocation,nextLocation):
    #risque echange verti et hori
    vertical = nextLocation[0] - previousLocation[0]
    horizontal = nextLocation[1] - previousLocation[1]
    
    if vertical == 1:
        return DOWN
    elif vertical == -1:
        return UP
    elif horizontal== 1:
        return RIGHT
    else :
        return LEFT
    

# Dijkstra prend en entrée un nœud initial et un graphe
# Sa sortie est l'ensemble des longueurs des chemins les plus courts
# depuis le nœud initial à tous les autres nœuds atteignables dans le graphe
def dijkstra(noeud_initial, graphe):
    
    routage = [0]*len(graphe)

    # On défini d'abord les structures de données utiles
    # distances est le tableau rendu en fin d'algorithme qui contient toutes 
    # les longueurs des chemins minimaux depuis le noeud initial
    infini = R_barre(-1)
    distances = [infini] * len(graphe)
    indice_noeud_initial = pos_to_int(noeud_initial)
    distances[indice_noeud_initial] = R_barre(0)
    
    # L'algorithme de Dijkstra utilise une file de priorité, elle contient
    # initialement le nœud initial avec sa distance au nœud initial : 0
    filePriorite = []
    heapq.heappush(filePriorite, (0,noeud_initial) )

    # Corps de l'algorithme :
    while not filePriorite == [] :
        (distance , noeud_courant) = heapq.heappop(filePriorite)
        #debug(str(distance) + "," + str(noeud_courant))
        #pour tout noeud i voisin de noeud_courant:
        #debug(graphe[noeud_courant])
        for voisin in graphe[noeud_courant]:
            dist_par_courant = R_barre(distance + voisin[1])
            #i est le numero correspondant aux coordonnées du voisin 
            i = pos_to_int(voisin[0])
            #debug(str(voisin[0]) +" et "+ str(noeud_courant))
            #debug(str(voisin)+" avec "+str(dist_par_courant.num)+" et "+str(distances[i].num))
            #debug(str(voisin)+" avec "+str(pos_to_int(voisin[0])))
            #debug(str(noeud_courant)+" avec "+str(pos_to_int(noeud_courant)))
            #debug(largeurLabyrinthe)
            if dist_par_courant.lowerThan(distances[i]):
                #debug(str(voisin))
                distances[i] = dist_par_courant
                routage[i] = noeud_courant
                #remplacer(file_priorité, i, dist_par_courant)
                heapq.heappush(filePriorite, (dist_par_courant.num,voisin[0]) )
        #debug(str(filePriorite))
                

    # Il nous reste à rendre le résultat 
    return distances,routage,noeud_initial
    
def chooseNearestCoin(matrDist):

    liste = []
    nearcoin=coins[0]
    for coordCoin in coins: #on récup la distances des pièces
        i = pos_to_int(coordCoin)
        liste.append(matrDist[i].num)

    for j in range(len(liste)):#on cherche le plus proche
        distancemini= matrDist[pos_to_int(nearcoin)].num
        if liste[j] < distancemini:
            nearcoin=coins[j]
    return nearcoin

#à partir d'un routage, du noeud d'arrivé visé, donne toutes les cases rencontrées en chemin
def pathTracer(finishingNode,startingNode, routage):
    path = []
    path.append(finishingNode)
    #debug(str(coins[0]))
    while not path[-1] == startingNode:
        indice_currentNode = pos_to_int(path[-1])
        parent = routage[indice_currentNode]
        path.append(parent)
    #debug("3\n\n" + str(path)+"\n\n")
    return path
  

def directionMaker(pathList):
    directions = []
    while not len(pathList) == 1:
        actualLocation = pathList.pop()
        nextLocation = pathList[-1]
        nextdirection = adjacentWay(actualLocation, nextLocation)
        directions.append(nextdirection)
    #debug(str(directions))
    return directions


def choixvoyageur(choix,dist_totale,nombrePieceAPrendre, distcoin, longueurmini, meilleurchemin):

	if len(choix) >= nombrePieceAPrendre:
#        global longueurmini
		if dist_totale < longueurmini:
			longueurmini = dist_totale
#			global meilleurchemin
			meilleurchemin = choix

	else:
		for j in range(len(coins)):
			if j not in choix:
				choixvoyageur(choix + [j],dist_totale + distcoin[choix[-1]][j], nombrePieceAPrendre, distcoin, longueurmini, meilleurchemin)

	return longueurmini, meilleurchemin #renvoie le dernier chemin


def voyageurcommerce(nombrePlacesAVisiter = len(coins)+1 ):
    distcoin = []
    longueurmini = float('inf')
    meilleurchemin = []    
    directionList = []

    #initialisation distcoin
    distcoin = []
    for j in range(len(coins)+1):
        distcoin.append([])
        for i in range(len(coins)+1):
            distcoin[j].append(float("inf"))
    
    #calcul des valeurs de distcoin
    for j in range(len(coins)):
        (matriceDistances, matriceRoutage, noeudDepart) = dijkstra(coins[j],mazeMap)
        for i in range(j,len(coins)):
            dist = matriceDistances[pos_to_int(coins[i])].num
            distcoin[j][i] = dist
            distcoin[i][j] = dist
        dist = matriceDistances[pos_to_int(playerLocation)].num
        distcoin[len(coins)][j] = dist
        distcoin[j][len(coins)] = dist
    debug("initialisation distcoin ok")

    #calcul du chemin optimal sur nombrePlacesAVisiter pièces à prendre
    choixvoyageur([len(coins)], 0, nombrePlacesAVisiter, distcoin, longueurmini, meilleurchemin) 
    (ordrevoyage,distancetotale)=(meilleurchemin, longueurmini)
    debug("miraculi")

    #récupération des coordonnées des pièces à récup
    listeCoordonnees = [0]*len(ordrevoyage)
    for j in range(len(ordrevoyage)):
        if ordrevoyage[j] == len(coins):
            listeCoordonnees[j] = playerLocation
        else:
            listeCoordonnees[j] = coins[ordrevoyage[j]]

    #récupération du chemin
    for j in range(len(ordrevoyage)-1):
        (matriceDistances, matriceRoutage, noeudDepart) = dijkstra(listeCoordonnees[j], mazeMap)
        pathSolution = pathTracer(listeCoordonnees[j+1],listeCoordonnees[j], matriceRoutage)
        directionList += directionMaker(pathSolution)

    return directionList

#fincommerce




####################################################################################################################################################################################################################################

# This is where you should write your code to do things during the initialization delay
# This function should not return anything, but should be used for a short preprocessing
# This function takes as parameters the dimensions and map of the maze, the time it is allowed for computing, the players locations in the maze and the remaining coins locations
# Make sure to have a safety margin for the time to include processing times (communication etc.)

def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
	liste_move_op.append(opponentLocation)
	
	#commerce	
	global largeurLabyrinthe
	largeurLabyrinthe=mazeWidth
	global directionList
	directionList = []
    
	
    #fincommerce



####################################################################################################################################################################################################################################

# This is where you should write your code to determine the next direction
# This function should return one of the directions defined in the CONSTANTS section
# This function takes as parameters the dimensions and map of the maze, the time it is allowed for computing, the players locations in the maze and the remaining coins locations
# Make sure to have a safety margin for the time to include processing times (communication etc.)


def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
	while len(coins)>20:
		a=0
		liste_move_op.append(opponentLocation)	
		if liste_move_op[0]!=liste_move_op[1]:
			if liste_move_op[0][0]<liste_move_op[1][0]:  
				a=liste_move_op.pop(0) 
				return UP
			elif liste_move_op[0][0]>liste_move_op[1][0]:
				a=liste_move_op.pop(0)
				return DOWN
			elif liste_move_op[0][1]>liste_move_op[1][1]:
				a=liste_move_op.pop(0)
				return RIGHT
			elif liste_move_op[0][1]<liste_move_op[1][1]:
				a=liste_move_op.pop(0)
				return LEFT
		else:
			voisins=mazeMap[playerLocation]
			for i in voisins:
				if i[1]==10:
					if i[0][0]>playerLocation[0]:
						a=liste_move_op.pop(0)   
						return DOWN
					elif i[0][0]<playerLocation[0]:
						a=liste_move_op.pop(0)
						return UP
					elif i[0][1]<playerLocation[1]:
						a=liste_move_op.pop(0)
						return LEFT
					elif i[0][1]>playerLocation[1]:
						a=liste_move_op.pop(0)
						return RIGHT
			a=liste_move_op.pop(-1)
			return 'X'

	global directionList        
	directionList = voyageurcommerce(nombrePlacesAVisiter = 4 )
	if directionList == []:
		initialTime = time.time()
		(matriceDistances, matriceRoutage, noeudDepart) = dijkstra(playerLocation,mazeMap)
		debug("time needed to calculate : " + str((time.time() - initialTime)*1000)+ "ms")
       			
		aim = chooseNearestCoin(matriceDistances)
		pathSolution = pathTracer(aim,playerLocation,matriceRoutage)
		directionList = directionMaker(pathSolution)
	return directionList.pop(0)


    
    


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
