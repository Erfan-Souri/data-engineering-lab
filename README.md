# Data Engineering Lab

A hands-on data engineering lab built incrementally to explore modern data infrastructure, distributed systems, and data platform technologies.

The goal of this repository is to strengthen my understanding of data engineering by **building systems from scratch, experimenting with them, breaking them, and documenting what I learn along the way.**

Rather than following isolated tutorials, the lab evolves step by step. Each new component builds on concepts explored in previous labs.

---

## 🧪 Labs

| Lab                    | Focus                                                  | Status     | Version  |
| ---------------------- | ------------------------------------------------------ | ---------- | -------- |
| PostgreSQL             | Containers, initialization, persistence, health checks | ✅ Complete | `v0.1.0` |
| ClickHouse             | Columnar databases and analytical workloads            | ✅ Complete | `v0.2.0` |
| ClickHouse Cluster     | Replication, shards, replicas, cluster topology        | ✅ Complete | `v0.3.0` |
| ClickHouse Distributed | Distributed tables and cross-node queries              | ✅ Complete | `v0.4.0` |
| Kafka                  | Brokers, topics, partitions, producers, consumers      | ✅ Complete | `v0.5.0` |
| Airflow                | Workflow orchestration and DAGs                        | 🚧 Planned | —        |
| Cloud                  | Cloud infrastructure and data services                 | 🚧 Planned | —        |
| Kubernetes             | Container orchestration and distributed deployments    | 🚧 Planned | —        |

---

## 🧠 Concepts Explored

The lab currently covers concepts including:

* Docker and Docker Compose
* PostgreSQL
* ClickHouse
* Distributed database architecture
* Sharding and replication
* Distributed tables
* Apache Kafka
* Topics and partitions
* Producers and consumers
* Data persistence and container volumes
* Service health checks
* Linux and container networking

Future labs will expand the environment toward orchestration, cloud infrastructure, monitoring, and production-style data pipelines.

---

## 🗂 Repository Structure

```text
data-engineering-lab/
├── docs/
│   ├── architecture/
│   ├── images/
│   └── notes/
│
├── labs/
│   ├── 01-postgres/
│   ├── 02-clickhouse/
│   ├── 03-clickhouse-cluster/
│   ├── 04-clickhouse-distributed/
│   └── 05-kafka/
│
├── scripts/
└── README.md
```

Each lab contains its own documentation, configuration files, commands, experiments, and notes.

---

## 🔭 Planned Topics

The next stages of the lab will explore:

* Apache Airflow
* Kubernetes
* Cloud infrastructure
* Apache NiFi
* MongoDB
* HAProxy and load balancing
* Monitoring and observability
* End-to-end data pipelines

The long-term goal is to gradually connect these technologies into a more complete data platform rather than treating them as isolated tools.

---

## 💡 Lab Philosophy

Every component is introduced individually before being integrated with the rest of the environment.

For each technology, I aim to understand:

1. **What problem does it solve?**
2. **How does it work internally?**
3. **How do I deploy and operate it?**
4. **How does it interact with other components?**
5. **What breaks, and how do I troubleshoot it?**

The objective is not simply to create working containers or copy configurations, but to understand the engineering decisions behind the systems being built.

---

## 🚀 Direction

As the lab grows, the individual components will gradually be connected into realistic data engineering workflows:

**Sources → Ingestion → Streaming → Processing → Storage → Orchestration → Analytics**

The repository serves both as a learning environment and as a record of the engineering decisions, experiments, and lessons discovered while building it.
