import json

from confluent_kafka import Consumer, KafkaError


config = {
    "bootstrap.servers": "localhost:29092",
    "group.id": "order-processing",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(config)

consumer.subscribe(["orders-v2"])

print("Order consumer started...")
print("Waiting for events...\n")


try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue

            print(f"Consumer error: {msg.error()}")
            continue

        event = json.loads(msg.value().decode("utf-8"))

        print(
            f"partition={msg.partition()} "
            f"offset={msg.offset()} "
            f"event={event['event_type']} "
            f"order={event['order_id']} "
            f"version={event['version']}"
        )

except KeyboardInterrupt:
    print("\nStopping consumer...")

finally:
    consumer.close()