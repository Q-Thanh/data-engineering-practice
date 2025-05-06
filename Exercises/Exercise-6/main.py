from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
import zipfile
import os


def unzip_data(input_dir="data", output_dir="unzipped_data"):
    os.makedirs(output_dir, exist_ok=True)
    for fname in os.listdir(input_dir):
        if fname.endswith(".zip"):
            with zipfile.ZipFile(os.path.join(input_dir, fname), 'r') as zip_ref:
                zip_ref.extractall(output_dir)


def load_and_standardize_data(spark, path):
    files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".csv")]
    dfs = []

    for file in files:
        if "2019_Q4" in file:
            df_2019 = spark.read.option("header", True).csv(file)

            df_2019_std = df_2019.selectExpr([
                "trip_id as ride_id",
                "start_time as started_at",
                "end_time as ended_at",
                "from_station_name as start_station_name",
                "from_station_id as start_station_id",
                "to_station_name as end_station_name",
                "to_station_id as end_station_id",
                "usertype"
            ]).withColumn("rideable_type", lit("docked_bike")) \
              .withColumn("start_lat", lit(None).cast("double")) \
              .withColumn("start_lng", lit(None).cast("double")) \
              .withColumn("end_lat", lit(None).cast("double")) \
              .withColumn("end_lng", lit(None).cast("double")) \
              .withColumn("member_casual", when(col("usertype") == "Subscriber", "member")
                                         .when(col("usertype") == "Customer", "casual")
                                         .otherwise("unknown")) \
              .drop("usertype")

            dfs.append(df_2019_std)

        elif "2020_Q1" in file:
            df_2020 = spark.read.option("header", True).csv(file)
            dfs.append(df_2020)

    # Gộp các DataFrame lại
    return dfs[0].unionByName(dfs[1])


def average_trip_duration_per_day(df):
    return df.withColumn("date", to_date("started_at")) \
             .groupBy("date") \
             .agg(avg("tripduration").alias("avg_trip_duration"))


def trip_count_per_day(df):
    return df.withColumn("date", to_date("started_at")) \
             .groupBy("date") \
             .count().withColumnRenamed("count", "trip_count")


def most_popular_start_station_per_month(df):
    return df.withColumn("month", date_format("started_at", "yyyy-MM")) \
             .groupBy("month", "start_station_name") \
             .count() \
             .withColumn("rank", dense_rank().over(Window.partitionBy("month").orderBy(desc("count")))) \
             .filter(col("rank") == 1)


def top_3_stations_per_day_last_2_weeks(df):
    latest_date = df.select(to_date("started_at").alias("date")).agg(max("date")).first()["max(date)"]
    last_date = date_sub(lit(latest_date), 14)

    df_recent = df.withColumn("date", to_date("started_at")) \
                  .filter(col("date") >= last_date)

    return df_recent.groupBy("date", "start_station_name") \
                    .count() \
                    .withColumn("rank", dense_rank().over(Window.partitionBy("date").orderBy(desc("count")))) \
                    .filter(col("rank") <= 3)


def avg_trip_duration_by_gender(df):
    return df.groupBy("gender").agg(avg("tripduration").alias("avg_duration"))


def top_10_ages_longest_and_shortest_trips(df):
    current_year = 2019
    df_with_age = df.withColumn("age", current_year - col("birthyear"))
    longest = df_with_age.orderBy(desc("tripduration")).select("age").dropna().limit(1000)
    shortest = df_with_age.orderBy("tripduration").select("age").dropna().limit(1000)

    top_long = longest.groupBy("age").count().orderBy(desc("count")).limit(10)
    top_short = shortest.groupBy("age").count().orderBy(desc("count")).limit(10)

    return top_long.withColumn("type", lit("longest")), top_short.withColumn("type", lit("shortest"))


def write_report(df, filename):
    df.coalesce(1).write.csv(f"reports/{filename}", header=True, mode="overwrite")


def main():
    spark = SparkSession.builder.appName("Exercise6").getOrCreate()

    unzip_data()
    df = load_and_standardize_data(spark, "unzipped_data")

    os.makedirs("reports", exist_ok=True)

    write_report(average_trip_duration_per_day(df), "avg_trip_duration_per_day")
    write_report(trip_count_per_day(df), "trip_count_per_day")
    write_report(most_popular_start_station_per_month(df), "most_popular_start_station_per_month")
    write_report(top_3_stations_per_day_last_2_weeks(df), "top_3_stations_last_2_weeks")
    write_report(avg_trip_duration_by_gender(df), "avg_trip_duration_by_gender")

    top_long, top_short = top_10_ages_longest_and_shortest_trips(df)
    write_report(top_long, "top10_ages_longest")
    write_report(top_short, "top10_ages_shortest")


if __name__ == "__main__":
    main()
