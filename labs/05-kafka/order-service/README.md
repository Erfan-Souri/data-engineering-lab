# Order Service

## Overview

The Order Service is a lightweight Python application that simulates a production
order management system.

Its responsibility is to generate realistic order events and publish them
to Apache Kafka.

The service does not store data itself.

It only produces events.

These events will later be consumed by other services inside this lab,
including analytics pipelines, ClickHouse, and notification services.

---

## Responsibilities

- Generate realistic order events
- Serialize events as JSON
- Publish events to Kafka
- Use order_id as the Kafka message key

---

## Future Integrations

- ClickHouse
- Apache NiFi
- Notification Service
- Analytics Consumer

---

## Run

Coming soon.