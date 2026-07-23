# ClickHouse Cluster Lab

## Overview

This lab builds a minimal distributed ClickHouse cluster using Docker Compose.

The goal is to understand how ClickHouse nodes coordinate through ClickHouse Keeper, how replicated tables are created, and how distributed DDL (`ON CLUSTER`) works.

This lab intentionally focuses on **replication** rather than sharding. A single shard with two replicas provides the simplest topology for understanding distributed ClickHouse before moving on to multi-shard clusters.

---

## Architecture

```text
                 ClickHouse Keeper
                      :9181
                         │
          ┌──────────────┴──────────────┐
          │                             │
    clickhouse1                   clickhouse2
     Replica 1                     Replica 2
          │                             │
          └──────── ReplicatedMergeTree ────────┘
                 1 Shard • 2 Replicas
```

---

## Objectives

* Deploy ClickHouse Keeper
* Deploy multiple ClickHouse nodes
* Configure a ClickHouse cluster
* Understand shards and replicas
* Create replicated tables using `ReplicatedMergeTree`
* Execute distributed DDL using `ON CLUSTER`
* Verify automatic replication between nodes

---

## Project Structure

```text
03-clickhouse-cluster/
├── config/
│   ├── keeper/
│   ├── clickhouse1/
│   ├── clickhouse2/
│   └── shared/
├── docker-compose.yml
├── sql/
├── docs/
└── README.md
```

---

## Concepts Learned

### Replication vs Sharding

**Replication** increases availability by storing the same data on multiple nodes.

**Sharding** increases capacity by distributing different portions of the data across multiple nodes.

This lab demonstrates **replication** only.

---

### What is a ClickHouse Cluster?

A ClickHouse cluster is a named topology describing one or more shards and the replicas that belong to each shard.

The cluster definition is stored in `clusters.xml` and is referenced whenever `ON CLUSTER` statements are executed.

---

### ClickHouse Keeper

ClickHouse Keeper coordinates the cluster by storing metadata required for:

* Replica coordination
* Distributed DDL execution
* Replication metadata
* Leader election
* Cluster state

Keeper stores metadata only—it does **not** store table data.

---

## Lessons Learned

### Shared configuration

Initially each ClickHouse node had its own `clusters.xml`.

The configuration was later moved into a shared directory:

```text
config/shared/clusters.xml
```

This removes duplicated configuration and makes scaling the cluster easier.

---

### Configuration mounting

Mounting the entire configuration directory:

```yaml
./config/clickhouse1:/etc/clickhouse-server/config.d:ro
```

caused the HTTP interface to stop responding.

Symptoms included:

* DBeaver connection reset
* `curl http://localhost:8123/ping` returned `Connection reset by peer`

Mounting individual XML files resolved the issue:

```yaml
./config/clickhouse1/config.xml:/etc/clickhouse-server/config.d/config.xml:ro
./config/shared/clusters.xml:/etc/clickhouse-server/config.d/clusters.xml:ro
```

This approach proved to be more reliable and easier to maintain.

---

### Keeper network binding

Distributed DDL (`ON CLUSTER`) initially failed because Keeper accepted connections only from localhost.

The issue was traced using:

```bash
netstat -ltn
```

The fix was placing:

```xml
<listen_host>0.0.0.0</listen_host>
```

directly under the root `<clickhouse>` element.

Placing `listen_host` inside `<keeper_server>` did **not** expose the service externally.

Once corrected, Keeper listened on:

```text
0.0.0.0:9181
```

allowing ClickHouse nodes to communicate successfully across the Docker bridge network.

---

## Current Status

✅ ClickHouse Keeper

✅ 1 Shard

✅ 2 Replicas

✅ ReplicatedMergeTree

✅ Distributed DDL (`ON CLUSTER`)

✅ Automatic replication

