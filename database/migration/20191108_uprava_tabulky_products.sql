ALTER TABLE products DROP COLUMN IF EXISTS weight;
ALTER TABLE products DROP COLUMN IF EXISTS battery_capacity;
ALTER TABLE products DROP COLUMN IF EXISTS screen_size;
ALTER TABLE products DROP COLUMN IF EXISTS dimensions;
ALTER TABLE products DROP COLUMN IF EXISTS screen_resolution;
ALTER TABLE products ADD COLUMN inserted_at date;       
ALTER TABLE products ADD CONSTRAINT products_UK1 UNIQUE (name, introduced, product_categories_id);


