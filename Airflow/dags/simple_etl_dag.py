from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

# ------------------------
# Extract Step
# ------------------------
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
def transform():
    df = pd.read_csv("/tmp/etl/extracted_data.csv")

    df["total_price"] = df["price"] * df["quantity"]

    df.to_csv("/tmp/etl/transformed_data.csv", index=False)

    print("Data Transformed")
    print(df)


# ------------------------
# Load Step
# ------------------------
def load():
    df = pd.read_csv("/tmp/etl/transformed_data.csv")

    output_path = "/tmp/etl/final_output.csv"

    df.to_csv(output_path, index=False)

    print("Data Loaded")
    print(f"Final file saved at: {output_path}")
    print(df)


# ------------------------
# DAG Definition
# ------------------------
with DAG(
    dag_id="simple_etl_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["etl", "example"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load,
    )

    # ETL Flow
    extract_task >> transform_task >> load_task