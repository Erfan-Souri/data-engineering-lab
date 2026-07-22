# ClickHouse Lab

## Overview

This lab demonstrates how to deploy and work with a single-node ClickHouse instance using Docker Compose.

The goal is to build a solid understanding of ClickHouse fundamentals, including its storage engine, column-oriented architecture, and analytical query capabilities. This lab serves as the foundation for more advanced topics such as replication, clustering, and distributed query processing.

---

## Objectives

* Deploy ClickHouse using Docker Compose
* Configure the server using environment variables
* Persist data using Docker volumes
* Monitor container health with Docker health checks
* Connect using DBeaver and the native ClickHouse client
* Create and query MergeTree tables
* Generate synthetic analytical datasets
* Explore ClickHouse system tables
* Understand how ClickHouse differs from PostgreSQL

---

## Features

* Single-node ClickHouse deployment
* Docker Compose configuration
* Environment-based configuration (`.env`)
* Persistent Docker volume
* Health check
* MergeTree storage engine
* Sample analytical dataset
* Documentation and learning notes

---

## Project Structure

```
02-clickhouse/
├── docker-compose.yml
├── README.md
├── .env.example
└── ...
```

---

## Running the Lab

Start the lab:

```bash
docker compose up -d
```

Stop the lab:

```bash
docker compose down
```

Remove the lab together with its persistent data:

```bash
docker compose down -v
```

---

## Lessons Learned

### ClickHouse Network Ports

ClickHouse exposes two TCP ports, each serving a different protocol:

| Port | Purpose                                                                     |
| ---- | --------------------------------------------------------------------------- |
| 8123 | HTTP interface for browsers, `curl`, REST clients, and many tools           |
| 9000 | Native ClickHouse binary protocol used by database clients and applications |

Although both use TCP, they implement different application-layer protocols.

---

### Secure Default User

Recent ClickHouse Docker images disable remote access for the `default` user unless credentials are explicitly configured.

To enable client connections, configure:

* `CLICKHOUSE_USER`
* `CLICKHOUSE_PASSWORD`

using environment variables.

---

### MergeTree Fundamentals

`MergeTree` is the primary storage engine used for analytical workloads in ClickHouse.

Key concepts learned:

* Data is written into immutable **parts**.
* Every `INSERT` creates one or more new parts.
* Background merge processes continuously combine smaller parts into larger ones.
* Merge process can be forced using OPTIMIZE TABLE {table_name} FINAL;.
* Tables must define an `ORDER BY` key.
* The `ORDER BY` key determines the physical sort order of the data and is used to build ClickHouse's sparse primary index.
* This storage design allows ClickHouse to execute large analytical queries efficiently.

---

## Future Improvements

* Multi-node ClickHouse cluster
* ClickHouse Keeper
* Replication
* Sharding
* Distributed tables
* Materialized Views
* Performance experiments
* Production-style architecture

---

This lab is part of my personal **Data Engineering Lab**, where I build and document modern data platform technologies from first principles while exploring their architecture and internal design.
