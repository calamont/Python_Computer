"""The functions to allow the computer to compute."""
from .logic import AND, OR, XOR, NOT

def half_adder(A, B):
    sum = XOR(A, B)
    carry = AND(A, B)
    return sum, carry

def full_adder(A, B, carry_in=0):
    sum, carry = half_adder(A, B)
    sum_out = XOR(sum, carry_in)
    carry_out = AND(sum, carry_in)
    carry_out = OR(carry, carry_out)
    return sum_out, carry_out

# TODO: Add in tri-state logic to prevent this going out on the bus
def nbit_full_adder(A, B, n_bits=8, subtract=0):
    # TODO: Include error checking for len(A) == len(B) == n_bits
    B = twos_complement(B, enable=subtract)
    carry = subtract
    total = []
    for a, b in zip(reversed(A), reversed(B)):
        sum, carry = full_adder(a, b, carry)
        total.insert(0, sum)  # insert bits at index 0 not end of list
    overflow = AND(carry, NOT(subtract))
    if overflow:
        raise Exception("Overflow error!")
    return total

def twos_complement(input, enable=0):
    inverted_input = []
    for bit in input:
        inverted_input.append(XOR(bit, enable))
    return inverted_input

