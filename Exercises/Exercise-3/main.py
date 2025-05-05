import boto3
import gzip
import io
import os
import sys # Để ghi trực tiếp ra stdout, đôi khi hữu ích cho streaming

def main():
# --- Định nghĩa các tham số ---
    # Bucket S3 chứa dữ liệu Common Crawl
    COMMON_CRAWL_BUCKET = 'commoncrawl'
    # Khóa (key) của tệp .gz chứa danh sách các tệp WET paths
    WET_PATHS_GZ_KEY = 'crawl-data/CC-MAIN-2022-05/wet.paths.gz'

    print(f"--- Bắt đầu xử lý dữ liệu Common Crawl ---")

    try:
        # --- Bước 1: Khởi tạo S3 client ---
        # Tạo một phiên làm việc (session) với AWS.
        # Tạo một S3 client để tương tác với dịch vụ S3.
        # Client này sẽ sử dụng cấu hình AWS mặc định của bạn.
        s3 = boto3.client('s3')
        print(f"1. Đã kết nối thành công với S3.")

        # --- Bước 2: Tải tệp .gz ban đầu VÀO BỘ NHỚ (Yêu cầu nâng cao) ---
        # Sử dụng get_object để tải nội dung của tệp.
        # body = response['Body'] là một StreamingBody, đại diện cho nội dung tệp dưới dạng luồng byte.
        # Đọc toàn bộ luồng byte này vào một đối tượng BytesIO trong bộ nhớ.
        # Điều này đáp ứng yêu cầu KHÔNG tải xuống đĩa.
        print(f"2. Đang tải tệp '{WET_PATHS_GZ_KEY}' từ bucket '{COMMON_CRAWL_BUCKET}' vào bộ nhớ...")
        response = s3.get_object(Bucket=COMMON_CRAWL_BUCKET, Key=WET_PATHS_GZ_KEY)
        gz_body_bytes = response['Body'].read() # Đọc toàn bộ StreamingBody vào bytes
        gz_bytes_io = io.BytesIO(gz_body_bytes) # Gói bytes vào BytesIO để gzip có thể đọc từ đó
        print(f"   Đã tải xong {len(gz_body_bytes)} bytes vào bộ nhớ.")

        # --- Bước 3: Giải nén và đọc tệp .gz TỪ BỘ NHỚ ---
        # Sử dụng gzip.GzipFile để mở đối tượng BytesIO như một tệp gzip.
        # Điều này cho phép chúng ta đọc nội dung đã giải nén trực tiếp từ bộ nhớ.
        # 'rb' là chế độ đọc nhị phân.
        # Sử dụng 'with' statement để đảm bảo tệp gzip và BytesIO được đóng đúng cách.
        print(f"3. Đang giải nén và đọc dòng đầu tiên từ bộ nhớ...")
        with gzip.GzipFile(fileobj=gz_bytes_io, mode='rb') as gz_file:
            # Đọc dòng đầu tiên của tệp đã giải nén.
            # readline() sẽ đọc đến ký tự xuống dòng và bao gồm cả ký tự đó.
            # decode('utf-8') chuyển đổi bytes thành chuỗi ký tự (Common Crawl thường dùng UTF-8).
            first_line_bytes = gz_file.readline()
            wet_paths_uri = first_line_bytes.decode('utf-8').strip() # strip() để loại bỏ khoảng trắng và ký tự xuống dòng ở đầu/cuối

        # Sau khi thoát khỏi block 'with', gz_file và gz_bytes_io sẽ được đóng.
        print(f"   Dòng đầu tiên (URI tệp WET) là: {wet_paths_uri}")

        # --- Bước 4: Phân tích URI để lấy bucket và key của tệp WET ---
        # URI có dạng 's3://bucket-name/key-name'.
        # Chúng ta cần tách bucket và key ra.
        # Loại bỏ 's3://' khỏi chuỗi URI.
        if wet_paths_uri.startswith('s3://'):
            s3_path = wet_paths_uri[len('s3://'):]
        else:
            raise ValueError(f"URI không đúng định dạng S3: {wet_paths_uri}")

        # Tìm vị trí của dấu '/' đầu tiên sau phần 's3://'.
        first_slash_index = s3_path.find('/')
        if first_slash_index == -1:
            raise ValueError(f"URI không đúng định dạng (thiếu key): {wet_paths_uri}")

        # Tách bucket (phần trước dấu '/') và key (phần sau dấu '/').
        wet_bucket = s3_path[:first_slash_index]
        wet_key = s3_path[first_slash_index + 1:]

        print(f"4. Đã phân tích URI:")
        print(f"   - Bucket của tệp WET: {wet_bucket}")
        print(f"   - Key của tệp WET: {wet_key}")

        # --- Bước 5: Tải tệp WET và in từng dòng theo luồng (Yêu cầu nâng cao) ---
        # Sử dụng get_object để tải tệp WET.
        # Lần này, chúng ta sẽ KHÔNG đọc toàn bộ nội dung vào bộ nhớ ngay lập tức.
        # response['Body'] là một StreamingBody hỗ trợ đọc theo luồng.
        print(f"5. Đang tải tệp '{wet_key}' từ bucket '{wet_bucket}' và in từng dòng (streaming)...")
        wet_file_response = s3.get_object(Bucket=wet_bucket, Key=wet_key)
        wet_streaming_body = wet_file_response['Body']

        # Sử dụng iter_lines() của StreamingBody để đọc từng dòng.
        # Điều này hiệu quả về bộ nhớ vì nó chỉ đọc một phần dữ liệu tại một thời điểm.
        # iter_lines() trả về bytes cho mỗi dòng.
        # Chúng ta decode nó sang UTF-8 để in ra text.
        # rstrip('\r\n') loại bỏ ký tự xuống dòng cuối cùng để tránh in thêm dòng trống.
        line_count = 0
        for line in wet_streaming_body.iter_lines():
            print(line.decode('utf-8').rstrip('\r\n'))
            line_count += 1

        print(f"   Đã in xong {line_count} dòng từ tệp WET.")

        # --- Kết thúc ---
        print(f"--- Hoàn thành xử lý ---")

    except Exception as e:
        # Xử lý các lỗi có thể xảy ra trong quá trình (ví dụ: tệp không tồn tại, lỗi mạng, lỗi giải nén, lỗi phân tích URI).
        print(f"Đã xảy ra lỗi: {e}", file=sys.stderr)
        sys.exit(1) # Thoát với mã lỗi để báo hiệu thất bại


if __name__ == "__main__":
    main()
