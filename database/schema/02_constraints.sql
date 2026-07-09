/*
===============================================================================
Project   : Retail Intelligence Platform
File      : 02_constraints.sql
Database  : PostgreSQL

Purpose:
Adds foreign key and CHECK constraints to enforce
referential integrity and business rules.
===============================================================================
*/

-- ============================================================================
-- FOREIGN KEY CONSTRAINTS
-- ============================================================================

ALTER TABLE inventory
ADD CONSTRAINT fk_inventory_product
FOREIGN KEY (product_id)
REFERENCES product(product_id)
ON DELETE RESTRICT
ON UPDATE CASCADE;


ALTER TABLE inventory
ADD CONSTRAINT fk_inventory_store
FOREIGN KEY (store_id)
REFERENCES store(store_id)
ON DELETE RESTRICT
ON UPDATE CASCADE;


ALTER TABLE sale
ADD CONSTRAINT fk_sale_inventory
FOREIGN KEY (inventory_id)
REFERENCES inventory(inventory_id)
ON DELETE RESTRICT
ON UPDATE CASCADE;


ALTER TABLE sale
ADD CONSTRAINT fk_sale_customer
FOREIGN KEY (customer_id)
REFERENCES customer(customer_id)
ON DELETE RESTRICT
ON UPDATE CASCADE;


ALTER TABLE sale
ADD CONSTRAINT fk_sale_product
FOREIGN KEY (product_id)
REFERENCES product(product_id)
ON DELETE RESTRICT
ON UPDATE CASCADE;


ALTER TABLE sale
ADD CONSTRAINT fk_sale_store
FOREIGN KEY (store_id)
REFERENCES store(store_id)
ON DELETE RESTRICT
ON UPDATE CASCADE;


ALTER TABLE sale
ADD CONSTRAINT fk_sale_promotion
FOREIGN KEY (promotion_id)
REFERENCES promotion(promotion_id)
ON DELETE SET NULL
ON UPDATE CASCADE;

-- ============================================================================
-- CHECK CONSTRAINTS
-- ============================================================================

ALTER TABLE product
ADD CONSTRAINT chk_cost_price
CHECK (cost_price >= 0);

ALTER TABLE product
ADD CONSTRAINT chk_selling_price
CHECK (selling_price >= cost_price);

ALTER TABLE promotion
ADD CONSTRAINT chk_discount_percentage
CHECK (discount_percentage BETWEEN 0 AND 100);

ALTER TABLE inventory
ADD CONSTRAINT chk_stock_quantity
CHECK (stock_quantity >= 0);

ALTER TABLE inventory
ADD CONSTRAINT chk_reorder_level
CHECK (reorder_level >= 0);

ALTER TABLE sale
ADD CONSTRAINT chk_quantity
CHECK (quantity > 0);

ALTER TABLE sale
ADD CONSTRAINT chk_unit_price
CHECK (unit_price >= 0);

ALTER TABLE sale
ADD CONSTRAINT chk_discount_amount
CHECK (discount_amount >= 0);

ALTER TABLE sale
ADD CONSTRAINT chk_tax_amount
CHECK (tax_amount >= 0);

ALTER TABLE sale
ADD CONSTRAINT chk_total_amount
CHECK (total_amount >= 0);

ALTER TABLE sale
ADD CONSTRAINT chk_profit
CHECK (profit >= 0);

ALTER TABLE promotion
ADD CONSTRAINT chk_promotion_dates
CHECK (end_date >= start_date);

























