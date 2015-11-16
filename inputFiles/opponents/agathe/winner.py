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

TEAM_NAME = "Jerry"

####################################################################################################################################################################################################################################
########################################################################################################## YOUR CONSTANTS ##########################################################################################################
####################################################################################################################################################################################################################################

# valeur infinie
infini=float("inf")

####################################################################################################################################################################################################################################
########################################################################################################## YOUR VARIABLES ##########################################################################################################
####################################################################################################################################################################################################################################

# metagraphe des pieces au debut de la partie, a initialiser avec mazeMap, coins, playerLocation et dijkstra
Grand_metagraphe=0

# liste des positions a suivre
chemin=0

coord_num=0
num_coord=0

mode = 0

# pour exhaustif
meilleur_chemin=[]
mieux=infini
trajet_final=[]

# pour glouton dans zone interessante
taille_apetit = 0


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

# fonction qui cree deux dictionnaires en donnant un numero a chaque element de la liste
# dico[element de la liste] donne le numero associe
# recip[numero] donne l element associe a ce numero

def numeros(liste_noeud):
    dico={}
    recip={}
    numero=0
    for coordonnees in liste_noeud:
        dico[coordonnees]=numero
        recip[numero]=coordonnees
        
        numero=numero+1
        
    return dico, recip

# teste si une liste est vide
# vrai si elle est vide
# faux sinon
# amelioration avec len(liste)=0 ??

def vide(liste):
    if liste==[]:
        return True
    else:
        return False

# retire et retourne un element d une file priorite en enlevant l element avec la plus grande etiquette
# parcourt donc la file et retient le plus grand et son indice a chaque fois
# a l aide de l indice elle cree une file ou l element est retire
# retourne cle de l element retire, etiquette de l element retire, la nouvelle file de priorite

def retirer(file_priorite):
    element_a_retirer=file_priorite[0]
    indice_de_element_a_retirer=0
    for indice in range(1,len(file_priorite)):
        if file_priorite[indice][1]<element_a_retirer[1]:
            element_a_retirer=file_priorite[indice]
            indice_de_element_a_retirer=indice
    file_priorite=file_priorite[:indice_de_element_a_retirer]+file_priorite[indice_de_element_a_retirer+1:]
    return element_a_retirer[0], element_a_retirer[1], file_priorite

# on prend l'element correspondant au noeud et on le remplace par (i, distance) et si il n'y est pas on le met a la fin

def remplacer(file_priorite, noeud, distance):
    for indice in range(len(file_priorite)):
        if file_priorite[indice][0]==noeud:
            file_priorite[indice][1]=distance
            return file_priorite
    file_priorite.append([noeud,distance])
    return file_priorite

# fonction qui retourne la liste des voisins sous la forme (coordonnee, distance) de currentNode(coord) a partir de graph
def neighbor_list(currentNode, graph):
    
    voisins=[]
    for coordonnee_distance in graph[currentNode]:
        voisins.append(coordonnee_distance)
    
    return voisins

# Dijkstra prend en entree un nœud initial et un graphe
# Sa sortie est l'ensemble des longueurs des chemins les plus courts
# depuis le nœud initial à tous les autres nœuds atteignables dans le graphe
# il modifie la variable globale positions pour avoir un routage des predecesseurs

def dijkstra(noeud_initial, graphe, mazeWidth, mazeHeight):
    global infini
    # On defini d'abord les structures de donnees utiles
    # distances est le tableau rendu en fin d'algorithme qui contient toutes 
    # les longueurs des chemins minimaux depuis le noeud initial
    positions={}
    distances = [[infini for k in range(mazeWidth)] for l in range(mazeHeight)]
    distances[noeud_initial[0]][noeud_initial[1]] = 0
    positions[noeud_initial] = noeud_initial
    # L'algorithme de Dijkstra utilise une file de priorite, elle contient
    # initialement le nœud initial avec sa distance au nœud initial : 0
    
    file_priorite=[]
    file_priorite.append([noeud_initial,0])
 
    # Corps de l'algorithme :
 
    while not(vide(file_priorite)):
        noeud_courant, distance, file_priorite = retirer(file_priorite)
        for noeud_voisin in neighbor_list(noeud_courant, graphe):
            distance_par_courant = distance + noeud_voisin[1]
            if distances[noeud_voisin[0][0]][noeud_voisin[0][1]] > distance_par_courant:
                distances[noeud_voisin[0][0]][noeud_voisin[0][1]] = distance_par_courant
                remplacer(file_priorite, noeud_voisin[0], distance_par_courant)
                positions[noeud_voisin[0]]=noeud_courant
    
    # Il nous reste a rendre le resultat
    
    return distances, positions

# fonction qui indique la direction a prendre en comparant deux positions (doivent etre adjacentes sinon ne rend pas bon resultat)

def direction_a_prendre(position_avant,position_apres):
    if position_avant[0]<position_apres[0]:
        return DOWN
        
    elif position_avant[0]>position_apres[0]:
        return UP
        
    elif position_avant[1]<position_apres[1]:
        return RIGHT
        
    elif position_avant[1]>position_apres[1]:
        return LEFT

def metagraphe(coins, mazeMap, mazeWidth, mazeHeight):
    global coord_num
    global num_coord
    global infini
    
    graphe=[[infini for i in range(len(coins))] for j in range(len(coins))]
    for i in range(len(coins)):
        graphe[i][i]=-1
    
    for noeud_initial in coins:
        distances, positions = dijkstra(noeud_initial, mazeMap, mazeWidth, mazeHeight)
        for objectifNode in coins:
            if objectifNode!=noeud_initial:
                trajet=[]
                currentNode=objectifNode
                while currentNode != noeud_initial:
                    trajet.append(currentNode)
                    currentNode=positions[currentNode]
                graphe[coord_num[noeud_initial]][coord_num[objectifNode]]=[trajet,distances[objectifNode[0]][objectifNode[1]]]
                
    return graphe

def adjacents(position):
    i,j=position[0],position[1]
    return [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]

# retourne true si piece est dans le carre 3*3 de centre position

def dans_le_carre(position,piece):
    carre=adjacents(position)
    for case in carre:
        if case==piece:
            return True
    return False

#sous-fonction qui teste si la case appartient a la liste des pieces
def appartient(coins,case):
    for piece in coins:
        if piece == case:
            return True
    return False
    
# position est la position d'une piece
# retourne [true ou false, la liste des pieces dans le carre, le centre du carre]
def interessant(position, coins):
    carre=adjacents(position)
    pieces_dans_le_carre=[position]
    for case in carre:
        if appartient(coins,case):
            pieces_dans_le_carre = pieces_dans_le_carre + [case]
    if len(pieces_dans_le_carre)>=3:
        return [True, pieces_dans_le_carre, position]
    return [False, pieces_dans_le_carre, position]
    
def exhaustif(restants, noeud, chemin, poids, graphe):
    global mieux
    global meilleur_chemin
    global coord_num
    global num_coord
    if restants==[]:
        if poids<mieux:
            mieux=poids
            meilleur_chemin=chemin
    else:
        for noeud_restant in restants:
            temp = list(restants)
            temp.remove(noeud_restant)
            exhaustif(temp, noeud_restant, chemin+[noeud_restant], poids+graphe[coord_num[noeud]][coord_num[noeud_restant]][1], graphe)

# fonction qui retourne True si la piece que je veux attraper est toujours la, False sinon
# complexite au pire taille de coins

def piece_a_attrapper_tj_la(piece, coins):
    # entree : piece = coord de la piece que l'on veut atteindre
    # coins = liste des piece toujours la pour ce tour de jeu
    for piece_restante in coins:
        if piece == piece_restante:
            return True
    return False

# fonction aui retourne le chemin de la piece la pus proche de moi
def lost_vite_manger(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins):
    
    distances, positions = dijkstra(playerLocation, mazeMap, mazeWidth, mazeHeight)
    
    piecePlusProche = coins[0]
    distance = distances[piecePlusProche[0]][piecePlusProche[1]]
    for coin in coins:
        autreDistance = distances[coin[0]][coin[1]]
        if distance > autreDistance:
            piecePlusProche = coin
            distance = autreDistance
    
    trajet = []
    currentNode = piecePlusProche
    while currentNode != playerLocation:
        trajet.append(currentNode)
        currentNode = positions[currentNode]
    
    return trajet

# fonction qui dit si cette piece risque fortement detre atteinte par lenemy en premier
def risk(objectif, mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins):
    
    # il faut comparer ma distance a cette piece et la distance de ladversaire a cette piece
    # (probleme si lui va chercher dautres pieces entre temps la distance est plus grande et en fait jaurais pu prendre cette piece et les pieces alentour avant lui)
    # donc un dijkstra sur cet objectif suffit
    
    distances, positions = dijkstra(objectif, mazeMap, mazeWidth, mazeHeight)
    
    maDistance = distances[playerLocation[0]][playerLocation[1]]
    saDistance = distances[opponentLocation[0]][opponentLocation[1]]
    
    if maDistance > saDistance:
        return True # c'est risquer !!!
    else:
        return False # trankil il laura jamais avant moi celle la
    
# if risk true
# faire un lost vite manger avec coins sans cet objectif
# ou alors un ZI ??
    


####################################################################################################################################################################################################################################

# This is where you should write your code to do things during the initialization delay
# This function should not return anything, but should be used for a short preprocessing
# This function takes as parameters the dimensions and map of the maze, the time it is allowed for computing, the players locations in the maze and the remaining coins locations
# Make sure to have a safety margin for the time to include processing times (communication etc.)

def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    
    global infini
    global Grand_metagraphe
    global coord_num
    global num_coord
    global chemin
    global mode
    global taille_apetit
    
    
    coord_num, num_coord=numeros(coins+[playerLocation])
    
    # initialisation du Grand_metagraphe
    Grand_metagraphe = metagraphe(coins+[playerLocation], mazeMap, mazeWidth, mazeHeight)
    
    mode = 2
    
    t1=time.time()
    # on trouve des zones interessantes
    zones_interessantes=[]
    for piece in coins:
        caractinteret = interessant(piece, coins)
        if caractinteret[0]:
            zones_interessantes = [caractinteret] + zones_interessantes
    
    # on cree un chemin
    if len(zones_interessantes)>0: # si on a trouve des zones interessantes
        
        # on trouve la plus proche
        
        num_playerLocation = coord_num[playerLocation]
        prochaine_piece = zones_interessantes[0][2]
        zone = zones_interessantes[0]
        num_prochaine_piece = coord_num[prochaine_piece]
    
        for caractinteret in zones_interessantes:
            
            num_piece_restante = coord_num[caractinteret[2]]
            
            if Grand_metagraphe[num_playerLocation][num_piece_restante][1]<Grand_metagraphe[num_playerLocation][num_prochaine_piece][1]:
                zone = caractinteret
                prochaine_piece = caractinteret[2]
                num_prochaine_piece = coord_num[prochaine_piece]
        
        # on a le chemin pour aller au centre de cette zone
        chemin=Grand_metagraphe[coord_num[playerLocation]][coord_num[prochaine_piece]][0]
        
        # on a le nombre de fois que l'on doit faire le glouton pour ramasser ces pieces (ou dautres)
        nombre_pieces = len(zone[1])
        taille_apetit = nombre_pieces +3
        
    else:
        mode = 1
        prochaine_piece=coins[0]
        for piece_restante in coins:
            if Grand_metagraphe[coord_num[playerLocation]][coord_num[piece_restante]][1]<Grand_metagraphe[coord_num[playerLocation]][coord_num[prochaine_piece]][1]:
                prochaine_piece=piece_restante
        chemin=Grand_metagraphe[coord_num[playerLocation]][coord_num[prochaine_piece]][0]
    
    t2=time.time()
    duree = t2 - t1
    debug("\n" + 'nombre de zones interessantes trouvee = ' + str(len(zones_interessantes)) + "\n"
               + 'TEMPS POUR LES TROUVER = ' + str(duree))
    debug("\n" + 'mode = ' + str(mode))

    debug("\n" + "mazeWidth = " + str(mazeWidth) + "\n"
               + "mazeHeight = " + str(mazeHeight) + "\n"
               + "timeAllowed = " + str(timeAllowed) + "\n"
               + "playerLocation = " + str(playerLocation) + "\n"
               + "opponentLocation = " + str(opponentLocation) + "\n"
               + "coins = " + str(coins))
 

####################################################################################################################################################################################################################################

# This is where you should write your code to determine the next direction
# This function should return one of the directions defined in the CONSTANTS section
# This function takes as parameters the dimensions and map of the maze, the time it is allowed for computing, the players locations in the maze and the remaining coins locations
# Make sure to have a safety margin for the time to include processing times (communication etc.)

def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    global mode
    global chemin
    global Grand_metagraphe
    global taille_apetit
    global Grand_metagraphe
    global coord_num
    global num_coord
    
    if mode == 1: # mode glouton normal enclenche
        
        if len(chemin)>0:
            
            piece = chemin[0]
            if piece_a_attrapper_tj_la(piece, coins):
                position_avant=playerLocation
                position_apres=chemin.pop()
                return direction_a_prendre(position_avant,position_apres)
            
            else:
                debug('Jerry : He stole my coin !!!!!')
                chemin = lost_vite_manger(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins)
                position_avant=playerLocation
                position_apres=chemin.pop()
                return direction_a_prendre(position_avant,position_apres)
            
        else:
            facteurDeRisque = True
            liste_des_pieces = list(coins)
            while facteurDeRisque and len(liste_des_pieces)>=1:
                
                
                prochaine_piece=liste_des_pieces[0]
                for piece_restante in liste_des_pieces:
                    if Grand_metagraphe[coord_num[playerLocation]][coord_num[piece_restante]][1]<Grand_metagraphe[coord_num[playerLocation]][coord_num[prochaine_piece]][1]:
                        prochaine_piece=piece_restante
                
                
                facteurDeRisque = risk(prochaine_piece, mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, liste_des_pieces)
                if facteurDeRisque==True:
                    debug('Jerry : abandon')
                
                liste_des_pieces.remove(prochaine_piece)
            
            
                chemin=Grand_metagraphe[coord_num[playerLocation]][coord_num[prochaine_piece]][0]
                
            position_avant=playerLocation
            position_apres=chemin.pop()
            return direction_a_prendre(position_avant,position_apres)
    
    ###################################################################################################################################
    if mode == 2: # mode zones interessantes enclenche
        
        if len(chemin)>0:
            
            piece = chemin[0]
            if piece_a_attrapper_tj_la(piece, coins):
                
                position_avant=playerLocation
                position_apres=chemin.pop()
                return direction_a_prendre(position_avant,position_apres)
            
            else:
                chemin = lost_vite_manger(mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins)
                position_avant=playerLocation
                position_apres=chemin.pop()
                return direction_a_prendre(position_avant,position_apres)
        
        
        else:
            
            taille_apetit = taille_apetit - 1
            if taille_apetit < 0: # alors on cherche une nouvelle zone
                
                t1=time.time()
                
                zones_interessantes=[]
                for piece in coins:
                    caractinteret = interessant(piece, coins)
                    if caractinteret[0]:
                        zones_interessantes = [caractinteret] + zones_interessantes
                    
                if len(zones_interessantes)>0:
                    
                    num_playerLocation = coord_num[playerLocation]
                    prochaine_piece = zones_interessantes[0][2]
                    zone = zones_interessantes[0]
                    num_prochaine_piece = coord_num[prochaine_piece]
                    
                    for caractinteret in zones_interessantes:
                        num_piece_restante = coord_num[caractinteret[2]]
                        
                        if Grand_metagraphe[num_playerLocation][num_piece_restante][1]<Grand_metagraphe[num_playerLocation][num_prochaine_piece][1]:
                            zone = caractinteret
                            prochaine_piece = caractinteret[2]
                            num_prochaine_piece = coord_num[prochaine_piece]
                        
                    chemin=Grand_metagraphe[coord_num[playerLocation]][coord_num[prochaine_piece]][0]
                    # on a le nombre de fois que l'on doit faire le glouton pour ramasser ces pieces (ou dautres)
                    nombre_pieces = len(zone[1])
                    taille_apetit = nombre_pieces +3
                    
                    t2=time.time()
                    duree = t2 - t1
                    debug("\n" + 'nombre de zones interessantes trouvee = ' + str(len(zones_interessantes)) + "\n"
                                   + 'TEMPS POUR LES TROUVER = ' + str(duree))
                    
                else:
                    mode=1
                    prochaine_piece=coins[0]
                    for piece_restante in coins:
                        if Grand_metagraphe[coord_num[playerLocation]][coord_num[piece_restante]][1]<Grand_metagraphe[coord_num[playerLocation]][coord_num[prochaine_piece]][1]:
                            prochaine_piece=piece_restante
                    chemin=Grand_metagraphe[coord_num[playerLocation]][coord_num[prochaine_piece]][0]
                
                position_avant=playerLocation
                position_apres=chemin.pop()
                return direction_a_prendre(position_avant,position_apres)
            else: # on fait le glouton encore une fois, sans changer de mode
                prochaine_piece=coins[0]
                for piece_restante in coins:
                    if Grand_metagraphe[coord_num[playerLocation]][coord_num[piece_restante]][1]<Grand_metagraphe[coord_num[playerLocation]][coord_num[prochaine_piece]][1]:
                        prochaine_piece=piece_restante
                chemin=Grand_metagraphe[coord_num[playerLocation]][coord_num[prochaine_piece]][0]
                
                position_avant=playerLocation
                position_apres=chemin.pop()
                return direction_a_prendre(position_avant,position_apres)

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
