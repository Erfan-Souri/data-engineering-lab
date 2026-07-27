import json
import time

from confluent_kafka import Producer

from event_generator import generate_event


producer = Producer(
    {
        "bootstrap.servers": "localhost:29092",
    }
)


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
        return

    print(
        f"[{msg.offset():05}] "
        f"partition={msg.partition()} "
        f"key={msg.key().decode()}"
    )


try:

    while True:

        event = generate_event()

        producer.produce(
            topic="orders",
            key=str(event["order_id"]),
            value=json.dumps(event),
            callback=delivery_report,
        )

        producer.poll(0)

        print(
            f"{event['event_type']:18}"
            f" order={event['order_id']} "
            f"customer={event['customer_id']} "
            f"version={event['version']}"
        )

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopping producer...")

finally:
    producer.flush()