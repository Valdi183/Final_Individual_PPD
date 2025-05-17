"""
Este script, simula un camarero que se encarga de mostrar la carta a los clientes y tomar las ordenes
"""

import asyncio
import queue
from menu_api import fetch_menu

def print_menu(menu):
    print("\n  CARTA:")
    for i, itm in enumerate(menu, 1):
        print(f"{i:2}. {itm['name']:<25}  €{itm['price']:.2f}")

async def take_orders(order_q: queue.Queue):
    menu = await fetch_menu()
    print_menu(menu)
    mesas = int(input("\n¿Cuántas reservas hay hoy? "))
    for m in range(1, mesas+1):
        sel = input(f" Mesa {m} – introduce números separados por coma: ")
        idxs = [int(x)-1 for x in sel.split(",") if x.strip().isdigit()]
        for i in idxs:
            item = menu[i]
            order_q.put((f"Mesa {m} - {item['name']}", item['price']))
