--  E-Commerce Customer Purchase Analysis - SQL Tasks

--  1. Create & populate the table
CREATE TABLE IF NOT EXISTS purchases (
    customer_id   INT,
    customer_name VARCHAR(50),
    city          VARCHAR(50),
    product       VARCHAR(50),
    quantity      INT,
    price         DECIMAL(10,2)
);

INSERT INTO purchases VALUES
(1, 'Arjun', 'Pune',   'Mobile',     1, 20000),
(2, 'Sneha', 'Mumbai', 'Laptop',     1, 60000),
(3, 'Akash', 'Pune',   'Headphones', 2,  2000),
(4, 'Ritu',  'Nagpur', 'Tablet',     1, 25000),
(5, 'Meena', 'Mumbai', 'Mobile',     2, 20000);


-- Task 1: Display all purchase records
SELECT
    customer_id,
    customer_name,
    city,
    product,
    quantity,
    price,
    (quantity * price) AS total_purchase
FROM purchases
ORDER BY customer_id;


-- Task 2: Total spending per customer
SELECT
    customer_id,
    customer_name,
    SUM(quantity * price) AS total_spending
FROM purchases
GROUP BY customer_id, customer_name
ORDER BY total_spending DESC;


-- Task 3: Most purchased product (by quantity)
SELECT
    product,
    SUM(quantity)        AS total_qty_sold,
    SUM(quantity * price) AS total_revenue
FROM purchases
GROUP BY product
ORDER BY total_qty_sold DESC
LIMIT 1;

-- Full product popularity table
SELECT
    product,
    SUM(quantity)        AS total_qty_sold,
    COUNT(*)             AS num_orders,
    SUM(quantity * price) AS total_revenue
FROM purchases
GROUP BY product
ORDER BY total_qty_sold DESC;


-- Task 4: City-wise revenue
SELECT
    city,
    SUM(quantity * price) AS total_revenue,
    ROUND(
        100.0 * SUM(quantity * price) /
        (SELECT SUM(quantity * price) FROM purchases), 1
    ) AS revenue_share_pct
FROM purchases
GROUP BY city
ORDER BY total_revenue DESC;
