DROP DATABASE warehouse;
CREATE DATABASE warehouse WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';

DROP TABLE public.categories;
CREATE TABLE public.categories (
    id bigint NOT NULL,
    name character varying(255) NOT NULL
);

DROP TABLE public.goods;
CREATE TABLE public.goods (
    id bigint NOT NULL,
    category_id bigint NOT NULL,
    name character varying(255) NOT NULL,
    quantity integer NOT NULL,
    quantity_unit character varying(255) NOT NULL,
    term integer NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL
);

ALTER TABLE ONLY public.categories DROP CONSTRAINT categories_pkey;
ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.goods DROP CONSTRAINT goods_pkey;
ALTER TABLE ONLY public.goods
    ADD CONSTRAINT goods_pkey PRIMARY KEY (id);
