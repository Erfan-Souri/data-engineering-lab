SELECT
    department,
    COUNT(employee_id) AS employee_count,
    ROUND(AVG(salary), 2) AS average_salary,
    MIN(salary) AS minimum_salary,
    MAX(salary) AS maximum_salary,
    SUM(salary) AS total_salary
FROM {{ ref('stg_employees') }}
GROUP BY department