# PostgreSQL Lab

## Overview

This lab demonstrates how to deploy and manage a PostgreSQL 17 database using Docker Compose.

It is the first milestone of my **Data Engineering Lab**, where I recreate the technologies and workflows I have used professionally while documenting my learning journey.

---

## Objectives

The goal of this lab is to understand:

- Docker Compose fundamentals
- PostgreSQL container deployment
- Environment variable management with `.env`
- Persistent Docker volumes
- Automatic database initialization using `init.sql`
- Docker health checks
- Git workflow using feature branches and Pull Requests

---

## Project Structure

```text
01-postgres/
├── docker-compose.yml
├── init.sql
├── .env.example
└── README.md
```

---

## Features

- PostgreSQL 17
- Docker Compose
- Named Docker volume
- Environment variables
- Automatic schema creation
- Sample dataset (1000 randomly generated employees)
- Container health check

---

## Getting Started

Clone the repository and navigate to the PostgreSQL lab.

Create your local environment file:

```bash
cp .env.example .env
```

Start the lab:

```bash
docker compose up -d
```

Verify the container:

```bash
docker compose ps
```

The PostgreSQL container should eventually report a **healthy** status.

---

## Connecting to PostgreSQL

Using psql:

```bash
psql -U postgres -d appdb
```

Verify the generated dataset:

```sql
SELECT COUNT(*) FROM employees;
```

Expected result:

```text
1000
```

---

## Useful Commands

Start the lab:

```bash
docker compose up -d
```

Stop the lab:

```bash
docker compose down
```

Stop and remove all data:

```bash
docker compose down -v
```

List Docker volumes:

```bash
docker volume ls
```

Remove a volume:

```bash
docker volume rm <volume_name>
```

---

## Lessons Learned

During this lab I learned:

- Docker Compose provides a cleaner way to manage multi-container applications.
- Environment variables should be separated from configuration files.
- PostgreSQL executes initialization scripts only during the first database initialization.
- Named Docker volumes preserve data between container restarts.
- Removing a volume recreates the database from scratch.
- Docker health checks verify service readiness instead of only checking whether a container is running.
- Connecting to the correct PostgreSQL database is important when working with initialization scripts.