CREATE SEQUENCE product_articles_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE product_articles(
  product_articles_id integer DEFAULT nextval('product_articles_seq') NOT NULL,
  products_id integer NOT NULL,
  url character varying(4000) NOT NULL,
  keywords character varying(1000),
  CONSTRAINT product_articles_PK PRIMARY KEY (product_articles_id), 
  CONSTRAINT product_articles_FK FOREIGN KEY (products_id) REFERENCES products (products_id)
);

ALTER TABLE product_articles ADD COLUMN article_title character varying(500) NOT NULL;
ALTER TABLE product_articles ADD COLUMN publication_date DATE;
ALTER TABLE product_articles ADD COLUMN mongo_id character varying(100);
