Docker command	Meaning
docker compose run --rm dbt debug	Runs dbt debug
docker compose run --rm dbt init dbt_learning	Runs dbt init dbt_learning
docker compose run --rm dbt --help	Runs dbt --help

todo in readme: add .dbt/profiles.yml to root project 
One correction to your thought: profiles.yml should generally not be committed, even if it doesn't currently contain a real production password. It contains connection details and may eventually contain sensitive credentials. We'll document the expected profile configuration separately if needed.

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