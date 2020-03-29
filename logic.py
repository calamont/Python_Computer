"""The second most basic components of our computer, the logic gates!"""

from transistor import transistor

def AND(A, B, source=1):
    source, out1 = transistor(A, source=source)
    source, out2 = transistor(B, source=out1)
    return out2

def OR(A, B, source=1):
    source, out1 = transistor(A)
    source, out2 = transistor(B)
    if out1:
        return out1
    return out2 

def XOR(A, B, source=1):
    out1 = OR(A, B, source=source)
    out2 = NAND(A, B, source=source)
    return AND(out1, out2, source=source)

def NAND(A, B, source=1):
    out1, out2 = transistor(B, source=1, drain=0)
    source, out1 = transistor(A, source=source, drain=out1)
    return source

def NOR(A, B, source=1):
    source, out1 = transistor(A, source=source, drain=0)
    source, out2 = transistor(B, source=source, drain=0)
    return source

def NOT(A, source=1):
    source, drain = transistor(A, source=source, drain=0)
    return source
