-- Adminer 4.7.1 PostgreSQL dump

DROP TABLE IF EXISTS "reviews_ngrams";
DROP SEQUENCE IF EXISTS reviews_ngrams_reviews_ngrams_id_seq;
CREATE SEQUENCE reviews_ngrams_reviews_ngrams_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."reviews_ngrams" (
    "reviews_ngrams_id" integer DEFAULT nextval('reviews_ngrams_reviews_ngrams_id_seq') NOT NULL,
    "reviews_id" integer NOT NULL,
    "ngram" text NOT NULL,
    "feature_names_id" integer NOT NULL,
    "sentiment" character varying(200),
    "mongo_id" character(100),
    CONSTRAINT "reviews_ngrams_reviews_id" PRIMARY KEY ("reviews_ngrams_id"),
    CONSTRAINT "reviews_ngrams_feature_names_id_fkey" FOREIGN KEY (feature_names_id) REFERENCES feature_names(feature_names_id) NOT DEFERRABLE,
    CONSTRAINT "reviews_ngrams_reviews_id_fkey" FOREIGN KEY (reviews_id) REFERENCES reviews(reviews_id) NOT DEFERRABLE
) WITH (oids = false);

-- 2020-10-08 10:31:06.092703+00
