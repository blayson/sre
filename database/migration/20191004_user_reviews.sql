CREATE SEQUENCE user_reviews_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."user_reviews" (
    "id" integer DEFAULT nextval('user_reviews_id_seq') NOT NULL,
    "users_id" integer,
    "products_id" integer NOT NULL,
    "languages_id" integer NOT NULL,
    "text" text NOT NULL,
    "created_at" timestamp NOT NULL,
    "updated_at" timestamp,
    CONSTRAINT "user_reviews_id" PRIMARY KEY ("id"),
    CONSTRAINT "user_reviews_users_id_products_id" UNIQUE ("users_id", "products_id"),
    CONSTRAINT "user_reviews_languages_id_fkey" FOREIGN KEY (languages_id) REFERENCES languages(id) ON DELETE RESTRICT NOT DEFERRABLE,
    CONSTRAINT "user_reviews_products_id_fkey" FOREIGN KEY (products_id) REFERENCES products(id) ON DELETE RESTRICT NOT DEFERRABLE,
    CONSTRAINT "user_reviews_users_id_fkey" FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE SET NULL NOT DEFERRABLE
) WITH (oids = false);

CREATE INDEX "user_reviews_languages_id" ON "public"."user_reviews" USING btree ("languages_id");
CREATE INDEX "user_reviews_products_id" ON "public"."user_reviews" USING btree ("products_id");
CREATE INDEX "user_reviews_users_id" ON "public"."user_reviews" USING btree ("users_id");

CREATE SEQUENCE user_review_texts_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."user_review_texts" (
    "id" integer DEFAULT nextval('user_review_texts_id_seq') NOT NULL,
    "user_reviews_id" integer NOT NULL,
    "sentiment" character varying(200) NOT NULL,
    "text" text NOT NULL,
    CONSTRAINT "user_review_texts_id" PRIMARY KEY ("id"),
    CONSTRAINT "user_review_texts_user_reviews_id_fkey" FOREIGN KEY (user_reviews_id) REFERENCES user_reviews(id) ON DELETE CASCADE NOT DEFERRABLE
) WITH (oids = false);

CREATE INDEX "user_review_texts_user_reviews_id" ON "public"."user_review_texts" USING btree ("user_reviews_id");
