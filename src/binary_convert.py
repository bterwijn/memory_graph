import memory_graph as mg
mg.config.type_to_vertical[list] = False  # horizontal lists

def binary(value: int) -> list[int]:
    if value == 0:
        return []
    quotient, remainder = divmod(value, 2)
    return binary(quotient) + [remainder]

print( binary(100) )
