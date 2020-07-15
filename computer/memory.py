"""The static RAM for the computer."""
# from .bus import BUS
from .transistor import transistor
from .logic import AND, NOT, tri_state, multi_AND
from .switch import OneBitRegister, tri_state_logic


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
            results.append(multi_AND(*address))
    return results


class RAM:  # Get name of sub unit of RAM this is actually called.
    def __init__(self, n_bits):
        self.n_bits = n_bits
        # Create n_bit number of arrays of latches for storing data. For a 4 bit computer we would
        # have 4 arrays. The row and columns are addressed with 2 bits, giving 2^2 positions.
        self.memory = [[[OneBitRegister() for _ in range((n_bits//2)**2)]
                         for _ in range((n_bits//2)**2)]
                         for _ in range(n_bits)]

    def __call__(self, data, addr, read=0, write=0, clock=0):
        row_addr = nbit_decoder(addr[:self.n_bits//2])
        col_addr = nbit_decoder(addr[self.n_bits//2:])
        output = []
        for i in range(len(data)):
            output.append(self.bit(data, i, row_addr, col_addr, read, clock, write))

    def bit(self, data, bit_pos, row_addr, col_addr, read=0, clock=0, write=0):
        for i, row_V in enumerate(row_addr):
            for j, col_V in enumerate(col_addr):
                # Store value at address or read it to the bus. We are looking
                # over every address in memory but only one will have the row
                # and column wire high.
                bit_select = AND(row_V, col_V)
                bit_write = AND(write, bit_select)
                bit_read = AND(read, bit_select)
                # If write=1 then write value to latch, otherwise read
                latch_val = self.memory[bit_pos][i][j](data[bit_pos], bit_write, clock)
                # Should only write to data line if read is enabled.
                data[bit_pos] = tri_state(latch_val, bit_read, data[bit_pos])
