"""Various switches that can be built using our logic gates."""
from logic import AND, OR, NOT, NOR

class DLatch(SRLatch):

    def __call__(self, input=0, enable=0):
        set_val = AND(input, enable)
        reset_val = AND(NOT(input), enable)
        return super().__call__(set_val, reset_val)
        
        
class SRLatch:

    def __init__(self): 
        self.Q = 1
        self.inv_Q = 0

    def __call__(self, set_val=0, reset_val=0):
        # TODO: create and raise InvalidStateError if set_val and reset_val
        # set to 1
        
        if reset_val:
            self.Q = NOR(reset_val, self.inv_Q)
            self.inv_Q = NOR(set_val, self.Q)
        if set_val:
            self.inv_Q = NOR(set_val, self.Q)
            self.Q = NOR(reset_val, self.inv_Q)

        return self.Q, self.inv_Q


class OneBitRegister(DLatch):

    def __init__(self): 
        self.Q = 0
        self.inv_Q = 1

    def __call__(self, input=0, load=0, clock=0, enable=0):
        inv_load = NOT(load)
        D_input1 = AND(self.Q, inv_load)
        D_input2 = AND(load, input)
        D_input = OR(D_input1, D_input2)
        output =  super().__call__(D_input, clock)[0]
        return self.tri_state_logic(input, output, enable)

    @staticmethod
    def tri_state_logic(input, output, enable):
        if enable:
            return output
        return input


class NBitRegister:

    def __init__(self, n_bits):
        self.n_bits = n_bits
        self.bits = [OneBitRegister() for _ in range(self.n_bits)]

    def __call__(self, input=None, load=0, clock=0, enable=0):
        if input is None:
            input = [0] * self.n_bits

        output = []
        for bit, i in zip(self.bits, input):
            output.append(bit(i, load, clock, enable))
        return output
