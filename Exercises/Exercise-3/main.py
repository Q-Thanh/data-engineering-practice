import requests
import gzip
import io
import sys # Để ghi trực tiếp ra stdout, đôi khi hữu ích cho streaming

# URL gốc của Common Crawl
COMMON_CRAWL_BASE_URL = 'https://data.commoncrawl.org'

def download_file(url):
    """Tải tệp từ URL và trả về nội dung"""
    print(f"Đang tải tệp từ URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Phát sinh ngoại lệ nếu status code không phải 2xx
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Đã xảy ra lỗi khi tải tệp: {e}", file=sys.stderr)
        raise

def s3_uri_to_http_url(uri):
    """Chuyển đổi S3 URI hoặc đường dẫn tương đối thành URL HTTP cho Common Crawl"""
    if uri.startswith('s3://'):
        s3_path = uri[len('s3://'):]
        # Bỏ qua phần bucket (thường là 'commoncrawl')
        path = s3_path[s3_path.find('/') + 1:]
        return f"{COMMON_CRAWL_BASE_URL}/{path}"
    else:
        # Nếu là đường dẫn tương đối, sử dụng trực tiếp
        return f"{COMMON_CRAWL_BASE_URL}/{uri}"

def main():
    # --- Định nghĩa các tham số ---
    # URL của tệp wet.paths.gz
    WET_PATHS_URL = f"{COMMON_CRAWL_BASE_URL}/crawl-data/CC-MAIN-2022-05/wet.paths.gz"

    print(f"--- Bắt đầu xử lý dữ liệu Common Crawl ---")

    try:
        # --- Bước 1: Tải tệp .gz ban đầu ---
        print(f"1. Đang tải tệp wet.paths.gz từ {WET_PATHS_URL}")
        gz_content = download_file(WET_PATHS_URL)
        print(f"   Đã tải xong {len(gz_content)} bytes.")

        # --- Bước 2: Giải nén và đọc tệp .gz ---
        print(f"2. Đang giải nén và đọc dòng đầu tiên...")
        with gzip.GzipFile(fileobj=io.BytesIO(gz_content), mode='rb') as gz_file:
            wet_uri = gz_file.readline().decode('utf-8').strip()

        print(f"   Dòng đầu tiên (URI tệp WET) là: {wet_uri}")

        # --- Bước 3: Chuyển đổi S3 URI thành URL HTTP ---
        wet_url = s3_uri_to_http_url(wet_uri)
        print(f"3. URL của tệp WET: {wet_url}")

        # --- Bước 4: Tải tệp WET và xử lý ---
        print(f"4. Đang tải tệp WET...")
        wet_content = download_file(wet_url)
        print(f"   Đã tải tệp WET thành công ({len(wet_content)} bytes).")

        # --- Bước 5: Xử lý và hiển thị nội dung tệp WET ---
        print(f"5. Nội dung của tệp WET:")
        wet_fileobj = io.BytesIO(wet_content)
        # WET files are gzipped, so we need to decompress them
        with gzip.GzipFile(fileobj=wet_fileobj, mode='rb') as wet_file:
            line_count = 0
            for line in wet_file:
                decoded_line = line.decode('utf-8', errors='replace').rstrip('\r\n')
                print(decoded_line)
                line_count += 1
                # Giới hạn số dòng hiển thị để tránh quá nhiều đầu ra
                if line_count >= 100:
                    print("... (còn nhiều dòng khác)")
                    break

        print(f"   Đã hiển thị {line_count} dòng từ tệp WET.")
        print(f"--- Hoàn thành xử lý ---")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}", file=sys.stderr)
        sys.exit(1)  # Thoát với mã lỗi để báo hiệu thất bại


if __name__ == "__main__":
    main()
