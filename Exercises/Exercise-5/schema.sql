-- Table: accounts
CREATE TABLE accounts (
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

CREATE INDEX idx_accounts_last_name ON accounts(last_name);

-- Table: products
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_code INT,
    product_description VARCHAR(100)
);

CREATE INDEX idx_products_code ON products(product_code);

-- Table: transactions
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY,
    transaction_date DATE,
    product_id INT REFERENCES products(product_id),
    product_code INT,
    product_description VARCHAR(100),
    quantity INT,
    account_id INT REFERENCES accounts(customer_id)
);

CREATE INDEX idx_transactions_product_id ON transactions(product_id);
CREATE INDEX idx_transactions_account_id ON transactions(account_id);