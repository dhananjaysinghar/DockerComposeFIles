from airflow.sdk import dag, task 
from datetime import datetime
import pandas as pd
import os



@dag(
        dag_id="simple_etl_pipeline",
        start_date=datetime(2025, 1, 1),
        schedule="@daily",
        catchup=False,
        tags=["etl", "example"],
        is_paused_upon_creation=False
)
def execute():

    # ------------------------
    # Extract Step
    # ------------------------
    @task.python
    def extract():
        data = [
            {"product": "Laptop", "price": 50000, "quantity": 2},
            {"product": "Mouse", "price": 500, "quantity": 5},
            {"product": "Keyboard", "price": 1500, "quantity": 3},
        ]

        df = pd.DataFrame(data)

        os.makedirs("/tmp/etl", exist_ok=True)

        df.to_csv("/tmp/etl/extracted_data.csv", index=False)

        print("Data Extracted")
        print(df)


    # ------------------------
    # Transform Step
    # ------------------------
    @task.python
    def transform():
        df = pd.read_csv("/tmp/etl/extracted_data.csv")

        df["total_price"] = df["price"] * df["quantity"]

        df.to_csv("/tmp/etl/transformed_data.csv", index=False)

        print("Data Transformed")
        print(df)


    # ------------------------
    # Load Step
    # ------------------------
    @task.python
    def load():
        df = pd.read_csv("/tmp/etl/transformed_data.csv")

        output_path = "/tmp/etl/final_output.csv"

        df.to_csv(output_path, index=False)

        print("Data Loaded")
        print(f"Final file saved at: {output_path}")
        print(df)


    # ETL Flow
    extract() >> transform() >> load()

# Instantiating the DAG
execute()