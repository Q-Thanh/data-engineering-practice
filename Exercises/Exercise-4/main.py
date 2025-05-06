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