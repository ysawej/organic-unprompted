
from typing import Any

class Node:
    def __init__(self, val: Any):
        self.val: Any = val
        self.next: Node = None
    def getnext(self):
        return self.next

class LinkedList:
    def __init__(self):
        self.root = None
        self.last = None

    def add(self, val: Any):
        if not self.root:
            self.root = Node(val)
            self.last = self.root
        else:
            new_node = Node(val)
            self.last.next = new_node
            self.last = new_node


def __main__():
    vs = [5,4,3,1]
    myl = LinkedList()
    for v in vs:
        myl.add(v)
    r = myl.root
    while r != None:
        print (r.val)
        r = r.getnext()
        

if __name__ == '__main__':
    __main__()
