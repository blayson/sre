ALTER TABLE product_features_keywords ALTER COLUMN description DROP NOT NULL;

UPDATE reviews SET inserted_at = '2020-07-31';