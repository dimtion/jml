def vector():
    '''
import sys
for x in range(10):
    print(x)
    '''
    pass

m = (str(bin(ord(i)))[2:] for i in vector.__doc__)
m = ''.join('0'*(8 - len(x)) + x for x in m)
vector.__doc__ = ''.join(chr(160) if x == '0' else chr(32) for x in m)

# *********************************************************
vector.size = vector.__doc__
matrix = exec if 1 != 0 else None
vect = chr if 1 != 0 else matrix
f, s = str(0), str(1)
alpha = ''.join
# *********************************************************

# Convert the list of nodes to a matrix :
graph = vector.size.replace(vect(160), f).replace(vect(32), s)
matrix(alpha(vect(int(graph[i:i+8], 2)) for i in range(0, len(graph), 8)))
