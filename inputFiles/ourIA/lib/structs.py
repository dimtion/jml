class StackQueue(list):
    """A class that is either a Stack or a Queue"""

    def __init__(self, isStack=True):
        self.isStack = isStack

    def pop(self):
        if self.isStack:
            return super().pop()
        else:
            return super().pop(0)

class Stack(StackQueue):
    """ A stack"""
    def __init__(self):
        super().__init__(isStack=True)

class Queue(StackQueue):
    """A queue"""
    def __init__(self):
        super().__init__(isStack=False)

class MinStack(dict):
    """The min-stack class"""

    def add(self, elt, weight):
        """Add an element to the MinStack with elt as key and weight as label"""
        self[elt] = weight
    
    def remove(self):
        """Remove and return from the MinStack its minimum element 
        and the key of the minimum element as a tuple"""
        mini = min(j for i,j in self.items())
        key_mini = next(key for key, value in self.items() if value == mini)
        del self[key_mini]
        return key_mini, mini

    def empty(self):
        """Return True if the MinStack is empty, else return False"""
        return len(self) == 0

def filledStack(mazeMap):
    """Return a MinStack of the maze nodes with distances initialized to 'infinity' """
    stack = MinStack()
    for node in mazeMap:
        stack.add(node, float("inf"))
    return stack
