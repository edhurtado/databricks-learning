from kafka import KafkaProducer
import pandas as pd
import json
import pyarrow.parquet as pq
import pyarrow.orc as orc

# Default producer
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',  # Cambia esto según tu configuración de Docker
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

DEFAULT_TOPIC = "default_topic"

def send_csv_to_kafka(csv_file: str):
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        message = row.to_dict()  # Converting to dict format
        producer.send(DEFAULT_TOPIC, value=message)  # Sending Message

if __name__ == "__main__":
    file_path= r"C:\\Users\\User\\Documents\\repos\\Previous\\data.csv"
    send_csv_to_kafka(file_path)