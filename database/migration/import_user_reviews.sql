-- Adminer 4.7.0 PostgreSQL dump

INSERT INTO "user_reviews" ("user_reviews_id", "users_id", "products_id", "languages_id", "text", "created_at", "updated_at") VALUES
(1,	1,	16662,	1,	'Textová recenze',	'2020-09-24 12:33:55.844907',	NULL);

INSERT INTO "user_review_texts" ("user_review_texts_id", "user_reviews_id", "sentiment", "text") VALUES
(1,	1,	'positive',	'Vysoká kvalita fotek'),
(2,	1,	'positive',	'Světelný objektiv'),
(3,	1,	'negative',	'Přemrštěná cena'),
(4,	1,	'negative',	'Malá výdrž baterie');


-- 2019-02-03 15:15:55.663222+01
