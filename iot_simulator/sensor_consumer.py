from kafka import KafkaConsumer
import json
from pymongo import MongoClient

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

for message in consumer:
    try:
        if isinstance(message.value, bytes):
            data = json.loads(message.value.decode('utf-8'))
        else:
            data = message.value
        collection.insert_one(data)
        print(f"Inserted data {data}")
    except KeyboardInterrupt:
        print("Consumer interrupted.")
        consumer.close()
        print("Closed consumer")
    except Exception as e:
        print(f"Error: {e}")
    #finally:
        