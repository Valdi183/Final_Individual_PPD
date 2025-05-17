"""
El script main, es desde donde se ejecuta el programa. Llamo a los métodos necearios del resto de scripts, para poner en marcha
la simulación del restaurante, con los camareros empezando a tomar las órdenes y los cocineros empezando a procesarlas.
"""

import asyncio
import host
import kitchen
import time
import queue

if __name__ == "__main__":
    order_q = kitchen.order_q         
    start = time.time()
    asyncio.run(host.take_orders(order_q))
    aux = queue.Queue()
    while not order_q.empty():
        o, p = order_q.get_nowait()
        aux.put(((o, p), time.time()))
    kitchen.order_q = aux
    kitchen.run_kitchen()
    print(f"  Duración total: {time.time()-start:.1f}s")
