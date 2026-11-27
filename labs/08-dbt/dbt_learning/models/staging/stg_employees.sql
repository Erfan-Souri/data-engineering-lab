SELECT
    id AS employee_id,
    TRIM(first_name) AS first_name,
    TRIM(last_name) AS last_name,
    TRIM(department) AS department,
    salary,
    hire_date
FROM {{ source('raw', 'employees') }}
