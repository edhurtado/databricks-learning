import pyarrow as pa
import pyarrow.orc as orc

import pandas as pd
from faker import Faker
from typing import List
from collections import defaultdict
import json

fake_data_generator = Faker()

allowed_types = {'country':fake_data_generator.country,
                 'city':fake_data_generator.city,
                 'country_code':fake_data_generator.country_code,
                 'street_address':fake_data_generator.street_address,
                 'post_code':fake_data_generator.postcode,
                 'street_addres': fake_data_generator.street_address,
                 'bank_account': fake_data_generator.iban,
                 'social_security': fake_data_generator.ssn,
                 'phone_number': fake_data_generator.phone_number,
                 'job': fake_data_generator.job,
                 'credit_card': fake_data_generator.credit_card_number,
                 'ccv': fake_data_generator.credit_card_security_code,
                 'card_expire': fake_data_generator.credit_card_expire,
                 }


# Generate fake data
def generate_fake_row(fields:List[str]) -> defaultdict:
    if fields is None:
        fields = allowed_types.keys()
    row = defaultdict()
    for field in fields:
        if field in allowed_types:
            row[field] = allowed_types[field]()
        else:
            print(f"Required field type: {field}, not allowed for this implementation, skipping.")    
    return row
        

def generate_fake_data(required_rows, fields:List[str]=None) -> List[defaultdict]:
    data = []
    
    for _ in range(required_rows):
        data.append(generate_fake_row(fields=fields))
    
    return data

# Exporting data in different formats:

# Structuring pandas object
def create_data_df(data:List[defaultdict]) -> pd.DataFrame:
    # Create Dataframe based on data
    return pd.DataFrame(data)


# Parquet
def export_to_parquet(data: List[defaultdict], output_file: str = "data.parquet"):
    df = create_data_df(data)
    df.to_parquet(output_file, engine='pyarrow', index=False)


# ORC
def export_to_orc(data: List[defaultdict], output_file: str="data.orc"):
    df = create_data_df(data)
    
    # Convert Dataframe into a PyArrow Table
    table = pa.Table.from_pandas(df)

    # Save it in ORC format
    with open(output_file, "wb") as f:
        orc.write_table(table, f)


# CSV
def export_to_csv(data, nombre_archivo="data.csv"):
    df = create_data_df(data)
    df.to_csv(nombre_archivo, index=False)


# JSON
def export_to_json(data, nombre_archivo="data.json"):
    with open(nombre_archivo, "w") as archivo:
        json.dump(data, archivo, indent=4)


# Excel
def export_to_excel(data, nombre_archivo="data.xlsx"):
    df = create_data_df(data)
    df.to_excel(nombre_archivo, index=False)

if __name__ == "__main__": # Main class
    fake_data = generate_fake_data(100)
    export_to_csv(fake_data)
    export_to_json(fake_data)
    export_to_excel(fake_data)
    export_to_orc(fake_data)
    export_to_parquet(fake_data)