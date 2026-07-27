import json
import time

from confluent_kafka import Producer

from event_generator import generate_order_created


config = {
    "bootstrap.servers": "localhost:29092"
}


producer = Producer(config)


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Delivered key={msg.key().decode()} "
            f"partition={msg.partition()} "
            f"offset={msg.offset()}"
        )


try:

    while True:

        event = generate_order_created()

        producer.produce(
            topic="orders",
            key=str(event["order_id"]),
            value=json.dumps(event),
            callback=delivery_report,
        )

        producer.poll(0)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping producer...")

finally:
    producer.flush()