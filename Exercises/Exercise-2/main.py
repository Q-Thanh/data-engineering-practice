import requests
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
