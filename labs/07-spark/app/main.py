from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SparkLearningLab")
    .master("local[*]")
    .getOrCreate()
)

data = [
    (1, "Alice", 1200),
    (2, "Bob", 1800),
    (3, "Charlie", 900),
]

columns = ["id", "name", "amount"]

df = spark.createDataFrame(data, columns)

df.show()

print(f"Total records: {df.count()}")

spark.stop()
