import json
import os

import psycopg2
from psycopg2.extras import Json
from confluent_kafka import Consumer, KafkaError


consumer = Consumer({
    "bootstrap.servers": "localhost:29092",
    "group.id": "order-postgres-ingestion",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
})

# Local lab settings come from the Airflow Compose configuration.
db_conn = psycopg2.connect(
    host=os.getenv("PGHOST", "localhost"),
    port=int(os.getenv("PGPORT", "5432")),
    dbname=os.getenv("PGDATABASE", "airflow"),
    user=os.getenv("PGUSER", "airflow"),
    password=os.getenv("PGPASSWORD", "airflow"),
)

insert_sql = """
    INSERT INTO lab.raw_order_events (
        event_id,
        event_type,
        order_id,
        customer_id,
        amount,
        currency,
        version,
        event_created_at,
        payload,
        kafka_topic,
        kafka_partition,
        kafka_offset
    )
    VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    )
    ON CONFLICT DO NOTHING
"""

consumer.subscribe(["orders-v2"])

print("PostgreSQL ingestion consumer started...")

try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            raise RuntimeError(msg.error())

        event = json.loads(msg.value().decode("utf-8"))

        # First, persist the event in a database transaction.
        with db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute(
                    insert_sql,
                    (
                        event["event_id"],
                        event["event_type"],
                        event["order_id"],
                        event["customer_id"],
                        event["amount"],
                        event["currency"],
                        event["version"],
                        event["created_at"],
                        Json(event),
                        msg.topic(),
                        msg.partition(),
                        msg.offset(),
                    ),
                )
                inserted = cursor.rowcount == 1

        # Only acknowledge the Kafka message after the DB transaction commits.
        consumer.commit(message=msg, asynchronous=False)

        status = "inserted" if inserted else "duplicate skipped"
        print(
            f"{status}: event={event['event_type']} "
            f"order={event['order_id']} "
            f"partition={msg.partition()} "
            f"offset={msg.offset()}"
        )

except KeyboardInterrupt:
    print("\nStopping ingestion consumer...")

finally:
    consumer.close()
    db_conn.close()
