
#!/bin/sh
set -eu

KAFKA_TOPICS="/opt/kafka/bin/kafka-topics.sh"
BOOTSTRAP_SERVER="kafka:9092"
TOPIC="orders-v2"
DESIRED_PARTITIONS=3

echo "Ensuring topic $TOPIC exists..."

# Create the topic if it doesn't exist.
"$KAFKA_TOPICS" \
  --bootstrap-server "$BOOTSTRAP_SERVER" \
  --create \
  --if-not-exists \
  --topic "$TOPIC" \
  --partitions "$DESIRED_PARTITIONS" \
  --replication-factor 1

# Inspect the existing topic.
description=$(
  "$KAFKA_TOPICS" \
    --bootstrap-server "$BOOTSTRAP_SERVER" \
    --describe \
    --topic "$TOPIC"
)

printf '%s\n' "$description"

# Extract the current partition count from the topic description.
current_partitions=$(
  printf '%s\n' "$description" |
    sed -n 's/.*PartitionCount: \([0-9][0-9]*\).*/\1/p' |
    head -n 1
)

if [ -z "$current_partitions" ]; then
  echo "ERROR: Could not determine the partition count." >&2
  exit 1
fi

# Increase the partition count if the topic has fewer than three.
if [ "$current_partitions" -lt "$DESIRED_PARTITIONS" ]; then
  echo "Increasing partitions from $current_partitions to $DESIRED_PARTITIONS..."

  "$KAFKA_TOPICS" \
    --bootstrap-server "$BOOTSTRAP_SERVER" \
    --alter \
    --topic "$TOPIC" \
    --partitions "$DESIRED_PARTITIONS"
elif [ "$current_partitions" -gt "$DESIRED_PARTITIONS" ]; then
  echo "WARNING: Topic already has $current_partitions partitions."
  echo "Kafka cannot reduce the partition count automatically."
fi

echo "Final topic configuration:"
"$KAFKA_TOPICS" \
  --bootstrap-server "$BOOTSTRAP_SERVER" \
  --describe \
  --topic "$TOPIC"
