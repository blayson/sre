ALTER TABLE product_articles ADD languages_id integer;
ALTER TABLE product_articles ADD CONSTRAINT product_articlesFK2 FOREIGN KEY (languages_id) REFERENCES languages(languages_id);

 -- Velmi naivny update attributu lang :)
UPDATE product_articles SET languages_id = 1 WHERE url LIKE '%.cz%';
UPDATE product_articles SET languages_id = 2 WHERE url NOT LIKE '%.cz%';