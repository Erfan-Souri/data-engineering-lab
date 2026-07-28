# Order Consumer

A simple Python Kafka consumer used to process order lifecycle events produced by the Order Service in the Kafka lab.

The consumer subscribes to the `orders-v2` topic and joins the `order-processing` consumer group.

The project demonstrates practical Kafka consumer concepts including:

* Consumer groups
* Partition assignment
* Consumer scaling
* Consumer offsets
* Consumer lag
* Rebalancing and failure recovery

---

## Architecture

```text
                    Order Service
                         │
                         ▼
                       Kafka
                  ┌──────┼──────┐
                  │      │      │
                 P0     P1     P2
                  │      │      │
                  ▼      ▼      ▼
             Consumer Consumer Consumer
                 A       B       C

                 order-processing
                  consumer group
```

All consumer instances use the same consumer group:

```text
order-processing
```

Kafka therefore distributes topic partitions among the available consumers.

With three partitions and three consumers:

```text
P0 → Consumer A
P1 → Consumer B
P2 → Consumer C
```

If another consumer joins the same group, it remains idle because there are no additional partitions available.

If an active consumer stops, Kafka rebalances the group and assigns its partition to another available consumer.

---

## Project Structure

```text
order-consumer/
├── consumer.py
├── requirements.txt
└── README.md
```

---

## Requirements

* Python 3
* Apache Kafka running locally
* `orders-v2` Kafka topic
* Order Service producer running for continuous test data

The Kafka topic used by this consumer currently contains three partitions.

---

## Python Environment

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Kafka Connection

The Python consumer runs on the host machine and connects to Kafka using:

```text
localhost:29092
```

Kafka applications running inside the Docker network use the internal Kafka listener instead:

```text
kafka:9092
```

The consumer configuration includes:

```python
{
    "bootstrap.servers": "localhost:29092",
    "group.id": "order-processing",
    "auto.offset.reset": "earliest",
}
```

`auto.offset.reset=earliest` is used only when the consumer group does not have a valid committed offset for a partition.

Existing committed offsets take precedence.

---

## Running the Consumer

Make sure Kafka and the Order Service producer are running first.

Start one consumer:

```bash
python consumer.py
```

Example output:

```text
Order consumer started...
Waiting for events...

partition=0 offset=1328 event=ORDER_CREATED order=1453 version=1
partition=2 offset=547 event=ORDER_PAID order=1449 version=2
partition=1 offset=532 event=ORDER_SHIPPED order=1438 version=3
```

Stop the consumer with:

```text
Ctrl+C
```

The consumer closes its Kafka connection gracefully before exiting.

---

## Running Multiple Consumers

Open multiple terminals from the `order-consumer` directory.

Activate the virtual environment in each terminal:

```bash
source .venv/bin/activate
```

Then run:

```bash
python consumer.py
```

### One Consumer

With three partitions:

```text
Consumer A → P0, P1, P2
```

### Two Consumers

Kafka distributes the partitions between both workers:

```text
Consumer A → P0, P2
Consumer B → P1
```

The exact assignment may vary.

### Three Consumers

Each consumer can own one partition:

```text
Consumer A → P0
Consumer B → P1
Consumer C → P2
```

### Four Consumers

Only three consumers can actively consume because the topic has three partitions:

```text
Consumer A → P0
Consumer B → P1
Consumer C → P2
Consumer D → idle
```

A partition can be assigned to only one consumer within the same consumer group at a time.

A single consumer, however, can own multiple partitions.

---

## Consumer Rebalancing

Kafka automatically rebalances partition ownership when consumer-group membership changes.

For example:

```text
P0 → Consumer A
P1 → Consumer B
P2 → Consumer C
```

If Consumer B stops:

```text
Consumer B ✕
     │
     ▼
Group membership changes
     │
     ▼
Kafka rebalances
     │
     ▼
P1 assigned to another consumer
```

No manual partition reassignment is required.

The replacement consumer continues processing according to the consumer group's offset state.

---

## Inspect Consumer Groups

The Kafka CLI tools are available inside the Kafka container under:

```text
/opt/kafka/bin/
```

Describe the `order-processing` consumer group:

```bash
/opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --group order-processing
```

Example:

```text
GROUP             TOPIC      PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
order-processing  orders-v2  0          1311            1311            0
order-processing  orders-v2  1           506             506            0
order-processing  orders-v2  2           523             523            0
```

Important fields:

**CURRENT-OFFSET** — the consumer group's committed progress for the partition.

**LOG-END-OFFSET** — the current end of the partition's Kafka log.

**LAG** — the amount of data the consumer group has not yet processed.

Conceptually:

```text
LAG = LOG-END-OFFSET - CURRENT-OFFSET
```

---

## Observing Consumer Lag

Start the Order Service producer and consumer.

Once the consumer has caught up, the lag should approach zero.

Stop the consumer:

```text
Ctrl+C
```

Keep the producer running.

Kafka continues receiving events while the consumer group's committed position remains behind.

Inspect the group again:

```bash
/opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --group order-processing
```

The `LOG-END-OFFSET` will continue increasing and `LAG` will grow.

Restart:

```bash
python consumer.py
```

The consumer resumes from the group's committed progress, processes the backlog, and eventually catches up with the producer.

---

## Kafka Topic Inspection

List topics:

```bash
/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --list
```

Describe the order topic:

```bash
/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic orders-v2
```

Increase the topic to three partitions if required:

```bash
/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --alter \
  --topic orders-v2 \
  --partitions 3
```

Changing the number of partitions on an existing keyed topic should be done carefully because key-to-partition mappings can change.

Existing records are not redistributed when partitions are added.

---

## Docker Volume Note

Stopping the Kafka environment normally preserves its persisted data:

```bash
docker compose down
```

Using:

```bash
docker compose down -v
```

also removes Docker volumes.

For this lab, that means persisted Kafka topics, records, offsets, and other broker state can be lost.

After recreating the environment, topics and their partition configuration may need to be recreated.

---

## Key Concepts Demonstrated

This consumer demonstrates an important Kafka scalability rule:

```text
Maximum active consumers in a consumer group
≈
number of partitions being consumed
```

Adding consumers beyond the available partitions does not increase parallelism for that topic.

Partitions therefore affect not only how Kafka distributes stored records, but also how much parallelism a consumer group can achieve.

---

## Purpose

This application is intentionally small.

Its purpose is not to implement complex order-processing business logic. It provides a practical consumer that can be used to observe Kafka behavior directly and build an understanding of consumer groups, offsets, lag, partition ownership, scaling, and rebalancing.
