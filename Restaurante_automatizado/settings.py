"""
En este script, están definidos los parametros del número de codineros (cada uno actúa como un hilo), el tiempo máximo de espera en la cola y el tiempo que se mantiene el menú
en la memoria cach. Están también definidas las apis que se consultan para realizar los pedidos, una contiene gran cantidad de comidas, y la otra bebidas. También hay opción de 
utilizar un menú local, activando el "mock_menu" con True
"""

NUM_COOKS      = 7   
ORDER_TIMEOUT  = 5      # segundos    
MENU_CACHE_TTL = 1000       # segundos

# APIs
MENU_API_URL = "https://www.themealdb.com/api/json/v1/1/search.php?f=p"
DRINKS_API_URL = "https://www.thecocktaildb.com/api/json/v1/1/search.php?f=b"

USE_MOCK_API = False  # Cambiar a True para utilizar el menú simulado