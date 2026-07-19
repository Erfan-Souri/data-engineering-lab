-- ============================================================
-- PostgreSQL Lab Initialization Script
-- This script is executed automatically on the first startup
-- of a fresh PostgreSQL data directory.
--
-- Sample dataset:
--   - 1000 employees
--   - Random departments
--   - Random salaries
--   - Random hire dates (within the last 10 years)
-- ============================================================

DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary NUMERIC(10,2) NOT NULL,
    hire_date DATE NOT NULL
);

INSERT INTO employees (
    first_name,
    last_name,
    department,
    salary,
    hire_date
)
SELECT
    (
        ARRAY[
            'Alice','John','Emma','Michael','Olivia',
            'James','Sophia','David','Daniel','Erfan',
            'Sarah','Lucas','Emily','Matthew','Linda'
        ]
    )[floor(random()*15 + 1)],

    (
        ARRAY[
            'Smith','Johnson','Brown','Davis','Wilson',
            'Taylor','Moore','Thomas','Martin','Souri',
            'Anderson','Jackson','White','Harris','Clark'
        ]
    )[floor(random()*15 + 1)],

    (
        ARRAY[
            'Engineering',
            'Data',
            'Finance',
            'HR',
            'Sales',
            'Marketing',
            'Support'
        ]
    )[floor(random()*7 + 1)],

    ROUND((3000 + random() * 7000)::numeric, 2),

    CURRENT_DATE - ((random() * 3650)::int)

FROM generate_series(1,1000);

-- Verify initialization
SELECT COUNT(*) AS total_employees
FROM employees;