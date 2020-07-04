"""The static RAM for the computer."""
from .bus import BUS
from .logic import AND, NOT
from .switch import NBitRegister


def two_bit_decoder(input):
    """A 2 bit address decoder. This is less flexible but more readable."""
    inv_input = [NOT(i) for i in input]
    output = [
        AND(inv_input[0], inv_input[1]),
        AND(inv_input[0], input[1]),
        AND(input[0], inv_input[1]),
        AND(input[0], input[1]),
    ]
    return output


def nbit_decoder(input, idx=0, address=None, results=None):
    """Recurively decodes address of any length."""
    if address is None:
        address = [None for _ in input]
    if results is None:
        results = []
    for i in [NOT(input[idx]), input[idx]]:
        address[idx] = i
        try:
            nbit_decoder(input, idx=idx + 1, address=address, results=results)
        except:  # TODO: what type of exception are you expecting?
            results.append(_many_AND(address))
    return results


def _many_AND(input):
    out = 1
    for i in input:
        out = AND(i, out)
    return out


class RAM:  # Get name of sub unit of RAM this is actually called.
    def __init__(self, n_bits):
        self.n_bits = n_bits
        self.memory = [[[NBitRegister(1) for _ in range(n_bits//2)] for _ in range(n_bits//2)]
                       for _ in range(n_bits)]

    def __call__(self, row_addr, col_addr, read=0, write=0):
        # Maybe pass on the OneBitRegister and actually hook this up as an matrix of switches
        # TODO: Whats happening with the data? How does this get written if we use our bus
        #       to transfer the address? Is there a temporary register that is used to hold
        #       this information?
        for i in range(self.n_bits):
            self.bit(0, i, row_addr, col_addr, read, write)

    def bit(self, bit_val, bit_pos, row_addr, col_addr, read=0, write=0):
        for i, row_V in enumerate(row_addr):
            for j, col_V in enumerate(col_addr):
                # Store value at address or read it to the bus. We are looking
                # over every address in memory but only one will have the row
                # and column wire high.
                bit_select = AND(row_V, col_V)
                read = AND(read, bit_select)
                write = AND(write, bit_select)
                self.memory[bit_pos][i][j](bit_val, read, clock, write)
