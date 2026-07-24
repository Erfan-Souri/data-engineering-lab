# ClickHouse Cluster Lab (2 Shards × 2 Replicas)

## Overview

This lab extends the previous single-shard ClickHouse cluster by introducing a distributed architecture with **2 shards** and **2 replicas** coordinated by **ClickHouse Keeper**.

The goal is to understand how ClickHouse scales horizontally, how replication differs from sharding, and how distributed queries are executed across multiple nodes.

---

## Objectives

* Build a ClickHouse cluster using Docker Compose
* Configure ClickHouse Keeper for cluster coordination
* Deploy a **2-shard, 2-replica** topology
* Configure cluster metadata using macros and shared cluster configuration
* Create replicated tables using `ReplicatedMergeTree`
* Create distributed tables using the `Distributed` engine
* Execute distributed DDL using `ON CLUSTER`
* Understand shard routing and replica synchronization
* Verify cluster behavior during node failures

---

## Cluster Topology

```
                    ClickHouse Keeper
                          │
         ┌────────────────┴────────────────┐
         │                                 │
     Shard 1                           Shard 2
  ┌──────────────┐                 ┌──────────────┐
  │ clickhouse1  │                 │ clickhouse3  │
  │ clickhouse2  │                 │ clickhouse4  │
  └──────────────┘                 └──────────────┘
```

* **Shards** distribute different portions of the data.
* **Replicas** store identical copies of the data for high availability.
* The `Distributed` engine provides a single logical table for querying the entire cluster.

---

## Project Structure

```
03-clickhouse-cluster/
├── config/
│   ├── keeper/
│   ├── clickhouse1/
│   ├── clickhouse2/
│   ├── clickhouse3/
│   ├── clickhouse4/
│   └── shared/
├── docker-compose.yml
├── sql/
├── docs/
└── README.md
```

Shared cluster configuration is stored separately from node-specific macros to simplify scaling and maintenance.

---

## What I Learned

During this lab I learned how ClickHouse operates as a distributed database instead of a standalone server.

Key concepts explored include:

* ClickHouse Keeper and cluster coordination
* Shards versus replicas
* Cluster-wide DDL using `ON CLUSTER`
* `ReplicatedMergeTree`
* `Distributed` tables
* Sharding using a hash function
* Replica synchronization
* Distributed query execution
* Cluster metadata through macros
* Failure tolerance when a replica becomes unavailable

---

## Lessons Learned

### Distributed tables

The `Distributed` engine does not store data itself. Instead, it routes INSERT operations to the appropriate shard and merges query results from all shards into a single result set.

---

### Replication vs Sharding

Replication and sharding solve different problems.

* **Replication** improves availability by storing identical copies of data.
* **Sharding** improves scalability by distributing different portions of data across multiple nodes.

---

### Cluster Authentication

Distributed queries require ClickHouse servers to authenticate with one another.

When custom users are configured, every replica entry inside `clusters.xml` must include the corresponding user and password. Otherwise distributed queries fail with authentication errors even though client connections succeed.

---

### Keeper Network Configuration

ClickHouse Keeper must listen on an external interface for other ClickHouse nodes to communicate with it.

The following configuration is required at the root `<clickhouse>` level:

```xml
<listen_host>0.0.0.0</listen_host>
```

Placing this option under `<keeper_server>` is not sufficient and results in Keeper listening only on localhost, preventing distributed DDL operations such as `CREATE TABLE ... ON CLUSTER`.

---

### Configuration Organization

Node-specific configuration (macros) and shared cluster configuration should be separated.

This avoids duplicating cluster definitions across nodes and makes future expansion significantly easier.

---

## Result

The final cluster successfully provides:

* 2 shards
* 2 replicas per shard
* ClickHouse Keeper coordination
* ReplicatedMergeTree tables
* Distributed tables
* Cluster-wide DDL
* Distributed reads and writes
* Replica failover during node outages

This lab serves as the foundation for larger distributed data engineering environments and future streaming pipelines.
