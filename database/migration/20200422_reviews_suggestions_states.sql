DROP TABLE IF EXISTS "reviews_suggestions_states";
DROP SEQUENCE IF EXISTS reviews_suggestions_states_id_seq;
CREATE SEQUENCE reviews_suggestions_states_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE reviews_suggestions_states(
	reviews_suggestions_states_id integer DEFAULT nextval('reviews_suggestions_states_id_seq') NOT NULL,
	name character varying(50) NOT NULL,
  CONSTRAINT reviews_suggestions_statesPK PRIMARY KEY (reviews_suggestions_states_id)
);

ALTER TABLE reviews_suggestions ADD COLUMN reviews_suggestions_states_id integer;

ALTER TABLE reviews_suggestions ADD CONSTRAINT review_reviews_suggestions_statesFK FOREIGN KEY (reviews_suggestions_states_id) REFERENCES reviews_suggestions_states(reviews_suggestions_states_id);
