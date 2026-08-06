from datetime import datetime

from airflow.sdk import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import get_current_context
from airflow.sdk import Variable
from airflow.utils.trigger_rule import TriggerRule


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

        context = get_current_context()
        staging_table = f"stg_orders_{context['ts_nodash']}"
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

        hook.run(
        f"""
        CREATE TABLE {staging_table} AS
        SELECT *
        FROM customer_orders;
        """
        )

        print(f"Created {staging_table}")

        return staging_table


    @task
    def transform(staging_table: str):
        """
        Deleting orders that don't meet the criteria.
        """

        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        hook.run(
            f"""
            DELETE
            FROM {staging_table}
            WHERE status <> 'completed'
            OR amount <= 0;
            """
        )

        print(f"Deleted invalid orders from {staging_table}")
        return staging_table

    @task
    def load(staging_table: str):
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
                    f"""
                    INSERT INTO reporting_orders (
                    order_id,
                    customer_name,
                    category,
                    payment_method,
                    amount,
                    created_at
                    )
                    SELECT
                    order_id,
                    customer_name,
                    category,
                    payment_method,
                    amount,
                    created_at
                    FROM {staging_table};
                    """
                )

            conn.commit()

            print("Reporting table loaded successfully.")

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    @task(trigger_rule=TriggerRule.ALL_SUCCESS)
    def cleanup(staging_table: str):

        cleanup_enabled = Variable.get(
            "cleanup_enabled",
            default="false"
        )

        if cleanup_enabled.lower() != "true":
            print("Cleanup disabled.")
            return

        hook = PostgresHook(
            postgres_conn_id=POSTGRES_CONN_ID
        )

        hook.run(
            f"""
            DROP TABLE IF EXISTS {staging_table};
            """
        )

        print(f"Dropped {staging_table}")

    staging_table = extract()

    transformed_table = transform(staging_table)

    load(transformed_table)

    cleanup(transformed_table)

orders_etl()