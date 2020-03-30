"""Various switches that can be built using our logic gates."""
from logic import NOR

def D_latch():
    pass

def D_flip_flop():
    pass

class SRLatch:

    def __init__(self): 
        self._Q = 1
        self._inv_Q = 0

    def __call__(self, set_val=0, reset_val=0):
        # TODO: create and raise InvalidStateError if set_val and reset_val
        # set to 1
        
        if set_val:
            self._Q = NOR(set_val, self._inv_Q)
            self._inv_Q = NOR(reset_val, self._Q)
        if reset_val:
            self._inv_Q = NOR(reset_val, self._Q)
            self._Q = NOR(set_val, self._inv_Q)

        return self._Q, self._inv_Q

