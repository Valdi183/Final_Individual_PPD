"""
Este script contiene un cliente asíncrono para descargar y combinar Comidas (TheMealDB), y Bebidas (TheCocktailDB).
Si settings.USE_MOCK_API es True (en este caso, en settings está definido como False pero se puede cambiar a True 
para probar esta versión), se genera un menú simulado sin necesidad de conexión a APIs. En este script, consigo 
optimizar tiempos de espera en llamadas a la API aprovechando la asincronía. Es un claro ejemplo de concurrencia,
ya que se realizan distintas tareas indepenientes a la vez, aprovecando los tiempos de espera de respuesta de la red
para que el programa siga ejecutandose.
"""

import asyncio
import time
import random
import aiohttp
import settings

# Utilizo 
_cache = {"ts": 0, "data": []}          

# Menú fijo (sencillo), con simulación de latencia de red para utilizar asincronía
async def _mock_menu():
    await asyncio.sleep(random.uniform(0.2, 0.6))
    return [
        {"name": "Pizza Margarita", "price": 8.5, "cat": "plato"},
        {"name": "Lasagna",          "price": 9.8, "cat": "plato"},
        {"name": "Agua",             "price": 1.5, "cat": "bebida"},
        {"name": "Cerveza",          "price": 3.0, "cat": "bebida"},
        {"name": "Tiramisú",         "price": 4.2, "cat": "postre"},
    ]

# Devuelve los datos de cada plato, con la información de la API (comidas) (los precios los pongo de forma random porque no aparecen en la API)
def _parse_mealdb(resp_json):
    meals = resp_json.get("meals") or []
    parsed = []
    for m in meals:
        name = m.get("strMeal")
        if name:
            parsed.append(
                {"name": name, "price": round(random.uniform(7, 19), 2), "cat": "plato"}
            )
    return parsed

# Como la función anterior pero con las bebidas
def _parse_cocktaildb(resp_json):
    drinks = resp_json.get("drinks") or []
    parsed = []
    for d in drinks:
        name = d.get("strDrink")
        if name:
            parsed.append(
                {"name": name, "price": round(random.uniform(2, 5), 2), "cat": "bebida"}
            )
    return parsed

# Realiza peticiones a la web de forma asíncrona 
async def _fetch_json(session, url):
    try:
        async with session.get(url, timeout=10) as resp:
            return await resp.json()
    except Exception as exc:                               # El parse devuelve un diccionario vacío en caso de error al llamar a la API para evitar cerrar el programa
        print(f"Error al contactar {url}: {exc}")
        return {}

# Descarga de los menus para el usuario
async def _download_real_menu():
    async with aiohttp.ClientSession() as sess:
        meal_task   = _fetch_json(sess, settings.MENU_API_URL)
        drink_task  = _fetch_json(sess, settings.DRINKS_API_URL)
        meal_json, drink_json = await asyncio.gather(meal_task, drink_task) # Descarga de ambas en paralelo (distintas APIs)

    meals  = _parse_mealdb(meal_json)
    drinks = _parse_cocktaildb(drink_json)
    return meals + drinks

async def fetch_menu():
    now = time.time()

    if now - _cache["ts"] < settings.MENU_CACHE_TTL and _cache["data"]:
        return _cache["data"]                     

    # Descarga de los menus, dependiendo de si se está conectando a las APIs o no
    if getattr(settings, "USE_MOCK_API", False) or settings.MENU_API_URL == "mock":
        data = await _mock_menu()
    else:
        data = await _download_real_menu()

    # Guarda el cahcé y lo devuelve
    _cache.update(ts=now, data=data)
    return data
