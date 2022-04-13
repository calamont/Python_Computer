"""Program counter to tell the computer what to do next."""
from .logic import NOT, AND, NAND, NOR, OR
from .switch import PrimarySecondaryJKFlipFlop

# class Counter:

#     def __init__(self, nbits):
#         self.nbits = nbits
#         self.latches = [PrimarySecondaryJKFlipFlop() for _ in range(nbits)]

#     def __call__(self, clock=1):
#         count = []
#         for FlipFlop in self.latches:
#             clock, _ = FlipFlop(1, 1, clock)
#             count.append(NOT(clock))
#         return count


class Counter:
    """Synchronous n-bit counter"""
    def __init__(self, nbits):
        self.nbits = nbits
        self.latches = [PrimarySecondaryJKFlipFlop() for _ in range(nbits)]

    def __call__(self, clock=1):
        output = []
        input = 1
        for FlipFlop in self.latches:
            Q, _ = FlipFlop(input, input, clock)
            output.append(NOT(Q))
            input = AND(Q, input)
        return output


class ProgramCounterLoad:
    """Program counter with load functionality"""

    def __init__(self, nbits):
        self.nbits = nbits
        self.latches = [PrimarySecondaryJKFlipFlop() for _ in range(nbits)]

    def __call__(self, clock=1, load=0, clear=0, data=None):
        if data is None:
            data = [0 for _ in range(self.nbits)]

        output = []
        input = 1
        for FlipFlop, d in zip(self.latches, data):
            J = OR(AND(input, NOT(load)), AND(NOT(d), load))
            K = OR(AND(input, NOT(load)), AND(d, load))
            Q, _ = FlipFlop(J, K, clock)
            output.append(NOT(Q))
            input = AND(Q, input)
        return output


class ProgramCounterClear:
    """Program counter with clear functionality"""

    def __init__(self, nbits):
        self.nbits = nbits
        self.latches = [PrimarySecondaryJKFlipFlop() for _ in range(nbits)]

    def __call__(self, clock=1, clear=0):
        output = []
        input = 1
        for FlipFlop in self.latches:
            # NAND of the clock and clear should input a 0 to the J input when
            # clear and the clock is high, given an output of 0.
            Q, _ = FlipFlop(OR(clear, OR(input, clear)),
                            NOR(clear, NOR(input, clear)), clock)
            output.append(NOT(Q))
            input = AND(Q, input)
        return output


# class ProgramCounter(SynchronousCounter):

#     def __init__(self, nbits):
#         super().__init__(nbits)

#     def __call__(self, write, jump, clock, clear=0):
#         # Try to add clear functionality next
#         return super().__call__(AND(write, clock))
