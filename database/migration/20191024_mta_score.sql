-- Adminer 4.7.1 PostgreSQL dump

CREATE SEQUENCE mta_score_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."mta_score" (
    "id" integer DEFAULT nextval('mta_score_id_seq') NOT NULL,
    "products_id" integer NOT NULL,
    "score" numeric(4,2) NOT NULL,
    CONSTRAINT "mta_score_id" PRIMARY KEY ("id"),
    CONSTRAINT "mta_score_products_id" UNIQUE ("products_id"),
    CONSTRAINT "mta_score_products_id_fkey" FOREIGN KEY (products_id) REFERENCES products(id) ON DELETE CASCADE NOT DEFERRABLE
) WITH (oids = false);


-- 2019-10-24 15:42:59.945305+00
