from queue import PriorityQueue

# PriorityQueue is missing a few things, 
# which will be implemented by PriorityQ
class PriorityQ(PriorityQueue):
    def peek(self):
        # PriorityQueue is implemented with a heap
        # that is stored in the "queue" list. The 1st
        # element of the list is guaranteed to be the
        # highest-priority one
        # (but the rest of the list is not sorted icyww)
        return self.queue[0]


    # this iterates over the priority queue
    # RANDOMLY, meaning that the order in which
    # the elements are visisted is not dependent
    # on their priority
    def __iter__(self):
        return iter(self.queue)