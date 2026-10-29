CREATE SCHEMA IF NOT EXISTS lab;

CREATE TABLE IF NOT EXISTS lab.raw_order_events (
    event_id UUID PRIMARY KEY,
    event_type TEXT NOT NULL,
    order_id BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    version INTEGER NOT NULL CHECK (version >= 1),

    event_created_at TIMESTAMPTZ NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    payload JSONB NOT NULL,

    kafka_topic TEXT NOT NULL,
    kafka_partition INTEGER NOT NULL,
    kafka_offset BIGINT NOT NULL,

    CONSTRAINT uq_raw_order_events_kafka_position
        UNIQUE (kafka_topic, kafka_partition, kafka_offset)
);
