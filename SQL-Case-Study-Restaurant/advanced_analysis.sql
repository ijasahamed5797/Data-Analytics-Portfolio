-- Additional SQL Queries for Restaurant Analysis
-- Demonstrating advanced SQL skills

-- Customer spending patterns by month
SELECT 
    customer_id,
    YEAR(order_date) as year,
    MONTH(order_date) as month,
    COUNT(*) as total_orders,
    SUM(price) as monthly_spending
FROM sales s
INNER JOIN menu m USING(product_id)
GROUP BY customer_id, YEAR(order_date), MONTH(order_date)
ORDER BY customer_id, year, month;

-- Average order value per customer
SELECT 
    customer_id,
    ROUND(AVG(order_value), 2) as avg_order_value
FROM (
    SELECT 
        customer_id,
        order_date,
        SUM(price) as order_value
    FROM sales s
    INNER JOIN menu m USING(product_id)
    GROUP BY customer_id, order_date
) as order_totals
GROUP BY customer_id;

-- Product popularity over time
SELECT 
    product_name,
    YEAR(order_date) as year,
    MONTH(order_date) as month,
    COUNT(*) as times_ordered
FROM sales s
INNER JOIN menu m USING(product_id)
GROUP BY product_name, YEAR(order_date), MONTH(order_date)
ORDER BY product_name, year, month;

-- Customer retention analysis
SELECT 
    first_month,
    COUNT(DISTINCT customer_id) as starting_customers,
    COUNT(DISTINCT CASE WHEN month_diff = 1 THEN customer_id END) as retained_1_month,
    COUNT(DISTINCT CASE WHEN month_diff = 2 THEN customer_id END) as retained_2_months
FROM (
    SELECT 
        customer_id,
        DATE_FORMAT(MIN(order_date), '%Y-%m-01') as first_month,
        PERIOD_DIFF(DATE_FORMAT(order_date, '%Y%m'), DATE_FORMAT(MIN(order_date), '%Y%m')) as month_diff
    FROM sales
    GROUP BY customer_id, order_date
) as customer_months
GROUP BY first_month;
