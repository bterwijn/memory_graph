import memory_graph as mg
mg.config.type_to_vertical[list] = False  # horizontal lists

def binary(value: int) -> list[int]:
    mg.render(mg.stack(), 'binary.png', numbered=True)
    if value == 0:
        return []
    quotient, remainder = divmod(value, 2)
    result = binary(quotient) + [remainder]
    mg.render(mg.stack(), 'binary.png', numbered=True)
    return result

print( binary(100) )
