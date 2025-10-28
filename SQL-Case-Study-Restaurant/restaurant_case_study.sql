-- Restaurant Sales Analysis - SQL Case Study
-- Comprehensive analysis of customer behavior and sales patterns

-- Database setup
create database case_study;
use case_study;

-- 1. What is the total amount each customer spent at the restaurant?
SELECT 
    customer_id,
    SUM(price) as total_amount_spend 
FROM sales as s 
INNER JOIN menu as m USING (product_id) 
GROUP BY customer_id;

-- 2. How many days has each customer visited the restaurant?
SELECT 
    customer_id, 
    COUNT(DISTINCT order_date) as visit_days 
FROM sales 
GROUP BY customer_id;

-- 3. What was the first item from the menu purchased by each customer?
SELECT 
    customer_id, 
    product_name as first_order 
FROM(
    SELECT 
        *,
        ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date ASC) as item 
    FROM sales as s 
    INNER JOIN menu as m USING(product_id)
) as t 
WHERE item = 1;

-- 4. What is the most purchased item on the menu and how many times was it purchased by all customers?
SELECT 
    product_name,
    COUNT(*) as no_of_times
FROM sales as s 
INNER JOIN menu as m USING (product_id)
GROUP BY product_name 
ORDER BY no_of_times DESC 
LIMIT 1;

-- 5. Which item was the most popular for each customer?
SELECT 
    customer_id, 
    product_name as most_popular_item 
FROM(
    SELECT 
        customer_id,
        product_name,
        COUNT(*) as most_popular_item, 
        RANK() OVER(PARTITION BY customer_id ORDER BY COUNT(*) DESC) as rn
    FROM sales as s 
    INNER JOIN menu as m USING(product_id) 
    GROUP BY customer_id, product_name
) as t
WHERE rn = 1;

-- 6. Which item was purchased first by the customer after they became a member?
SELECT 
    customer_id, 
    product_name 
FROM(
    SELECT 
        *,
        ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date ASC) as rn
    FROM sales as s 
    INNER JOIN menu as m USING(product_id)
    INNER JOIN members as mb USING(customer_id) 
    WHERE s.order_date > mb.join_date
) as t
WHERE rn = 1;

-- 7. Which item was purchased just before the customer became a member?
SELECT * 
FROM(
    SELECT 
        *,
        RANK() OVER(PARTITION BY customer_id ORDER BY order_date DESC) as rnk 
    FROM sales as s 
    INNER JOIN menu m USING (product_id)
    INNER JOIN members as mb USING (customer_id) 
    WHERE s.order_date < mb.join_date
) as t
WHERE rnk = 1;

-- 8. What is the total items and amount spent for each member before they became a member?
SELECT 
    customer_id, 
    COUNT(*) as total_items, 
    SUM(price) as total_amount_spent 
FROM sales s 
INNER JOIN menu m USING(product_id) 
INNER JOIN members mb USING(customer_id)
WHERE s.order_date < mb.join_date 
GROUP BY customer_id 
ORDER BY customer_id ASC;

-- 9. If each $1 spent equates to 10 points and sushi has a 2x points multiplier - how many points would each customer have?
SELECT 
    customer_id,
    SUM(CASE 
        WHEN product_name = "sushi" THEN price * 20 
        ELSE price * 10 
    END) as total_Points
FROM sales s 
INNER JOIN menu m USING(product_id) 
GROUP BY customer_id;
