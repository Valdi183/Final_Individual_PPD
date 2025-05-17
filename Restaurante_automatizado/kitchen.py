"""
En este script, se reciben los pedidos de la cola donde se almacenan para simular su preparación, utilizando hilos (cada cdinerom es un hilo)
que trabajan simultáneamente (utilizan los mismos recursos).
"""

import threading
import time
import queue
import settings
import performance

order_q = queue.Queue()
perf = performance.PerformanceTracker()
lock = threading.Lock()

# Con esta función, simulo el procedimiento que realiza cada camarero
def cook_worker(cid: int):
    while True:
        try:
            (order, price), t0 = order_q.get(timeout=settings.ORDER_TIMEOUT)
        except queue.Empty:
            break
        print(f"Cook{cid} preparando {order}")
        time.sleep(3.2)                         # simula el tiempo de cocción (uno no realista para que el programa vaya rápido)
        with lock:
            perf.record_order(time.time() - t0, price)
        print(f"Cook{cid} listo: {order}")
        order_q.task_done()

# Se crean los hilos 
def run_kitchen():
    threads = [threading.Thread(target=cook_worker, args=(i+1,), daemon=True)
               for i in range(settings.NUM_COOKS)]
    for th in threads: th.start()
    for th in threads: th.join()
    perf.print_summary()
