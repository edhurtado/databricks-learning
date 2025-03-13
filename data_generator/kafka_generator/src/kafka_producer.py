from kafka import KafkaProducer
import pandas as pd
import json
import pyarrow.parquet as pq
import pyorc

# Default producer
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',  # Cambia esto según tu configuración de Docker
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

DEFAULT_TOPIC = "default_topic"

def send_csv_to_kafka(csv_file: str, limit:int = None):
    count = 0
    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        if limit and count >= limit:
            break
        count += 1
        
        message = row.to_dict()  # Converting to dict format
        message["origin"] = "csv"
        producer.send(DEFAULT_TOPIC, value=message)  # Sending Message

def send_parquet_to_kafka(parquet_file: str, limit:int = None):
    count = 0
    table = pq.read_table(parquet_file)
    df = table.to_pandas()  # Convert table to DataFrame
    for index, row in df.iterrows():
        if limit and count >= limit:
            break
        count += 1
        
        message = row.to_dict()
        message["origin"] = "parquet"
        producer.send(DEFAULT_TOPIC, value=message)


def send_orc_to_kafka(orc_file: str, limit:int = None):
    count = 0
    with open(orc_file, 'rb') as f:
        reader = pyorc.Reader(f)
        
        # Getting colum names from ORC Schema
        column_names = [field for field in reader.schema.fields.keys()]

        for record in reader:
            if limit and count >= limit:
                break
            count += 1
            message = {column_names[i]: record[i] for i in range(len(record))}
            message["origin"] = "orc"
            producer.send(DEFAULT_TOPIC, value=message)


def send_json_to_kafka(json_file: str, limit:int = None):
    count = 0
    with open(json_file, 'r') as f:
        data = json.load(f)
        for record in data:
            if limit and count >= limit:
                break
            count += 1
        
            record["origin"] = "json"
            producer.send(DEFAULT_TOPIC, value=record)
            

def send_file_to_kafka(file_path: str, limit: int=10):
    extension = file_path.split('.')[-1].lower()
    
    if extension == 'csv':
        send_csv_to_kafka(file_path, limit)
    elif extension == 'parquet':
        send_parquet_to_kafka(file_path, limit)
    elif extension == 'orc':
        send_orc_to_kafka(file_path, limit)
    elif extension == 'json':
        send_json_to_kafka(file_path, limit)
    else:
        print(f"File format from file: {extension} not currently supported.")


if __name__ == "__main__":
    file_path= r"C:\\Users\\User\\Documents\\repos\\Previous\\data.csv"
    send_file_to_kafka(file_path, 10)

    file_path= r"C:\\Users\\User\\Documents\\repos\\Previous\\data.json"
    send_file_to_kafka(file_path, 10)
    
    file_path= r"C:\\Users\\User\\Documents\\repos\\Previous\\data.orc"
    send_file_to_kafka(file_path, 10)
    
    file_path= r"C:\\Users\\User\\Documents\\repos\\Previous\\data.parquet"
    send_file_to_kafka(file_path, 10)
