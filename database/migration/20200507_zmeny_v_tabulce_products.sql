ALTER TABLE products DROP CONSTRAINT products_uk1;
ALTER TABLE products ADD md5_hash character varying(130);
ALTER TABLE products ADD CONSTRAINT products_uk_md5_hash UNIQUE (md5_hash);

UPDATE products 
SET md5_hash=md5(regexp_replace(
      CASE  WHEN introduced IS NULL  THEN  lower(name)
            ELSE lower(name)||introduced
      END ||
      CASE WHEN product_categories_id = 1 THEN  'cameras'
           WHEN product_categories_id = 2 THEN  'lenses'
           WHEN product_categories_id = 3 THEN  'cellphones'
      END,
      '\s', '', 'g')); 
ALTER TABLE products ALTER COLUMN md5_hash SET NOT NULL;