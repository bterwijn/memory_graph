mg.config.type_to_horizontal[list] = True  # horizontal lists

def binary(value: int) -> list[int]:
    if value == 0:
        return []
    quotient, remainder = divmod(value, 2)
    return binary(quotient) + [remainder]

print( binary(100) )
