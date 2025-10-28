-- Restaurant Case Study - Database Schema
-- Creates the necessary tables and sample data

CREATE DATABASE IF NOT EXISTS case_study;
USE case_study;

-- Menu table with product details
CREATE TABLE menu (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL(10,2)
);

-- Sales table with customer orders
CREATE TABLE sales (
    customer_id VARCHAR(1),
    order_date DATE,
    product_id INT,
    FOREIGN KEY (product_id) REFERENCES menu(product_id)
);

-- Members table with membership information
CREATE TABLE members (
    customer_id VARCHAR(1) PRIMARY KEY,
    join_date DATE
);

-- Sample data insertion
INSERT INTO menu (product_id, product_name, price) VALUES
(1, 'sushi', 10),
(2, 'curry', 15),
(3, 'ramen', 12);

INSERT INTO sales (customer_id, order_date, product_id) VALUES
('A', '2021-01-01', 1),
('A', '2021-01-01', 2),
('A', '2021-01-07', 2),
('A', '2021-01-10', 3),
('A', '2021-01-11', 3),
('A', '2021-01-11', 3),
('B', '2021-01-01', 2),
('B', '2021-01-02', 2),
('B', '2021-01-04', 1),
('B', '2021-01-11', 1),
('B', '2021-01-16', 3),
('B', '2021-02-01', 3),
('C', '2021-01-01', 3),
('C', '2021-01-01', 3),
('C', '2021-01-07', 3);

INSERT INTO members (customer_id, join_date) VALUES
('A', '2021-01-07'),
('B', '2021-01-09');
