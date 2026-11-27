# Data Engineering Lab

A hands-on data engineering lab built incrementally to explore modern data infrastructure, distributed systems, data processing, and data platform technologies.

The goal of this repository is to strengthen my understanding of data engineering by **building systems from scratch, experimenting with them, breaking them, and documenting what I learn along the way.**

Rather than following isolated tutorials, the lab evolves step by step. Each new component builds on concepts explored in previous labs.

---

## 🧪 Labs

| Lab | Focus | Status | Version |
|---|---|---|---|
| PostgreSQL | Containers, initialization, persistence, health checks | ✅ Complete | `v0.1.0` |
| ClickHouse | Columnar databases and analytical workloads | ✅ Complete | `v0.2.0` |
| ClickHouse Cluster | Replication, shards, replicas, cluster topology | ✅ Complete | `v0.3.0` |
| ClickHouse Distributed | Distributed tables and cross-node queries | ✅ Complete | `v0.4.0` |
| Kafka | Brokers, topics, partitions, producers, consumers | ✅ Complete | `v0.5.0` |
| Airflow | Workflow orchestration, DAGs, and task dependencies | ✅ Complete | `v0.6.0` |
| Spark | Distributed data processing, PySpark, DataFrames, transformations, and ETL | ✅ Complete | — |
| dbt | SQL transformations, data modeling, testing, source freshness, and documentation | ✅ Complete | — |
| Cloud | Cloud infrastructure and data services | 🚧 Planned | — |
| Kubernetes | Container orchestration and distributed deployments | 🚧 Planned | — |

---

## 🧠 Concepts Explored

The lab currently covers concepts including:

**Infrastructure and Databases**
- Docker and Docker Compose
- PostgreSQL
- ClickHouse
- Columnar databases and analytical workloads
- Distributed database architecture
- Sharding and replication
- Distributed tables
- Data persistence and container volumes
- Service health checks

**Streaming and Orchestration**
- Apache Kafka
- Brokers, topics, and partitions
- Producers and consumers
- Apache Airflow
- DAGs and task dependencies
- Workflow orchestration

**Data Processing and Transformation**
- Apache Spark and PySpark
- Spark DataFrames and Spark SQL
- Transformations and actions
- Lazy evaluation and distributed execution
- Data ingestion, cleaning, and validation
- ETL pipeline development
- dbt Core
- Source definitions and model dependencies
- Staging and mart layers
- SQL model materializations
- Data quality testing
- Source freshness monitoring
- dbt documentation and lineage visualization

**System and Development Fundamentals**
- Linux and container networking
- Git and feature branch workflows
- SQL and Python
- YAML-based configuration
- Database connectivity and troubleshooting

Future labs will expand the environment toward cloud infrastructure, advanced data processing, monitoring, and production-style data pipelines.

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
│   ├── 05-kafka/
│   ├── 06-airflow/
│   ├── 07-spark/
│   └── 08-dbt/
│
├── scripts/
└── README.md
```

Each lab contains its own documentation, configuration files, commands, experiments, and notes.

Labs are developed independently using feature branches, allowing each technology to be explored and validated before being integrated into the main branch.

---

## 🔭 Planned Topics

The next stages of the lab will explore:

- Databricks and its data engineering ecosystem
- Advanced Apache Spark concepts
- Incremental data processing and optimization
- dbt advanced features and orchestration
- Kubernetes
- Cloud infrastructure and data services
- Apache NiFi
- MongoDB
- HAProxy and load balancing
- Monitoring and observability
- End-to-end data pipelines

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

**Sources → Ingestion → Streaming → Processing → Storage → Transformation → Orchestration → Analytics**

The repository serves both as a learning environment and as a record of the engineering decisions, experiments, and lessons discovered while building it.
