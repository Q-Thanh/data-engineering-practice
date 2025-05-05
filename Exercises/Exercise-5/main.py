import psycopg2
import csv
import uuid
from datetime import datetime
import os

def create_tables(cur):
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
    cur.execute("CREATE INDEX IF NOT EXISTS idx_accounts_last_name ON accounts(last_name);")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT PRIMARY KEY,
            product_code INT,
            product_description VARCHAR(100)
        );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_products_code ON products(product_code);")

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
    cur.execute("CREATE INDEX IF NOT EXISTS idx_transactions_product_id ON transactions(product_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions(account_id);")


def import_csv(cur, conn):
    base_path = os.path.join(os.path.dirname(__file__), "data")

    # Accounts
    with open(os.path.join(base_path, "accounts.csv"), newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO accounts (
                    customer_id, first_name, last_name, address_1, address_2,
                    city, state, zip_code, join_date
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (customer_id) DO NOTHING;
            """, (
                int(row["customer_id"]),
                row["first_name"],
                row["last_name"],
                row["address_1"],
                row["address_2"] if row["address_2"] != "NaN" else None,
                row["city"],
                row["state"],
                row["zip_code"],
                datetime.strptime(row["join_date"], "%Y/%m/%d").date()
            ))
        conn.commit()

    # Products
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

    # Transactions
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


def main():
    host = "postgres"
    database = "postgres"
    user = "postgres"
    pas = "postgres"
    conn = psycopg2.connect(host=host, database=database, user=user, password=pas)
    cur = conn.cursor()

    create_tables(cur)
    conn.commit()

    import_csv(cur, conn)

    print("✅ Tables created and CSV data imported successfully.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
