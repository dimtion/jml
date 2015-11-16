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
import time
import heapq
import copy
import random

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

TEAM_NAME = "POKEPYRAT"

####################################################################################################################################################################################################################################
########################################################################################################## YOUR CONSTANTS ##########################################################################################################
####################################################################################################################################################################################################################################

#distance maxi entre deux pièces pour qu'elles forment un paquet.
OPTIDISTPAQUET = 2

#Constantes pour le voyageur de commerce :
#taille maxi du trajet prévu, en nombre de pièces
OPTIMINITCOINNUMBER = 5 # à l'initialisation
OPTIMTURNCOINNUMBER = 6 # pendant un tour de jeu.
#7 maxi pendant un tour, réduire si trop gros
#nombre de pièces mini pour réaliser un voyageur de commerce
VCPcoinMIN = 2
#portée de la recherche de la prochaine pièce dans le voyageur de commerce
OPTISEARCHCOIN = 8

#constantes pour le voyageur de commerce par paquets
#portée de la recherche du prochain paquet dans le voyageur de commerce par paquets
OPTISEARCHPAQUET = 7
#taille maxi du trajet prévu, en nombre de paquets
OPTICOMMERCEPAQUET = 4
#nombre de paquets mini pour réaliser un voyageur de commerce par paquets
MINNUMBEROFPAQUETSFORPAQUETSTRATEGY = 2
#nombre de pièces mini pour réaliser un voyageur de commerce par paquets
PAQcoinMIN = 8

#constantes pour le moyenneur (ZON)
ZONcoinMIN = 2

#constantes pour la stratégie fourmis
ANTcoinMIN = 2
ANTEVAP = 0.997
ANT_START_PHERO = 100000
ANT_POW_PATH = 1.5
ANT_POW_VISIBILITY = 3
ANT_POW_PUT_PHERO = 1.5

ANT_EFFICACITY = 5
ANT_MUTANT = 0.6

MIN_NUMBER_OF_TURNS_BETWEEN_TWO_CHANGES_OF_DECISIONS = 2

#constantes pour la stratégie glouton
GLUcoinMIN = 1

#constantes stratégie symétrique
#number of coins left when exit opponent side
COIN_MIN_OPPONENT_SIDE = 10
VICTORY_CONDITION = 20.5
SYMcoinMIN = 2

#strat monte carlo
 


###################choose the strategy !
TYPEOFSTRATEGY = 3 #3 = ant
init_function = []
nextmove_function = []
strat_function = []
strategy_vector = []
#init_function = [init_VCP, init_PAQ, init_ZON, init_ANT, init_GLU, init_SYM]

####################################################################################################################################################################################################################################
########################################################################################################## YOUR VARIABLES ##########################################################################################################
####################################################################################################################################################################################################################################

#variable globales

#est initialisée pendant initialization
largeurLabyrinthe =0 #largeur du labyrinthe, sert pour les fonctions pos_toint et int_to_pos

#graphe correspondant à MazeMap sans les impasses, qui sont inintéressantes
meta_graphe = {}

#graphe correspondat à mazeMap ne contenant que les pièces et les intersections.
#c'est à dire on a supprimé les impasses et raccourcis les couloirs
zone_graphe = {}#on réduit beaucoup le nombre de noeuds, c'est cool !

#variables retenant le résultats de dijkstra dans les points demandés.
#les clés sont des coordonnées de noeuds du graphe (meta ou zone) (la clé d'un dictionnaire et le genre d'indice que l'on met en entrée du dictionnaire
#les sorties sont deux variables : la matrice des distances et le routage à partir de la clé.
meta_distrout = {}
zone_distrout = {}

#dictionnaire donnant la distance entre deux pièces
#la clé est un tuple (coordD'unePièce, coordD'uneAutrePièce).
#exemple de clé (coin[0],coin[1]) ou ((0,1),(8,6)) ou [(0,1),(8,6)]
distcoin = {}

#Variables les plus importantes du programme !
#liste des pièces qui vont être mangées, dans l'ordre
aimedCoins = [] #aimedCoins[0] est la prochaine pièce à être mangée, aimedCoins[1] la seconde etc...
#liste des mouvements pour atteindre aimedCoins[0]
directionList = [] 
aimedPaquets = []

#Variables relatives aux paquets
#dictionnaire donnant la distance entre 2 paquets
#une clé est un tuple  avec le numero de deux paquets
#exemple de clé : (i,j) avec i <= j ou (4,9) etc...
#la sortie est une distance (un entier positif correspondant à un nombre de cases entre les deux paquets). Pour le calcul cf la fonciton correspondante
distpaquet = {}
#dictionnaire associant à un noeud son numero de paquet, ie le paquet dans lequel se trouve ce noeud.
#le numero de paquet varie entre -3 et N, N le nombre de paquets
#le numero de paquet -3 correspond à la position de l'adversaire (dans un futur proche ce sera les cases visitées par l'adversaire)
#le numero de paquet -2 correspond aux cases sans paquets
#le numero de paquet -1 correspond à la position du joueur
#à partir de 0 ce sont des paquets normaux.
appartenanceCoin = {}
#liste des paquets, et des pièces à l'intérieur
#paquets[j] est une liste de pièces. c'est la liste des pièces du paquet de pièces numero j.
paquets = []
#dictionnaire compiqué, je me souviens plus, cf init_territorypaquets
territorypaquets = {}

#à chaque tour ces 4 variables vont être mises à jours.
#Elles donnent la matrice des distances et le routage en partant de la position du joueur et de celle de l'adversaire. Ce sont des informations utiles à chaque tour, d'où l'utilisation de 4 variables globales pour.
playerMatriceDistances = []
playerMatriceRoutage = []
opponentMatriceDistances = []
opponentMatriceRoutage = []

pheromones = {}

ant_phero = []
ant_pheromones_ways = []
nbrEvap = 0
efficiencyMax = [0,[] ]
lastNumberOfAntsSent = float('inf')

previous_position = [[],[], 0]

classificationCoin = {}

resultsSinceBegining = [[0], [0], [0]]

score = [0,0]
previousCoins =[]

numberOfTurnSinceLastChangeOfDirection = 2

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

############################################################### sous-fonction

def trou(liste,index):
    """renvoie la liste d'entrée sans l'élément d'index 'index' ie on fait un trou dans la liste"""
    return liste[:index] + liste[index+1:]

#nonlinear weight function
def f(x, puissance = 2):
    """renvoie x à la fonction puissance, si puissance n'est pas précisé, on renvoie x**2"""
    return x**puissance
    
def indexOfMax(liste):
    maxi = liste[0]
    indexmaxi = 0
    for j in range(len(liste)):
        if liste[j] > maxi:
            indexmaxi = j
            maxi = liste[j]
    return indexmaxi

#apprendre à reconnaitre un glouton, un copieur, ie mémoriser les coups.
#piéger un copieur, à coté d'une barrière
#améliorer le choisisseur de dist mini avec un glouton adverse, ou un chemin direct, ou....
#mieux gérer la disparition des pièces : créer la variable d'interruption
#faire le branche and bound sur le voyageur de commerce
#implémenter les tas de fibonacci

#essayer un montecarlo ?

############################################################### heap

def heapAdd(liste, element, priority):
    if not len(liste) == 0:
        i = 0
        lenght = len(liste)
        elementPresentBefore = False
        while liste[i][0] < priority:
            if liste[i][1] == element:
                elementPresentBefore = True
                break
            i +=1
            if i == lenght:
                break
        j = i
        if not elementPresentBefore:
            if i == lenght:
                liste.append( (priority, element) )
            else:
                while i < lenght:
                    if liste[i][1] == element:
                        liste.pop(i)
                        break
                    i +=1
                liste = liste[:j]+[(priority, element)] + liste[j:]
    else :
        liste = [(priority, element)]
    return liste

def heapSuppr(liste):
    a = liste.pop(0)
    return a, liste



############################################################### gestion des données sur le graphe

#abandonnée
def update_constantes():
    #update opticoinnumber
    global OPTIMTURNCOINNUMBER
    nombrePlacesAVisiter = min(len(coins), OPTIMTURNCOINNUMBER)
    #si le nombre de pièce est compris entre 2 et 8
    if nombrePlacesAVisiter == len(coins) and len(coins) >= VCPcoinMIN and len(coins) <= PAQcoinMIN: # début de l'heuristique
        #alors on diminue la constante OPTIMTURNCOINNUMBER
        nombrePlacesAVisiter -= 1
    # ce qui signifie que on n'optimise jamais un voyageur de commerce pour atteindre la dernière pièce d'un labyrinthe
    #le but de cet diminution et d'éviter d'aller chercher une pièce complètement isolée  quand il en reste deux qui sont proche à l'autre bout du labyrinthe
    OPTIMTURNCOINNUMBER = nombrePlacesAVisiter


def deleteImpasse(graphe, node):
    """supprime node de graphe si c'est une impasse"""
    #et recommence récursivement  sur le voisin du noeud-impasse
    #Une impasse est un noeud qui n'a qu'un seul voisin et sur lequel il n'y a pas de pièce.
    #et aussi qui ne soit ni la position de départ du joueur, ni la position de départ de l'adversaire
    if (len(graphe[node]) == 1) and (node not in coins) and (not node == playerLocation) and (not node == opponentLocation):
        #on récupère l'adresse du voisin de l'impasse
        voisin = graphe[node][0][0]
        #debug("node = " + str(node) + "\nvoisin = " + str(voisin) + "\ngraphe[voisin] = " + str(graphe[voisin]) + "\n")
        
        #on supprime l'impasse parmis la liste des voisins de 'voisin'
        indexToPop = 0
        for j in range(len(graphe[voisin])):
            #debug(str(j) + " " + str(graphe[voisin][j]))
            candidatExpulsion = graphe[voisin][j]
            if candidatExpulsion[0] == node:
                indexToPop = j
        #debug("\nimpasse a suprr = " + str(node) + "\nvoisins de base = " + str(graphe[node]) + "\nvoisin = " + str(voisin) + "\n" +str(graphe[voisin]) + "\n" )
        graphe[voisin].pop(indexToPop)
        
        #on considère aussi maintenant que l'impasse n'a plus de voisins
        #le but sera de la supprimer
        graphe[node] = [] 
        #on relance récursivement cette fonction sur le voisin
        #cette fonction supprimera le voisin s'il devient une impasse après suppression de 'node'
        graphe = deleteImpasse(graphe,voisin) # #recursivité
    return graphe #on met à jour le graphe à la fin, et on le renvoit.

def supprCouloir(grapheAmodif, noeud):
    """renvoie le graphe sans le couloir dans lequel se trouvait noeud"""
    #un noeud-couloir est un noeud qui a seulement 2 voisins, qui ne contient pas de pièce.
    #et aussi qui ne soit ni la position de départ du joueur, ni la position de départ de l'adversaire
    #supprimer un couloir consiste en supprimer les noeuds-couloirs entre deux noeuds-intersection (strictement plus de 2 voisins). et de considérer dorénavant que les deux noeuds-intersection sont voisins, avec une distance entre les deux correspondant à la taille du couloir.
    #on supprime un couloir petit à petit, noeud par noeud.
    if (len(grapheAmodif[noeud]) == 2) and (noeud not in coins) and (not noeud == playerLocation) and (not noeud == opponentLocation):
        #on récup les coordonnées des deux voisins du noeud couloir considéré
        voisin1 = grapheAmodif[noeud][0][0]
        voisin2 = grapheAmodif[noeud][1][0]
        dist1 = grapheAmodif[noeud][0][1] #et les distances !
        dist2 = grapheAmodif[noeud][1][1]
        
        #supprime noeud du graphe
        for x in [voisin1,voisin2]: #on supprime le noeud-couloir des voisins de voisin1 et voisin2
            #debug("\nnoeud a suprr = " + str(noeud) + "\nvoisins de base = " + str(grapheAmodif[noeud]) + "\nvoisin = " + str(x) + "\n" +str(grapheAmodif[x]) + "\n" )
            for j in range(len(grapheAmodif[x])): #pour supprimer le noeud, il faut parcourir la liste des voisins de x,
                voisindevoisin = grapheAmodif[x][j]
                if voisindevoisin[0] == noeud:
                    indiceApop = j
            grapheAmodif[x].pop(indiceApop) #puis le supprimer après la boucle, quand on a trouvé son indice
        grapheAmodif[noeud] = [] #ce noeud n'a plus de voisins !
        
        #on réajoute les distances
        grapheAmodif[voisin1].append( (voisin2, dist1 + dist2) )
        grapheAmodif[voisin2].append( (voisin1, dist1 + dist2) )
        #on reteste si voisin1 et 2 ne sont pas des couloirs aussi
        grapheAmodif = supprCouloir(grapheAmodif, voisin1)
        grapheAmodif = supprCouloir(grapheAmodif, voisin2)
    return grapheAmodif


def shortenMap(graphe):
    """renvoie le graphe sans impasses"""
    shortened_graphe = copy.deepcopy(graphe) #on réalise une copie du graphe pour la modifier
    for node in graphe: #on parcour tous les noeuds du graphe
        #on enlève les impasses
        shortened_graphe = deleteImpasse(shortened_graphe,node)
        #si le noeud n'a pas de voisins, on le supprime
        if shortened_graphe[node] == []:
            del shortened_graphe[node]
    #debug("mazeMap shortened of " + str(len(mazeMap)-len(shortened_graphe)) + "nodes")
    return shortened_graphe

def init_graphe_zone(actual_graphe):
    """renvoie le graphe d'entrée sans impasses ni couloirs"""
    new_graphe = copy.deepcopy(actual_graphe) #on copie le graphe (à la bien !)
    
    #debug("copie réussie : " + str(new_graphe == actual_graphe) )
    #on le modifie
    for node in new_graphe:
        if len(new_graphe[node]) == 2:
            new_graphe = supprCouloir(new_graphe, node)
    #on supprime les noeuds qui ne sont plus nécessaires
    for node in actual_graphe:
        if len(new_graphe[node]) == 0:
            del new_graphe[node]
    debug("mazeMap sans impasse ni couloir, economie de : " + str(len(mazeMap)-len(new_graphe)) + "nodes")
    return new_graphe

############################################################### primitives sur les coordonnées

def pos_to_int(position):
    """renvoie le numero de noeud, a partir de ses coordonnees"""
    global largeurLabyrinthe
    mazeWidth = largeurLabyrinthe
    return position[0] + mazeWidth * position[1]

def int_to_pos(integer):
    """renvoie les coordonnees d'un noeud, a partir du numero de noeud"""
    global largeurLabyrinthe
    mazeWidth = largeurLabyrinthe
    return (integer%mazeWidth,integer//mazeWidth)

def adjacentNodes(node, graphe):
    """renvoie la liste des coordonnees des voisins d'un noeud, en fonction du graphe, sans la liste des distances""" 
    liste = []
    for neighbourNode in graphe[node]:
        liste.append(neighbourNode[0])
    return liste

def adjacentWay(previousLocation,nextLocation):
    """renvoie la direction pour aller de previousLocation a nextLocation"""
    #on fait la différence entre les composantes verticales, et entre les composantes horizontales
    vertical = nextLocation[0] - previousLocation[0]
    horizontal = nextLocation[1] - previousLocation[1]
    if vertical == 1:
        return DOWN
    elif vertical == -1:
        return UP
    elif horizontal== 1:
        return RIGHT
    elif horizontal== -1:
        return LEFT
    else :
        return "ERROR"


def pathTracer(finishingNode,startingNode, routage):
    """à partir d'un routage, du noeud d'arrivé visé, donne toutes les cases rencontrées en chemin"""
    #on crée la liste des chemins, qui commence avec finishingNode et termine avec startingNode
    path = []
    path.append(finishingNode)
    #debug(str(coins[0]))
    
    #tant que le dernier noeud n'est pas startingNode
    #on récupère le parent du dernier noeud
    while not path[-1] == startingNode: 
        if type(path[-1]) == int:
            debug("\n " + str(path) + "\n "+str(routage))
        parent = routage[path[-1]]
        path.append(parent)
    #debug("3\n\n" + str(path)+"\n\n")
    return path
  

def directionMaker(pathList):
    """à partir d'une liste de cases formant un chemin, on fabrique la liste des décisions à prendre pour atteindre le noeud final"""
    directions = [] #on initialise la liste des directions à prendre
    while not len(pathList) == 1:
        actualLocation = pathList.pop() #on récupère le dernier élément de pathList
        #par la même occasion on réduit la taille de pathList, pour arrêter la boucle
        nextLocation = pathList[-1]
        nextdirection = adjacentWay(actualLocation, nextLocation)
        directions.append(nextdirection)
    #la prochaine direction à choisir en tant que joueur est directions[0]        
    #debug(str(directions))
    return directions

############################################################### recherche de pièces

# Dijkstra prend en entrée un nœud initial et un graphe
# Sa sortie est l'ensemble des longueurs des chemins les plus courts
# depuis le nœud initial à tous les autres nœuds atteignables dans le graphe
def dijkstra(noeud_initial, graphe):
    routage = [0]*len(mazeMap)
    time_taken = [0,0]
    # On défini d'abord les structures de données utiles
    # distances est le tableau rendu en fin d'algorithme qui contient toutes 
    # les longueurs des chemins minimaux depuis le noeud initial
    infini = float('inf')
    distances = [infini] * len(mazeMap)
    distances[noeud_initial] = 0
    
    # L'algorithme de Dijkstra utilise une file de priorité, elle contient
    # initialement le nœud initial avec sa distance au nœud initial : 0
    filePriorite = []
    heapq.heappush(filePriorite, (0,noeud_initial) )
    
    initTime = time.time()
    # Corps de l'algorithme :
    while not filePriorite == [] :
        stime = time.time()
        (distance , noeud_courant) = heapq.heappop(filePriorite)
        time_taken[0] += time.time() - stime
        stime = time.time()
        #pour tout noeud i voisin de noeud_courant:
        for voisin in graphe[noeud_courant]:
            dist_par_courant = distance + voisin[1]
            #i est le numero correspondant aux coordonnées du voisin 
            i = pos_to_int(voisin[0])
            if dist_par_courant <= distances[i]:
                distances[voisin[0]] = dist_par_courant
                routage[voisin[0]] = noeud_courant
                heapq.heappush(filePriorite, (dist_par_courant,voisin[0]) )
        time_taken[1] += time.time() - stime
    debug("heappop for " + str(time_taken[0]/(time_taken[0]+time_taken[1])) + "%\nand loop for " + str(time_taken[1]/(time_taken[0]+time_taken[1])) + "%" )
    debug("end of dijkstra in " + str((time.time() - initTime)*1000)+ "ms")
    # Il nous reste à rendre le résultat 
    return distances,routage

def dijkstra_self(noeud_initial, graphe):
    routage = {node:0 for node in graphe.keys()}
    time_taken = [0,0]
    # On défini d'abord les structures de données utiles
    # distances est le tableau rendu en fin d'algorithme qui contient toutes 
    # les longueurs des chemins minimaux depuis le noeud initial
    distances = {node:float('inf') for node in graphe}
    distances[noeud_initial] = 0
    
    # L'algorithme de Dijkstra utilise une file de priorité, elle contient
    # initialement le nœud initial avec sa distance au nœud initial : 0
    filePriorite = []
    filePriorite = heapAdd(filePriorite, noeud_initial, 0)
    
    #initTime = time.time()
    # Corps de l'algorithme :
    while not filePriorite == [] :
        stime = time.time()
        (distance , noeud_courant), filePriorite = heapSuppr(filePriorite)
        time_taken[0] += time.time() - stime
        stime = time.time()
        #pour tout noeud i voisin de noeud_courant:
        for voisin in graphe[noeud_courant]:
            dist_par_courant = distance + voisin[1]
            #i est le numero correspondant aux coordonnées du voisin 
            if dist_par_courant <= distances[voisin[0]]:
                distances[voisin[0]] = dist_par_courant
                routage[voisin[0]] = noeud_courant
                filePriorite = heapAdd(filePriorite,voisin[0], dist_par_courant)
        time_taken[1] += time.time() - stime
    #debug("heappop for " + str(time_taken[0]/(time_taken[0]+time_taken[1])) + "%\nand loop for " + str(time_taken[1]/(time_taken[0]+time_taken[1])) + "%" )
    #debug("end of dijkstra in " + str((time.time() - initTime)*1000)+ "ms")
    # Il nous reste à rendre le résultat 
    return distances,routage

def getdistrout(startingNode, graphe, outsidezonegraphe = False):
    """renvoie la matrice des distances et la table de routage d'origine startingNode dans le graphe considéré"""
    #l'intérêt de cette fonction est de ne pas toujours recalculer 
    
    #si on est perdu, on se raccroche à mazeMap
    #if startingNode not in graphe.keys():
        #result = dijkstra(startingNode, mazeMap)
    #outsidezonegraphe sert à faire un peu des exceptions
    #else :
    #réindenter

    #si on a pas déjà calculé ce chemin avant
    global meta_distrout
    if startingNode not in meta_distrout.keys(): 
        #on le cacule et on l'enregistre
        meta_distrout[startingNode] = dijkstra_self(startingNode, meta_graphe)
    #et on renvoit le résultat 
    result = meta_distrout[startingNode]
    return result


def getdistrout_zone(startingNode, graphe, outsidezonegraphe = False):
    """renvoie la matrice des distances et la table de routage d'origine startingNode dans le graphe considéré"""
    #l'intérêt de cette fonction est de ne pas toujours recalculer 
    
    #si on est perdu, on se raccroche à mazeMap
    if startingNode not in graphe.keys():
        result = dijkstra(startingNode, mazeMap)
    #outsidezonegraphe sert à faire un peu des exceptions
    elif graphe == zone_graphe:
        #si on a pas déjà calculé ce chemin avant
        if startingNode not in zone_distrout.keys():
            #on le cacule et on l'enregistre
            zone_distrout[startingNode] = dijkstra(startingNode, zone_graphe)
        #et on renvoit le résultat 
        result = zone_distrout[startingNode]
    #quand rien va, on affiche la présence d'une erreur
    else:
        debug("unrecognized graph")
        result = "error"
    return result

############################################################### gestion des données sur les pièces

def updateDistRoutplayers(playerpos, opponentpos):
    """met à jour les quatre variables globales avec les nouvelles valeurs de playerLocation et opponentLocation"""
    #à utiliser à l'initialisation et au début de chaque tour.
    global playerMatriceDistances
    global playerMatriceRoutage
    global opponentMatriceDistances
    global opponentMatriceRoutage
    #initTime = time.time()
    if opponentpos != (-1,-1):
        (opponentMatriceDistances, opponentMatriceRoutage) = getdistrout(opponentLocation, meta_graphe)
        #debug("end of getdistrout in " + str((time.time() - initTime)*1000)+ "ms")
    
    (playerMatriceDistances, playerMatriceRoutage) = getdistrout(playerLocation, meta_graphe)
    


def init_distcoin(startingNode, coins):
    """initialise distcoin le dictionnaire donnant les distances entre toutes les pièces"""
    global meta_graphe
    global distcoin #dictionnaire
    
    #initialisation distcoin
    distcoin[(startingNode,startingNode)] = 0
    
    #calcul des valeurs de distcoin
    #pour chaque pièce
    for j in range(len(coins)): 
        (matriceDistances, matriceRoutage) = getdistrout(coins[j],meta_graphe)
        #on calcule la distance à toutes les autres, moins celles que l'on a déjà calculées
        for i in range(j,len(coins)):
            #enregistrement des distances
        
            dist = matriceDistances[coins[i]]
            #rappel, les clés de distcoin sont des tuples de pos_to_int
            distcoin[(coins[i],coins[j])] = dist
            distcoin[(coins[j],coins[i])] = dist
        #enregistrement des distances depuis le joueur
        dist = matriceDistances[startingNode]
        distcoin[(startingNode, coins[j])] = dist
        distcoin[(coins[j], startingNode)] = dist
        #par la même occasion, on initialise appartenanceCoin, cf stratégie paquets
        appartenanceCoin[ coins[j] ] = -2 
    #debug("initialisation distcoin ok")

def update_distcoin(startingNode, ListCoins, startingNodeIsPlayerLocation):
    """mise à jour de distcoin, avec les coordonnées du joueur"""
    #si les distances par rapports à startingNode ont déjà été calculées, on ne refait pas le cacul
    #les calculs ont déjà été refaits s'il existe une combinaison de (posPlayer,posCoin) déjà présente dans distcoin
    if (startingNode,ListCoins[0]) not in distcoin:
        #on récup la matrice de distances partant du noeud de départ
        (matriceDistances, matriceRoutage) = getdistrout(startingNode, meta_graphe)
        for j in range(len(ListCoins)):
            #on récupère la distance entre intPos et intOrigin
            dist = matriceDistances[ListCoins[j]] 
            #on l'ajoute à distcoin
            distcoin[(startingNode, ListCoins[j])] = dist
            distcoin[(ListCoins[j], startingNode)] = dist

############################################################### stratégie de recherche de pièces
def nearestCoin(matrDist, listOfCoins):
    """renvoie les coordonnées de la pièce la plus proche selon matrDist"""
    nearestCoin = listOfCoins[0]
    distmini = 0
    #debug(str(len(matrDist)))
    for coin in listOfCoins:
        dist = matrDist[coin]
        if dist < distmini:
            distmini = dist
            nearestCoin = coin
    return nearestCoin

def chooseNearestCoin(startingNode,coinList):
    """renvoie les coordonées de la poèce la plus proche du joueur"""
    ## en réalité, cette fonction ne gère pas la présence de plusieurs pièces étant toutes le splus proches du joeur à la fois. 
   #il faucrait plus gérer ce cas avec comparaisonsolutions
    if len(coinList) == 1:  #on gère le cas d'une liste à 1 et zero éléments
        nearcoin=coinList[0]
        distancemini = distcoin[(startingNode,nearcoin)]
    elif len(coinList) == 0:
        return "Error, empty list "
        
    else:
        nearcoin=coinList[0]
        distancemini = float('inf')
        for coordCoin in coinList: #on récup la distances des pièces et on cherche la plus proche
            dist = distcoin[(startingNode,coordCoin)]
            #si la distance que l'on calcule est inférieure à distancemini actuelle
            if dist < distancemini: 
                #on met à jour distancemini actuel
                distancemini = dist
                nearcoin = coordCoin
    return nearcoin,distancemini


#donne les pièces les plus proches 
def findNearestCoinsProfondeur(coinMaxNumber,coinList, startingNode, coinBlackList = []):
    """renvoie les 'coinMaxNumber' pièces les plus proches de startingNode"""
    #le choix se fait dans la coinList
    liste = []#liste des pièces les plus proches
    if len(coinList) <= 1:#on règle le cas d'une liste de taille trop petite
        nearestCoins = coinList
    else :
        #on parcourt la liste de pièces.
        for coin in coinList: 
            # si la pièce ne fait pas parti de la blacklist
            #on l'ajoute à la liste des pièces
                
            if coin not in coinBlackList:
                #debug(str(len(matriceDistan)) + "\n" + str(pos_to_int(coin)) )
                #on récupère la distance entre startingNode et la pièce
                distToCoin = distcoin[(startingNode, coin)]
                #on ajoute cette pièce à la liste
                if len(liste) >= coinMaxNumber:#si il y a déja suffisament de pièces dans la liste
                    #on remplace les nouveaux éléments et on vire les anciens
                    #le signe moins sert à enlever en DERNIER les pièces les plus proches.
                    liste.pop()
                liste = heapAdd(liste, coin, distToCoin )
        #pn récupère les désignations des pièces.
        nearestCoins = [a[1] for a in liste ]  
    return nearestCoins

############################################################### travail sur le voyageur de commerce en pièces


def comparesolution(actualoptimalSolutions, newoptimalSolutions, efficiency = True ):
    if not efficiency: #seule la distance compte
        #on cherche un minimum
        if newoptimalSolutions[0][0] < actualoptimalSolutions[0][0]:
            actualoptimalSolutions = newoptimalSolutions
        elif newoptimalSolutions[0][0] == actualoptimalSolutions[0][0]:
            for solution in newoptimalSolutions:
                if solution not in actualoptimalSolutions:
                    actualoptimalSolutions.append( solution )
    else: #ici on prend en compte le poid attribué à la solution, en nombre de pièce
        actualEff = float(actualoptimalSolutions[0][2])
        newEff = float(newoptimalSolutions[0][2])
        #On cherche un maximum
        if newEff > actualEff:
            actualoptimalSolutions = newoptimalSolutions
        elif newEff == actualEff:
            for solution in newoptimalSolutions:
                if solution not in actualoptimalSolutions:
                    actualoptimalSolutions.append( solution )
    return actualoptimalSolutions    



def choixvoyageur(choix,dist_totale, optimumWay, leftCoins, coinList, startTurn, timeAllowed, profondeur1 = False ):
    """récursive, renvoie le meilleur chemin trouvé pour le moment"""
    #1ere condition d'arrêt
    if (len(choix) == len(coinList)) or (len(choix) >= OPTIMTURNCOINNUMBER + 1) or (time.time() - startTurn > timeAllowed * 0.8 ):
        if dist_totale > 0:
            #on crée la nouvelle solution
            newsolution = [ (dist_totale,choix, (len(choix)-1)/f(dist_totale) ) ]
            #on compare cette solution aux précédentes solutions
            optimumWay = comparesolution(optimumWay, newsolution, True )
        
    elif dist_totale >= optimumWay[0][0] :
        #arrêter de chercher dans cette direction
        #ne rien faire d'autre
        a = 0
    else:
        for indexJ in range( len(leftCoins) ):
            #mise à jours des variables de parcourt
            coin= leftCoins[indexJ]
            dist = dist_totale + distcoin[(choix[-1],coin)]
            nextchoix = choix + [coin]
            #mode exploration
            #on cherche la nouvelle pièce parmis les 12 pièces les plus proches
            leftCoinsnext = findNearestCoinsProfondeur(OPTISEARCHCOIN, coinList, coin, choix)
            #on execute choixvoyageur
            newsolution = choixvoyageur(nextchoix, dist , optimumWay, leftCoinsnext, coinList, startTurn, timeAllowed )
            #on récupère la meilleur solution
            optimumWay = comparesolution(optimumWay, newsolution, True )

    return optimumWay #renvoie les plus courts chemins



def voyageurcommerce(nombrePlacesAVisiter,startingNode, coinList, turnTime, timeAllowed, startingNodeIsPlayerLocation = True):
    global distcoin
    #initialisation de la solution, définie par ces 3variables
    longueurmini = float('inf')
    meilleurchemin = []
    poid = 0
    inisolution = [(longueurmini, meilleurchemin, poid)]
    #on vérifie qu'il reste assez de place pour executer le voyageur de commerce
    
    #on met à jour distcoin avec les coordonnées du joueur
    update_distcoin(startingNode, coinList, startingNodeIsPlayerLocation)    
    
    #pièces à étudier
    #ici ce sont les 'OPTISEARCHCOIN' pièces les plus proches du joueur
    interestingCoins = findNearestCoinsProfondeur(OPTISEARCHCOIN, coinList, startingNode)

    #calcul du chemin optimal sur nombrePlacesAVisiter pièces à prendre
    solutions = choixvoyageur([startingNode],0, inisolution , interestingCoins, coinList, turnTime, timeAllowed, True)
    
    #choix de la solution (si il y en a plusieurs)
    (distancetotale, ordrevoyage, poidsolution) = solutions[0]
    
    #on rajoute à aimedCoins les différentes  adresses des pièces présentes sur le graphe
    global aimedCoins
    aimedCoins = [j for j in ordrevoyage if j != startingNode]
    #debug(str(aimedCoins) + "\n")
    #debug( "next aimed coins = " +str(aimedCoins)+ "\n")

##VCP anciennement nananaBatman
def init_VCP(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins, startTurn):
    #debug("time needed to initiate : " + str((time.time() - startTurn)*1000)+ "ms")
    #debug("time needed to calculate : " + str((time.time() - startTurn)*1000)+ "ms")
    #on fait rien de spécial plus
    #car init_voyageurcommerce est déjà exécuté
    return
    
def nextmove_VCP(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, listOfCoins, turnTime, reworkPath, playerCoin):
    
    global aimedCoins
    global directionList
    if reworkPath:
        directionList = []
        initialTime = time.time()
        aimedCoins = []
        strat_VCP(playerLocation,listOfCoins, turnTime, timeAllowed, playerCoin)
        #debug("time needed to calculate : " + str((time.time() - initialTime)*1000)+ "ms")
        debug("end of recalc after "+ str((time.time() - turnTime)*1000)+ "ms\naimedCoins = "+str(aimedCoins) + "\n")
    

def strat_VCP(playerLocation,listOfCoins, turnTime, timeAllowed, playerCoin = []):
    voyageurcommerce(OPTIMTURNCOINNUMBER, playerLocation, listOfCoins, turnTime, timeAllowed)

def glouton_coins(orderCoins, cumulatedDist, startingNode, coinChoice):
    if coinChoice == []:
        orderOfCoins = orderCoins
    else :
        nextCoin, dist = chooseNearestCoin(startingNode,coinChoice)
        orderCoins += [nextCoin]
        cumulatedDist += dist
        coinChoice.remove(nextCoin)
        orderOfCoins, cumulatedDist = glouton_coins(orderCoins, cumulatedDist, startingNode, coinChoice)
    return orderOfCoins, cumulatedDist
        
############################################################### stratégie zones
                        
def choose_mindistance_way(startingNode, listOfCoins, opponentNode, interruption = False):
    #optimisation sur le nombre de dijkstra à réaliser. utilisation de paquets fort probable
    eloignementCoin = []
    oeloignementCoin = []
    bestsolutions = [( float('inf'), 0, -float('inf') )]
    for j in range(len(listOfCoins)): #choix de la destination
        eloignementCoin.append(0)
        oeloignementCoin.append(0)
        aimCoin = listOfCoins[j]
        matrdistZone, matrroutZone = getdistrout(startingNode, zone_graphe, True)
        ppath = pathTracer(aimCoin, startingNode, matrroutZone)

        if not opponentNode == (-1,-1):
            omatrdistZone, omatrroutZone = getdistrout(opponentNode, zone_graphe, True)#true car opponent not in zone_graphe
            opath = pathTracer(aimCoin, opponentNode, omatrroutZone)
        
        
        #nouvelle liste de pièce pour calculer la distance à toute les pièces après s'être déplacé.

        #faire de même avec l'ennemi        
        
        #calcul dist à toute les pièces
        for k in range(len(listOfCoins)):
            #préparation de l'implémentation paquet
            if listOfCoins[k] not in ppath: #(ET paquet non vide)
                distCoin = matrdistZone[listOfCoins[k]]
                eloign = distCoin #calcul de la distance
                eloignementCoin[j] +=  eloign ** 2
            if not opponentNode == (-1,-1):
                if listOfCoins[k] not in opath: #(ET paquet non vide)
                    odistCoin = omatrdistZone[listOfCoins[k]]
                    oeloign = odistCoin #calcul de la distance
                    oeloignementCoin[j] +=  oeloign ** 2
        if not opponentNode == (-1,-1):
            #on cherche un poid maximum
            newsolution = [( eloignementCoin[j], listOfCoins[j], (eloignementCoin[j]-oeloignementCoin[j])/f(eloignementCoin[j],4) )]
            bestsolutions = comparesolution(bestsolutions, newsolution, True ) #false avec piece, true avec paquets
        else : 
            #on cherche un éloignemenCoin minimum
            newsolution = [( eloignementCoin[j],listOfCoins[j])]
            bestsolutions = comparesolution(bestsolutions, newsolution, False ) #false avec piece, true avec paquets
    return bestsolutions
            

def strategie_zone(playerLoc, opponentLoc, listOfCoins):
    
    choix = choose_mindistance_way(playerLoc, listOfCoins, opponentLoc)
    nextcoin = choix[0][1]
    return [nextcoin]

def init_ZON(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins,startTurn) :
    
    global zone_graphe
    zone_graphe = init_graphe_zone(meta_graphe)
    strat_ZON(playerLocation, coins, opponentLocation)
    #debug("time needed for initializationCode : " + str((time.time() - startTurn)*1000)+ "ms")
    

def nextmove_ZON(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, listOfCoins,turnTime, reworkPath, playerCoin) :
    global directionList
    if reworkPath:
        directionList = []
        strat_ZON(playerLocation, listOfCoins, opponentLocation)
    
    
def strat_ZON(playerLocation,listOfCoins, opponentLocation):
    strategie_zone(playerLocation, opponentLocation, listOfCoins)
    
        
        
############################################################### stratégie fourmis

def update_phero_dist(listOfCoins):
    #update the player distance to coins
    for coin in listOfCoins:
        pheromones["p"][coin][0] = playerMatriceDistances[coin]

def evaporationphero():
    global nbrEvap
    global pheromones
    nbrEvap += 1
    for pos in pheromones.keys():
        for pos2 in pheromones[pos].keys():
            if pos != pos2:
                pheromones[pos][pos2][1] *= ANTEVAP 
            
def integrate(infos, isNotPlayer=0):
    efficacity = 0
    lenghtpath = sum(infos[1])
    #nombreVilles = len(infos[2])
    for j, length in enumerate(infos[1]):
        efficacity +=  (j) * infos[1][j] / (lenghtpath)
    return efficacity

def get_efficiency(cheminInfo, tailleCheminGlouton):
    path, taillechemin, villes = cheminInfo[0], cheminInfo[1], cheminInfo[2]
    lenghtpath = min( sum(taillechemin), tailleCheminGlouton)
    
    #nombreVilles = len(villes)
    efficacity = 0
    lengthway = 0
    for j in range(len(taillechemin)):
        lengthway += taillechemin[j]
        if lengthway <= tailleCheminGlouton:
            efficacity +=  (j) * taillechemin[j] / (lenghtpath)
        else:
            difference = lengthway - tailleCheminGlouton
            efficacity +=  (j) * (taillechemin[j]-difference) / (lenghtpath)
            break
    if lengthway < tailleCheminGlouton:
        difference = tailleCheminGlouton - lengthway
        efficacity +=  (j) * (taillechemin[j] + difference) / (lenghtpath)
        
    return efficacity


def show_efficient_graph():
    # import
    try:
        import matplotlib.pyplot as plt
    except:
        debug ("Matplotlib not found")
        return
    
    debug("loading graphs")
    resultsSinceBegining[0].pop(0)
    resultsSinceBegining[1].pop(0)
    
    plt.figure(0)
    plt.clf()
    for j in range(1,len(resultsSinceBegining[0])):
        t = [j-1, j, j]
        plt.plot( t, [resultsSinceBegining[0][a] for a in t ], 'b.-')
    for j in range(1,len(resultsSinceBegining[1])):
        t = [j-1, j, j]
        plt.plot( t, [resultsSinceBegining[1][a] for a in t ], 'r.-')
    plt.show()


def deposephero(cheminInfo, resultGlouton, oresultGlouton, tailleCheminGlouton):
    global pheromones
    global ant_pheromones_ways
    global efficiencyMax
    
    path, taillechemin, villes = cheminInfo[0], cheminInfo[1], cheminInfo[2]  
    nombreVilles = len(villes)
    weightpath = sum( [ f(j,ANT_POW_PATH) for j in taillechemin ] )
    
    efficiency = get_efficiency(cheminInfo, tailleCheminGlouton)
    
    #calcul de la quantitée de phéromone à déposer sur le chemin
    #ANT_PUT_PHERO_MULT = (nombreVilles * f(5,ANT_POW_PATH) )
    ANT_PUT_PHERO_MULT = 30000
    #pheromon = f( ANT_PUT_PHERO_MULT/weightpath, ANT_POW_PUT_PHERO) 
    #pheromon = (efficacity**2 /(resultGlouton * oresultGlouton) )**ANT_EFFICACITY *ANT_PUT_PHERO_MULT/f(weightpath,ANT_POW_PUT_PHERO)
    if resultGlouton == 0:
        a = efficiency
    else:
        a = efficiency / resultGlouton
    b = ANT_PUT_PHERO_MULT/f(weightpath,ANT_POW_PUT_PHERO) 
    pheromon = f(a, ANT_EFFICACITY) * ANT_PUT_PHERO_MULT/f(weightpath,ANT_POW_PUT_PHERO) 
    #pheromon = f(efficiency / resultGlouton, ANT_EFFICACITY) *f( ANT_PUT_PHERO_MULT/weightpath, ANT_POW_PUT_PHERO) 
    #pheromon = f(efficacity / resultGlouton, ANT_EFFICACITY)
    #pheromon = (efficacity - resultGlouton)/resultGlouton

    if efficiency > efficiencyMax[0]:
        efficiencyMax = [efficiency, path ]
    
    #if efficiency >= resultGlouton:        
    if 1:
        #si le glouton est meilleur, ne pas ajouter de phéromones
        ant_pheromones_ways.append(pheromon)
        #ancien test
        if path[0] not in villes:
            indexstart = 2
        else: 
            indexstart = 1
        
        #on les ajoute sur tout le chemin
        for j in range(indexstart,len(path)):
            firstNode = path[j - 1]
            secondNode = path[j]
            #on ajoute les pheromones sur le tronçon considéré
            pheromones[firstNode][secondNode][1] += pheromon
    return efficiency


def choosepheropath(listOfCoins, cheminrestant, startingNode, startInPreviousCoins, mode):
    global pheromones
    taillechemin = []
    chemin = [startingNode]
    #chemin aller
    if startInPreviousCoins:
        prochainNoeud = startingNode
    else:
        prochainNoeud = "p"
    
    #we need at least one element in the list
    boolean = 1
    
    while (len(cheminrestant) != 0) and boolean:
        #on change de noeud actuel
        noeudActuel = prochainNoeud
        tempList = [ pheromones[noeudActuel][coin][1]/f(pheromones[noeudActuel][coin][0],ANT_POW_VISIBILITY) for coin in cheminrestant ]
        if mode == 4:
            try:
                temp = [ pheromones[noeudActuel][coin][1]/f(pheromones[noeudActuel][coin][0],ANT_POW_VISIBILITY) for coin in cheminrestant if pheromones[noeudActuel][coin][0] <= pheromones[noeudActuel][aimedCoins[0]][0] ]
            except:
                debug("error of coin")
                debug( "aimedcoin in list == " + str(aimedCoins[0] in pheromones[noeudActuel].keys() ) )
                debug("aimed coin is starting node == " + str(aimedCoins[0] == startingNode) )
                debug("aimed coin is player loc == " + str(aimedCoins[0] == playerLocation) )
                debug("coin in previousCoins = " + str(aimedCoins[0] in  previousCoins))
                debug( str(pheromones[ noeudActuel ][ aimedCoins[0] ] ) )
                raise
            if len(temp) != 0:
                tempList = temp
            mode = 0
            
        if len(tempList) == 0:
            debug('no nodes in list')
            
        if mode == 0:
            #on choisit la prochaine ville à visiter
            hasard = random.random()
            #en fonction des phéromones présentes
            pheromonTotal = sum(tempList) #initialisation de pheromonTotal
            #si il ne reste plus de phéromones, on choisit la pièce la plus proche
            if pheromonTotal == 0:
                debug('no pheromones found')
                debug(str(tempList))
                tempList = [ -pheromones[noeudActuel][ cheminrestant[w] ][0] for w in range(len(cheminrestant)) ]
                count = indexOfMax(tempList )
            else:
                #pondération du hasard
                count = 0
                proba = 0
                while proba <= hasard: #on regarde à quel segment appartient hasard
                        proba += tempList[count]/pheromonTotal
                        if proba<= hasard:
                            count +=1
        elif mode == 1 : 
            #debug("noeudActuel = " + str(noeudActuel) + "\ncheminrestant = " + str(cheminrestant) )
            #debug("tempList = " + str(tempList) )
            count = indexOfMax(tempList )
        elif mode == 2 or mode == 3:
            #mode glouton pour évaluer un chemin
            tempList = [ -pheromones[noeudActuel][ cheminrestant[w] ][0] for w in range(len(cheminrestant)) ]
            count = indexOfMax(tempList )
            
        #la ville est choisie,d'index 'count'
        #on ajoute cette nouvelle ville au trajet
        prochainNoeud = cheminrestant[count]
        cheminrestant.pop(count)
        chemin += [prochainNoeud]
        #on récupère la distance entre la prochaine ville à visiter et la vile actuelle
        taillechemin.append(pheromones[noeudActuel][prochainNoeud][0])
    
        if mode == 2 or mode == 0 or mode == 4:
            boolean = ( (score[0] + len(chemin) - 1 ) <= VICTORY_CONDITION) or (len(chemin) <=1)
        elif mode == 3:
            boolean = ( (score[1] + len(chemin) - 1 ) <= VICTORY_CONDITION) or (len(chemin) <=1)
    
    return chemin, taillechemin


def parcoursUneFourmis(listOfCoins, startingNode, startInPreviousCoins, mode = 0 ):
    #si le depart fut une case avec une pièce
    global ant_phero
    
    cheminrestant = [ coin for coin in listOfCoins]
    
    #chemin aller
    chemin , taillechemin = choosepheropath(listOfCoins, cheminrestant, startingNode, startInPreviousCoins, mode)    
    
    #chemin retour
    if mode == 0:
        ant_phero.append((chemin, taillechemin, listOfCoins))
    elif mode == 1:
        pglouton = parcoursUneFourmis(listOfCoins, startingNode, startInPreviousCoins, 2)
        resultGlouton = integrate(pglouton, 0)
        gchemin, gtaillechemin, glistOfCoins = pglouton[0], pglouton[1], pglouton[2]
        efficiency = get_efficiency( (chemin , taillechemin, listOfCoins), sum(gtaillechemin) )
        
        if efficiency < resultGlouton and resultGlouton > efficiencyMax[0]:
            debug("stratglouton avec efficacité de " + str(resultGlouton) + "par rapport a " + str(efficiency))
            ant_phero.append((gchemin, gtaillechemin, glistOfCoins))
            return gchemin
        else:
            ant_phero.append((chemin, taillechemin, listOfCoins))
            return efficiencyMax[1]
        #sinon on retourne le chemin normal
        
    elif mode == 2:
        ant_phero.append((chemin, taillechemin, listOfCoins))
        return chemin, taillechemin, listOfCoins
    elif mode == 3:
        return chemin, taillechemin, listOfCoins
    #debug("trajet de la fourmis = " + str(chemin) )
    return chemin
        
           
def fourmis(timeAllowed, playerLocation, opponentLoc, listOfCoins, startingTime, playerCoin, opponentCoin) :
    global pheromones
    global ant_phero
    global ant_pheromones_ways
    global lastNumberOfAntsSent
    startingNode = playerLocation
    playerInCoins = startingNode in previousCoins
    numberOfAnts = 0
    aimedCoinsPasVide = (len(aimedCoins) != 0)

    if playerInCoins:
        for coin in listOfCoins:
            pheromones["p"][coin][1] = ANT_START_PHERO
    
    pglouton = parcoursUneFourmis(listOfCoins, startingNode, playerInCoins, 2)
    oglouton = parcoursUneFourmis(listOfCoins, opponentLoc, playerInCoins, 3)
    
    resultGlouton = integrate(pglouton, 0)
    oresultGlouton = integrate(oglouton, 1)
    
    #on lance autant de fourmis qu'on peut
    while time.time() - startingTime < timeAllowed*0.93:
        numberOfAnts += 1
        if numberOfAnts >= ANT_MUTANT*lastNumberOfAntsSent and aimedCoinsPasVide:
            parcoursUneFourmis(listOfCoins, startingNode, playerInCoins, 4)
        else:
            parcoursUneFourmis(listOfCoins, startingNode, playerInCoins, 0)
        if numberOfAnts%50 == 0:
            while ant_phero != []:
                update = ant_phero.pop(0)
                deposephero(update, resultGlouton, oresultGlouton, sum(pglouton[1]) )
            evaporationphero()

    while ant_phero != []:
        update = ant_phero.pop(0)
        deposephero(update, resultGlouton, oresultGlouton, sum(pglouton[1]) )
    evaporationphero()
    #debug("phero moyenne = " + str( sum(ant_pheromones_ways)/len(ant_pheromones_ways)))
    #debug(str(len(listOfCoins)) + " phero max = " + str( max(ant_pheromones_ways)) )
    #debug("phero max = " + str( max(ant_pheromones_ways)) + " time needed = " + str((time.time() - startingTime)*1000)+ "ms")
    #k = indexOfMax(ant_pheromones_ways)
    #secondMax = max(trou(ant_pheromones_ways, k))
    #debug("phero convergence = " + str(secondMax/ant_pheromones_ways[k]))
    #debug(str(len(listOfCoins)) + " phero impact = " + str( max(ant_pheromones_ways)/(ANT_START_PHERO * f(ANTEVAP, nbrEvap)) ) )
    #debug(str(len(listOfCoins)) + " phero impact = " + str( sum(ant_pheromones_ways)/(ANT_START_PHERO * f(ANTEVAP, nbrEvap)) ) )
    #debug(str(len(listOfCoins)) + " phero max = " + str( max(ant_pheromones_ways)) + "phero moyenne = " + str( sum(ant_pheromones_ways)/len(ant_pheromones_ways)))
    ant_pheromones_ways = []
    lastNumberOfAntsSent = numberOfAnts
    debug("number of ants sent = " + str(numberOfAnts) )



def init_ANT(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, listOfCoins,startTurn) :
    
    global pheromones
    pheromones = { node:{nextNode : [distcoin[(node,nextNode)], ANT_START_PHERO] for nextNode in listOfCoins if nextNode != node} for node in listOfCoins}
    pheromones["p"] = {nextNode : [distcoin[(playerLocation,nextNode)], ANT_START_PHERO] for nextNode in listOfCoins}
    playerCoin = nearestCoin(playerMatriceDistances, coins)
    if not opponentLocation == (-1,-1):
        opponentCoin = nearestCoin(opponentMatriceDistances, coins)
        
    strat_ANT(timeAllowed, playerLocation, opponentLocation, listOfCoins, startTurn, playerCoin, opponentCoin)
    
    
    
def nextmove_ANT(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, listOfCoins,turnTime, reworkPath, playerCoin, opponentCoin) :
    
    global aimedCoins
    global directionList
    global efficiencyMax
    
    if reworkPath:
        directionList = []
        efficiencyMax = [0, []]
            #debug("aim remains " + str(aimedCoins))
        #debug("rework ants")
    strat_ANT(timeAllowed, playerLocation, opponentLocation, listOfCoins, turnTime, playerCoin, opponentCoin)
    
def strat_ANT(timeAllowed, playerLocation, opponentLocation, listOfCoins, turnTime, playerCoin, opponentCoin) :
    #on lance les fourmis lalala
    global aimedCoins
    global playerMatriceDistances
    
    playerInCoins = playerLocation in previousCoins
    
    update_phero_dist(listOfCoins)
    fourmis(timeAllowed, playerLocation, opponentLocation, listOfCoins, turnTime, playerCoin, opponentCoin)
    cheminmax = parcoursUneFourmis(listOfCoins, playerLocation, playerInCoins, 1)
    #debug(str(tableChoix))
    #choix du chemin, parcours d'une fourmi cherchant les arêtes maxi
    while playerLocation in cheminmax:
        cheminmax.remove(playerLocation)
        #debug('repetition')
    if numberOfTurnSinceLastChangeOfDirection >= MIN_NUMBER_OF_TURNS_BETWEEN_TWO_CHANGES_OF_DECISIONS:
        aimedCoins = [j for j in cheminmax]
        numberOfTurnSinceLastChangeOfDirection
    
    #debug("strat decided " + str(aimedCoins))
############################################################### strategie glouton

def init_GLU(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins,startTurn) :
    #do nothing
    return

def nextmove_GLU(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, listOfCoins,turnTime, reworkPath, playerCoin, opponentCoin) :
    
    global directionList
    
    if reworkPath:
        directionList = []
        strat_GLU(playerLocation, listOfCoins, playerCoin)
    
def strat_GLU(playerLoc, listOfCoins, playerCoin):
    
    global aimedCoins
    if playerCoin in listOfCoins:
        nextAim = playerCoin
    else:
        update_distcoin(playerLoc, listOfCoins, True)
        nextAim, dist = chooseNearestCoin(playerLoc, listOfCoins)
    aimedCoins = [nextAim]
    
        

############################################################### symetric strategy

def update_score(playerLocation, opponentLocation, coinList):
    global previousCoins
    global score
    global resultsSinceBegining
    playerGotCoinAlone = False
    
    if playerLocation == opponentLocation:
        if playerLocation in previousCoins:
            score[0]+=0.5
            score[1]+=0.5
            efficiencyMax[0] -= 1
            resultsSinceBegining[0].append(0.5 + resultsSinceBegining[0][-1] )
            resultsSinceBegining[1].append(0.5 + resultsSinceBegining[1][-1] )
        else:
            resultsSinceBegining[0].append(0 + resultsSinceBegining[0][-1] )
            resultsSinceBegining[1].append(0 + resultsSinceBegining[1][-1] )
            
    else:
        if playerLocation in previousCoins:
            score[0]+=1
            efficiencyMax[0] -= 1
            resultsSinceBegining[0].append(1+ resultsSinceBegining[0][-1] )
            playerGotCoinAlone = False
        else:
            resultsSinceBegining[0].append(0+ resultsSinceBegining[0][-1] )
            
        if opponentLocation in previousCoins:
            score[1] += 1
            resultsSinceBegining[1].append(1 + resultsSinceBegining[1][-1] )
        else:
            resultsSinceBegining[1].append(0 + resultsSinceBegining[1][-1] )
    previousCoins = copy.deepcopy(coinList)
    return playerGotCoinAlone
    

def cutHalf(integer):
    return (integer - 1)/2

def getSymetric(mazeWidth, mazeHeight, position):
    middle = (cutHalf(mazeWidth), cutHalf(mazeHeight))
    symetric = (int(2*middle[0]-position[0]), int(2*middle[1] - position[1]) )
    return symetric
    
def init_SYM(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, listOfCoins, startTurn) :
    init_ANT(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, listOfCoins, startTurn)
    

def nextmove_SYM(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, listOfCoins,turnTime, reworkPath, playerCoin) :
    
    opponentSymetric = getSymetric(mazeWidth, mazeHeight, opponentLocation)
    osDist, osRout = getdistrout(opponentSymetric, meta_graphe)
    middle = (int(cutHalf(mazeWidth)), int(cutHalf(mazeHeight)))
    mDist, mRout = getdistrout(middle, meta_graphe)
    coinList = [[],[],[],[]]
    dist1pmini = float('inf')
    dist1nmini = -float('inf')
    dist1pcoin = []
    dist1ncoin = []
    for coin in listOfCoins:
        dist1 = opponentMatriceDistances[coin] - osDist[coin]
        if dist1 < dist1pmini and 0 < dist1:
            dist1pmini = dist1
            dist1pcoin = coin
        if dist1 > dist1nmini  and dist1 < 0:
            dist1nmini = dist1
            dist1ncoin = coin
        
        dist2 = opponentMatriceDistances[coin] - mDist[coin]
        cointuple = (coin, dist1, dist2)
        if dist1 >= 0 and dist2 >= 0 :
            coinList[3].append(cointuple)
        elif dist1 >= 0 and dist2 < 0:
            coinList[2].append(cointuple)
        elif dist1 < 0 and dist2 >= 0:
            coinList[1].append(cointuple)
        elif dist1 < 0 and dist2 < 0:
            coinList[0].append(cointuple)
    
    dist1 = opponentMatriceDistances[playerLocation] - osDist[playerLocation]
    dist2 = opponentMatriceDistances[playerLocation] - mDist[playerLocation]
    if dist1 >= 0 and dist2 >= 0 :
        playerPos = 3
    elif dist1 >= 0 and dist2 < 0:
        playerPos = 2
    elif dist1 < 0 and dist2 >= 0:
        playerPos = 1
    elif dist1 < 0 and dist2 < 0:
        playerPos = 0
    strat_SYM(playerLocation, listOfCoins, turnTime, timeAllowed, playerCoin, coinList, dist1ncoin, dist1pcoin, playerPos)
    

def strat_SYM(playerLocation, listOfCoins, turnTime, timeAllowed, playerCoin, coinList, dist1ncoin, dist1pcoin, playerPos):
    
    if playerPos == 2 or playerPos == 3:
        if score[1] + len(coinList[2]+coinList[3]) >= VICTORY_CONDITION:
            theCoinList = [ a[0] for a in coinList[2]+coinList[3] ]
        elif len(coinList[2] + coinList[3]) < COIN_MIN_OPPONENT_SIDE:
            theCoinList = [ a[0] for a in coinList[0]+coinList[1] ]
        elif score[0] + len(coinList[0]+coinList[1]) < VICTORY_CONDITION:
            theCoinList = [ a[0] for a in coinList[0]+coinList[1]+coinList[2]]
        else :
            theCoinList = listOfCoins
    else :
        theCoinList = listOfCoins
        
    strat_ANT(playerLocation, theCoinList, turnTime, timeAllowed, playerCoin )

############################################################### montecarlo

def init_MTC(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins,startTurn) :
    #do nothing
    return

def nextmove_MTC(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, listOfCoins,turnTime, reworkPath, playerCoin) :
    
    return
    
def strat_MTC(playerLocation, listOfCoins, turnTime, timeAllowed, opponentLocation):
    timeline = []
    while time.time() - turnTime < timeAllowed:
        createway(playerLocation, opponentLocation, listOfCoins)
        
def createway(playerLoc, opponentLoc, listOfCoins):
    coinList = copy.copy(listOfCoins)
    playerWay = []
    opponentWay = []
    pCumulatedDist = 0
    oCumulatedDist = 0
    while coinList:
        pdist, prout = getdistrout(playerLoc, meta_graphe)
        odist, orout = getdistrout(opponentLoc, meta_graphe)
        
        pcoin = coinList[ random.randint(0,len(coinList)) ]
        ocoin = coinList[ random.randint(0,len(coinList)) ]
        
        
        
        if pcoin in playerWay and pcoin in opponentWay:
            coinList.remove(pcoin)
        if ocoin in playerWay and ocoin in opponentWay:
            coinList.remove(ocoin)
        
    return

############################################################### paquet bis

def classifyCoins(coin, coins):
    """crée la liste des paquets"""
    #pour cela, il faut choisir une pièce et créer un paquet pour elle, puis regarder si ses voisins ne sont pas déjà dans un paquet
    global classificationCoin
    
    typeCoin = 0
    if classificationCoin[coin] != -2:
        j = classificationCoin[coin]
    
    #on regarde toutes les pièces
    for voisinCoin in [x for x in coins if x != coin]:
        #si la distance entre la pièce de départ et la pièce considérée est suffisament petite
        if distcoin[(voisinCoin,coin)] <= OPTIDISTPAQUET:
            typeCoin = 2
            #on élimine le cas où on considère la pièce de départ elle même
            
            #si la pièce considérée est déjà dans un paquet
            if  classificationCoin[voisinCoin] != -2:
                if not classificationCoin[voisinCoin] == classificationCoin[coin]:
                    x = paquets.pop(j)
                    i = classificationCoin[voisinCoin]
                    debug("index i = " + str(i) + "\npaquets = " + str(paquets) + "\nlenght of paquets = " + str(len(paquets)) + "\n")
                    for travelingCoin in x:
                        classificationCoin[travelingCoin] = i
                        paquets[i].append(travelingCoin)
            #sinon...
            else:
                paquets[j].append(voisinCoin)
                classificationCoin[voisinCoin] = j
                cherchepaquet(voisinCoin, coins)
        elif distcoin[(voisinCoin,coin)] < 10 and typeCoin ==0:
            typeCoin = 1
            
    return typeCoin

def init_PAK(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, listOfCoins,startTurn) :
    for coin in listOfCoins:
        coinType[coin] = classifyCoins(coin, listOfCoins)
    for coin in [x for x in coins if coinType[x] == 2]:
        pakito[coin] = paquets[ classificationCoin[coin] ]
    
############################################################### anti copycat
        
def update_copycat(playerLoc,opponentLoc):
    global previous_position
    previous_position[0].append(playerLoc)
    previous_position[1].append(opponentLoc)
    
def detect_copycat(mazeWidth, mazeHeight):
    if previous_position[2] >= 2:
        IsCopyCat = True
    else :
        compareList = trou(previous_position[1], 0)
        if len(compareList)%5==4:
            copy = True
            for j in range(len(previous_position[0]) - 2):
                if not getSymetric(mazeWidth, mazeHeight, previous_position[0][j]) == compareList[j]:
                    copy = False
        else :
            copy = False
            
        if copy :
            previous_position[2]+=1
        if previous_position[2] >= 2:
            IsCopyCat = True
        else:
            IsCopyCat = False
    return IsCopyCat

def explode_copycat(playerLoc, mazeMap):
    """KABOOM"""
    global directionList
    global previous_position
    trapPossible = False
    for voisin in mazeMap[playerLoc]:
        if voisin[1] == 10:
            trapPossible = True
    if trapPossible:
        directionList = ['S'] + directionList
        previous_position[2] = -1
        previous_position[0] = []
        previous_position[1] = []
    
    
        
####################################################################################################################################################################################################################################

# This is where you should write your code to do things during the initialization delay
# This function should not return anything, but should be used for a short preprocessing
# This function takes as parameters the dimensions and map of the maze, the time it is allowed for computing, the players locations in the maze and the remaining coins locations
# Make sure to have a safety margin for the time to include processing times (communication etc.)

def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    
    startTurn = time.time()
    #initialisation des variables de stratégies
    global init_function
    global nextmove_function
    global strat_function
    global strategy_vector
    global previousCoins
    init_function = [init_VCP, "", init_ZON, init_ANT, init_GLU, init_SYM]
    nextmove_function = [nextmove_VCP, "", nextmove_ZON, nextmove_ANT, nextmove_GLU, nextmove_SYM]
    strat_function = [strat_VCP, "", strat_ZON, strat_ANT,strat_GLU, strat_SYM]
    strategy_vector = [VCPcoinMIN, PAQcoinMIN, ZONcoinMIN, ANTcoinMIN, GLUcoinMIN, SYMcoinMIN ]    
    
    previousCoins = copy.deepcopy(coins)

    global largeurLabyrinthe
    largeurLabyrinthe = mazeWidth
    global meta_graphe
    meta_graphe = shortenMap(mazeMap)
    #initTime = time.time()
    updateDistRoutplayers(playerLocation, opponentLocation)
    #debug("end of distrout in " + str((time.time() - initTime)*1000)+ "ms")
    init_distcoin(playerLocation,coins)
    #init_voyageurcommerce_paquets(playerLocation, coins)
    #debug("end of general initialization in " + str((time.time() - startTurn)*1000)+ "ms")
    
    if TYPEOFSTRATEGY == 3:
        debug("ANT_POW_PATH = " + str(ANT_POW_PATH) + " and ANT_POW_VISIBILITY = " + str(ANT_POW_VISIBILITY) + "\nand ANT_POW_PUT_PHERO = " + str(ANT_POW_PUT_PHERO) )
    
    init_function[TYPEOFSTRATEGY](mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins,startTurn)
    #debug("end of strategic initialization in " + str((time.time() - startTurn)*1000)+ "ms\n")
    
    
####################################################################################################################################################################################################################################

# This is where you should write your code to determine the next direction
# This function should return one of the directions defined in the CONSTANTS section
# This function takes as parameters the dimensions and map of the maze, the time it is allowed for computing, the players locations in the maze and the remaining coins locations
# Make sure to have a safety margin for the time to include processing times (communication etc.)

def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    
    turnTime = time.time()
    global aimedCoins
    global directionList
    global numberOfTurnSinceLastChangeOfDirection
    
    numberOfTurnSinceLastChangeOfDirection +=1
    #debug( "1aimed coins are in coins = " + str([(coin in coins) for coin in aimedCoins]) )    
    
    playerGotCoinAlone = update_score(playerLocation, opponentLocation, coins)
    if not previous_position[2] == -1:
        update_copycat(playerLocation, opponentLocation)
        detection = detect_copycat(mazeWidth, mazeHeight)
        if detection:
            explode_copycat(playerLocation,mazeMap)
    
    
    updateDistRoutplayers(playerLocation, opponentLocation)
    
    if not opponentLocation == (-1,-1):
        opponentCoin = nearestCoin(opponentMatriceDistances, coins)
    playerCoin = nearestCoin(playerMatriceDistances, coins)
    
    listOfStrategicCoins = copy.copy(coins)
    #vérifier que toutes les pièces visées sont présentes
    if not(aimedCoins == []):
        #si on a atteint notre cible, on passe à la suivante
        while playerLocation in aimedCoins: 
            aimedCoins.remove(playerLocation)
        if not opponentLocation == (-1,-1):
            #si la pièce visée est trop proche de l'adversaire et innateignable
            if playerMatriceDistances[opponentCoin] > opponentMatriceDistances[opponentCoin]:
                #on ne va pas la chercher
                listOfStrategicCoins.remove(opponentCoin)
                directionList = []
                
    #recherche des pièces manquantes sur notre trajet
    oneAimedCoinIsMissing = 0
    for target in aimedCoins:
        if target not in listOfStrategicCoins:
            oneAimedCoinIsMissing = True
            eatenCoin = target
            aimedCoins.remove(eatenCoin)
    if oneAimedCoinIsMissing and playerGotCoinAlone:
        aimedCoins.remove(eatenCoin)
        oneAimedCoinIsMissing = False
    #s'il ne reste plus de pièces possibles d'aprs une stratégie normale, on revient à la liste de pièces habituelle
    if listOfStrategicCoins == []:
        listOfStrategicCoins = coins

    #debug( "2aimed coins are in coins = " + str([(coin in coins) for coin in aimedCoins]) )
    #debug( "one aimed coin is missing = " + str(oneAimedCoinIsMissing))
    #debug("aimedCoins = " + str(aimedCoins))
    #debug("playerloc = " + str(playerLocation))
    #debug("opponentLocation = " + str(opponentLocation) )
    #debug("opponentCoin" + str(opponentCoin))
            
    reworkPath = oneAimedCoinIsMissing or aimedCoins == []
    #debug("before aimedCoins = "+str(aimedCoins))
    #debug("preparation of turn in " + str((time.time() - turnTime)*1000)+ "ms")
    #be sure we have enough coins befoore chosing a strategy
    i = TYPEOFSTRATEGY
    while strategy_vector[i] > len(listOfStrategicCoins):
        i += 1
        if i == len(strategy_vector):
            i-=2
            break
    nextmove_function[i](mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, listOfStrategicCoins, turnTime, reworkPath, playerCoin, opponentCoin)
    #debug("end of turn strategy in " + str((time.time() - turnTime)*1000)+ "ms")
    #debug("now aimedCoins = "+str(aimedCoins))

    #PARASITAGE
    if not opponentLocation == (-1,-1):
        if playerMatriceDistances[opponentCoin] == opponentMatriceDistances[opponentCoin] and opponentCoin != aimedCoins[0]:
            debug("parasitage !")
            aimedCoins = [opponentCoin] + aimedCoins
            directionList = []
    #recalcul de la trajectoire
    if directionList == []:
        nextAim = aimedCoins[0]
        pathSolution = pathTracer(nextAim, playerLocation, playerMatriceRoutage)
        directionList = directionMaker(pathSolution)
    #si les calculs n'ont pas aboutis
    if directionList == []:
        nextmove = 'X'
    else : 
        nextmove = directionList.pop(0)
    
    
    debug("score opponent = " + str(score[1]) + " et odist = " + str(opponentMatriceDistances[opponentCoin]) + " et pdist = " + str(playerMatriceDistances[opponentCoin]) )
    
    #if (score[0] >= 19.5 and playerMatriceDistances[playerCoin] == 1 ) or (score[1] >= 19.5 and opponentMatriceDistances[opponentCoin] == 1 ):
     #   show_efficient_graph()
    debug("end of turn in " + str((time.time() - turnTime)*1000)+ "ms")
    return nextmove

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
            #show_efficient_graph()
            break
        nextMove = determineNextMove(mazeWidth, mazeHeight, mazeMap, turnTime, playerLocation, opponentLocation, coins)
        writeToPipe(nextMove)
    
    

####################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################
