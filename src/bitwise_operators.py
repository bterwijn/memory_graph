import memory_graph as mg

class Bits(dict):
   """ Dictionary subclass that we will configure to show binary representations. """

def twos_complement(x: int, bits: int) -> str:
    """Return the two's complement bit string of x in `bits` bits."""
    mask = (1 << bits) - 1
    return format(x & mask, f"0{bits}b")

# configure memory_graph to show binary representations of values of type Bits
mg.config.type_to_node[Bits] = lambda x : mg.Node_Table(x,
   [ ["expression", "decimal", "bin(expression)", "16bit two's complement"] ] +
   [ [k,f'{v:>10}',f'{bin(v):>19}', twos_complement(v,16) ] for k,v in x.items()] )
mg.config.type_to_slicer[Bits] = (mg.Slicer(), mg.Slicer())  # no slicing
mg.config.type_to_color[Bits] = 'gold'
mg.config.fontname = 'Courier' # monospace font

bits = Bits()

# now add some some variables and expressions
bits['a'] = 1
bits['b'] = 32
bits['c'] = 127
bits['a << 3'] = bits['a'] << 3         # bit shift left by 3
bits['b >> 3'] = bits['b'] >> 3         # bit shift right by 3
bits['a | b']  = bits['a'] | bits['b']  # bitwise or
bits['b & c']  = bits['b'] & bits['c']  # bitwise and
bits['b ^ c']  = bits['b'] ^ bits['c']  # bitwise exclusive or

# negative numbers, inverse, and two's complement
bits['d'] = 240
bits['e'] = -240
bits['f'] = -241                        # -(d+1)
bits['~d'] = ~ bits['d']                # inverse -(x+1)
bits['~e'] = ~ bits['e']                # inverse -(x+1)
bits['~f'] = ~ bits['f']                # inverse -(x+1)
