from kafka import KafkaConsumer
import json

KAFKA_BROKER = "localhost:29092"
TOPIC = "default_topic"
DEFAULT_GROUP = "my-consumer-group"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    group_id=DEFAULT_GROUP,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
)

def consume_messages():
    print(f"Connected to topic: {TOPIC}. Waiting for messages...")
    try:
        for message in consumer:
            print(f"Message received: {message.value}")
    except KeyboardInterrupt:
        print("Consumer interrupted.")
    finally:
        consumer.close()
        print("Closed consumer")

if __name__ == '__main__':
    consume_messages()
