from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper

from . import config


def main():
    spark = (
        SparkSession.builder.appName("dummy-job")
        .master(config.SPARK_MASTER_URL)
        .getOrCreate()
    )

    data = [
        ("alice", 34, "oslo"),
        ("bob", 45, "bergen"),
        ("carol", 29, "trondheim"),
        ("dave", 51, "oslo"),
    ]
    columns = ["name", "age", "city"]

    df = spark.createDataFrame(data, columns)

    print("Initial DataFrame:")
    df.show()

    result = (
        df.filter(col("age") > 30)
        .withColumn("name_upper", upper(col("name")))
        .groupBy("city")
        .count()
    )

    print("Result DataFrame:")
    result.show()

    spark.stop()


if __name__ == "__main__":
    main()
