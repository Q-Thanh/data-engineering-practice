from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
from pyspark.sql import Window
import tempfile
import zipfile
import os


def unzip_to_temp(zip_path):
    temp_dir = tempfile.mkdtemp()  # Tạo một thư mục tạm thời
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Lọc ra file CSV thật sự (bỏ qua thư mục _MACOSX hoặc file rác)
        csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv') and not f.startswith('__MACOSX')]
        
        print("Found CSV files:", csv_files)
        
        if len(csv_files) != 1:
            # Nếu không tìm thấy đúng 1 file CSV, raise lỗi
            raise ValueError(f"Expected exactly one CSV file inside the zip, but found {len(csv_files)}: {csv_files}")
        
        extracted_path = zip_ref.extract(csv_files[0], temp_dir)  # Giải nén file CSV ra thư mục tạm
    return extracted_path


def read_csv(spark: SparkSession, csv_path: str) -> DataFrame:
    """Đọc file CSV đã giải nén."""
    return spark.read.option("header", True).csv(csv_path)


def add_source_file(df: DataFrame, source_file: str) -> DataFrame:
    """Thêm cột source_file để ghi lại tên file nguồn."""
    return df.withColumn("source_file", F.lit(source_file))


def extract_file_date(df: DataFrame) -> DataFrame:
    """Trích xuất ngày từ cột source_file và tạo cột file_date."""
    return df.withColumn(
        "file_date",
        F.to_date(
            F.regexp_extract("source_file", r"(\d{4}-\d{2}-\d{2})", 1),  # Lấy chuỗi ngày định dạng yyyy-MM-dd
            "yyyy-MM-dd"
        )
    )


def add_brand(df: DataFrame) -> DataFrame:
    """Thêm cột brand dựa trên cột model (lấy từ đầu tiên của model)."""
    return df.withColumn(
        "brand",
        F.when(
            F.instr(F.col("model"), " ") > 0,  # Nếu model có chứa dấu cách
            F.split(F.col("model"), " ").getItem(0)  # Lấy từ đầu tiên làm brand
        ).otherwise(F.lit("unknown"))  # Nếu không có dấu cách, gán là 'unknown'
    )


def add_storage_ranking(df: DataFrame) -> DataFrame:
    """Thêm cột storage_ranking dựa vào capacity_bytes và model."""
    window_spec = F.row_number().over(
        Window.orderBy(F.col("capacity_bytes").cast("long").desc())
    )

    # Tính max_capacity theo từng model và xếp hạng giảm dần
    ranking_df = (
        df.groupBy("model")
        .agg(F.max(F.col("capacity_bytes").cast("long")).alias("max_capacity"))
        .orderBy(F.col("max_capacity").desc())
    ).withColumn("storage_ranking", F.row_number().over(Window.orderBy(F.col("max_capacity").desc())))

    # Join bảng ranking vào bảng chính theo model để có cột storage_ranking
    df_with_rank = df.join(ranking_df.select("model", "storage_ranking"), on="model", how="left")

    return df_with_rank


def add_primary_key(df: DataFrame) -> DataFrame:
    """Tạo cột primary_key là hash SHA-256 từ các cột định danh."""
    identifying_cols = ["date", "serial_number", "model"]
    return df.withColumn(
        "primary_key",
        F.sha2(F.concat_ws("||", *[F.col(c).cast("string") for c in identifying_cols]), 256)
    )


def process_data(spark: SparkSession, zip_path: str) -> DataFrame:
    # Giải nén file zip ra thư mục tạm
    csv_path = unzip_to_temp(zip_path)
    file_name = os.path.basename(zip_path)

    # Đọc dữ liệu CSV
    df = read_csv(spark, csv_path)

    # Thực hiện các bước transform dữ liệu
    df = add_source_file(df, file_name)
    df = extract_file_date(df)
    df = add_brand(df)
    df = add_storage_ranking(df)
    df = add_primary_key(df)

    return df


def main():
    # Tạo SparkSession với Hive support
    spark = SparkSession.builder.appName("Exercise7").enableHiveSupport().getOrCreate()

    # Đường dẫn tới file zip cần xử lý
    zip_path = "./data/hard-drive-2022-01-01-failures.csv.zip"

    # Xử lý dữ liệu
    df = process_data(spark, zip_path)

    # Hiển thị kết quả cuối cùng
    df.show(truncate=False)
    df.printSchema()


if __name__ == "__main__":
    main()
