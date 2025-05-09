"""Base de Datos SQL - Crear y Borrar Tablas"""

import sqlite3

def crear_tabla():
    """Implementar la funcion crear_tabla, que cree una tabla Persona con:
        - IdPersona: Int() (autoincremental)
        - Nombre: Char(30)
        - FechaNacimiento: Date()
        - DNI: Int()
        - Altura: Int()
    """
    db=sqlite3.connect("db.db")
    cursor = db.cursor()
    cursor.execute('CREATE TABLE Persona (IdPersona INTEGER PRIMARY KEY AUTOINCREMENT, Nombre CHAR(30), FechaNacimiento DATE, DNI INTEGER , Altura INTEGER)')
    db.commit()
    db.close()


def borrar_tabla():
    """Implementar la funcion borrar_tabla, que borra la tabla creada 
    anteriormente."""
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute("""DROP TABLE IF EXISTS Persona""")
    db.commit()
    db.close()

# NO MODIFICAR - INICIO
def reset_tabla(func):
    def func_wrapper():
        borrar_tabla()
        crear_tabla()
        func()
        borrar_tabla()
    return func_wrapper
# NO MODIFICAR - FIN