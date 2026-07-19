CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    salary NUMERIC(10,2)
);

INSERT INTO employees (first_name, last_name, salary)
VALUES
('Erfan', 'Souri', 5000.00),
('Alice', 'Johnson', 6200.00),
('John', 'Doe', 5800.00);