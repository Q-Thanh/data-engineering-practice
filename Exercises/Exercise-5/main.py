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
