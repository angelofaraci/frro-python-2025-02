"""Magic Methods"""

from __future__ import annotations
from typing import List


# NO MODIFICAR - INICIO
class Article:
    """Agregar los métodos que sean necesarios para que los test funcionen.
    Hint: los métodos necesarios son todos magic methods
    Referencia: https://docs.python.org/3/reference/datamodel.html#basic-customization
    """


    # NO MODIFICAR - FIN
    def __init__(self, name: str) -> None:
        self.name = name
    def __lt__(self, other: Article) -> bool:
        if not isinstance(other, Article):
            return NotImplemented
        return self.name < other.name
    def __str__(self) -> str:
        return self.name.capitalize()
    def __repr__(self) -> str:
        return f"Article('{self.name}')"
    def __eq__(self, other: Article) -> bool:
        if not isinstance(other, Article):
            return False
        return self.name == other.name


# NO MODIFICAR - INICIO
class ShoppingCart:
    """Agregar los métodos que sean necesarios para que los test funcionen.
    Hint: los métodos necesarios son todos magic methods
    Referencia: https://docs.python.org/3/reference/datamodel.html#basic-customization
    """

    def __init__(self, articles: List[Article] = None) -> None:
        if articles is None:
            self.articles = []
        else:
            self.articles = articles

    def add(self, article: Article) -> ShoppingCart:
        self.articles.append(article)
        return self

    def remove(self, remove_article: Article) -> ShoppingCart:
        new_articles = []

        for article in self.articles:
            if article != remove_article:
                new_articles.append(article)

        self.articles = new_articles

        return self
    

    

    # NO MODIFICAR - FIN
    
    def __str__(self) -> str:
        return str([str(article) for article in self.articles])
    def __repr__(self) -> str:
            return f"ShoppingCart({self.articles})"
        
    def __eq__(self, other: ShoppingCart) -> bool:
        if not isinstance(other, ShoppingCart):
            return False
        return sorted(self.articles) == sorted(other.articles)
    def __add__(self, other: ShoppingCart) -> ShoppingCart:
        if not isinstance(other, ShoppingCart):
            raise TypeError("No se puede sumar un carrito con otro objeto")
        return ShoppingCart(self.articles + other.articles)
    
    # Completar


# NO MODIFICAR - INICIO

manzana = Article("Manzana")
pera = Article("Pera")
tv = Article("Television")

# Test de conversión a String
assert str(ShoppingCart().add(manzana).add(pera)) == "['Manzana', 'Pera']"

# Test de reproducibilidad
carrito = ShoppingCart().add(manzana).add(pera)

assert carrito == eval(repr(carrito))

# Test de igualdad
assert ShoppingCart().add(manzana) == ShoppingCart().add(manzana)

# Test de remover objeto
assert ShoppingCart().add(tv).add(pera).remove(tv) == ShoppingCart().add(pera)

# Test de igualdad con distinto orden
assert ShoppingCart().add(tv).add(pera) == ShoppingCart().add(pera).add(tv)

# Test de suma
combinado = ShoppingCart().add(manzana) + ShoppingCart().add(pera)
assert combinado == ShoppingCart().add(manzana).add(pera)

# NO MODIFICAR - FIN
