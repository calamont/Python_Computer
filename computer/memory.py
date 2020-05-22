"""The static RAM for the computer."""
from .bus import BUS
from .logic import AND, NOT
from .switch import OneBitRegister


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
        self.memory = [[OneBitRegister() for _ in range(n_bits)] for _ in range(n_bits)]

    def __call__(self, row_addr, col_addr, read=0, write=0):
        # Maybe pass on the OneBitRegister and actually hook this up as an matrix of switches
        pass
