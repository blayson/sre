--
-- PostgreSQL models dump
--

-- Dumped from models version 11.3
-- Dumped by pg_dump version 11.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: characteristics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.characteristics (
    id integer NOT NULL
);


ALTER TABLE public.characteristics OWNER TO postgres;

--
-- Name: characteristics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.characteristics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.characteristics_id_seq OWNER TO postgres;

--
-- Name: characteristics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.characteristics_id_seq OWNED BY public.characteristics.id;


--
-- Name: characteristics_names; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.characteristics_names (
    id integer NOT NULL,
    language_id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.characteristics_names OWNER TO postgres;

--
-- Name: favourites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.favourites (
    products_id integer NOT NULL,
    users_id integer NOT NULL
);


ALTER TABLE public.favourites OWNER TO postgres;

--
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reviews_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_id_seq OWNER TO postgres;

--
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    id integer DEFAULT nextval('public.reviews_id_seq'::regclass) NOT NULL,
    products_id integer NOT NULL,
    text text NOT NULL,
    sentiment character varying(200),
    published_at date,
    retrieved_at date,
    features_text_id integer NOT NULL,
    mongo_id character(100)
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- Name: features; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.features AS
 SELECT reviews.products_id,
    reviews.features_text_id,
    reviews.sentiment,
    (count(reviews.features_text_id))::integer AS quantity
   FROM public.reviews
  GROUP BY reviews.products_id, reviews.sentiment, reviews.features_text_id;


ALTER TABLE public.features OWNER TO postgres;

--
-- Name: features_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.features_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.features_id_seq OWNER TO postgres;

--
-- Name: features_text_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.features_text_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.features_text_id_seq OWNER TO postgres;

--
-- Name: features_text; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.features_text (
    id integer DEFAULT nextval('public.features_text_id_seq'::regclass) NOT NULL,
    text text NOT NULL,
    languages_id integer NOT NULL,
    cluster_id integer,
    product_categories_id integer
);


ALTER TABLE public.features_text OWNER TO postgres;

--
-- Name: languages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.languages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.languages_id_seq OWNER TO postgres;

--
-- Name: languages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.languages (
    id integer DEFAULT nextval('public.languages_id_seq'::regclass) NOT NULL,
    title_czech character varying(50),
    title_english character varying(50),
    title_native character varying(50),
    abbreviation character varying(50)
);


ALTER TABLE public.languages OWNER TO postgres;

--
-- Name: product_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.product_categories_id_seq OWNER TO postgres;

--
-- Name: product_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_categories (
    id integer DEFAULT nextval('public.product_categories_id_seq'::regclass) NOT NULL
);


ALTER TABLE public.product_categories OWNER TO postgres;

--
-- Name: product_category_names; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_category_names (
    id integer NOT NULL,
    languages_id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.product_category_names OWNER TO postgres;

--
-- Name: product_names_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_names_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_names_id_seq OWNER TO postgres;

--
-- Name: product_names; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_names (
    id integer DEFAULT nextval('public.product_names_id_seq'::regclass) NOT NULL,
    products_id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE public.product_names OWNER TO postgres;

--
-- Name: product_visits; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_visits (
    id integer NOT NULL,
    products_id integer NOT NULL,
    visited timestamp without time zone NOT NULL,
    user_id integer
);


ALTER TABLE public.product_visits OWNER TO postgres;

--
-- Name: product_visits_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_visits_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_visits_id_seq OWNER TO postgres;

--
-- Name: product_visits_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.product_visits_id_seq OWNED BY public.product_visits.id;


--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer DEFAULT nextval('public.products_id_seq'::regclass) NOT NULL,
    name character varying(200) NOT NULL,
    brand character varying(200),
    model character varying(200),
    introduced smallint,
    url_img character varying(1000),
    url_web character varying(1000),
    product_categories_id integer,
    retrieved_at date,
    weight smallint,
    battery_capacity smallint,
    screen_size character varying(10),
    dimensions character varying(20),
    screen_resolution character varying(20)
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_characteristics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products_characteristics (
    products_id integer NOT NULL,
    characteristics_id integer NOT NULL,
    char_value character varying(200) NOT NULL
);


ALTER TABLE public.products_characteristics OWNER TO postgres;

--
-- Name: reset_passwords; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reset_passwords (
    users_id integer NOT NULL,
    token text NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.reset_passwords OWNER TO postgres;

--
-- Name: reviews_analysis_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reviews_analysis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_analysis_id_seq OWNER TO postgres;

--
-- Name: reviews_analysis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews_analysis (
    id integer DEFAULT nextval('public.reviews_analysis_id_seq'::regclass) NOT NULL,
    products_id integer,
    text text NOT NULL,
    features_text_id integer NOT NULL,
    sentiment character varying(200),
    published_at date,
    retrieved_at date,
    mongo_id character varying(100)
);


ALTER TABLE public.reviews_analysis OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer DEFAULT nextval('public.users_id_seq'::regclass) NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    registered timestamp without time zone NOT NULL,
    register_language integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: characteristics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.characteristics ALTER COLUMN id SET DEFAULT nextval('public.characteristics_id_seq'::regclass);


--
-- Name: product_visits id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_visits ALTER COLUMN id SET DEFAULT nextval('public.product_visits_id_seq'::regclass);


--
-- Name: characteristics characteristicsPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.characteristics
    ADD CONSTRAINT "characteristicsPK" PRIMARY KEY (id);


--
-- Name: characteristics_names characteristics_namesPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.characteristics_names
    ADD CONSTRAINT "characteristics_namesPK" PRIMARY KEY (id, language_id);


--
-- Name: favourites favourites_products_id_users_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favourites
    ADD CONSTRAINT favourites_products_id_users_id PRIMARY KEY (products_id, users_id);


--
-- Name: features_text features_textPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.features_text
    ADD CONSTRAINT "features_textPK" PRIMARY KEY (id);


--
-- Name: languages languagesPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT "languagesPK" PRIMARY KEY (id);


--
-- Name: product_categories product_categoriesPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_categories
    ADD CONSTRAINT "product_categoriesPK" PRIMARY KEY (id);


--
-- Name: product_category_names product_category_namesPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_category_names
    ADD CONSTRAINT "product_category_namesPK" PRIMARY KEY (id, languages_id);


--
-- Name: product_category_names product_category_namesUNQ; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_category_names
    ADD CONSTRAINT "product_category_namesUNQ" UNIQUE (languages_id, name);


--
-- Name: product_names product_namesPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_names
    ADD CONSTRAINT "product_namesPK" PRIMARY KEY (id);


--
-- Name: product_names product_namesUNQ; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_names
    ADD CONSTRAINT "product_namesUNQ" UNIQUE (products_id, name);


--
-- Name: product_visits product_visits_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_visits
    ADD CONSTRAINT product_visits_id PRIMARY KEY (id);


--
-- Name: products productsPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT "productsPK" PRIMARY KEY (id);


--
-- Name: products_characteristics products_characteristicsPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products_characteristics
    ADD CONSTRAINT "products_characteristicsPK" PRIMARY KEY (products_id, characteristics_id);


--
-- Name: reset_passwords reset_passwords_token; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reset_passwords
    ADD CONSTRAINT reset_passwords_token UNIQUE (token);


--
-- Name: reviews reviewsPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT "reviewsPK" PRIMARY KEY (id);


--
-- Name: reviews_analysis reviews_analysisPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews_analysis
    ADD CONSTRAINT "reviews_analysisPK" PRIMARY KEY (id);


--
-- Name: features_text uq_classid_productscategoriesid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.features_text
    ADD CONSTRAINT uq_classid_productscategoriesid UNIQUE (cluster_id, product_categories_id, languages_id);


--
-- Name: users usersPK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT "usersPK" PRIMARY KEY (id);


--
-- Name: users usersUNQ; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT "usersUNQ" UNIQUE (email);


--
-- Name: product_visits_products_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX product_visits_products_id ON public.product_visits USING btree (products_id);


--
-- Name: characteristics_names characteristics_namesFK1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.characteristics_names
    ADD CONSTRAINT "characteristics_namesFK1" FOREIGN KEY (language_id) REFERENCES public.languages(id);


--
-- Name: characteristics_names characteristics_namesFK3; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.characteristics_names
    ADD CONSTRAINT "characteristics_namesFK3" FOREIGN KEY (id) REFERENCES public.characteristics(id);


--
-- Name: favourites favourites_products_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favourites
    ADD CONSTRAINT favourites_products_id_fkey FOREIGN KEY (products_id) REFERENCES public.products(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: favourites favourites_users_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favourites
    ADD CONSTRAINT favourites_users_id_fkey FOREIGN KEY (users_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: features_text features_textFK1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.features_text
    ADD CONSTRAINT "features_textFK1" FOREIGN KEY (languages_id) REFERENCES public.languages(id);


--
-- Name: features_text features_textFK2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.features_text
    ADD CONSTRAINT "features_textFK2" FOREIGN KEY (product_categories_id) REFERENCES public.product_categories(id);


--
-- Name: product_category_names product_category_namesFK1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_category_names
    ADD CONSTRAINT "product_category_namesFK1" FOREIGN KEY (languages_id) REFERENCES public.languages(id);


--
-- Name: product_category_names product_category_namesFK2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_category_names
    ADD CONSTRAINT "product_category_namesFK2" FOREIGN KEY (id) REFERENCES public.product_categories(id);


--
-- Name: product_names product_namesFK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_names
    ADD CONSTRAINT "product_namesFK" FOREIGN KEY (products_id) REFERENCES public.products(id);


--
-- Name: product_visits product_visits_products_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_visits
    ADD CONSTRAINT product_visits_products_id_fkey FOREIGN KEY (products_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: product_visits product_visits_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_visits
    ADD CONSTRAINT product_visits_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: products productsFK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT "productsFK" FOREIGN KEY (product_categories_id) REFERENCES public.product_categories(id);


--
-- Name: products_characteristics products_characteristicsFK1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products_characteristics
    ADD CONSTRAINT "products_characteristicsFK1" FOREIGN KEY (products_id) REFERENCES public.products(id);


--
-- Name: products_characteristics products_characteristicsFK2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products_characteristics
    ADD CONSTRAINT "products_characteristicsFK2" FOREIGN KEY (characteristics_id) REFERENCES public.characteristics(id);


--
-- Name: reset_passwords reset_passwords_users_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reset_passwords
    ADD CONSTRAINT reset_passwords_users_id_fkey FOREIGN KEY (users_id) REFERENCES public.users(id);


--
-- Name: reviews reviewsFK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT "reviewsFK" FOREIGN KEY (products_id) REFERENCES public.products(id);


--
-- Name: reviews_analysis reviews_analysisFK1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews_analysis
    ADD CONSTRAINT "reviews_analysisFK1" FOREIGN KEY (products_id) REFERENCES public.products(id);


--
-- Name: reviews_analysis reviews_analysisFK2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews_analysis
    ADD CONSTRAINT "reviews_analysisFK2" FOREIGN KEY (features_text_id) REFERENCES public.features_text(id);


--
-- Name: reviews reviews_features_text_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_features_text_id_fkey FOREIGN KEY (features_text_id) REFERENCES public.features_text(id);


--
-- Name: users users_register_language_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_register_language_fkey FOREIGN KEY (register_language) REFERENCES public.languages(id);


--
-- PostgreSQL models dump complete
--

