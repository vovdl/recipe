-- Database: recipe

-- DROP DATABASE recipe;

CREATE DATABASE recipe
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
    
-- Table: public.admin

-- DROP TABLE public.admin;

CREATE TABLE public.admin
(
    "number" numrange NOT NULL,
    user_id uuid NOT NULL,
    CONSTRAINT admin_pkey PRIMARY KEY ("number"),
    CONSTRAINT userid FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.admin
    OWNER to postgres;
    
-- Table: public.recipes

-- DROP TABLE public.recipes;

CREATE TABLE public.recipes
(
    rid uuid NOT NULL,
    rname text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    steps text COLLATE pg_catalog."default",
    type text COLLATE pg_catalog."default",
    author uuid NOT NULL,
    blocked boolean,
    creation_date timestamp with time zone NOT NULL,
    photo bytea,
    hashtags json,
    likes json,
    CONSTRAINT recipes_pkey PRIMARY KEY (rid),
    CONSTRAINT foruid FOREIGN KEY (author)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.recipes
    OWNER to postgres;
    
-- Table: public.users

-- DROP TABLE public.users;

CREATE TABLE public.users
(
    id uuid NOT NULL,
    nickname text COLLATE pg_catalog."default" NOT NULL,
    blocked boolean,
    favorites uuid[],
    password text COLLATE pg_catalog."default" NOT NULL DEFAULT 1234,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT uniqname UNIQUE (nickname)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.users
    OWNER to postgres;