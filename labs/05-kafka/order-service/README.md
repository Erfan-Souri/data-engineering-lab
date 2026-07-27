# Order Service

A simple Python-based Order Service simulator that continuously publishes realistic order lifecycle events to Apache Kafka.

This project is part of a larger Kafka learning repository. Rather than generating completely random JSON, the service simulates how an e-commerce application produces business events, making it much easier to understand Kafka concepts such as partitions, message keys, consumer groups, offsets, and event replay.

---

## Features

* Generates realistic order lifecycle events
* Simulates active orders in memory
* Publishes events continuously to Kafka
* Uses `order_id` as the Kafka message key
* Produces JSON events
* Designed specifically for Kafka learning and experimentation

---

## Order Lifecycle

Each order follows a simple lifecycle:

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

Some orders are cancelled shortly after creation:

```text
ORDER_CREATED
        │
        ▼
ORDER_CANCELLED
```

Completed (`ORDER_DELIVERED`) and cancelled (`ORDER_CANCELLED`) orders are removed from the simulator's in-memory state. Their complete history remains available in Kafka.

---

## Sample Event

```json
{
  "event_id": "8a8b0e18-f0d5-4633-9c75-5cfdb3dd86b4",
  "event_type": "ORDER_PAID",
  "order_id": 1007,
  "customer_id": 42,
  "amount": 129.99,
  "currency": "USD",
  "version": 2,
  "created_at": "2026-07-27T12:34:56.789012+00:00"
}
```

---

## Project Structure

```text
order-service/
├── event_generator.py
├── producer.py
├── requirements.txt
└── README.md
```

---

## Requirements

* Python 3.11+
* Apache Kafka (running)
* Docker (recommended for Kafka)

---

## Installation

Clone the repository and move into the project directory.

```bash
cd order-service
```

Create a virtual environment.

```bash
python3 -m venv .venv
```

Activate the virtual environment.

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies.

```bash
pip install -r requirements.txt
```

---

## Kafka Configuration

The producer connects using:

```python
bootstrap.servers = "localhost:29092"
```

This assumes Kafka is running inside Docker and exposes the broker on port **29092**.

If the producer runs inside the same Docker network as Kafka, use:

```text
kafka:9092
```

instead.

---

## Running the Producer

Start Kafka first.

Then run:

```bash
python producer.py
```

The producer will continuously generate and publish events until interrupted.

Stop the producer with:

```text
Ctrl + C
```

---

## Example Output

```text
ORDER_CREATED      order=1001 customer=18 version=1
ORDER_CREATED      order=1002 customer=77 version=1
ORDER_PAID         order=1001 customer=18 version=2
ORDER_CREATED      order=1003 customer=5 version=1
ORDER_SHIPPED      order=1001 customer=18 version=3
ORDER_DELIVERED    order=1001 customer=18 version=4
ORDER_CANCELLED    order=1002 customer=77 version=2
```

---

## Design Notes

This service intentionally keeps only active orders in memory.

It is **not** intended to be a database or source of historical truth.

Responsibilities are separated as follows:

* **Order Service** → Maintains the current working state of active orders.
* **Kafka** → Stores the immutable history of all events.

This separation reflects a common event-driven architecture where services own operational state while Kafka acts as the event log.

---

## Kafka Topic

By default, events are published to:

```text
orders
```

Each message uses:

```text
Message Key = order_id
```

Using the order ID as the message key ensures that all events belonging to the same order are consistently routed to the same Kafka partition, preserving their ordering.

---

## Current Scope

At this stage, the project focuses only on producing events.

Upcoming Kafka labs will use this producer to demonstrate:

* Topic partitioning
* Message keys
* Consumer groups
* Rebalancing
* Consumer offsets
* Event replay
* Consumer lag
* Exactly-once and at-least-once delivery concepts

---
