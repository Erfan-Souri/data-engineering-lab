from datetime import datetime

from airflow.sdk import dag, task


@dag(
    dag_id="first_pipeline",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["learning"],
)
def first_pipeline():

    @task
    def extract():
        print("Extracting data...")
        return [10, 20, 30, 40, 50]

    @task
    def transform(numbers):
        print("Transforming data...")
        return [number * 2 for number in numbers]

    @task
    def load(numbers):
        print(f"Loading data: {numbers}")

    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)


first_pipeline()