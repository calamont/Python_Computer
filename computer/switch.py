"""Various switches that can be built using our logic gates."""
from . import bus
from .logic import AND, OR, NOT, NOR

class SRLatch:

    def __init__(self): 
        self.Q = 1
        self.inv_Q = 0
        self.BUS = BUS

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

class DLatch(SRLatch):

    def __call__(self, input=0, enable=0):
        set_val = AND(input, enable)
        reset_val = AND(NOT(input), enable)
        return super().__call__(set_val, reset_val)

class OneBitRegister(DLatch):

    def __init__(self): 
        self.Q = 0
        self.inv_Q = 1

    def __call__(self, input=0, load=0, clock=0):
        inv_load = NOT(load)
        D_input1 = AND(self.Q, inv_load)
        D_input2 = AND(load, input)
        D_input = OR(D_input1, D_input2)
        return super().__call__(D_input, clock)[0]

class NBitRegister:

    def __init__(self, n_bits):
        self.n_bits = n_bits
        self.bits = [OneBitRegister() for _ in range(self.n_bits)]

    def __call__(self, input=None, load=0, clock=0, enable=0):
        # TODO: `input` is being used for debugging. Change to bus.BUS (actually this may be useful for RAM)
        # TODO: should I have check for enable and load both being 1?
        if input is None:
            input = bus.BUS
        output = []
        for bit, i in zip(self.bits, input):
            output.append(bit(i, load, clock))  # if load=0 it will read stored values
        tri_state_logic(output, enable)  # if enable=1 output stored values to the bus

def tri_state_logic(output, enable):
    # TODO: work out if this is only meant to occur on a clock pulse.
    if enable:
        bus.BUS = output
