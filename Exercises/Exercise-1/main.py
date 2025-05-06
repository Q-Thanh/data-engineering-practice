# Import các thư viện cần thiết
import os               # Làm việc với hệ thống file (tạo thư mục, đường dẫn, xóa file)
import requests         # Gửi HTTP request để tải file từ Internet
import zipfile          # Giải nén các file .zip

# Danh sách các URL chứa dữ liệu cần tải xuống
download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",  # URL sai để kiểm tra bắt lỗi
]

# Thư mục lưu file sau khi tải và giải nén
DOWNLOAD_DIR = "downloads"

# Hàm xử lý tải xuống và giải nén một file
def download_and_extract(url):
    # Lấy tên file từ URL (vd: Divvy_Trips_2019_Q1.zip)
    filename = url.split("/")[-1]
    zip_path = os.path.join(DOWNLOAD_DIR, filename)  # Đường dẫn lưu file .zip

    try:
        print(f"Downloading: {filename}")

        # Gửi GET request đến URL
        response = requests.get(url)
        response.raise_for_status()  # Nếu lỗi HTTP (vd: 404, 403) sẽ raise exception

        # Ghi nội dung tải được vào file .zip
        with open(zip_path, "wb") as f:
            f.write(response.content)

        # Mở file .zip và giải nén tất cả nội dung vào thư mục DOWNLOAD_DIR
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(DOWNLOAD_DIR)

        # Xóa file .zip sau khi giải nén thành công
        os.remove(zip_path)

        print(f"✓ Done: {filename}")

    # Bắt lỗi HTTP (URL lỗi, không tồn tại...)
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error for {filename}: {http_err}")

    # Bắt lỗi nếu file tải về không phải file zip hợp lệ
    except zipfile.BadZipFile:
        print(f"❌ Not a valid zip file: {filename}")

    # Bắt các lỗi khác
    except Exception as e:
        print(f"❌ Failed {filename}: {e}")

# Hàm main điều phối quá trình
def main():
    # Tạo thư mục "downloads" nếu chưa tồn tại
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Lặp qua từng URL trong danh sách và xử lý
    for url in download_uris:
        download_and_extract(url)

# Khi chạy script trực tiếp, gọi hàm main
if __name__ == "__main__":
    main()
