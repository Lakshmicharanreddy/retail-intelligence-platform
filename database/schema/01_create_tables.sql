/*
===============================================================================
Project   : Retail Intelligence Platform
File      : 01_create_tables.sql
Database  : PostgreSQL

Purpose:
Creates all core operational tables for the Retail Intelligence Platform.

Notes:
- Only table definitions are included.
- Foreign Keys will be added in 02_constraints.sql
- Indexes will be added in 03_indexes.sql
- Views will be added in 04_views.sql
===============================================================================
*/

-- ============================================================================
-- CUSTOMER TABLE
-- ============================================================================

CREATE TABLE customer (

    customer_id SERIAL PRIMARY KEY,

    first_name VARCHAR(50) NOT NULL,

    last_name VARCHAR(50) NOT NULL,

    gender VARCHAR(20),

    date_of_birth DATE,

    email VARCHAR(255) UNIQUE,

    phone VARCHAR(20),

    city VARCHAR(100),

    state VARCHAR(100),

    join_date DATE NOT NULL DEFAULT CURRENT_DATE,

    loyalty_level VARCHAR(20) NOT NULL DEFAULT 'Bronze',

    customer_status VARCHAR(20) NOT NULL DEFAULT 'Active',

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

);


-- ============================================================================
-- PRODUCT TABLE
-- ============================================================================

CREATE TABLE product (

    product_id SERIAL PRIMARY KEY,

    product_name VARCHAR(255) NOT NULL,

    category VARCHAR(100) NOT NULL,

    subcategory VARCHAR(100),

    brand VARCHAR(100),

    supplier VARCHAR(100),

    cost_price NUMERIC(10,2) NOT NULL,

    selling_price NUMERIC(10,2) NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

);


-- ============================================================================
-- STORE TABLE
-- ============================================================================

CREATE TABLE store (

    store_id SERIAL PRIMARY KEY,

    store_name VARCHAR(100) NOT NULL,

    city VARCHAR(100) NOT NULL,

    state VARCHAR(100) NOT NULL,

    region VARCHAR(100) NOT NULL,

    manager_name VARCHAR(100),

    opening_date DATE,

    store_type VARCHAR(50),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

);


-- ============================================================================
-- PROMOTION TABLE
-- ============================================================================

CREATE TABLE promotion (

    promotion_id SERIAL PRIMARY KEY,

    promotion_name VARCHAR(100) NOT NULL,

    promotion_type VARCHAR(50),

    discount_percentage NUMERIC(5,2) NOT NULL,

    start_date DATE NOT NULL,

    end_date DATE NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

);


-- ============================================================================
-- INVENTORY TABLE
-- ============================================================================

CREATE TABLE inventory (

    inventory_id SERIAL PRIMARY KEY,

    product_id INTEGER NOT NULL,

    store_id INTEGER NOT NULL,

    stock_quantity INTEGER NOT NULL,

    reorder_level INTEGER NOT NULL,

    last_stock_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

);


-- ============================================================================
-- SALE TABLE
-- ============================================================================
CREATE TABLE sale (

    sale_id SERIAL PRIMARY KEY,

    invoice_number VARCHAR(50) NOT NULL UNIQUE,

    order_timestamp TIMESTAMP NOT NULL,

    customer_id INTEGER NOT NULL,

    product_id INTEGER NOT NULL,

    store_id INTEGER NOT NULL,

    inventory_id INTEGER NOT NULL,

    promotion_id INTEGER,

    quantity INTEGER NOT NULL,

    unit_price NUMERIC(10,2) NOT NULL,

    subtotal NUMERIC(10,2) NOT NULL,

    discount_amount NUMERIC(10,2) NOT NULL DEFAULT 0,

    tax_amount NUMERIC(10,2) NOT NULL DEFAULT 0,

    total_amount NUMERIC(10,2) NOT NULL,

    profit NUMERIC(10,2) NOT NULL,

    payment_method VARCHAR(30) NOT NULL,

    sales_channel VARCHAR(30) NOT NULL,

    order_status VARCHAR(30) NOT NULL
);
































