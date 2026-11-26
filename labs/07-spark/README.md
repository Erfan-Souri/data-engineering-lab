# Apache Spark & PySpark Lab

A local Apache Spark environment for learning and experimenting with PySpark, DataFrame operations, and batch data processing.

## Environment

- Apache Spark 4.3.0
- Python / PySpark
- Java 17
- JupyterLab
- Docker & Docker Compose
- Spark running in local mode (`local[*]`)

## Project Structure

```text
07-spark/
├── app/             # PySpark application scripts
├── data/            # Input datasets
├── notebooks/       # Jupyter notebooks
├── output/          # Generated datasets and results
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Getting Started

From the `labs/07-spark` directory, build and start the environment:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

## Access JupyterLab

Follow the container logs:

```bash
docker compose logs -f
```

Look for the JupyterLab startup message containing a URL similar to:

```text
http://127.0.0.1:8888/lab?token=<YOUR_TOKEN>
```

Copy the URL from the logs and open it in your browser.

Alternatively, if JupyterLab is already running and the token is not visible in recent logs, inspect the container logs or run:

```bash
docker compose exec <service_name> jupyter server list
```

The default local address is:

```text
http://127.0.0.1:8888/lab
```

## Stopping the Environment

Stop and remove the containers:

```bash
docker compose down
```

## Notes

- Spark runs in local mode using all available cores inside the container.
- This environment is intended for local development and learning, not multi-node distributed deployment.
- Input datasets belong in the `data/` directory.
- Generated outputs belong in the `output/` directory.