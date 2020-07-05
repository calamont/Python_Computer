"""The most basic component of our computer, the transistor!"""

# def transistor(gate, source=1, drain=1):
#     if source:
#         if drain == 0:  
#             # Pull down source potential if shorted to LO
#             source = source - gate
#             return source, drain
#         return source, gate 
#     return 0, 0

def transistor(gate, source=1, drain=1):
    if gate==1:
        if drain == 0:
            source = drain
        drain = source
    return gate, source, drain

def NMOS_transistor(gate, source, drain):
    if gate==1:
        if drain == 0:
            source = drain
        drain = source
    return gate, source, drain

def PMOS_transistor(gate, source, drain):
    if gate==0:
        if source == 1:
            drain = source
        source = drain
    return gate, source, drain
