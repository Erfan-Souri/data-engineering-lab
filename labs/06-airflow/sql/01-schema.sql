DROP TABLE IF EXISTS reporting_orders;
DROP TABLE IF EXISTS customer_orders;

CREATE TABLE customer_orders (
    order_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE reporting_orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    category VARCHAR(50),
    payment_method VARCHAR(30),
    amount NUMERIC(10,2),
    created_at TIMESTAMP
);