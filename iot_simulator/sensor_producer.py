import random
import time
import json

from kafka import KafkaProducer

DEFAULT_TOPIC = "sensor_topic"
# Default producer
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',  # Cambia esto según tu configuración de Docker
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def generate_temperature_data():
    temp = round(random.uniform(20.0, 30.0), 2)
    humidity = round(random.uniform(30.0, 90.0), 2)
    
    message = {
        "sensor_id": "tempSensor1",
        "temperature": temp,
        "humidity": humidity,
        "timestamp": time.time()
    }
    
    return message

def continuos_data_send():
    print(f"Sending data to Kafka...")
    try:
        while True:
            message = generate_temperature_data()
            producer.send(DEFAULT_TOPIC, value=message)  # Sending Message
            print(f"Temperature sent: {message}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Consumer interrupted.")
    finally:
        producer.close()
        print("Closed consumer")