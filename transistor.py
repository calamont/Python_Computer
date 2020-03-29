"""The most basic component of our computer, the transistor!"""

def transistor(gate, source=1, drain=1):
    if source:
        if drain == 0:  
            # Pull down source potential if shorted to LO
            source = source - gate
            return source, drain
        return source, gate 
    return 0, 0

