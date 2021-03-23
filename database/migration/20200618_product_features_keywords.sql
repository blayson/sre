CREATE TABLE product_features_keywords (
products_id integer NOT NULL, 
feature_names_id integer NOT NULL,
description VARCHAR(2000) NOT NULL,
CONSTRAINT product_features_keywordsPK PRIMARY KEY(products_id,feature_names_id),
CONSTRAINT product_features_keywordsFK_products_id FOREIGN KEY (products_id) REFERENCES products(products_id),
CONSTRAINT product_features_keywordsFK_feature_names_id FOREIGN KEY (feature_names_id) REFERENCES feature_names(feature_names_id)
);