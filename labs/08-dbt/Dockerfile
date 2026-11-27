FROM python:3.12-slim

WORKDIR /usr/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir dbt-postgres==1.11.0

ENTRYPOINT ["dbt"]
CMD ["--help"]