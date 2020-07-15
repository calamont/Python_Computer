"""Various switches that can be built using our logic gates."""
from . import bus
from .logic import AND, OR, NOT, NOR, multi_AND, NAND

class SRLatch:

    def __init__(self): 
        self.Q = 1
        self.inv_Q = 0

    def __call__(self, set_val=0, reset_val=0):

        prev_Q = self.Q
        prev_inv_Q = self.inv_Q

        self.Q = NOR(reset_val, self.inv_Q)
        self.inv_Q = NOR(set_val, self.Q)

        if (prev_Q != self.Q) or (prev_inv_Q != self.inv_Q):
            self.__call__(set_val, reset_val)
        return self.Q, self.inv_Q

class NAND_SRLatch:

    def __init__(self): 
        self.Q = 1
        self.inv_Q = 0

    def __call__(self, set_val=0, reset_val=0):

        prev_Q = self.Q
        prev_inv_Q = self.inv_Q

        self.Q = NAND(set_val, self.inv_Q)
        self.inv_Q = NAND(reset_val, self.Q)

        if (prev_Q != self.Q) or (prev_inv_Q != self.inv_Q):
            self.__call__(set_val, reset_val)
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


class JKFlipFlop:
    """Simple JK flip-flop that will continously toggle if set and reset are 1"""
    def __init__(self): 
        self.Q = 1
        self.inv_Q = 0

    def __call__(self, set_val=0, reset_val=0, clock=0):

        _set_val = multi_AND(set_val, clock, self.inv_Q)
        _reset_val = multi_AND(reset_val, clock, self.Q)

        prev_Q = self.Q
        prev_inv_Q = self.inv_Q

        self.Q = NOR(_reset_val, self.inv_Q)
        self.inv_Q = NOR(_set_val, self.Q)

        if (prev_Q != self.Q) or (prev_inv_Q != self.inv_Q):
            self.__call__(set_val, reset_val, clock)
        return self.Q, self.inv_Q


class NAND_JKFlipFlop:
    """Simple JK flip-flop that will continously toggle if set and reset are 1"""
    def __init__(self): 
        self.Q = 1
        self.inv_Q = 0
        self.latch = NAND_SRLatch()

    def __call__(self, set_val=0, reset_val=0, clock=0):

        prev_Q = self.latch.Q
        prev_inv_Q = self.latch.inv_Q

        _set_val = NAND(clock, AND(set_val, self.latch.inv_Q))
        _reset_val = NAND(clock, AND(reset_val, self.latch.Q))
        Q, inv_Q = self.latch(_set_val, _reset_val)

        if (prev_Q != self.latch.Q) or (prev_inv_Q != self.latch.inv_Q):
            self.__call__(set_val, reset_val, clock)
        return self.latch.Q, self.latch.inv_Q

class PrimarySecondaryJKFlipFlop:
    """Primary-secedonary JK flip flop arrangement used to prevent racing."""

    def __init__(self): 
        self.Q = 1
        self.inv_Q = 0
        self.primary_latch = NAND_SRLatch()
        self.secondary_latch = NAND_SRLatch()

    def __call__(self, set_val=0, reset_val=0, clock=0):

        prev_Q = self.secondary_latch.Q
        prev_inv_Q = self.secondary_latch.inv_Q

        _set_val = NAND(self.secondary_latch.inv_Q, AND(set_val, clock))
        _reset_val = NAND(self.secondary_latch.Q, AND(reset_val, clock))
        _set_val, _reset_val = self.primary_latch(_set_val, _reset_val)

        # Relicating behaviour of a NAND gate with a NOT(clock) signal by
        # simply inverting the set and reset inputs
        Q, inv_Q = self.secondary_latch(NOT(_set_val), NOT(_reset_val))
        return self.secondary_latch.Q, self.secondary_latch.inv_Q
