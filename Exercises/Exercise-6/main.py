from pyspark.sql import SparkSession
<<<<<<< Updated upstream
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
=======
from pyspark.sql.functions import avg, count, to_date, date_format, col, desc, expr
from pyspark.sql.window import Window
import zipfile
import glob
import os

# Hàm giải nén các file zip trong thư mục data vào thư mục output
def unzip_files(data_folder, output_folder):
    # Tạo thư mục giải nén nếu chưa có
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Tìm tất cả file .zip trong thư mục data
    zip_files = glob.glob(f"{data_folder}/*.zip")
    for zip_path in zip_files:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            print(f"Unzipping: {zip_path} into {output_folder}")
            zip_ref.extractall(output_folder)
>>>>>>> Stashed changes


# Hàm đọc dữ liệu CSV từ thư mục đã giải nén
def read_data(spark, unzipped_folder):
    # Đọc tất cả file CSV trong thư mục đã giải nén
    csv_files = glob.glob(f"{unzipped_folder}/*.csv")
    df = spark.read.csv(csv_files, header=True, inferSchema=True)  # Đọc CSV và tự suy đoán schema
    return df


# Báo cáo: Thời lượng chuyến đi trung bình theo ngày
def average_trip_duration_per_day(df, reports_folder):
    result = (
        df.withColumn("date", to_date("start_time"))  # Thêm cột ngày từ start_time
          .groupBy("date")
          .agg(avg("tripduration").alias("avg_trip_duration"))  # Tính trung bình thời lượng
          .orderBy("date")
    )
    # Lưu kết quả ra file CSV
    result.write.csv(f"{reports_folder}/average_trip_duration_per_day", header=True, mode="overwrite")


# Báo cáo: Số chuyến đi theo ngày
def trips_per_day(df, reports_folder):
    result = (
        df.withColumn("date", to_date("start_time"))
          .groupBy("date")
          .agg(count("*").alias("trip_count"))  # Đếm số chuyến mỗi ngày
          .orderBy("date")
    )
    result.write.csv(f"{reports_folder}/trips_per_day", header=True, mode="overwrite")


# Báo cáo: Trạm xuất phát phổ biến nhất theo tháng
def most_popular_start_station_per_month(df, reports_folder):
    result = (
        df.withColumn("month", date_format("start_time", "yyyy-MM"))  # Tạo cột tháng dạng yyyy-MM
          .groupBy("month", "from_station_name")
          .agg(count("*").alias("trip_count"))
    )
    # Xác định trạm có nhiều chuyến nhất trong mỗi tháng
    window = Window.partitionBy("month").orderBy(desc("trip_count"))
    ranked = result.withColumn("rank", expr("row_number() over (partition by month order by trip_count desc)"))
    top_stations = ranked.filter(col("rank") == 1).drop("rank")
    top_stations.write.csv(f"{reports_folder}/most_popular_start_station_per_month", header=True, mode="overwrite")


# Báo cáo: Top 3 trạm xuất phát theo từng ngày trong 2 tuần gần nhất
def top_3_trip_stations_last_two_weeks(df, reports_folder):
    max_date = df.select(to_date("start_time").alias("date")).agg({"date": "max"}).collect()[0][0]
    window_start = expr(f"date_sub('{max_date}', 13)")  # 14 ngày gần nhất (13 + ngày hiện tại)

    # Lọc dữ liệu của 14 ngày gần nhất
    recent_df = df.withColumn("date", to_date("start_time")).filter(col("date") >= window_start)
    result = (
        recent_df.groupBy("date", "from_station_name")
                 .agg(count("*").alias("trip_count"))
    )
    window = Window.partitionBy("date").orderBy(desc("trip_count"))
    ranked = result.withColumn("rank", expr("row_number() over (partition by date order by trip_count desc)"))
    top_3 = ranked.filter(col("rank") <= 3)
    top_3.write.csv(f"{reports_folder}/top_3_trip_stations_last_two_weeks", header=True, mode="overwrite")


# Báo cáo: Thời lượng chuyến đi trung bình theo giới tính
def avg_trip_duration_by_gender(df, reports_folder):
    result = (
        df.groupBy("gender")
          .agg(avg("tripduration").alias("avg_trip_duration"))
    )
    result.write.csv(f"{reports_folder}/avg_trip_duration_by_gender", header=True, mode="overwrite")


# Báo cáo: Top 10 độ tuổi có thời lượng chuyến đi dài nhất và ngắn nhất
def top_10_ages_by_trip_duration(df, reports_folder):
    df_with_age = df.withColumn("age", 2019 - col("birthyear"))  # Tính tuổi từ năm sinh (năm 2019)
    result = (
        df_with_age.groupBy("age")
                   .agg(avg("tripduration").alias("avg_trip_duration"))
                   .filter(col("age").isNotNull())
    )
    # Top 10 tuổi có thời lượng chuyến đi dài nhất
    longest = result.orderBy(desc("avg_trip_duration")).limit(10)
    # Top 10 tuổi có thời lượng chuyến đi ngắn nhất
    shortest = result.orderBy("avg_trip_duration").limit(10)

    longest.write.csv(f"{reports_folder}/top_10_ages_longest_trips", header=True, mode="overwrite")
    shortest.write.csv(f"{reports_folder}/top_10_ages_shortest_trips", header=True, mode="overwrite")


# Hàm chính để chạy toàn bộ pipeline
def main():
<<<<<<< Updated upstream
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
=======
    # Khởi tạo SparkSession
    spark = SparkSession.builder.appName("Exercise6").enableHiveSupport().getOrCreate()

    data_folder = "./data"
    unzipped_folder = "./unzipped"
    reports_folder = "./reports"

    # Bước 1: Giải nén file zip
    unzip_files(data_folder, unzipped_folder)

    # Bước 2: Đọc dữ liệu CSV đã giải nén
    df = read_data(spark, unzipped_folder)

    # Bước 3: Tạo thư mục reports nếu chưa có
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)

    # Bước 4: Chạy các báo cáo
    average_trip_duration_per_day(df, reports_folder)
    trips_per_day(df, reports_folder)
    most_popular_start_station_per_month(df, reports_folder)
    top_3_trip_stations_last_two_weeks(df, reports_folder)
    avg_trip_duration_by_gender(df, reports_folder)
    top_10_ages_by_trip_duration(df, reports_folder)
>>>>>>> Stashed changes


# Khi chạy file trực tiếp thì thực hiện hàm main()
if __name__ == "__main__":
    main()
