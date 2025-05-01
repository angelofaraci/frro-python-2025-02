"""Expresiones Booleanas."""


def es_vocal_if(letra: str) -> bool:
    if letra.lower() == 'a':
        return True
    elif letra.lower() == 'e':
        return True
    elif letra.lower() == 'i':
        return True
    elif letra.lower() == 'o':
        return True
    elif letra.lower() == 'u':
        return True
    return False


# NO MODIFICAR - INICIO
assert es_vocal_if("a")
assert not es_vocal_if("b")
assert es_vocal_if("A")
# NO MODIFICAR - FIN


###############################################################################


def es_vocal_if_in(letra: str) -> bool:
    vocales = ['a','e','i','o','u']
    if letra.lower() in vocales:
        return True
    return False

# NO MODIFICAR - INICIO
assert es_vocal_if_in("a")
assert not es_vocal_if_in("b")
assert es_vocal_if_in("A")
# NO MODIFICAR - FIN


###############################################################################


def es_vocal_in(letra: str) -> bool:
    """Re-escribir utilizando el operador IN pero sin utilizar IF."""
    pass # Completar
    vocales = ['a','e','i','o','u']
    return letra.lower() in vocales

# NO MODIFICAR - INICIO
assert es_vocal_in("a")
assert not es_vocal_in("b")
assert es_vocal_in("A")
# NO MODIFICAR - FIN
