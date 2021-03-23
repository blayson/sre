CREATE SEQUENCE user_roles_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE user_roles(
  user_roles_id integer DEFAULT nextval('user_roles_id_seq') NOT NULL,
  name character varying(50) NOT NULL,
  CONSTRAINT user_rolesPK PRIMARY KEY (user_roles_id)
);

ALTER TABLE users ADD COLUMN  user_roles_id integer;

ALTER TABLE users ADD CONSTRAINT user_user_rolesFK FOREIGN KEY (user_roles_id) REFERENCES user_roles(user_roles_id);

CREATE SEQUENCE reviews_suggestions_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE reviews_suggestions(
  reviews_suggestions_id integer DEFAULT nextval('reviews_suggestions_id_seq') NOT NULL,
  users_id integer NOT NULL,
  suggestion_time timestamp NOT NULL,
  reviews_id integer NOT NULL,
  sentiment character varying(200),
  feature_names_id integer,
  CONSTRAINT reviews_suggestionsPK PRIMARY KEY (reviews_suggestions_id),
  CONSTRAINT reviews_suggestions_userFK FOREIGN KEY (users_id) REFERENCES users(users_id),
  CONSTRAINT reviews_suggestionsFK FOREIGN KEY (reviews_id) REFERENCES reviews(reviews_id),
  CONSTRAINT reviews_suggestions_feature_namesFK FOREIGN KEY (feature_names_id) REFERENCES feature_names(feature_names_id)
); 
