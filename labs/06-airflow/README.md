# 06 - Apache Airflow

## Overview

This lab introduces **Apache Airflow** by building a small but realistic ETL pipeline from scratch.

Instead of focusing on every Airflow feature, the objective is to understand how Airflow orchestrates workflows, communicates between tasks, manages metadata, and coordinates an ETL pipeline while keeping each task independent.

The project intentionally starts with a minimal pipeline and evolves step by step into a more production-like workflow using PostgreSQL.

---
# Architecture

```
                           +----------------------+
                           |     Airflow UI       |
                           +----------+-----------+
                                      |
                                      v
                           +----------------------+
                           |      Scheduler       |
                           +----------+-----------+
                                      |
                                      v
                           +----------------------+
                           |    DAG Processor     |
                           +----------+-----------+
                                      |
                                      v

                                orders_etl DAG

      +-----------+      +-------------+      +--------+      +----------+
      |  Extract  | ---> | Transform   | ---> |  Load  | ---> | Cleanup  |
      +-----------+      +-------------+      +--------+      +----------+
             |                                   |
             |                                   |
             +------ Creates Dynamic Stage ------+
                       stg_orders_<run_id>

                                      |
                                      v

                               PostgreSQL Database

                 public schema              lab schema
             -------------------     -------------------------
             Airflow Metadata        customer_orders
             dag_run                reporting_orders
             task_instance          stg_orders_<run_id>
             xcom
```

---

# Project Structure

```
06-airflow/
│
├── dags/
│   ├── first_pipeline.py
│   └── orders_etl.py
│
├── postgres/
│   └── init/
│       ├── schema.sql
│       └── seed.sql
│
├── docker-compose.yml
│
└── README.md
```

---

# Running the Lab

Start the environment:

```bash
docker compose up -d
```

Stop the environment:

```bash
docker compose down
```

Completely reset everything:

```bash
docker compose down -v
docker compose up -d
```

---

# Airflow Login

This lab uses **Simple Authentication Manager**.

Since the password is automatically generated during initialization, retrieve it using:

```bash
docker exec -it airflow-api-server \
cat /opt/airflow/simple_auth_manager_passwords.json.generated
```

Username:

```
admin
```

---

# Airflow Connection

The PostgreSQL connection is configured entirely through Docker Compose using an environment variable.

```
AIRFLOW_CONN_POSTGRES_LAB
```

No manual connection creation inside Airflow is required.

---

# Airflow Variables

Cleanup behavior is configurable through an Airflow Variable.

```
cleanup_enabled
```

Configured via Docker Compose:

```
AIRFLOW_VAR_CLEANUP_ENABLED=false
```

Possible values:

```
true
false
```

This allows the pipeline to run in two modes:

**Learning Mode**

- Keep staging tables
- Inspect intermediate data

**Production Mode**

- Automatically remove staging tables after successful execution

---

# ETL Pipeline

## Extract

Responsibilities:

- Validate source data exists.
- Create a unique staging table.
- Return the staging table name using XCom.

---

## Transform

Responsibilities:

- Remove invalid rows.
- Operate directly on the staging table.
- Preserve the staging table name through XCom.

---

## Load

Responsibilities:

- Execute inside a database transaction.
- Truncate reporting table.
- Insert transformed data.
- Commit on success.
- Rollback on failure.

---

## Cleanup

Responsibilities:

- Controlled through Airflow Variables.
- Executes only after successful pipeline completion.
- Removes temporary staging tables.

---

# Dynamic Staging

Instead of sharing a single staging table

```
stg_orders
```

every pipeline execution creates its own isolated staging table.

Example:

```
stg_orders_20260806T153012
```

Benefits:

- No collisions between runs.
- Easier debugging.
- Parallel-safe execution.
- Temporary resources are isolated.

---

# XCom Usage

XCom is intentionally **not** used for passing datasets.

Instead it passes lightweight metadata:

```
staging_table_name
```

Example:

```
stg_orders_20260806T153012
```

This reflects how Airflow is typically used in production systems, where XCom transports metadata rather than large datasets.

---

# PostgreSQL Schema

Business tables are isolated from Airflow metadata using a dedicated schema.

```
public
```

Contains:

- dag_run
- task_instance
- xcom
- Airflow metadata tables

```
lab
```

Contains:

- customer_orders
- reporting_orders
- staging tables

This keeps infrastructure metadata separated from business data.

---

# Design Decisions

## Why Dynamic Staging?

Each DAG run owns its own temporary resources.

Advantages:

- Isolation
- Easier debugging
- Safe parallel execution

---

## Why XCom?

Only lightweight metadata is exchanged between tasks.

Large datasets remain inside PostgreSQL.

---

## Why Transactions?

Prevent partial loads into reporting tables.

The reporting table should either contain a complete successful load or remain unchanged.

---

## Why Cleanup?

Temporary resources should not accumulate indefinitely.

---

## Why Cleanup is Configurable?

During learning, keeping staging tables makes debugging much easier.

In production, temporary resources should be removed automatically.

---

## Why Trigger Rules?

Cleanup should execute **only** after a successful pipeline.

Failed pipelines intentionally preserve staging tables for investigation.

---

# Debugging Lessons Learned

## Invalid Execution API Authentication

### Symptoms

- Tasks immediately failed.
- Task hostname remained empty.
- Worker logs were unavailable.
- Tasks stayed queued before failing.

### Investigation

1. Scheduler logs
2. LocalExecutor configuration
3. Scheduler log server (8793)
4. Docker DNS
5. task_instance metadata
6. Raw task logs

Eventually the following error was identified:

```
ServerResponseError:
Invalid auth token
```

### Root Cause

Airflow services were using different JWT secrets.

### Resolution

Configure a shared:

```
AIRFLOW__API_AUTH__JWT_SECRET
```

across every Airflow service.

---

## Useful Debugging Commands

Retrieve generated admin password:

```bash
docker exec -it airflow-api-server \
cat /opt/airflow/simple_auth_manager_passwords.json.generated
```

Inspect scheduler logs:

```bash
docker logs airflow-scheduler
```

Inspect DAG processor logs:

```bash
docker logs airflow-dag-processor
```

Inspect Airflow configuration:

```bash
docker exec -it airflow-scheduler airflow info
```

Inspect task logs:

```
/opt/airflow/logs/
```

---

# Evolution of the Lab

The project was intentionally developed incrementally.

1. Initialize Airflow infrastructure.
2. Configure PostgreSQL.
3. Build the first DAG.
4. Create a simple ETL pipeline.
5. Generate realistic seed data.
6. Separate business tables into a dedicated schema.
7. Introduce dynamic staging.
8. Pass metadata through XCom.
9. Add configurable cleanup using Airflow Variables.
10. Execute cleanup only after successful pipeline completion.

Each major concept was introduced in its own Git commit to keep the repository history educational and easy to follow.

---

# Key Concepts Learned

- Airflow Architecture
- DAGs
- TaskFlow API
- Python Tasks
- XCom
- PostgresHook
- Airflow Variables
- Trigger Rules
- Retry Behavior
- Transactions
- Dynamic Staging
- Resource Cleanup
- PostgreSQL Schemas
- Metadata Database
- Airflow Debugging

---

# Future Improvements

This lab intentionally stops after building a minimal production-style ETL orchestration workflow.

Possible future extensions include:

- Scheduling
- Branching
- Dynamic Task Mapping
- Sensors
- Task Groups
- Kafka Integration
- ClickHouse Integration
- dbt
- Remote Logging
- Kubernetes Executor
- Celery Executor

---

# Final Thoughts

The goal of this project was **not** to learn every Airflow feature.

Instead, the objective was to understand how Airflow orchestrates an ETL pipeline, how tasks communicate through metadata, how temporary resources are managed, and how thoughtful workflow design improves reliability and maintainability.

This lab will serve as the foundation for future projects where Airflow orchestrates larger data platform components such as Kafka, ClickHouse, and additional data engineering services.