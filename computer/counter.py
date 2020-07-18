"""Program counter to tell the computer what to do next."""
from .logic import NOT, AND
from .switch import PrimarySecondaryJKFlipFlop

class Counter:

    def __init__(self, nbits):
        self.nbits = nbits
        self.latches = [PrimarySecondaryJKFlipFlop() for _ in range(nbits)]

    def __call__(self, clock=1):
        count = []
        for FlipFlop in self.latches:
            clock, _ = FlipFlop(1, 1, clock)
            count.append(NOT(clock))
        return count


class ProgramCounter(Counter):

    def __init__(self, nbits):
        super().__init__(nbits)

    def __call__(self, write, jump, clock):
        return super().__call__(AND(write, clock))
