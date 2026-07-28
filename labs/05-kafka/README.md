# Lab 05 — Apache Kafka Fundamentals

A hands-on Apache Kafka lab for learning the fundamentals of event streaming, partitioning, producers, consumers, consumer groups, offsets, lag, and rebalancing.

The lab uses Docker to run a single Kafka broker and includes two small Python applications:

* **Order Service** — continuously generates realistic order lifecycle events and publishes them to Kafka.
* **Order Consumer** — consumes those events as part of a Kafka consumer group.

The goal of this lab is not to build a production Kafka platform. It is to create a minimal environment where the core Kafka concepts can be observed directly.

---

# Architecture

```text
                         Host Machine
                              │
                     localhost:29092
                              │
                              ▼
                    ┌─────────────────┐
                    │      Kafka      │
                    │   Single Broker │
                    │                 │
                    │    orders-v2    │
                    │                 │
                    │  P0   P1   P2   │
                    └──┬────┬────┬────┘
                       │    │    │
              ┌────────┘    │    └────────┐
              ▼             ▼             ▼
         Consumer A     Consumer B     Consumer C
              └──────────────┬──────────────┘
                             │
                       order-processing
                        consumer group


Order Service
     │
     │ order_id used as message key
     └──────────────────────► Kafka
```

Kafka runs inside Docker while the Python producer and consumers run on the host machine.

Kafka exposes an external listener for host applications:

```text
localhost:29092
```

Kafka CLI commands executed inside the container use:

```text
localhost:9092
```

---

# Project Structure

```text
.
├── README.md
├── config
├── docker-compose.yml
├── docs
├── order-consumer
│   ├── README.md
│   ├── consumer.py
│   └── requirements.txt
├── order-service
│   ├── README.md
│   ├── event_generator.py
│   ├── producer.py
│   └── requirements.txt
└── scripts
```

---

# Requirements

* Docker
* Docker Compose
* Python 3
* `pip`

Verify Docker:

```bash
docker --version
docker compose version
```

Verify Python:

```bash
python3 --version
```

---

# Starting Kafka

From the Kafka lab directory:

```bash
docker compose up -d
```

Check the running containers:

```bash
docker compose ps
```

Follow Kafka logs:

```bash
docker compose logs -f kafka
```

Kafka is ready when the broker reaches its started state.

---

# Entering the Kafka Container

Kafka CLI tools are available inside the container under:

```text
/opt/kafka/bin/
```

Open a shell:

```bash
docker exec -it kafka bash
```

The commands throughout this README that start with `/opt/kafka/bin/` are intended to be executed from this shell.

---

# Creating the Order Topic

This lab uses:

```text
orders-v2
```

with three partitions:

```text
orders-v2
├── Partition 0
├── Partition 1
└── Partition 2
```

Create it explicitly:

```bash
/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic orders-v2 \
  --partitions 3 \
  --replication-factor 1
```

The replication factor is `1` because this lab currently contains only one Kafka broker.

Verify the topic:

```bash
/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic orders-v2
```

List all topics:

```bash
/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --list
```

---

# Why Three Partitions?

Partitions allow Kafka topics to scale horizontally.

Instead of maintaining one continuous log:

```text
orders
└── P0
```

the topic is divided into independent logs:

```text
orders-v2

P0 ─────────────────────────►

P1 ─────────────────────────►

P2 ─────────────────────────►
```

This allows records and consumer workloads to be distributed.

Three partitions were chosen for this lab because they are enough to clearly demonstrate:

* Key-based routing
* Multiple independent partition logs
* Multiple consumers
* Consumer-group parallelism
* Rebalancing
* Idle consumers

The number `3` is an educational choice, not a production recommendation.

Production partition counts should be selected based on expected throughput, consumer parallelism, ordering requirements, growth, and operational constraints.

---

# Increasing the Partition Count

Kafka allows the number of partitions to be increased:

```bash
/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --alter \
  --topic orders-v2 \
  --partitions 3
```

Existing records are **not redistributed** when partitions are added.

For example, if a topic originally contained one partition with 800 records:

```text
P0 → 800 records
```

and two additional partitions are introduced, the historical records remain in P0:

```text
P0 → 800+
P1 → new records
P2 → new records
```

New records can then be distributed across all three partitions.

Changing partition count also deserves special care for keyed data because the mapping of a key to a partition can change when the partition count changes.

For this reason, the recommended approach for this lab is to create `orders-v2` with three partitions from the beginning.

---

# Order Service

The Order Service is a small Python producer that simulates realistic order lifecycle events.

An order can progress through:

```text
ORDER_CREATED
      │
      ▼
ORDER_PAID
      │
      ▼
ORDER_SHIPPED
      │
      ▼
ORDER_DELIVERED
```

Orders can also be cancelled.

Each state transition produces a new Kafka event.

Example:

```json
{
  "event_id": "1cb48784-f53f-49a7-a814-a871ee27dc71",
  "event_type": "ORDER_PAID",
  "order_id": 1042,
  "customer_id": 78,
  "amount": 159.45,
  "currency": "USD",
  "version": 2,
  "created_at": "2026-07-28T10:15:30+00:00"
}
```

---

# Running the Order Service

Move into:

```bash
cd order-service
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the producer:

```bash
python producer.py
```

The service continuously produces events until stopped with:

```text
Ctrl+C
```

---

# Message Keys and Partition Routing

The Order Service publishes records using:

```python
key=str(event["order_id"])
```

The important distinction is:

```text
Partitions  → horizontal distribution
Message key → routing decision
```

Partitions can exist without message keys.

When a key is provided, the producer's partitioning strategy deterministically maps that key to a partition.

Conceptually:

```text
order_id
    │
    ▼
  hash(key)
    │
    ▼
partition selection
    │
    ▼
 P0 / P1 / P2
```

Therefore all events for a particular order are consistently routed to the same partition while the partition count and partitioning strategy remain unchanged.

For example:

```text
Order 1001

ORDER_CREATED   ─┐
ORDER_PAID       │
ORDER_SHIPPED    ├──► Partition 2
ORDER_DELIVERED ─┘
```

This matters because Kafka guarantees ordering **within a partition**, not globally across an entire multi-partition topic.

Using `order_id` as the key therefore preserves the ordering of events belonging to the same order.

Without a key, the producer's partitioner is free to distribute records according to its configured keyless partitioning strategy. Applications should not rely on related keyless records remaining together.

---

# Inspecting Individual Partitions

A specific partition can be consumed directly:

```bash
/opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic orders-v2 \
  --partition 0
```

Change the partition number to inspect:

```text
0
1
2
```

Running one console consumer for each partition makes the producer's partition distribution directly observable.

---

# Order Consumer

The Python Order Consumer subscribes to:

```text
orders-v2
```

and joins:

```text
order-processing
```

as its consumer group.

Run it from:

```bash
cd order-consumer
```

Create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the consumer:

```bash
python consumer.py
```

Example output:

```text
partition=0 offset=1328 event=ORDER_CREATED order=1453 version=1
partition=2 offset=547 event=ORDER_PAID order=1449 version=2
partition=1 offset=532 event=ORDER_SHIPPED order=1438 version=3
```

---

# Consumer Groups

A consumer group represents a logical consuming application.

This lab uses:

```text
order-processing
```

Multiple instances of `consumer.py` can join the same group.

Kafka distributes partitions between those consumers.

## One Consumer

```text
P0 ─┐
P1 ─┼──► Consumer A
P2 ─┘
```

One consumer can own multiple partitions.

## Two Consumers

```text
P0 ──► Consumer A
P1 ──► Consumer B
P2 ──► Consumer A
```

The exact assignment can vary.

## Three Consumers

```text
P0 ──► Consumer A
P1 ──► Consumer B
P2 ──► Consumer C
```

This provides three-way consumer parallelism.

## Four Consumers

```text
P0 ──► Consumer A
P1 ──► Consumer B
P2 ──► Consumer C

       Consumer D → idle
```

There is no fourth partition for Consumer D to own.

Therefore:

> The maximum useful parallelism of a consumer group for a single topic is bounded by the number of partitions being consumed.

A partition can be assigned to only one consumer within the same consumer group at a time, while a consumer can own multiple partitions.

---

# Testing Multiple Consumers

Open multiple terminal windows.

In each terminal:

```bash
cd order-consumer
source .venv/bin/activate
python consumer.py
```

With three terminals, Kafka can assign one partition to each consumer.

Start a fourth consumer and it should remain idle while all three partitions are already owned.

---

# Consumer Rebalancing

Kafka monitors consumer-group membership.

Suppose:

```text
P0 → Consumer A
P1 → Consumer B
P2 → Consumer C
```

If Consumer B stops:

```text
Consumer B
    ✕
    │
    ▼
group membership changes
    │
    ▼
Kafka rebalances
    │
    ▼
P1 assigned to another consumer
```

An idle fourth consumer can therefore become active when another consumer leaves the group.

This behavior can be tested by running four consumer instances and stopping one of the three active consumers.

---

# Consumer Offsets

Each Kafka partition is an ordered log containing records identified by offsets.

Conceptually:

```text
Partition 0

offset
  0   event
  1   event
  2   event
  3   event
  4   event
  ...
```

Consumer progress is tracked independently for each partition.

The relevant identity is effectively:

```text
Consumer Group
      +
Topic
      +
Partition
```

This allows a consumer process to stop and another process in the same group to continue processing from the group's committed progress.

---

# Inspecting Consumer Groups

Inside the Kafka container:

```bash
/opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --group order-processing
```

Example:

```text
GROUP             TOPIC      PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
order-processing  orders-v2  0          1311            1313            2
order-processing  orders-v2  1           506             506            0
order-processing  orders-v2  2           523             525            2
```

Important columns:

### `CURRENT-OFFSET`

The consumer group's committed progress for that partition.

### `LOG-END-OFFSET`

The current end of the Kafka partition.

### `LAG`

The difference between the end of the log and the consumer group's committed progress.

Conceptually:

```text
CURRENT-OFFSET                     LOG-END-OFFSET
       │                                  │
       ▼                                  ▼
───────●──────────────────────────────────●
       │<------------- LAG -------------->│
```

---

# Consumer Lag Experiment

Start:

1. Kafka
2. Order Service
3. Order Consumer

Once the consumer catches up, lag should approach zero.

Stop only the consumer:

```text
Ctrl+C
```

Keep the producer running.

The producer continues appending events to Kafka:

```text
Producer
   │
   ▼
Kafka ███████████████████████████►

Consumer
            ✕
```

Inspect the consumer group again:

```bash
/opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --group order-processing
```

`LOG-END-OFFSET` continues increasing while `CURRENT-OFFSET` remains behind, causing lag to grow.

Restart:

```bash
python consumer.py
```

The consumer processes the backlog until it catches up.

This demonstrates why consumer lag is an important operational metric in Kafka systems.

---

# Console Consumer with a Consumer Group

A console consumer can also join the same group:

```bash
/opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic orders-v2 \
  --group order-processing
```

Stopping and restarting the same group demonstrates that Kafka can resume according to its committed offsets instead of blindly replaying the entire topic.

---

# Reading from the Beginning

For exploratory consumption:

```bash
/opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic orders-v2 \
  --from-beginning
```

`--from-beginning` is useful for inspecting historical records.

In application consumers, offset-reset behavior applies when there is no valid committed offset for the consumer group; it does not normally override an existing valid committed position.

---

# Docker Persistence

Kafka data is stored in Docker volumes.

Stop the environment while preserving its volumes:

```bash
docker compose down
```

Restart:

```bash
docker compose up -d
```

Kafka's persisted state should remain available.

To completely reset the lab:

```bash
docker compose down -v
```

**Warning:** `-v` removes the associated Docker volumes.

This can remove:

* Kafka records
* Topics stored in broker state
* Consumer offsets
* Other persisted Kafka metadata

After:

```bash
docker compose down -v
docker compose up -d
```

the environment should be treated as a fresh Kafka installation and the lab topic may need to be recreated.

---

# Recreating the Lab from Scratch

Start Kafka:

```bash
docker compose up -d
```

Enter the container:

```bash
docker exec -it kafka bash
```

Create the topic:

```bash
/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic orders-v2 \
  --partitions 3 \
  --replication-factor 1
```

Start the Order Service in another terminal:

```bash
cd order-service
source .venv/bin/activate
python producer.py
```

Start the Order Consumer:

```bash
cd order-consumer
source .venv/bin/activate
python consumer.py
```

Additional consumer instances can be started in separate terminals to observe consumer-group scaling and rebalancing.

---

# Notes and Key Takeaways

## Kafka Broker

A Kafka broker is responsible for storing events durably and serving them to producers and consumers as part of the Kafka cluster.

Kafka decouples producers from consumers:

```text
Producer → Kafka → Consumer
```

The producer does not need to know which application will eventually process an event, and consumers do not need to be running when the event is produced.

---

## Kafka Is an Append-Only Distributed Event Log

Kafka stores events by appending them to partition logs.

Existing events are not normally updated in place as they would be in a traditional transactional database table.

Conceptually:

```text
Event 1
Event 2
Event 3
Event 4
   ↓
new events appended here
```

Consumers maintain their own progress through these logs.

---

## Partitions and Message Keys Solve Different Problems

Partitions provide horizontal distribution:

```text
Topic
├── P0
├── P1
└── P2
```

Message keys influence how events are routed to those partitions.

Therefore:

```text
Partitions = horizontal scaling
Message key = routing strategy
```

They are related concepts, but they are not the same thing.

Kafka can still publish records when no key is provided. In that case, the configured producer partitioner determines how keyless records are distributed.

---

## Ordering Is Per Partition

Kafka preserves record order within an individual partition.

It does not provide one global ordering across all partitions of a topic.

Therefore, records requiring ordering should generally be routed using an appropriate key.

For this lab:

```text
key = order_id
```

keeps the lifecycle of an individual order within the same partition.

---

## Consumer Group Rule

Within one consumer group:

> A partition is assigned to at most one active consumer at a time.

However:

> One consumer can own multiple partitions.

For three partitions:

```text
1 consumer  → 3 + 0 + 0
2 consumers → 2 + 1
3 consumers → 1 + 1 + 1
4 consumers → 1 + 1 + 1 + 0
```

Therefore the partition count places an upper bound on useful consumer parallelism for that topic within the group.

---

## Consumer Groups Provide Independent Consumption

Different consumer groups can independently consume the same Kafka topic.

Conceptually:

```text
                       orders
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       order-processing       analytics-service
        consumer group         consumer group
```

Each group maintains its own processing progress.

This allows the same event stream to support multiple independent downstream applications.

---

## Rebalancing Provides Failure Recovery

When consumers join or leave a consumer group, Kafka can rebalance partition ownership.

This allows another consumer to take responsibility for partitions whose previous consumer disappeared.

Combined with consumer-group offsets, this provides the foundation for scalable and fault-tolerant event processing.

---

# Concepts Covered

This lab provides hands-on experience with:

* Kafka brokers
* Topics
* Partitions
* Producers
* Message keys
* Key-based partition routing
* Ordering within partitions
* Python Kafka producers
* Python Kafka consumers
* Consumer groups
* Partition assignment
* Consumer parallelism
* Consumer offsets
* Consumer lag
* Consumer-group rebalancing
* Consumer failure recovery
* Kafka CLI tools
* Docker networking
* Kafka persistence using Docker volumes

Advanced topics such as multi-broker replication, ISR, delivery semantics, manual offset management, Schema Registry, Kafka Connect, transactions, security, and production monitoring are intentionally outside the scope of this fundamentals lab.

---

# Lab Scope

This lab intentionally uses:

```text
1 Kafka broker
3 partitions
1 producer application
1 consumer application
N consumer instances
```

It is designed for learning Kafka fundamentals rather than reproducing a production Kafka deployment.

The resulting pipeline is:

```text
                 ┌─────────────────┐
                 │  Order Service  │
                 │ Python Producer │
                 └────────┬────────┘
                          │
                    keyed events
                          │
                          ▼
                ┌───────────────────┐
                │       Kafka       │
                │                   │
                │ orders-v2         │
                │ P0 │ P1 │ P2      │
                └─┬────┬────┬───────┘
                  │    │    │
                  ▼    ▼    ▼
                ┌───────────────────┐
                │  Order Consumer   │
                │ order-processing  │
                │  Consumer Group   │
                └───────────────────┘
```

This provides a minimal but practical foundation for using Kafka in future data-engineering pipelines.
