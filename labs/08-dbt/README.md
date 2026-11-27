# dbt Learning Lab

A Docker-based environment for learning dbt Core with PostgreSQL.

## Prerequisites

- Docker Desktop
- Docker Compose
- A running PostgreSQL instance
- Git

## Project Structure

- `Dockerfile`: Defines the dbt execution environment.
- `docker-compose.yml`: Runs dbt in Docker.
- `config/profiles.example.yml`: Example dbt connection profile.
- `.dbt/profiles.yml`: Local dbt connection configuration (not tracked).
- `dbt_learning/`: Main dbt project.

## Initial Setup

### 1. Configure environment variables

Create a `.env` file in the project root:

```dotenv
POSTGRES_PASSWORD=postgres
```

Replace the password with the credentials of your PostgreSQL instance.

### 2. Configure the dbt profile

Create the local profile directory and copy the example:

```bash
mkdir -p .dbt
cp config/profiles.example.yml .dbt/profiles.yml
```

The profile name must match the `profile` value in `dbt_learning/dbt_project.yml`.

### 3. Configure the database connection

The default configuration uses:

- Host: `host.docker.internal`
- Port: `5432`
- Database: `appdb`
- User: `postgres`
- Schema: `dbt_dev`

Update `.dbt/profiles.yml` and `.env` if your PostgreSQL configuration differs.

Ensure PostgreSQL is running and accessible from Docker.

### 4. Build the dbt image

```bash
docker compose build
```

### 5. Verify the connection

```bash
docker compose run --rm dbt debug \
  --project-dir dbt_learning \
  --profiles-dir /root/.dbt
```

A successful connection should report `All checks passed!`.

## Running dbt

Run dbt commands through Docker Compose:

```bash
docker compose run --rm dbt --help
```

For example:

```bash
docker compose run --rm dbt run \
  --project-dir dbt_learning \
  --profiles-dir /root/.dbt
```

## Security

Do not commit `.env` or `.dbt/profiles.yml`. They contain local connection configuration and potentially sensitive credentials.

erfansouri@Mac 08-dbt % docker compose run --rm dbt run \
  --project-dir dbt_learning \
  --profiles-dir /root/.dbt \
  --select stg_employees
#####################
# dbt Learning Lab

A hands-on learning environment for **dbt Core**, PostgreSQL, and Docker Compose.

This lab demonstrates how to build SQL-based data transformations, organize models into layers, validate data quality, monitor source freshness, and generate interactive project documentation.

## Architecture

```text
PostgreSQL
└── appdb
    └── public
        └── employees
              |
              v
        dbt source definition
              |
              v
        Staging layer
        └── stg_employees (view)
              |
              v
        Mart layer
        └── employees_by_department (table)
              |
              v
        PostgreSQL
        └── dbt_dev schema
```

dbt manages the transformation dependencies using `source()` and `ref()`.

## Technology Stack

- dbt Core
- dbt PostgreSQL adapter
- PostgreSQL 17
- Docker
- Docker Compose
- SQL and YAML

## Project Structure

```text
08-dbt/
├── .dbt/
│   └── profiles.yml
├── config/
│   └── profiles.example.yml
├── dbt_learning/
│   ├── models/
│   │   ├── staging/
│   │   │   └── employees/
│   │   │       ├── _sources.yml
│   │   │       └── stg_employees.sql
│   │   ├── marts/
│   │   │   └── employees/
│   │   │       └── employees_by_department.sql
│   │   └── _models.yml
│   └── dbt_project.yml
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

Local configuration and generated files such as `.env`, `.dbt/`, and `dbt_learning/target/` are excluded from Git.

## Prerequisites

- Docker Desktop and Docker Compose
- Git
- A running PostgreSQL instance
- PostgreSQL database and credentials accessible from the dbt container

This lab reuses the PostgreSQL environment from `labs/01-postgres`.

### PostgreSQL configuration

| Setting | Value |
|---|---|
| Database | `appdb` |
| Source schema | `public` |
| Source table | `employees` |
| dbt target schema | `dbt_dev` |
| PostgreSQL port | `5432` |

The source table contains employee information and a `created_at` timestamp used for source freshness monitoring.

## Initial Setup

Run these commands from the `labs/08-dbt` directory.

### 1. Start PostgreSQL

If using the existing PostgreSQL lab:

```bash
docker compose -f ../01-postgres/docker-compose.yml up -d
```

Verify that the container is healthy:

```bash
docker compose -f ../01-postgres/docker-compose.yml ps
```

### 2. Configure environment variables

Create a local `.env` file:

```dotenv
POSTGRES_PASSWORD=postgres
```

Replace the password with the password configured for your PostgreSQL instance.

### 3. Configure the dbt profile

Create the local profile directory:

```bash
mkdir -p .dbt
```

Copy the example configuration:

```bash
cp config/profiles.example.yml .dbt/profiles.yml
```

The profile name must match the `profile` value in `dbt_learning/dbt_project.yml`.

Update the connection settings if your PostgreSQL environment differs.

### 4. Build the dbt Docker image

```bash
docker compose build
```

### 5. Verify the installation and database connection

```bash
docker compose run --rm dbt debug \
  --project-dir dbt_learning \
  --profiles-dir /root/.dbt
```

A successful result should report:

```text
All checks passed!
```

## Running dbt

All dbt commands are executed through Docker Compose.

### Initilize dbt 
```bash
docker compose run --rm dbt init dbt_learning
```

### Build models

```bash
docker compose run --rm dbt run \
  --project-dir dbt_learning \
  --profiles-dir /root/.dbt
```

### Run data quality tests

```bash
docker compose run --rm dbt test \
  --project-dir dbt_learning \
  --profiles-dir /root/.dbt
```

### Build models and execute associated tests

```bash
docker compose run --rm dbt build \
  --project-dir dbt_learning \
  --profiles-dir /root/.dbt
```

`dbt build` builds selected resources in dependency order and runs their associated tests. Source freshness is a separate command.

### Check source freshness

```bash
docker compose run --rm dbt source freshness \
  --project-dir dbt_learning \
  --profiles-dir /root/.dbt
```

The source freshness configuration currently uses:

- Warning threshold: 24 hours
- Error threshold: 48 hours

The `created_at` column represents the source record loading timestamp.

## dbt Documentation

This project uses dbt Docs to generate a local documentation website and visualize model dependencies.

### 1. Generate documentation

```bash
docker compose run --rm dbt docs generate \
  --project-dir dbt_learning \
  --profiles-dir /root/.dbt
```

Generated artifacts are written to:

```text
dbt_learning/target/
```

### 2. Start the documentation server

```bash
docker compose run --rm --service-ports dbt docs serve \
  --project-dir dbt_learning \
  --profiles-dir /root/.dbt \
  --host 0.0.0.0 \
  --port 8580 \
  --no-browser
```

### 3. Open the documentation website

Visit:

http://localhost:8580

The documentation interface provides model information, source metadata, and an interactive lineage graph.

Stop the server with `Ctrl+C`.

Regenerate the documentation after changing models, sources, or descriptions.

## Key dbt Concepts Covered

| Concept | Description |
|---|---|
| Sources | Define existing database tables as upstream data sources |
| Models | SQL transformations managed by dbt |
| `source()` | References an upstream source |
| `ref()` | References another dbt model and establishes a dependency |
| DAG | Directed Acyclic Graph representing model dependencies |
| Materializations | Control whether a model becomes a view, table, incremental model, or ephemeral resource |
| Tests | Validate data assumptions such as uniqueness and non-null values |
| Source freshness | Detect stale upstream data |
| dbt Docs | Generate project documentation and visualize lineage |

## Important Notes

- `dbt_project.yml` defines the dbt project configuration.
- `profiles.yml` defines the database connection.
- `.dbt/profiles.yml` and `.env` must be created locally and should not be committed.
- `config/profiles.example.yml` is the tracked profile template.
- `dbt build` does not automatically execute source freshness checks.
- `target/`, `logs/`, and `dbt_packages/` contain generated or downloaded files and should not be committed.
- `dbt init` is only needed when creating a new dbt project, not when cloning this existing project.

## Learning Scope

This lab focuses on dbt fundamentals and a small PostgreSQL-based transformation pipeline.

Advanced topics such as incremental models, snapshots, macros, custom generic tests, and orchestration with Airflow can be explored in subsequent labs.