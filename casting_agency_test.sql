--
-- PostgreSQL database dump
--

-- Dumped from database version 12.14
-- Dumped by pg_dump version 12.14

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

SET default_table_access_method = heap;

--
-- Name: Actor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Actor" (
    id integer NOT NULL,
    name character varying,
    age character varying,
    gender character varying,
    image_link character varying(500)
);


ALTER TABLE public."Actor" OWNER TO postgres;

--
-- Name: Actor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Actor_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Actor_id_seq" OWNER TO postgres;

--
-- Name: Actor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Actor_id_seq" OWNED BY public."Actor".id;


--
-- Name: Movie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Movie" (
    id integer NOT NULL,
    title character varying,
    release_date character varying(120),
    image_link character varying(500)
);


ALTER TABLE public."Movie" OWNER TO postgres;

--
-- Name: Movie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Movie_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Movie_id_seq" OWNER TO postgres;

--
-- Name: Movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Movie_id_seq" OWNED BY public."Movie".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: Actor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Actor" ALTER COLUMN id SET DEFAULT nextval('public."Actor_id_seq"'::regclass);


--
-- Name: Movie id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Movie" ALTER COLUMN id SET DEFAULT nextval('public."Movie_id_seq"'::regclass);


--
-- Data for Name: Actor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Actor" (id, name, age, gender, image_link) FROM stdin;
1	Tom Cruise 1	61	Male	https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSBLeRgKyes_KnoMlt9eQd2YxXV5y3mhAVzCLteT4c7qQf_bp-eEJPUuLeSsnvQk-ecvGOMwXXPgTS2RLs
2	Tom Cruise 2	62	Male	https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSBLeRgKyes_KnoMlt9eQd2YxXV5y3mhAVzCLteT4c7qQf_bp-eEJPUuLeSsnvQk-ecvGOMwXXPgTS2RLs
3	Tom Cruise 3	63	Male	https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSBLeRgKyes_KnoMlt9eQd2YxXV5y3mhAVzCLteT4c7qQf_bp-eEJPUuLeSsnvQk-ecvGOMwXXPgTS2RLs
4	Tom Cruise 4	64	Male	https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSBLeRgKyes_KnoMlt9eQd2YxXV5y3mhAVzCLteT4c7qQf_bp-eEJPUuLeSsnvQk-ecvGOMwXXPgTS2RLs
5	Tom Cruise 5	65	Male	https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSBLeRgKyes_KnoMlt9eQd2YxXV5y3mhAVzCLteT4c7qQf_bp-eEJPUuLeSsnvQk-ecvGOMwXXPgTS2RLs
\.


--
-- Data for Name: Movie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Movie" (id, title, release_date, image_link) FROM stdin;
1	Avengers: Endgame 1	28/12/2019	https://prod-ripcut-delivery.disney-plus.net/v1/variant/disney/863E75A035911DBA10F8D7EE1E433A12A1BF4915670B66597AC31C585A291942/scale?width=1200&aspectRatio=1.78&format=jpeg
2	Avengers: Endgame 2	28/12/2020	https://prod-ripcut-delivery.disney-plus.net/v1/variant/disney/863E75A035911DBA10F8D7EE1E433A12A1BF4915670B66597AC31C585A291942/scale?width=1200&aspectRatio=1.78&format=jpeg
3	Avengers: Endgame 3	28/12/2021	https://prod-ripcut-delivery.disney-plus.net/v1/variant/disney/863E75A035911DBA10F8D7EE1E433A12A1BF4915670B66597AC31C585A291942/scale?width=1200&aspectRatio=1.78&format=jpeg
4	Avengers: Endgame 4	28/12/2022	https://prod-ripcut-delivery.disney-plus.net/v1/variant/disney/863E75A035911DBA10F8D7EE1E433A12A1BF4915670B66597AC31C585A291942/scale?width=1200&aspectRatio=1.78&format=jpeg
5	Avengers: Endgame 5	28/12/2023	https://prod-ripcut-delivery.disney-plus.net/v1/variant/disney/863E75A035911DBA10F8D7EE1E433A12A1BF4915670B66597AC31C585A291942/scale?width=1200&aspectRatio=1.78&format=jpeg
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
e5eaad9478c1
\.


--
-- Name: Actor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Actor_id_seq"', 5, true);


--
-- Name: Movie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Movie_id_seq"', 5, true);


--
-- Name: Actor Actor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Actor"
    ADD CONSTRAINT "Actor_pkey" PRIMARY KEY (id);


--
-- Name: Movie Movie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Movie"
    ADD CONSTRAINT "Movie_pkey" PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- PostgreSQL database dump complete
--

