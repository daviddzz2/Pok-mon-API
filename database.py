import sqlite3
import requests
import time
from memory_profiler import profile

@profile
# Función para obtener datos de la API
def obtener_datos(nombre):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        tipo = datos['types'][0]['type']['name']
        vida = datos['stats'][0]['base_stat']
        ataque = datos['stats'][1]['base_stat']
        defensa = datos['stats'][2]['base_stat']
        velocidad = datos['stats'][5]['base_stat']
        return (nombre, tipo, vida, ataque, defensa, velocidad)
    else:
        return None

# Conexión a la base de datos SQLite3
conexion = sqlite3.connect('pokemon.db')
cursor = conexion.cursor()

# Crear la tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS pokemons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    vida INTEGER NOT NULL,
    ataque INTEGER NOT NULL,
    defensa INTEGER NOT NULL,
    velocidad INTEGER NOT NULL
)
''')
conexion.commit()

# Obtener y guardar datos de la API
nombres_pokemon = ['pikachu', 'bulbasaur', 'charmander', 'squirtle']
for nombre in nombres_pokemon:
    datos = obtener_datos(nombre)
    if datos:
        cursor.execute('''
        INSERT INTO pokemons (nombre, tipo, vida, ataque, defensa, velocidad)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', datos)
conexion.commit()

# Consumir datos desde la base de datos
print("Datos desde la base de datos:")
cursor.execute('SELECT * FROM pokemons')
for fila in cursor.fetchall():
    print(fila)

# Modificar datos con input
pokemon_id = int(input("Introduce el ID del Pokémon que quieres modificar: "))
nuevo_nombre = input("Introduce el nuevo nombre: ")
cursor.execute('''
UPDATE pokemons
SET nombre = ?
WHERE id = ?
''', (nuevo_nombre, pokemon_id))
conexion.commit()

# Comparar eficiencia entre API y base de datos
print("\nComparando eficiencia...")
inicio_api = time.time()
for nombre in nombres_pokemon:
    obtener_datos(nombre)
fin_api = time.time()

inicio_db = time.time()
cursor.execute('SELECT * FROM pokemons')
for fila in cursor.fetchall():
    pass
fin_db = time.time()

print(f"Tiempo iterando desde la API: {fin_api - inicio_api:.4f} segundos")
print(f"Tiempo iterando desde la base de datos: {fin_db - inicio_db:.4f} segundos")

# Cerrar la conexión
conexion.close()
