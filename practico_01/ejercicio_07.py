"""Slicing."""


def es_palindromo(palabra: str) -> bool:
    """Toma un string y devuelve un booleano en base a si se lee igual al
    derecho y al revés.

    Restricción: No utilizar bucles - Usar Slices de listas.
    Referencia: https://docs.python.org/3/tutorial/introduction.html#lists
    """
    if(palabra == ""):
        return True
    if(len(palabra)%2!=0):
        centro = len(palabra)//2
        palabra = palabra[:centro] + palabra[centro+1:]

    mitad1 = palabra[0:len(palabra)//2]
    mitad2 = palabra[len(palabra)//2:len(palabra)]
    mitad2 = mitad2[::-1]
    if(mitad1 == mitad2):
        return True
    return False


# NO MODIFICAR - INICIO
assert not es_palindromo("amor")
assert es_palindromo("radar")
assert es_palindromo("")
# NO MODIFICAR - FIN


###############################################################################


def mitad(palabra: str) -> str:

    if(len(palabra)%2!=0):
        mitad = palabra[0:len(palabra)//2+1]
    else:
        mitad = palabra[0:len(palabra)//2]
        

    return mitad


# NO MODIFICAR - INICIO
assert mitad("hello") == "hel"
assert mitad("Moon") == "Mo"
assert mitad("") == ""
# NO MODIFICAR - FIN
