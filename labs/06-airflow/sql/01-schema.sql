CREATE TABLE customer_orders (
    order_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    amount NUMERIC(10,2),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE reporting_orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    amount NUMERIC(10,2),
    created_at TIMESTAMP
);