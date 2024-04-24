from pyspark.sql import SparkSession
from pyspark.sql.types import TimestampType, StructType, StructField, IntegerType, FloatType, StringType
from pyspark.sql.functions import from_json, col, udf, year, month, dayofmonth, date_format
import uuid

def save_to_cassandra(writeDF, epoch_id):
    print("Printing epoch_id: ")
    print(epoch_id)
  
    writeDF.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode('append') \
        .options(table="sales_table", keyspace="sales_ks") \
        .save()
  
    print(epoch_id, "saved to Cassandra")

schema = StructType([
    StructField("pos_id", IntegerType()),
    StructField("pos_name", StringType()),
    StructField("article", StringType()),
    StructField("quantity", FloatType()),
    StructField("unit_price", FloatType()),
    StructField("total", FloatType()),
    StructField("sale_type", StringType()),
    StructField("payment_mode", StringType()),
    StructField("sale_time", StringType()),
])
spark = SparkSession \
    .builder \
    .appName("Spark Kafka Streaming Data Pipeline") \
    .master("local[*]") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.cassandra.connection.port", "9042") \
    .config("spark.cassandra.auth.username", "cassandra") \
    .config("spark.cassandra.auth.password", "cassandra") \
    .config("spark.driver.host", "localhost") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

input_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "Sales") \
    .option("startingOffsets", "earliest") \
    .load() 

expanded_df = input_df \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("sales")) \
    .select("sales.*") \
    .withColumn("year", year("sale_time")) \
    .withColumn("month", month("sale_time")) \
    .withColumn("day_of_month", dayofmonth("sale_time")) \
    .withColumn("week_number", ((col("day_of_month") - 1) / 7 + 1).cast("int")) \
    .withColumn("day_of_week", date_format(col("sale_time"), "EEEE")) \
    .drop("day_of_month")  

uuid_udf = udf(lambda: str(uuid.uuid4()), StringType()).asNondeterministic()

query1 = expanded_df \
    .withColumn("uuid", uuid_udf()) \
    .writeStream \
    .trigger(processingTime="1 seconds") \
    .foreachBatch(save_to_cassandra) \
    .outputMode("update") \
    .start()

query1.awaitTermination()
