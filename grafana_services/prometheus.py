from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import time

# Crear una nueva métrica
registry = CollectorRegistry()
g = Gauge('kafka_event_count', 'Total events consumed from Kafka', registry=registry)

# Simula un contador que incrementa con el tiempo (por ejemplo, eventos consumidos)
for i in range(10):
    g.set(i)  # Establece el valor de la métrica
    push_to_gateway('localhost:9091', job='kafka_consumer', registry=registry)
    print(f"Pushed {i} to Push Gateway")
    time.sleep(1)
