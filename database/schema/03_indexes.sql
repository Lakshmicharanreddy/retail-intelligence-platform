/*
===============================================================================
Project   : Retail Intelligence Platform
File      : 03_indexes.sql
Database  : PostgreSQL

Purpose:
Creates indexes to improve query performance.
===============================================================================
*/

-- ============================================================================
-- SALE TABLE INDEXES
-- ============================================================================

CREATE INDEX idx_sale_timestamp
ON sale(sale_timestamp);

CREATE INDEX idx_sale_customer
ON sale(customer_id);

CREATE INDEX idx_sale_product
ON sale(product_id);

CREATE INDEX idx_sale_store
ON sale(store_id);

CREATE INDEX idx_sale_order
ON sale(order_id);

-- ============================================================================
-- INVENTORY TABLE INDEXES
-- ============================================================================

CREATE INDEX idx_inventory_product
ON inventory(product_id);

CREATE INDEX idx_inventory_store
ON inventory(store_id);

-- ============================================================================
-- CUSTOMER TABLE INDEXES
-- ============================================================================

CREATE INDEX idx_customer_loyalty
ON customer(loyalty_level);

-- ============================================================================
-- PRODUCT TABLE INDEXES
-- ============================================================================

CREATE INDEX idx_product_category
ON product(category);

CREATE INDEX idx_product_subcategory
ON product(subcategory);