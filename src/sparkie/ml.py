import logging
import sys

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession

from . import config

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    spark = (
        SparkSession.builder.appName("toy-linear-regression")
        .master(config.SPARK_MASTER_URL)
        .getOrCreate()
    )

    # Toy data: y = 2x + 1 with some noise
    data = [
        (1.0, 2.9),
        (2.0, 5.1),
        (3.0, 6.8),
        (4.0, 9.2),
        (5.0, 11.1),
        (6.0, 12.8),
        (7.0, 15.3),
        (8.0, 17.0),
        (9.0, 18.9),
        (10.0, 21.2),
    ]
    columns = ["x", "y"]

    df = spark.createDataFrame(data, columns)

    logger.info("Raw data:")
    df.show()

    assembler = VectorAssembler(inputCols=["x"], outputCol="features")
    df = assembler.transform(df)

    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    lr = LinearRegression(featuresCol="features", labelCol="y")
    model = lr.fit(train_df)

    logger.info(f"Coefficient: {model.coefficients[0]:.4f}")
    logger.info(f"Intercept: {model.intercept:.4f}")

    predictions = model.transform(test_df)

    logger.info("Predictions on test set:")
    predictions.select("x", "y", "prediction").show()

    evaluator = RegressionEvaluator(
        labelCol="y", predictionCol="prediction", metricName="rmse"
    )
    rmse = evaluator.evaluate(predictions)
    logger.info(f"RMSE on test data: {rmse:.4f}")

    spark.stop()


if __name__ == "__main__":
    main()
