from queue import PriorityQueue
import copy

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

    # since PriorityQueue does not allow
    # iterating over the queue without
    # emptying it, PriorityQ makes a copy
    # of the queue and then proceeds with 
    # the iteration
    def __iter__(self):
        tmpQueue = self.queue[:] #copy.deepcopy(self.queue)
        self.backupQueue = tmpQueue
        return self
    
    def __next__(self):
        if self.empty():
            self.queue = self.backupQueue # restore original queue
            del self.backupQueue
            raise StopIteration()
        else:
            return self.get()