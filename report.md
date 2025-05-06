# REPORT - LAB 9: ULTIMATE PRACTICE
## MÔN: NHẬP MÔN KỸ THUẬT DỮ LIỆU - LỚP: DHKHDL19A
## Danh sách thành viên:
>> 1. Bùi Quang Thành
>> 2. Nguyễn Thị Phương Thảo
>> 3. Trương Đặng Hoàng Tuyến

# BÀI LÀM
> 1. Đăng nhập vào tài khoảng Github

> 2. Truy cập vào link:
> 
> 3. Chọn fork
![image](https://github.com/user-attachments/assets/78bc5f7e-3354-46d3-93ae-37df89da9613)

> 4. Click Create fork
![image](https://github.com/user-attachments/assets/bf0a8369-8568-401f-a337-7457d2c25a3b)

## EXERCISE 1

> 1. Thực thi lệnh sau trong CMD: git clone để clone GitHub repo về máy của mình
![image](https://github.com/user-attachments/assets/03a1821e-dd25-4748-931d-afee36e47d7e).

> 2. Sau đó tiến hành chạy lệnh `cd data-engineering-practice/Exercises/Exercise-1` để thay đổi đường dẫn thư mục Exercise-1

> 3. Tiếp tục thực hiện lệnh: `docker build --tag=exercise-1 .` để build Docker image Quá trình sẽ mất vài phút
![70fb32a899772b297266](https://github.com/user-attachments/assets/250e5f8f-4bf3-4263-b32d-9832969553f4)
![3c90cf92794dcb13925c](https://github.com/user-attachments/assets/9e3bd508-8290-41bf-8e1a-6223464211c3)
![7a5be3c75018e246bb09](https://github.com/user-attachments/assets/ee05f4d0-72e5-4105-8326-aef28a6f8d41)


> 4. Sử dụng Visual để chạy main.py
![c7929cded400665e3f11](https://github.com/user-attachments/assets/e9934529-5d0d-4e97-985f-69e06a9041eb)


> ##### Code sử dụng cho main.py
```
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

```
> Đoạn code trên thực hiện các tác vụ: 
- Tạo thư mục downloads nếu chưa tồn tại

- Tải từng file từ danh sách download\_uris

- Giữ tên gốc của file từ URL

- Giải nén .zip thành .csv

- Xóa file .zip sau khi giải nén

- Bỏ qua URL không hợp lệ (ví dụ: cái Divvy\_Trips\_2220\_Q1.zip không tồn tại)

> 5. Sau khi save `main.py`, chạy lệnh `docker-compose up run` (mất khoảng 5 phút)
![bada83a1af7f1d21446e](https://github.com/user-attachments/assets/0c8b5d85-dd88-486c-b4bf-f1f9ccfa7eab)


## EXERCISE 2

> 1. Thay đổi đường dẫn thư mục tại CMD thành `Exercise-2`

> 2. Chạy lệnh docker `build --tag=exercise-2 .` để build image Docker (Quá trình diễn ra trong 2 – 3 phút)
> ![1504b98db053020d5b42](https://github.com/user-attachments/assets/734aab65-dc74-4c71-ab0f-d5de198ec074)

> 3. Sau khi build xong, truy cập file main.py bằng VS code


##### Nội dung file main.py

```import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL của trang web chứa các tệp cần tải
BASE_URL = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"

# Dấu thời gian cần tìm kiếm trên trang web
TARGET_TIMESTAMP = "2024-01-19 10:27"

def find_target_file():
    """
    Hàm này sẽ duyệt qua trang web, tìm kiếm tệp với dấu thời gian
    TARGET_TIMESTAMP và trả về tên tệp tương ứng.
    """
    response = requests.get(BASE_URL)  # Gửi yêu cầu GET tới trang web
    response.raise_for_status()  # Kiểm tra nếu yêu cầu thành công

    soup = BeautifulSoup(response.text, 'lxml')  # Phân tích trang HTML

    # Tìm tất cả các dòng trong bảng
    rows = soup.find_all("tr")

    for row in rows:
        cols = row.find_all("td")  # Tìm các ô trong dòng
        if len(cols) >= 2:
            timestamp = cols[1].text.strip()  # Lấy dấu thời gian
            if timestamp == TARGET_TIMESTAMP:
                filename = cols[0].text.strip()  # Lấy tên tệp
                return filename  # Trả về tên tệp nếu tìm thấy

    # Nếu không tìm thấy tệp với dấu thời gian yêu cầu
    raise Exception(f"File with timestamp {TARGET_TIMESTAMP} not found.")

def download_file(filename):
    """
    Hàm này sẽ tải tệp từ URL và lưu tệp vào thư mục 'downloads'.
    """
    download_url = BASE_URL + filename  # Xây dựng URL đầy đủ để tải tệp
    local_path = os.path.join("downloads", filename)  # Đường dẫn lưu tệp

    # Tạo thư mục 'downloads' nếu chưa tồn tại
    os.makedirs("downloads", exist_ok=True)

    # Gửi yêu cầu GET để tải tệp
    response = requests.get(download_url)
    response.raise_for_status()  # Kiểm tra nếu yêu cầu thành công

    # Lưu tệp vào hệ thống
    with open(local_path, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded file to {local_path}")  # Thông báo tệp đã được tải
    return local_path  # Trả về đường dẫn của tệp tải về

def analyze_file(filepath):
    """
    Hàm này sẽ mở tệp CSV, tìm bản ghi có nhiệt độ cao nhất và in ra.
    """
    df = pd.read_csv(filepath)  # Đọc tệp CSV vào DataFrame của Pandas

    # Kiểm tra xem cột 'HourlyDryBulbTemperature' có tồn tại không
    if 'HourlyDryBulbTemperature' not in df.columns:
        raise Exception("'HourlyDryBulbTemperature' column not found in the file.")  # Nếu không có, ném lỗi

    # Chuyển đổi cột 'HourlyDryBulbTemperature' thành kiểu số (nếu cần)
    df['HourlyDryBulbTemperature'] = pd.to_numeric(df['HourlyDryBulbTemperature'], errors='coerce')

    # Tìm giá trị nhiệt độ cao nhất
    max_temp = df['HourlyDryBulbTemperature'].max()
    # Lọc ra các bản ghi có nhiệt độ cao nhất
    hottest_records = df[df['HourlyDryBulbTemperature'] == max_temp]

    print("\n🌡 Records with the highest HourlyDryBulbTemperature:")
    print(hottest_records)  # In ra các bản ghi có nhiệt độ cao nhất

def main():
    """
    Hàm chính sẽ gọi các hàm trên để tìm kiếm tệp, tải tệp và phân tích dữ liệu.
    """
    try:
        print("Looking for file...")  # Thông báo đang tìm kiếm tệp
        filename = find_target_file()  # Tìm tệp với dấu thời gian cần tìm

        print(f"Found file: {filename}")  # Thông báo tìm thấy tệp
        filepath = download_file(filename)  # Tải tệp về

        print("Analyzing file...")  # Thông báo đang phân tích tệp
        analyze_file(filepath)  # Phân tích tệp để tìm bản ghi có nhiệt độ cao nhất

    except Exception as e:
        print(f"Error: {e}")  # In ra lỗi nếu có

# Chạy hàm main nếu tệp này được thực thi trực tiếp
if __name__ == "__main__":
    main()

```

> 4. Sau khi save file main.py, chạy dòng lệnh `docker-compose up run`

> 5. Kết quả thu được
> ![8800406e25b797e9cea6](https://github.com/user-attachments/assets/3b78c261-28a4-4f6a-986c-dab636f84045)

## EXERCISE 3

> 1. Thay đổi đường dẫn thư mục tại CMD thành `Exercise-3`

> 2. Chạy lệnh docker `build --tag=exercise-3 .` để build image Docker (Quá trình diễn ra trong 2 – 3 phút)
> ![image](https://github.com/user-attachments/assets/19b9503f-2c9b-4fcc-8476-1dfcb0a388a9)


> 3. Sau khi build xong, truy cập file `main.py` bằng VS code

##### Code sử dụng cho main.py:
```
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

```
> 4. Sau khi lưu file `main.py`, thực hiện lệnh `docker-compose up run`
> 5. Kết quả sau khi thực hiện
> ![image](https://github.com/user-attachments/assets/fc59b0b3-f477-43cc-9d15-0f07215786a1)



## EXERCISE-4

> 1. Thay đổi đường dẫn thư mục tại CMD thành `Exercise-4`

> 2. Chạy lệnh docker `build --tag=exercise-4 .` để build image Docker (Quá trình diễn ra trong 2 – 3 phút)
> ![image](https://github.com/user-attachments/assets/086ebd6b-8fb8-4996-8b61-ea52b64207b7)


> 3. Nội dung file `main.py`
```
import json
import csv
import glob
import os

def flatten_json(json_obj, parent_key='', sep='_'):
    """
    Làm phẳng một đối tượng JSON có cấu trúc lồng nhau.
    
    Args:
        json_obj: Đối tượng JSON cần làm phẳng
        parent_key: Khóa cha (sử dụng để đệ quy)
        sep: Ký tự phân tách giữa khóa cha và con
    
    Returns:
        dict: Dictionary đã được làm phẳng
    """
    flattened = {}
    
    # Duyệt qua tất cả các cặp key-value trong json_obj
    for key, value in json_obj.items():
        # Tạo tên khóa mới bằng cách nối khóa cha và khóa hiện tại
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        
        # Nếu giá trị là từ điển (dict), gọi đệ quy để làm phẳng nó
        if isinstance(value, dict):
            # Cập nhật flattened với kết quả từ hàm đệ quy
            flattened.update(flatten_json(value, new_key, sep))
        else:
            # Nếu không phải dict, gán giá trị trực tiếp
            flattened[new_key] = value
    
    return flattened

def json_to_csv(json_file_path, csv_file_path):
    """
    Chuyển đổi một file JSON thành file CSV.
    
    Args:
        json_file_path: Đường dẫn đến file JSON
        csv_file_path: Đường dẫn để lưu file CSV
    """
    print(f"Đang chuyển đổi {json_file_path} -> {csv_file_path}")
    
    # Đọc file JSON
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    
    # Làm phẳng JSON
    flattened_data = flatten_json(json_data)
    
    # Lấy tất cả các khóa để làm tiêu đề cho CSV
    fieldnames = flattened_data.keys()
    
    # Ghi ra file CSV
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # Viết dòng tiêu đề
        writer.writerow(flattened_data)  # Viết dòng dữ liệu

def main():
    """
    Hàm chính thực hiện các bước xử lý:
    1. Tìm tất cả file JSON trong thư mục data
    2. Chuyển đổi chúng thành file CSV
    """
    # Đường dẫn gốc đến thư mục data
    data_dir = 'data'
    
    # Tìm tất cả file .json trong data_dir và tất cả thư mục con của nó
    # ** nghĩa là tìm kiếm đệ quy trong tất cả các thư mục con
    # *.json nghĩa là tìm tất cả các file có đuôi .json
    json_files = glob.glob(os.path.join(data_dir, '**', '*.json'), recursive=True)
    
    print(f"Danh sách file JSON tìm thấy bởi glob: {json_files}")
    
    print(f"Đã tìm thấy {len(json_files)} file JSON:")
    for file in json_files:
        print(f"  - {file}")
    
    # Duyệt qua từng file JSON và chuyển đổi nó thành CSV
    for json_file in json_files:
        # Tạo tên file CSV từ tên file JSON (thay đuôi .json thành .csv)
        csv_file = json_file.replace('.json', '.csv')
        
        # Gọi hàm để chuyển đổi
        json_to_csv(json_file, csv_file)
    
    print("\nHoàn tất chuyển đổi!")

if __name__ == "__main__":
    main()
```

> 4. Sau khi save file ` main.py`, thực thi lệnh `docker-compose up run`
> 5. Kết quả sau khi thực hiện:

![image](https://github.com/user-attachments/assets/51311436-0077-4ad4-af9c-9c9cb91bae90)

![image](https://github.com/user-attachments/assets/da9d720a-35b7-4a8d-9908-ba14146c8f8e)

![image](https://github.com/user-attachments/assets/188b1474-9f76-412d-87a9-68dab9ab4110)


## EXERCISE-5

> 1.Thay đổi đường dẫn thư mục tại CMD thành `Exercise-5`

> 2. Chạy lệnh docker `build --tag=exercise-5 .` để build image Docker
> ![image](https://github.com/user-attachments/assets/b75fd14b-9a7b-4de5-a087-e1dd36bdca41)


#### Nội dung file main.py:
```
import psycopg2  # Thư viện để kết nối và thao tác với PostgreSQL
import csv       # Đọc file CSV
import uuid      # Thư viện tạo UUID (không dùng trong đoạn này nhưng có thể hữu ích sau)
from datetime import datetime  # Để xử lý định dạng ngày tháng
import os        # Thao tác với hệ thống file

# Hàm tạo các bảng trong cơ sở dữ liệu nếu chưa tồn tại
def create_tables(cur):
    # Tạo bảng 'accounts'
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            customer_id INT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            address_1 VARCHAR(100),
            address_2 VARCHAR(100),
            city VARCHAR(50),
            state VARCHAR(20),
            zip_code VARCHAR(10),
            join_date DATE
        );
    """)
    # Tạo index cho trường 'last_name' để tăng tốc truy vấn
    cur.execute("CREATE INDEX IF NOT EXISTS idx_accounts_last_name ON accounts(last_name);")

    # Tạo bảng 'products'
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT PRIMARY KEY,
            product_code INT,
            product_description VARCHAR(100)
        );
    """)
    # Tạo index cho trường 'product_code'
    cur.execute("CREATE INDEX IF NOT EXISTS idx_products_code ON products(product_code);")

    # Tạo bảng 'transactions'
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            transaction_date DATE,
            product_id INT REFERENCES products(product_id),
            product_code INT,
            product_description VARCHAR(100),
            quantity INT,
            account_id INT REFERENCES accounts(customer_id)
        );
    """)
    # Tạo index để tối ưu truy vấn trên product_id và account_id
    cur.execute("CREATE INDEX IF NOT EXISTS idx_transactions_product_id ON transactions(product_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions(account_id);")


# Hàm nhập dữ liệu từ các file CSV vào database
def import_csv(cur, conn):
    base_path = os.path.join(os.path.dirname(__file__), "data")  # Đường dẫn tới thư mục 'data'

    # Nhập dữ liệu cho bảng 'accounts'
    with open(os.path.join(base_path, "accounts.csv"), newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO accounts (
                    customer_id, first_name, last_name, address_1, address_2,
                    city, state, zip_code, join_date
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (customer_id) DO NOTHING;  -- Nếu trùng khóa chính thì bỏ qua
            """, (
                int(row["customer_id"]),
                row["first_name"],
                row["last_name"],
                row["address_1"],
                row["address_2"] if row["address_2"] != "NaN" else None,  # Chuyển 'NaN' thành None
                row["city"],
                row["state"],
                row["zip_code"],
                datetime.strptime(row["join_date"], "%Y/%m/%d").date()  # Chuyển chuỗi thành kiểu DATE
            ))
        conn.commit()  # Lưu thay đổi sau khi chèn xong

    # Nhập dữ liệu cho bảng 'products'
    with open(os.path.join(base_path, "products.csv"), newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO products (
                    product_id, product_code, product_description
                ) VALUES (%s, %s, %s)
                ON CONFLICT (product_id) DO NOTHING;
            """, (
                int(row["product_id"]),
                int(row["product_code"]),
                row["product_description"]
            ))
        conn.commit()

    # Nhập dữ liệu cho bảng 'transactions'
    with open(os.path.join(base_path, "transactions.csv"), newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO transactions (
                    transaction_id, transaction_date, product_id, product_code,
                    product_description, quantity, account_id
                ) VALUES (%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (transaction_id) DO NOTHING;
            """, (
                row["transaction_id"],
                datetime.strptime(row["transaction_date"], "%Y/%m/%d").date(),
                int(row["product_id"]),
                int(row["product_code"]),
                row["product_description"],
                int(row["quantity"]),
                int(row["account_id"])
            ))
        conn.commit()


# Hàm chính để chạy toàn bộ chương trình
def main():
    # Thông tin kết nối tới database
    host = "postgres"
    database = "postgres"
    user = "postgres"
    pas = "postgres"
    conn = psycopg2.connect(host=host, database=database, user=user, password=pas)
    cur = conn.cursor()

    # Tạo bảng nếu chưa có
    create_tables(cur)
    conn.commit()

    # Nhập dữ liệu từ CSV
    import_csv(cur, conn)

    print("✅ Tables created and CSV data imported successfully.")

    # Đóng kết nối
    cur.close()
    conn.close()


# Khi chạy file trực tiếp thì thực hiện hàm main()
if __name__ == "__main__":
    main()

```

> 3. Sau khi lưu lại, thực thi lệnh `docker-compose up run`
> 4. Kết quả sau khi thực hiện:
![image](https://github.com/user-attachments/assets/4625ce20-fb40-49e9-b9c0-be0f6bb9acbf)

> Truy vấn các bảng vừa tạo trong container posgres-1
![image](https://github.com/user-attachments/assets/e70ea051-15fc-4f1b-9cbd-0e3e85bf7830)

## PIPELINE TỰ ĐỘNG THỰC HIỆN BÀI TẬP 1- 5
#### Code cho pipeline.py:
```
import os
import subprocess

# List các Exercise bạn muốn chạy
exercises = ['Exercise-1', 'Exercise-2', 'Exercise-3', 'Exercise-4', 'Exercise-5']

# Hàm kiểm tra xem image đã có chưa
def check_image_exists(image_name):
    result = subprocess.run(['docker', 'images', '-q', image_name], stdout=subprocess.PIPE)
    return result.stdout.decode().strip() != ''

# Hàm build image nếu chưa có
def build_image(exercise_name):
    print(f"Image {exercise_name} chưa có, bắt đầu build...")
    result = subprocess.run(['docker', 'build', '-t', exercise_name, f'D:/NMKTDL/data-engineering-practice-main/Exercises/{exercise_name}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Build image {exercise_name} thất bại. Dừng pipeline.")
        print(result.stderr.decode())
        exit(1)
    print(f"Build image {exercise_name} thành công.")

# Hàm chạy docker-compose
def run_docker_compose(exercise_name):
    print(f"Đang chạy {exercise_name} bằng image {exercise_name}...")
    compose_file = f'D:/NMKTDL/data-engineering-practice-main/Exercises/{exercise_name}/docker-compose.yml'
    result = subprocess.run(['docker-compose', '-f', compose_file, 'up'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Lỗi khi chạy {exercise_name}. Dừng pipeline.")
        print(result.stderr.decode())
        exit(1)
    
    # Kiểm tra logs của các container
    print("Kiểm tra logs của các container...")
    logs_result = subprocess.run(['docker-compose', '-f', compose_file, 'logs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(logs_result.stdout.decode())  # In logs để xem chi tiết

    print(f"{exercise_name} đã hoàn tất!")

# Pipeline
def run_pipeline():
    for exercise in exercises:
        # Kiểm tra image đã tồn tại chưa
        if not check_image_exists(exercise.lower()):
            build_image(exercise)
        else:
            print(f"Image {exercise} đã có sẵn.")
        
        # Chạy docker-compose cho bài
        run_docker_compose(exercise)

    print("\nPipeline hoàn tất!")

if __name__ == "__main__":
    run_pipeline()
```
> #### Kết quả thực hiện:
> ##### Exercise-1
> ![image](https://github.com/user-attachments/assets/63d6cecb-88f2-48c4-816d-1dfc4b767f61)
> ##### Exercise-2 & 3
> ![image](https://github.com/user-attachments/assets/fedd1e65-6da1-4dc1-b9c3-ad1e2b8f21a3)
> ##### Exercise-4
> ![image](https://github.com/user-attachments/assets/71196633-75a3-4ead-b33b-21cdd6eafd2f)
> 

### CẤU TRÚC THƯ MỤC ĐỂ CHẠY DAG AIRFLOW
```
data-engineering-practice-Le_Trung_Huu/
│
├── dags/                    ← 📂 Chứa pipeline_dag.py
│   └── pipeline_dag.py  
│
├── Exercises/                   ← 📂 Chứa các bài tập với Dockerfile riêng
│   ├── Exercise-1/
│   │   ├── main.py 
│   ├── Exercise-2/
│   │   ├── main.py 
│   ├── Exercise-3/
│   ├── Exercise-4/
│   └── Exercise-5/
│
├── pipeline.py                  ← 📄 Code pipeline gốc nếu muốn gọi ngoài Airflow
└── requirements.txt
└── docker-compose.yml       ← ✅ Chạy trong thư mục này
└── Dockerfile
```
#### Dockerfile
```
FROM python:3.10-slim

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn từ thư mục hiện tại vào trong container
COPY . /app

WORKDIR /app

# Lệnh chạy khi container được khởi động
CMD ["python", "main.py"]
```
#### Docker-compose:
```
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - app-network

  airflow-init:
    image: apache/airflow:2.9.1-python3.10
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    entrypoint: bash -c "
      airflow db init && \
      airflow users create \
        --username airflow \
        --password airflow \
        --firstname Air \
        --lastname Flow \
        --role Admin \
        --email airflow@example.com
      "
    volumes:
      - ./dags:/opt/airflow/dags
      - ./Exercises:/opt/airflow/Exercises  # Mount thư mục Exercises từ ngoài vào container
    networks:
      - app-network

  airflow-webserver:
    image: apache/airflow:2.9.1-python3.10
    depends_on:
      - airflow-init
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__WEBSERVER__EXPOSE_CONFIG: 'True'
    ports:
      - "8080:8080"
    command: ["airflow", "webserver"]
    volumes:
      - ./dags:/opt/airflow/dags
      - ./Exercises:/opt/airflow/Exercises  # Mount thư mục Exercises từ ngoài vào container
    networks:
      - app-network

  airflow-scheduler:
    image: apache/airflow:2.9.1-python3.10
    depends_on:
      - airflow-webserver
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    command: ["airflow", "scheduler"]
    volumes:
      - ./dags:/opt/airflow/dags
      - ./Exercises:/opt/airflow/Exercises  # Mount thư mục Exercises từ ngoài vào container
    networks:
      - app-network

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - postgres
    networks:
      - app-network

volumes:
  postgres-db-volume:

networks:
  app-network:
    driver: bridge

#docker-compose up airflow-init
```

#### Pipeline-dag.py
```
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import subprocess

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def run_main_py(path):
    print(f"🔁 Đang chạy: {path}")
    result = subprocess.run(["python", path], capture_output=True, text=True)
    print("📄 STDOUT:", result.stdout)
    print("❗ STDERR:", result.stderr)
    result.check_returncode()

with DAG(
    dag_id='exercise_main_pipeline',
    default_args=default_args,
    description='Chạy tất cả các main.py trong mỗi Exercise hàng ngày lúc 10h sáng',
    schedule_interval='0 10 * * *',  # 10:00 UTC mỗi ngày
    start_date=datetime(2025, 4, 25),
    catchup=False,
    tags=["exercise"],
) as dag:

    exercises_dir = "/opt/airflow/Exercises"

    if not os.path.exists(exercises_dir):
        raise FileNotFoundError(f"Không tìm thấy thư mục: {exercises_dir}")

    previous_task = None

    for ex in sorted(os.listdir(exercises_dir)):
        ex_path = os.path.join(exercises_dir, ex, "main.py")
        if os.path.isfile(ex_path):
            task = PythonOperator(
                task_id=f'run_{ex.lower()}',
                python_callable=run_main_py,
                op_args=[ex_path],
            )
            if previous_task:
                previous_task >> task
            previous_task = task
```

### KẾT QUẢ SAU KHI CHẠY DAG
>![image](https://github.com/user-attachments/assets/749ac8e5-5aea-428b-b2b4-df0cf866040c)

> ![image](https://github.com/user-attachments/assets/b889a380-7201-49db-af30-2384068a9653)
>![image](https://github.com/user-attachments/assets/5c9d74f3-9391-4b29-8a4a-6bc10718b474)

> # REPORT - LAB 8:
## EXERCISE 1

> 1. Thực thi lệnh sau trong CMD: git clone để clone GitHub repo về máy của mình
> ![649dabe12114934aca05](https://github.com/user-attachments/assets/d4b2284b-1f99-4733-95e8-388c142eeb00)


> 2. Sau đó tiến hành chạy lệnh `cd cd Build-data-warehouse-with-Airflow-Python-for-E-commerce

> 3. Tiếp tục thực hiện lệnh: 'docker-compose up -d' để build Docker image Quá trình sẽ mất vài phút
> ![Annotation 2025-05-06 211724](https://github.com/user-attachments/assets/44cda780-fdd2-4535-8973-e4596bcdad04)

> 4. Mở Airflow Web UI để xem quá trình chạy
> Mặc định, Airflow Web UI sẽ chạy tại: http://localhost:8080
> ![Annotation 2025-05-06 215312](https://github.com/user-attachments/assets/81a636bf-8c9c-492a-a5f3-bab8aeffe751)
> ![image](https://github.com/user-attachments/assets/93b7b823-de6b-4931-9f7b-133ba179dcf9)
> 5. Check lại trong dbeaver
> ![image](https://github.com/user-attachments/assets/733cbed6-c76c-44fa-8223-4d9a6f936319)
## EXERCISE 2

> 1. Chuẩn bị môi trường làm việc:

Tạo một thư mục dự án riêng biệt trên hệ thống máy tính để chứa tất cả các file cấu hình và mã nguồn liên quan đến Airflow.

Bên trong thư mục dự án, tạo một thư mục con có tên là dags. Đây là nơi sẽ chứa các file định nghĩa DAG của Airflow (các file .py).

Đặt các file định nghĩa DAG đã có sẵn (simple_dag_local.py, complex_dag_local.py, miai_dag.py, sensor_local.py) vào thư mục dags vừa tạo.
![image](https://github.com/user-attachments/assets/a7fecc65-8c3d-4927-8225-db3aaef9fc20)


> 2. Xây dựng file cấu hình Docker Compose (docker-compose.yaml):

Tạo file docker-compose.yaml ở thư mục gốc của dự án.

Cấu hình các dịch vụ cần thiết để chạy Airflow:

Dịch vụ Cơ sở dữ liệu (PostgreSQL): Định nghĩa một dịch vụ sử dụng image PostgreSQL để làm cơ sở dữ liệu lưu trữ metadata của Airflow. Cấu hình tên database, người dùng và mật khẩu phù hợp với yêu cầu của Airflow. Sử dụng Docker Volume để đảm bảo dữ liệu database được lưu trữ bền vững.

Dịch vụ Airflow: Định nghĩa một dịch vụ sử dụng image Apache Airflow. Cấu hình dịch vụ này để phụ thuộc vào dịch vụ cơ sở dữ liệu, đảm bảo database sẵn sàng trước khi Airflow khởi động. Ánh xạ (mount) thư mục dags từ máy host vào thư mục DAGs bên trong container Airflow. Cấu hình cổng (port) để truy cập giao diện web của Airflow từ máy host (mặc định là 8080).
code file docker-compose.yml:
```
# Sử dụng phiên bản Docker Compose
# Bạn có thể xóa dòng version: '3' để tránh cảnh báo obsolete nếu muốn
version: '3'

# Định nghĩa các dịch vụ (services)
services:
  # Dịch vụ cơ sở dữ liệu PostgreSQL cho Airflow metadata
  postgres:
    image: postgres:14 # Sử dụng image PostgreSQL phiên bản 14
    environment:
      # Cấu hình thông tin đăng nhập và tên database cho PostgreSQL
      # Airflow sẽ sử dụng database có tên 'airflow'
      - POSTGRES_USER=airflow # <-- Tên người dùng database (có thể đổi)
      - POSTGRES_PASSWORD=airflow # <-- Mật khẩu database (có thể đổi)
      - POSTGRES_DB=airflow # <-- Tên database mà Airflow sẽ kết nối
    volumes:
      # Lưu trữ dữ liệu của database vào một volume để dữ liệu không bị mất khi container dừng/xóa
      - postgres_data:/var/lib/postgresql/data
    ports:
      # Ánh xạ cổng 5432 của container ra cổng 5432 trên máy host (tùy chọn, hữu ích cho việc debug database)
      - "5432:5432"
    networks:
      # Kết nối dịch vụ này vào mạng nội bộ 'airflow-network'
      - airflow-network
    healthcheck: # Kiểm tra tình trạng sức khỏe của database
      test: [ "CMD", "pg_isready", "-U", "airflow" ] # Lệnh kiểm tra
      interval: 5s # Kiểm tra mỗi 5 giây
      retries: 5 # Thử lại 5 lần nếu lỗi

  # Dịch vụ Airflow
  airflow:
    image: apache/airflow:2.6.3 # Sử dụng image Airflow phiên bản 2.6.3
    depends_on:
      # Airflow phụ thuộc vào database, đảm bảo postgres khởi động trước
      postgres:
        condition: service_healthy # Chờ cho dịch vụ postgres ở trạng thái healthy
    volumes:
      # Ánh xạ thư mục 'dags' trên máy host vào thư mục DAGs bên trong container Airflow
      # Đây là nơi bạn sẽ đặt các file DAG của mình
      - ./dags:/opt/airflow/dags # <-- Thư mục DAGs trên host : Thư mục DAGs trong container
      # Ánh xạ các thư mục khác nếu DAG của bạn cần đọc/ghi file ở ngoài thư mục DAGs
      # Ví dụ:
      # - ./data:/opt/airflow/data # Thư mục data cho Complex DAG
      # - ./stock_data:/opt/airflow/stock_data # Thư mục stock_data cho ML DAG
      # - ./models:/opt/airflow/models # Thư mục models cho ML DAG
      # - ./data_in:/opt/airflow/data_in # Thư mục input cho Sensor DAG
    ports:
      # Ánh xạ cổng 8080 của webserver Airflow ra cổng 8080 trên máy host
      - "8080:8080" # <-- Cổng trên host : Cổng webserver trong container
    command: standalone # Chạy Airflow ở chế độ standalone (bao gồm webserver và scheduler)
    environment:
      # Cấu hình kết nối database cho Airflow
      # Đảm bảo thông tin này khớp với thông tin trong service postgres
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow # <-- Thông tin kết nối DB
      - AIRFLOW__CORE__LOAD_EXAMPLES=False # Không tải các DAG ví dụ đi kèm Airflow
      # Cấu hình múi giờ (tùy chọn)
      # - AIRFLOW__CFG__CORE__DEFAULT_TIMEZONE=Asia/Ho_Chi_Minh # <-- Đổi múi giờ nếu cần

      # Tăng thời gian timeout cho Gunicorn webserver
      - AIRFLOW__WEBSERVER__WEB_SERVER_MASTER_TIMEOUT=300 # <-- THÊM hoặc SỬA dòng này, tăng timeout lên 300 giây (5 phút)

    networks:
      # Kết nối dịch vụ này vào mạng nội bộ 'airflow-network'
      - airflow-network
    healthcheck: # Kiểm tra tình trạng sức khỏe của Airflow webserver
      test: [ "CMD", "curl", "--fail", "-s", "http://localhost:8080/health" ] # Lệnh kiểm tra
      interval: 30s # Kiểm tra mỗi 30 giây
      timeout: 30s # Timeout sau 30 giây
      retries: 5 # Thử lại 5 lần nếu lỗi

# Định nghĩa mạng nội bộ cho các dịch vụ
networks:
  airflow-network:
    driver: bridge # Sử dụng driver mạng bridge

# Định nghĩa các volume để lưu trữ dữ liệu bền vững
volumes:
  postgres_data: # Volume cho dữ liệu PostgreSQL

```

> 3. Tạo Dockerfile tùy chỉnh để cài đặt Dependencies:

Tạo file Dockerfile ở thư mục gốc của dự án.

Sử dụng image Apache Airflow gốc làm nền (FROM apache/airflow:...).

Thêm các lệnh RUN pip install để cài đặt các thư viện Python bổ sung mà các file DAG phức tạp cần (ví dụ: pymysql, pandas, sendgrid, scikit-learn, tensorflow). Điều này đảm bảo các DAG có thể được import và chạy mà không gặp lỗi thiếu thư viện.

Chỉnh sửa file docker-compose.yaml để dịch vụ Airflow sử dụng build: . thay vì image: ..., chỉ định Docker Compose xây dựng image từ Dockerfile này.
code dockerfile:
```
# Sử dụng image Airflow gốc làm nền
FROM apache/airflow:2.6.3

# Cài đặt các thư viện Python bổ sung mà các DAG của bạn cần
# Dựa trên các file DAG bạn cung cấp, chúng ta cần pymysql, pandas, sendgrid
# Bạn có thể thêm các thư viện khác vào đây nếu DAG của bạn cần
RUN pip install --no-cache-dir \
    pymysql \
    pandas \
    sendgrid \
    scikit-learn \
    tensorflow
    # Thêm các thư viện khác nếu cần, ví dụ:
    # scikit-learn \ # Cho miai_dag.py
    # tensorflow # Cho miai_dag.py

```

> 4. Khởi động môi trường Airflow:

Mở terminal hoặc command prompt và điều hướng đến thư mục gốc của dự án.

Chạy lệnh docker compose up -d --build. Lệnh này sẽ:

Build image Docker tùy chỉnh cho dịch vụ Airflow (bao gồm cả việc cài đặt các thư viện bổ sung).

Tải image PostgreSQL (nếu chưa có).

Tạo và khởi động các container cho dịch vụ cơ sở dữ liệu và Airflow ở chế độ nền.

Tạo người dùng quản trị đầu tiên:

Sau khi các container khởi động và dịch vụ Airflow đã sẵn sàng (có thể mất vài phút), sử dụng lệnh docker compose exec để chạy lệnh Airflow CLI bên trong container Airflow nhằm tạo người dùng quản trị đầu tiên. Lệnh có dạng: docker compose exec airflow bash -c "airflow users create --username <tên> --password <mật khẩu> --firstname <tên> --lastname <họ> --email <email> --role Admin".
![image](https://github.com/user-attachments/assets/35d865b8-644f-423d-83ae-ad476c307d85)
![image](https://github.com/user-attachments/assets/a107abdb-486b-4029-b60e-3cc07cdbbab0)
![image](https://github.com/user-attachments/assets/10fc7c4e-a329-450b-b8d7-8003a177d087)


> 5. Truy cập giao diện web và kích hoạt DAGs:

Mở trình duyệt web và truy cập địa chỉ http://localhost:8080.

Đăng nhập bằng thông tin tài khoản quản trị vừa tạo.

Trên giao diện web, kiểm tra danh sách các DAG. Các DAG đã copy vào thư mục dags sẽ xuất hiện.

Kích hoạt (Unpause) các DAG mong muốn bằng cách nhấn vào nút gạt bên cạnh tên DAG.
![image](https://github.com/user-attachments/assets/270c0a38-4637-4f1b-8a97-50c50608cf6e)

