FROM spark:4.3.0-scala2.13-java17-python3-ubuntu

USER root

RUN python3 -m pip install --no-cache-dir \
    jupyterlab \
    ipykernel

ENV PYTHONPATH="/opt/spark/python/lib/pyspark.zip:/opt/spark/python/lib/py4j-0.10.9.9-src.zip"

WORKDIR /opt/spark-apps
