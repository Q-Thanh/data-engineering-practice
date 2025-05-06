import boto3
from botocore import UNSIGNED
from botocore.client import Config
import gzip
import io
import os
import sys # Để ghi trực tiếp ra stdout, đôi khi hữu ích cho streaming

# Endpoint S3 cho us-east-1
S3_ENDPOINT_URL = 'https://s3.us-east-1.amazonaws.com'

def main():
# --- Định nghĩa các tham số ---
    # Bucket S3 chứa dữ liệu Common Crawl
    COMMON_CRAWL_BUCKET = 'commoncrawl'
    # Khóa (key) của tệp .gz chứa danh sách các tệp WET paths
    WET_PATHS_GZ_KEY = 'crawl-data/CC-MAIN-2022-05/wet.paths.gz'

    print(f"--- Bắt đầu xử lý dữ liệu Common Crawl ---")

    try:
        # --- Bước 1: Khởi tạo S3 client ---
        # Tạo một S3 client với cấu hình đặc biệt để truy cập dữ liệu Common Crawl
        # - use_ssl=True để đảm bảo kết nối an toàn
        # - verify=True để xác minh chứng chỉ SSL
        # - signature_version=UNSIGNED vì dữ liệu Common Crawl là public
        # - region_name='us-east-1' là region của dữ liệu Common Crawl
        s3_config = Config(
            signature_version=UNSIGNED, 
            s3={'addressing_style': 'path'},  # Sử dụng path-style URLs
            region_name='us-east-1'
        )
        s3 = boto3.client('s3', config=s3_config)
        print(f"1. Đã kết nối thành công với S3 (chế độ unsigned, path-style URLs).")

        # --- Bước 2: Tải tệp .gz ban đầu VÀO BỘ NHỚ ---
        print(f"2. Đang tải tệp '{WET_PATHS_GZ_KEY}' từ bucket '{COMMON_CRAWL_BUCKET}' vào bộ nhớ...")
        response = s3.get_object(Bucket=COMMON_CRAWL_BUCKET, Key=WET_PATHS_GZ_KEY)
        gz_body_bytes = response['Body'].read()
        gz_bytes_io = io.BytesIO(gz_body_bytes)
        print(f"   Đã tải xong {len(gz_body_bytes)} bytes vào bộ nhớ.")

        # --- Bước 3: Giải nén và đọc tệp .gz ---
        print(f"3. Đang giải nén và đọc dòng đầu tiên từ bộ nhớ...")
        with gzip.GzipFile(fileobj=gz_bytes_io, mode='rb') as gz_file:
            first_line_bytes = gz_file.readline()
            wet_paths_uri = first_line_bytes.decode('utf-8').strip()

        print(f"   Dòng đầu tiên (URI tệp WET) là: {wet_paths_uri}")

        # --- Bước 4: Phân tích URI để lấy bucket và key của tệp WET ---
        if wet_paths_uri.startswith('s3://'):
            s3_path = wet_paths_uri[len('s3://'):]
        else:
            raise ValueError(f"URI không đúng định dạng S3: {wet_paths_uri}")

        first_slash_index = s3_path.find('/')
        if first_slash_index == -1:
            raise ValueError(f"URI không đúng định dạng (thiếu key): {wet_paths_uri}")

        wet_bucket = s3_path[:first_slash_index]
        wet_key = s3_path[first_slash_index + 1:]

        print(f"4. Đã phân tích URI:")
        print(f"   - Bucket của tệp WET: {wet_bucket}")
        print(f"   - Key của tệp WET: {wet_key}")

        # --- Bước 5: Tải tệp WET và in từng dòng theo luồng ---
        print(f"5. Đang tải tệp '{wet_key}' và in từng dòng (streaming)...")
        # Cũng để bucket trống khi yêu cầu tệp WET
        wet_file_response = s3.get_object(Bucket='', Key=wet_key)
        wet_streaming_body = wet_file_response['Body']

        line_count = 0
        for line in wet_streaming_body.iter_lines():
            print(line.decode('utf-8').rstrip('\r\n'))
            line_count += 1

        print(f"   Đã in xong {line_count} dòng từ tệp WET.")
        print(f"--- Hoàn thành xử lý ---")

    except Exception as e:
        # Xử lý các lỗi có thể xảy ra trong quá trình (ví dụ: tệp không tồn tại, lỗi mạng, lỗi giải nén, lỗi phân tích URI).
        print(f"Đã xảy ra lỗi: {e}", file=sys.stderr)
        sys.exit(1) # Thoát với mã lỗi để báo hiệu thất bại


if __name__ == "__main__":
    main()
