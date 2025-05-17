import threading
import time
from queue import Queue
from ordenes import MENU_ITEMS
from procesado import PerformanceTracker

order_queue = Queue()
performance = PerformanceTracker()
lock = threading.Lock()

def get_user_orders():
    mesas = int(input("¿Cuántas mesas están reservadas hoy? "))
    pedidos = []
    print("\nMenú disponible:")
    for item in MENU_ITEMS:
        print(f" - {item}")
    print("\n")

    for mesa in range(1, mesas + 1):
        print(f"🪑 Mesa {mesa}: ¿Qué van a pedir? (separa múltiples items con coma)")
        entrada = input(">> ")
        ordenes = [item.strip() for item in entrada.split(",") if item.strip()]
        for orden in ordenes:
            pedidos.append((f"Mesa {mesa} - {orden}", time.time()))
    return pedidos

def cook(cook_id):
    while True:
        try:
            order, timestamp = order_queue.get(timeout=5)
        except:
            break
        print(f"    [👨‍🍳 Cocinero {cook_id}] Cocinando {order}")
        time.sleep(1)  # Simula tiempo de cocina
        with lock:
            performance.record_order(time.time() - timestamp)
        print(f"    [👨‍🍳 Cocinero {cook_id}] Pedido listo: {order}")
        order_queue.task_done()

def start_process():
    pedidos = get_user_orders()
    num_cooks = 3

    print("\n📦 Enviando pedidos a la cocina...\n")
    for pedido in pedidos:
        order_queue.put(pedido)

    threads = []
    for i in range(num_cooks):
        t = threading.Thread(target=cook, args=(i+1,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\n✅ Todos los pedidos han sido procesados.")
    performance.print_summary()
