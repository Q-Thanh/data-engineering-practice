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
> ![image](https://github.com/user-attachments/assets/b4dc7f5e-843b-4e94-810b-596e8595e37e)

> 3. Sau khi build xong, truy cập file `main.py` bằng VS code

##### Code sử dụng cho main.py:
```
import io
import gzip
import requests
from dotenv import load_dotenv

load_dotenv()
def download_file_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error downloading file: {response.status_code}")
        return None
def main():
    url = 'https://data.commoncrawl.org/crawl-data/CC-MAIN-2022-05/wet.paths.gz'
    gz_content = download_file_from_url(url)
    
    if gz_content:
        with gzip.GzipFile(fileobj=io.BytesIO(gz_content)) as f:
            first_line = f.readline().decode('utf-8').strip() 
            print(f"First line from wet.paths.gz: {first_line}")
            uri = first_line
            print(f"Extracted URI: {uri}")
            print("\nPrinting the first 50 lines from wet.paths.gz:")
            for i, line in enumerate(f):
                if i >= 50:  
                    break
                print(line.decode('utf-8').strip()) 
if __name__ == "__main__":
    main()
```
> 4. Sau khi lưu file `main.py`, thực hiện lệnh `docker-compose up run`
> 5. Kết quả sau khi thực hiện
![Screenshot 2025-04-24 133824](https://github.com/user-attachments/assets/9b19ff56-eee5-41e7-a62b-5050c8958066)


## EXERCISE-4

> 1. Thay đổi đường dẫn thư mục tại CMD thành `Exercise-4`

> 2. Chạy lệnh docker `build --tag=exercise-4 .` để build image Docker (Quá trình diễn ra trong 2 – 3 phút)
> ![image](https://github.com/user-attachments/assets/0429e78f-9d6b-4c9c-8d67-c06d6831a270)

> 3. Nội dung file `main.py`
```
import os
import json
import csv
import glob

def flatten\_json(nested\_json, parent\_key='', sep='\_'):

    """Giải nén JSON lồng nhau thành cấu trúc phẳng (flat structure)"""

    items = []

    if isinstance(nested\_json, dict):  # Kiểm tra nếu là dictionary

        for k, v in nested\_json.items():

            new\_key = f"{parent\_key}{sep}{k}" if parent\_key else k

            if isinstance(v, dict):  # Nếu giá trị là dict, tiếp tục giải nén

                items.extend(flatten\_json(v, new\_key, sep=sep).items())

            elif isinstance(v, list):  # Nếu giá trị là list, giải nén từng phần tử

                for i, sub\_item in enumerate(v):

                    items.extend(flatten\_json(sub\_item, f"{new\_key}{sep}{i}", sep=sep).items())

            else:  # Nếu giá trị không phải dict hoặc list (ví dụ như số, chuỗi, boolean)

                items.append((new\_key, v))

    elif isinstance(nested\_json, list):  # Kiểm tra nếu là list

        for i, sub\_item in enumerate(nested\_json):

            items.extend(flatten\_json(sub\_item, f"{parent\_key}{sep}{i}", sep=sep).items())

    else:

        # Nếu giá trị là kiểu khác (ví dụ float, int, string), trả về giá trị trực tiếp

        items.append((parent\_key, nested\_json))

    return dict(items)

def convert\_json\_to\_csv(json\_file, csv\_file):

    """Chuyển đổi tệp JSON thành tệp CSV"""

    with open(json\_file, 'r') as f:

        data = json.load(f)

    # Giải nén JSON lồng nhau

    flat\_data = flatten\_json(data)

    # Lưu dữ liệu vào CSV

    with open(csv\_file, 'w', newline='', encoding='utf-8') as f:

        writer = csv.DictWriter(f, fieldnames=flat\_data.keys())

        writer.writeheader()

        writer.writerow(flat\_data)

def process\_json\_files\_in\_directory(data\_directory):

    """Duyệt qua thư mục và chuyển đổi tất cả tệp JSON thành CSV"""

    # Tìm tất cả tệp .json trong thư mục và các thư mục con

    json\_files = glob.glob(os.path.join(data\_directory, '**', '*.json'), recursive=True)

    for json\_file in json\_files:

        csv\_file = json\_file.replace('.json', '.csv')

        convert\_json\_to\_csv(json\_file, csv\_file)

        print(f"Đã chuyển đổi {json\_file} thành {csv\_file}")

def main():

    # Thư mục chứa dữ liệu

    data\_directory = './data'  # Thay đổi đường dẫn nếu cần

    process\_json\_files\_in\_directory(data\_directory)

if \_\_name\_\_ == "\_\_main\_\_":

    main()
```

> 4. Sau khi save file ` main.py`, thực thi lệnh `docker-compose up run`
> 5. Kết quả sau khi thực hiện:

![image](https://github.com/user-attachments/assets/52637e8a-7e04-48de-9cfc-7dc66e3c5ea5)

![image](https://github.com/user-attachments/assets/ca55d07c-a19c-4235-aa86-2c2815547f2b)

![image](https://github.com/user-attachments/assets/00fd665a-2b77-4ac1-9dc3-c069996521ad)

## EXERCISE-5

> 1.Thay đổi đường dẫn thư mục tại CMD thành `Exercise-5`

> 2. Chạy lệnh docker `build --tag=exercise-5 .` để build image Docker (Quá trình diễn ra trong 2 – 3 phút)
> ![image](https://github.com/user-attachments/assets/3eb12b93-1146-4adf-bba8-5ad4cc3750fd)

#### Nội dung file main.py:
```
import psycopg2
import csv

# Kết nối đến PostgreSQL
conn = psycopg2.connect(

    dbname="postgres",  # Tên cơ sở dữ liệu

    user="postgres",    # Tên người dùng PostgreSQL

    password="postgres",# Mật khẩu PostgreSQL

    host="postgres",    # Máy chủ (PostgreSQL chạy trên localhost)

    port="5432"         # Cổng PostgreSQL (mặc định)

)

# Tạo một con trỏ để thực thi các câu lệnh SQL

with conn.cursor() as cur:

    # 1. Xóa tất cả các ràng buộc khóa ngoại nếu có

    remove\_constraints = """

    ALTER TABLE IF EXISTS orders DROP CONSTRAINT IF EXISTS orders\_product\_id\_fkey;

    """

    cur.execute(remove\_constraints)

    conn.commit()

    # 2. Xóa các bảng nếu đã tồn tại

    drop\_tables = """

    DROP TABLE IF EXISTS transactions, accounts, products CASCADE;

    """

    cur.execute(drop\_tables)

    conn.commit()

    # 3. Tạo lại các bảng

    create\_products\_table = """

    CREATE TABLE IF NOT EXISTS products (

        product\_id INT PRIMARY KEY,

        product\_code VARCHAR(10),

        product\_description VARCHAR(255)

    );

    """

    

    # Tạo bảng accounts

    create\_accounts\_table = """

    CREATE TABLE IF NOT EXISTS accounts (

        customer\_id INT PRIMARY KEY,

        first\_name VARCHAR(100),

        last\_name VARCHAR(100),

        address\_1 VARCHAR(255),

        address\_2 VARCHAR(255),

        city VARCHAR(100),

        state VARCHAR(50),

        zip\_code VARCHAR(20),

        join\_date DATE

    );

    """

    

    # Tạo bảng transactions (sau khi bảng products đã được tạo)

    create\_transactions\_table = """

    CREATE TABLE IF NOT EXISTS transactions (

        transaction\_id VARCHAR(50) PRIMARY KEY,

        transaction\_date DATE,

        product\_id INT,

        product\_code VARCHAR(10),

        product\_description VARCHAR(255),

        quantity INT,

        account\_id INT

    );

    """

    

    # 4. Chạy các câu lệnh tạo bảng

    print("Creating products table...")

    cur.execute(create\_products\_table)  # Đảm bảo tạo bảng products trước

    print("Creating accounts table...")

    cur.execute(create\_accounts\_table)

    print("Creating transactions table...")

    cur.execute(create\_transactions\_table)

    # Commit changes

    conn.commit()

    # 5. Thêm khóa ngoại sau khi các bảng đã được tạo

    add\_foreign\_keys = """

    ALTER TABLE transactions

    ADD CONSTRAINT fk\_product\_id FOREIGN KEY (product\_id) REFERENCES products(product\_id) ON DELETE CASCADE,

    ADD CONSTRAINT fk\_account\_id FOREIGN KEY (account\_id) REFERENCES accounts(customer\_id) ON DELETE CASCADE;

    """

    print("Adding foreign key constraints...")

    cur.execute(add\_foreign\_keys)

    

    # Commit changes

    conn.commit()

    # 6. Chèn dữ liệu từ CSV vào các bảng

    def load\_data\_from\_csv(csv\_file, table\_name, columns):

        with open(csv\_file, 'r') as file:

            reader = csv.reader(file)

            next(reader)  # Bỏ qua dòng tiêu đề (header row)

            

            for row in reader:

                # Tạo câu truy vấn để chèn dữ liệu

                query = f"INSERT INTO {table\_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

                cur.execute(query, row)

        

        conn.commit()

    # 7. Chèn dữ liệu cho từng bảng

    load\_data\_from\_csv("data/accounts.csv", "accounts", ["customer\_id", "first\_name", "last\_name", "address\_1", "address\_2", "city", "state", "zip\_code", "join\_date"])

    load\_data\_from\_csv("data/products.csv", "products", ["product\_id", "product\_code", "product\_description"])

    load\_data\_from\_csv("data/transactions.csv", "transactions", ["transaction\_id", "transaction\_date", "product\_id", "product\_code", "product\_description", "quantity", "account\_id"])

# 8. Đóng kết nối

conn.close()

print("Data has been loaded successfully.")
```

> 3. Sau khi lưu lại, thực thi lệnh `docker-compose up run`
> 4. Kết quả sau khi thực hiện:
![image](https://github.com/user-attachments/assets/e4013e15-1978-4dff-926d-69ac7c8b3a3e)
> Truy vấn các bảng vừa tạo trong DBeaver
![image](https://github.com/user-attachments/assets/5ead3335-5ae2-4cee-b049-52af90313eae)

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
