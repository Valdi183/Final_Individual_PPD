class PerformanceTracker:
    def __init__(self):
        self.total_orders = 0
        self.total_time = 0.0

    def record_order(self, duration):
        self.total_orders += 1
        self.total_time += duration

    def print_summary(self):
        if self.total_orders == 0:
            print("No se procesaron pedidos.")
        else:
            avg = self.total_time / self.total_orders
            print(f"Pedidos procesados: {self.total_orders}")
            print(f"Tiempo promedio de preparación: {avg:.2f} segundos")
