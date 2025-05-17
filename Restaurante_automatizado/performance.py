"""
En este script se hace un seguimiento de los pedidos procesados para mostrar después de
todos los pedidos hechos, los ingresos obtenidos, el tiempomedio de ejecución...
y así permie comprobar que se está haciendo bien el uso de concurrencia
"""

class PerformanceTracker:
    def __init__(self):
        self.n = 0
        self.total_time = 0.0
        self.revenue = 0.0
    def record_order(self, dur, price):
        self.n += 1
        self.total_time += dur
        self.revenue += price
    def print_summary(self):
        if not self.n:
            print("No se procesaron pedidos.")
            return
        print(f"\n Resumen: {self.n} pedidos")
        print(f"Tiempo medio preparación: {self.total_time/self.n:.2f}s")
        print(f"Ingresos brutos: €{self.revenue:.2f}")
