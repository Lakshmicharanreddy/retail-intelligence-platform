/*
===============================================================================
Project   : Retail Intelligence Platform
File      : 04_views.sql

Purpose:
Creates reporting views for analytics and Tableau dashboards.
===============================================================================
*/

-- ============================================================================
-- VIEW: SALES DETAILS
-- ============================================================================

CREATE OR REPLACE VIEW vw_sales_details AS

SELECT

    s.sale_id,
    s.order_id,
    s.sale_timestamp,

    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.city AS customer_city,
    c.state AS customer_state,
    c.loyalty_level,

    p.product_id,
    p.product_name,
    p.category,
    p.subcategory,
    p.brand,

    st.store_id,
    st.store_name,
    st.region,
    st.store_type,

    pr.promotion_name,
    pr.promotion_type,

    s.quantity,
    s.unit_price,
    s.discount_amount,
    s.tax_amount,
    s.total_amount,
    s.profit,
    s.payment_method,
    s.order_status

FROM sale s

JOIN customer c
ON s.customer_id = c.customer_id

JOIN product p
ON s.product_id = p.product_id

JOIN store st
ON s.store_id = st.store_id

LEFT JOIN promotion pr
ON s.promotion_id = pr.promotion_id;




-- ============================================================================
-- VIEW: DAILY SALES
-- ============================================================================

CREATE OR REPLACE VIEW vw_daily_sales AS

SELECT

    DATE(sale_timestamp) AS sales_date,

    COUNT(DISTINCT order_id) AS total_orders,

    SUM(quantity) AS units_sold,

    SUM(total_amount) AS revenue,

    SUM(profit) AS total_profit,

    ROUND(AVG(total_amount),2) AS average_order_value

FROM sale

GROUP BY DATE(sale_timestamp)

ORDER BY sales_date;





-- ============================================================================
-- VIEW: STORE PERFORMANCE
-- ============================================================================

CREATE OR REPLACE VIEW vw_store_performance AS

SELECT

    st.store_id,

    st.store_name,

    st.region,

    COUNT(DISTINCT s.order_id) AS total_orders,

    SUM(s.quantity) AS units_sold,

    SUM(s.total_amount) AS revenue,

    SUM(s.profit) AS total_profit,

    RANK() OVER (
        ORDER BY SUM(s.total_amount) DESC
    ) AS revenue_rank

FROM store st

JOIN sale s
ON st.store_id = s.store_id

GROUP BY

    st.store_id,
    st.store_name,
    st.region;




-- ============================================================================
-- VIEW: PRODUCT PERFORMANCE
-- ============================================================================

CREATE OR REPLACE VIEW vw_product_performance AS

SELECT

    p.product_id,

    p.product_name,

    p.category,

    p.subcategory,

    SUM(s.quantity) AS units_sold,

    SUM(s.total_amount) AS revenue,

    SUM(s.profit) AS total_profit,

    RANK() OVER (
        PARTITION BY p.category
        ORDER BY SUM(s.total_amount) DESC
    ) AS category_rank

FROM product p

JOIN sale s
ON p.product_id = s.product_id

GROUP BY

    p.product_id,
    p.product_name,
    p.category,
    p.subcategory;






-- ============================================================================
-- VIEW: CUSTOMER SUMMARY
-- ============================================================================

CREATE OR REPLACE VIEW vw_customer_summary AS

SELECT

    c.customer_id,

    CONCAT(c.first_name,' ',c.last_name) AS customer_name,

    c.loyalty_level,

    COUNT(DISTINCT s.order_id) AS total_orders,

    SUM(s.total_amount) AS lifetime_value,

    SUM(s.profit) AS lifetime_profit,

    MAX(s.sale_timestamp) AS last_purchase,

    ROUND(AVG(s.total_amount),2) AS average_order_value

FROM customer c

JOIN sale s
ON c.customer_id = s.customer_id

GROUP BY

    c.customer_id,
    c.first_name,
    c.last_name,
    c.loyalty_level;






SELECT * FROM vw_sales_details;
SELECT * FROM vw_daily_sales;
SELECT * FROM vw_store_performance;
SELECT * FROM vw_product_performance;
SELECT * FROM vw_customer_summary;





