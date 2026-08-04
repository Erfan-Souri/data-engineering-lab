from datetime import datetime

from airflow.sdk import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


POSTGRES_CONN_ID = "postgres_lab"


@dag(
    dag_id="orders_etl",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "postgres"],
)
def orders_etl():

    @task
    def extract():
        """
        Validate that source data exists.
        """

        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        records = hook.get_first(
            """
            SELECT COUNT(*)
            FROM customer_orders;
            """
        )

        count = records[0]

        print(f"Found {count} orders in source table.")

        if count == 0:
            raise ValueError("customer_orders table is empty.")

    @task
    def transform():
        """
        Create a staging table containing only
        completed orders.
        """

        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        hook.run(
            """
            DROP TABLE IF EXISTS stg_orders;

            CREATE TABLE stg_orders AS
            SELECT
                order_id,
                customer_name,
                amount,
                created_at
            FROM customer_orders
            WHERE status = 'completed'
              AND amount > 0;
            """
        )

        print("Staging table created.")

    @task
    def load():
        """
        Load staging data into reporting table.
        """

        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        conn = hook.get_conn()

        try:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    TRUNCATE TABLE reporting_orders;
                    """
                )

                cursor.execute(
                    """
                    INSERT INTO reporting_orders (
                        order_id,
                        customer_name,
                        amount,
                        created_at
                    )
                    SELECT
                        order_id,
                        customer_name,
                        amount,
                        created_at
                    FROM stg_orders;
                    """
                )

            conn.commit()

            print("Reporting table loaded successfully.")

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    extract() >> transform() >> load()


orders_etl()