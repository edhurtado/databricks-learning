from kafka import KafkaConsumer
import json
from pymongo import MongoClient
import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

KAFKA_BROKER = "localhost:29092"
TOPIC = "sensor_topic"
DEFAULT_GROUP = "my-consumer-group"

MONGO_USER = "root"
MONGO_PASSWORD = "rootpassword"
MONGO_PORT = "27017"
MONGO_HOST = "localhost"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    group_id=DEFAULT_GROUP,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
)

# Conexión a MongoDB
mongo_url = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
client = MongoClient(mongo_url)
db = client.mydatabase
collection = db.events  # Puedes crear tu colección o utilizar una existente

# Configuring Prometheus metrics ()
registry = CollectorRegistry()
temperature_gauge = Gauge('iot_temperature', 'Temperature IOT sensor', registry=registry)
humidity_gauge = Gauge('iot_humidity', 'Humidity IOT sensor', registry=registry)

def send_metrics_to_pushgateway():
    push_to_gateway('localhost:9091', job='kafka_consumer', registry=registry)  # Envíalo a PushGateway

for message in consumer:
    try:
        if isinstance(message.value, bytes):
            data = json.loads(message.value.decode('utf-8'))
        else:
            data = message.value
        collection.insert_one(data)
        print(f"Inserted data {data}")
        
        print(f"Sending data to Grafana")
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        
        if temperature is not None:
            temperature_gauge.set(temperature)
        if humidity is not None:
            humidity_gauge.set(humidity)
            
        send_metrics_to_pushgateway()

    except KeyboardInterrupt:
        print("Consumer interrupted.")
        consumer.close()
        print("Closed consumer")
    except Exception as e:
        print(f"Error: {e}")
    #finally:
    
