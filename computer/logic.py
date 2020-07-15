"""The second most basic components of our computer, the logic gates!"""

from .transistor import transistor, NMOS_transistor, PMOS_transistor

# TODO: Reimplement all the logic gates using NMOS and PMOS transistors.

# def AND(A, B, source=1):
#     source, out1 = transistor(A, source=source)
#     source, out2 = transistor(B, source=out1)
#     return out2

def AND(A, B, source=1):
    A, source, out1 = transistor(1, source=1, drain=A)
    B, source, out2 = transistor(1, source=B, drain=source)
    return source

def multi_AND(*input):
    out = 1
    for i in input:
        out = AND(i, out)
    return out

# def OR(A, B, source=1):
#     source, out1 = transistor(A)
#     source, out2 = transistor(B)
#     if out1:
#         return out1
#     return out2 

def OR(A, B, source=1):
    A, source, out1 = transistor(1, source=1, drain=A)
    B, source, out2 = transistor(1, source=1, drain=B)
    if out1:
        return out1
    return out2 

def XOR(A, B, source=1):
    out1 = OR(A, B, source=source)
    out2 = NAND(A, B, source=source)
    return AND(out1, out2, source=source)

def NAND(A, B, source=1):
    B, out1, out2 = transistor(B, source=1, drain=0)
    A, source, out1 = transistor(A, source=source, drain=out1)
    return source

def NOR(A, B, source=1):
    A, source, out1 = transistor(A, source=source, drain=0)
    B, source, out2 = transistor(B, source=source, drain=0)
    return source

def NOT(A, source=1):
    A, source, drain = transistor(A, source=source, drain=0)
    return source

def tri_state(input, enable, output):
    """Tri-state logic.If enable is HIGH then output = input,
    else output = output.
    """
    NMOS_gate = NOR(input, NOT(enable))
    _, output, _ = NMOS_transistor(NMOS_gate, output, 0)
    PMOS_gate = NAND(input, enable)
    *_, output = PMOS_transistor(PMOS_gate, 1, output)
    return output
