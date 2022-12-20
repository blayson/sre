ALTER TABLE reviews_suggestions ADD COLUMN old_sentiment character varying(200);
ALTER TABLE reviews_suggestions ADD COLUMN old_feature_names_id integer;

ALTER TABLE reviews_suggestions ADD CONSTRAINT reviews_suggestions_old_feature_namesFK FOREIGN KEY (old_feature_names_id) REFERENCES feature_names(feature_names_id);
