--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE "FabioDanesin";
ALTER ROLE "FabioDanesin" WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:2yPRqdAWUmrtUmYEBd8vUQ==$Ayj4E0l8Hxy9tytvDVf2zEnijqM4uZSndKn0qnIG87A=:gJYnAmi/hM8oI23hH9GZhVpTXb/1L9hlo2UZ4Z4f6LI=';
CREATE ROLE "Vir2em_Danilo";
ALTER ROLE "Vir2em_Danilo" WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:Xd10harN+GTPUlrMkZBweQ==$mlbklr1p/yRY1e0arEF0VK/KO5tIpqENut93Qq/qq98=:vy1jnv51ZKb3poXVkfbbe1onsIXxHxPX6lxB7prJOlQ=';
CREATE ROLE "Vir2em_Fabio";
ALTER ROLE "Vir2em_Fabio" WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:t1aV1nFxTpRSG+Ylxpx54Q==$/BzU/NQVRZcmt1Ne8vkZZk6qIXHs5KgJg1WVgAw/ax8=:s6k4I/ldhc0Hc89byArel2prh6G3bbA5Ic2pb/QSw0M=';
CREATE ROLE "Vir2em_Silvia";
ALTER ROLE "Vir2em_Silvia" WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:96AQJA4A/9Qlr56wBE6H8g==$Se0JRdcsYZ6t/fgrTJniFg6O3Gu7qdSneUVSdUkCeOo=:eDCNMKqlM9if9QdMs/GgBPf6eadu16B19xSGTKjM58k=';
CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:75BaU9VaBkQLoe/VhLya0w==$6X1VlN472m2F8I5AMisxZ/VresV0oNcMCI/Iqwt9mPI=:hAB7x4YEVAs8tMUJMBKAPztIdAcG9wVY1vXgPBC9vyU=';






--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4 (Ubuntu 14.4-1.pgdg20.04+1)
-- Dumped by pg_dump version 14.4 (Ubuntu 14.4-1.pgdg20.04+1)

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

--
-- PostgreSQL database dump complete
--

--
-- Database "data" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4 (Ubuntu 14.4-1.pgdg20.04+1)
-- Dumped by pg_dump version 14.4 (Ubuntu 14.4-1.pgdg20.04+1)

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

--
-- Name: data; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE data WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'it_IT.UTF-8';


ALTER DATABASE data OWNER TO postgres;

\connect data

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
-- Name: Test; Type: TABLE; Schema: public; Owner: Vir2em_Fabio
--

CREATE TABLE public."Test" (
    "Timestamp" date,
    "Hour" integer,
    "Value" character varying(20)
);


ALTER TABLE public."Test" OWNER TO "Vir2em_Fabio";

--
-- Name: testvariable; Type: TABLE; Schema: public; Owner: Vir2em_Fabio
--

CREATE TABLE public.testvariable (
    "Timestamp" date NOT NULL,
    "Hour" integer NOT NULL,
    "Value" character varying(20) NOT NULL
);


ALTER TABLE public.testvariable OWNER TO "Vir2em_Fabio";

--
-- Data for Name: Test; Type: TABLE DATA; Schema: public; Owner: Vir2em_Fabio
--

COPY public."Test" ("Timestamp", "Hour", "Value") FROM stdin;
\.


--
-- Data for Name: testvariable; Type: TABLE DATA; Schema: public; Owner: Vir2em_Fabio
--

COPY public.testvariable ("Timestamp", "Hour", "Value") FROM stdin;
2021-11-16	14	21
2021-11-16	14	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-18	11	21
2021-11-18	12	21
2021-12-03	11	21
2021-12-03	11	21
\.


--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4 (Ubuntu 14.4-1.pgdg20.04+1)
-- Dumped by pg_dump version 14.4 (Ubuntu 14.4-1.pgdg20.04+1)

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

--
-- Name: get_max_attempts(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_max_attempts() RETURNS integer
    LANGUAGE plpgsql IMMUTABLE LEAKPROOF COST 1 PARALLEL SAFE
    AS $$
BEGIN
    RETURN 5;
END;$$;


ALTER FUNCTION public.get_max_attempts() OWNER TO postgres;

--
-- Name: FUNCTION get_max_attempts(); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public.get_max_attempts() IS 'Funzione di workaround per ottenere il massimo numero di tentativi di login prima di attivare il blocco account';


--
-- Name: hash_user_on_insertion(); Type: FUNCTION; Schema: public; Owner: Vir2em_Fabio
--

CREATE FUNCTION public.hash_user_on_insertion() RETURNS trigger
    LANGUAGE plpgsql STABLE LEAKPROOF
    AS $$DECLARE 
    HASHED_PASSWORD TEXT;
    HASHED_USERNAME TEXT;
    
    BEGIN
        HASHED_PASSWORD := HASHSTRING(NEW.PASSWORD);
        HASHED_USERNAME := HASHSTRING(NEW.NAME);
        NEW.PASSWORD := TRIM(LEADING '\x' FROM HASHED_PASSWORD);
        NEW.NAME := TRIM(LEADING '\x' FROM HASHED_USERNAME);
        RETURN NEW;
    END;
    $$;


ALTER FUNCTION public.hash_user_on_insertion() OWNER TO "Vir2em_Fabio";

--
-- Name: hashstring(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.hashstring(i text) RETURNS text
    LANGUAGE plpgsql
    AS $$
        BEGIN
                RETURN (sha256(i :: bytea));
        END;
$$;


ALTER FUNCTION public.hashstring(i text) OWNER TO postgres;

--
-- Name: lock_users(); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.lock_users()
    LANGUAGE plpgsql
    AS $$DECLARE
    MAXATTEMPTS INTEGER;
BEGIN 
    MAXATTEMPTS = GET_MAX_ATTEMPTS();
    
    UPDATE USERS
    SET LOCKED = TRUE
    WHERE NAME =ANY (
        SELECT D.USERNAME 
        FROM LOGIN_ATTEMPTS L JOIN LOGIN_DATA_USED D ON D.CONNECTION_ID = L.CONNECTION_ID
        WHERE L.ATTEMPTS >= MAXATTEMPTS
        GROUP BY D.USERNAME
    );
END;$$;


ALTER PROCEDURE public.lock_users() OWNER TO postgres;

--
-- Name: lock_users_after_max_attempt(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.lock_users_after_max_attempt() RETURNS trigger
    LANGUAGE plpgsql LEAKPROOF
    AS $$BEGIN 
    CALL LOCK_USERS();
    
    DELETE FROM LOGIN_ATTEMPTS 
    WHERE ATTEMPTS > GET_MAX_ATTEMPTS();
    
    RETURN NULL;
END;$$;


ALTER FUNCTION public.lock_users_after_max_attempt() OWNER TO postgres;

--
-- Name: tr_maintain_one_admin(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.tr_maintain_one_admin() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
	
	BEGIN 
		IF NEW.PERMISSION='ADMIN'
		THEN RETURN NULL;
		ELSE RETURN NEW;
		END IF;
	END;

$$;


ALTER FUNCTION public.tr_maintain_one_admin() OWNER TO postgres;

--
-- Name: unique_connection_id(); Type: FUNCTION; Schema: public; Owner: Vir2em_Fabio
--

CREATE FUNCTION public.unique_connection_id() RETURNS trigger
    LANGUAGE plpgsql IMMUTABLE LEAKPROOF
    AS $$
BEGIN 
 
    IF (
        SELECT C.CONNECTION_ID
        FROM LOGIN_ATTEMPTS C
        WHERE C.CONNECTION_ID = NEW.CONNECTION_ID
      ) != NULL
    
    THEN 
        
        UPDATE LOGIN_ATTEMPTS C
        SET C.ATTEMPTS = C.ATTEMPTS + 1
        WHERE C.CONNECTION_ID = NEW.CONNECTION_ID;
        
        RETURN NULL;
    ELSE
    
        RETURN NEW;
    
    END IF;
END;$$;


ALTER FUNCTION public.unique_connection_id() OWNER TO "Vir2em_Fabio";

--
-- Name: FUNCTION unique_connection_id(); Type: COMMENT; Schema: public; Owner: Vir2em_Fabio
--

COMMENT ON FUNCTION public.unique_connection_id() IS 'Trigger per uniqueness nel database in modo da fare silent fail. ';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Test; Type: TABLE; Schema: public; Owner: Vir2em_Fabio
--

CREATE TABLE public."Test" (
    "Timestamp" date,
    "Hour" integer,
    "Value" character varying(20)
);


ALTER TABLE public."Test" OWNER TO "Vir2em_Fabio";

--
-- Name: login_attempts; Type: TABLE; Schema: public; Owner: Vir2em_Fabio
--

CREATE TABLE public.login_attempts (
    connection_id character varying(70) NOT NULL,
    attempts smallint DEFAULT (0)::smallint NOT NULL
);


ALTER TABLE public.login_attempts OWNER TO "Vir2em_Fabio";

--
-- Name: login_data_used; Type: TABLE; Schema: public; Owner: Vir2em_Fabio
--

CREATE TABLE public.login_data_used (
    connection_id character varying(65) NOT NULL,
    username character varying(65) NOT NULL,
    password character varying(65) NOT NULL
);


ALTER TABLE public.login_data_used OWNER TO "Vir2em_Fabio";

--
-- Name: tabletest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tabletest (
    "Name" character varying(20) NOT NULL,
    "Age" integer NOT NULL
);


ALTER TABLE public.tabletest OWNER TO postgres;

--
-- Name: testvariable; Type: TABLE; Schema: public; Owner: Vir2em_Fabio
--

CREATE TABLE public.testvariable (
    "Timestamp" date NOT NULL,
    "Hour" integer NOT NULL,
    "Value" character varying(20) NOT NULL
);


ALTER TABLE public.testvariable OWNER TO "Vir2em_Fabio";

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying NOT NULL,
    password character varying NOT NULL,
    permission character varying DEFAULT 'NONE'::character varying NOT NULL,
    locked boolean DEFAULT false NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: TABLE users; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.users IS 'Tabella degli user registrati al sito. Indexata per ottenere migliori performance durante operazioni di lettura.';


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: Test; Type: TABLE DATA; Schema: public; Owner: Vir2em_Fabio
--

COPY public."Test" ("Timestamp", "Hour", "Value") FROM stdin;
\.


--
-- Data for Name: login_attempts; Type: TABLE DATA; Schema: public; Owner: Vir2em_Fabio
--

COPY public.login_attempts (connection_id, attempts) FROM stdin;
i	4
ADD	19
\.


--
-- Data for Name: login_data_used; Type: TABLE DATA; Schema: public; Owner: Vir2em_Fabio
--

COPY public.login_data_used (connection_id, username, password) FROM stdin;
i	iiiii	iii
ADD	F	F
\.


--
-- Data for Name: tabletest; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tabletest ("Name", "Age") FROM stdin;
pain	21
eqe	2221
ffff	2313
\.


--
-- Data for Name: testvariable; Type: TABLE DATA; Schema: public; Owner: Vir2em_Fabio
--

COPY public.testvariable ("Timestamp", "Hour", "Value") FROM stdin;
2021-11-16	14	21
2021-11-16	14	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-18	11	21
2021-11-18	12	21
2021-12-03	11	21
2021-12-03	11	21
2021-11-16	14	21
2021-11-16	14	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-18	11	21
2021-11-18	12	21
2021-12-03	11	21
2021-12-03	11	21
2021-11-16	14	21
2021-11-16	14	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-16	15	21
2021-11-18	11	21
2021-11-18	12	21
2021-12-03	11	21
2021-12-03	11	21
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, password, permission, locked) FROM stdin;
2	F	F	WRITE	t
1	ac6e64cc3b26d5a2021e45f47477c7b2318e15930e16eef2a3088c7fae16ef74	7c97da358f978fc737e871d3212ba92c0274ef6c5e7aae785640e01d32f69faf	ADMIN	f
3	4424343a3c7d78f6cc7a7689d6a542b61b842045ce7f0b10bd634f88a75cd335	3a26ef7aa2f5c30226a2c45538eddec1fec94ea04b6451a831c2a2102aa1522e	READ	f
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: login_data_used connection_id_unique; Type: CONSTRAINT; Schema: public; Owner: Vir2em_Fabio
--

ALTER TABLE ONLY public.login_data_used
    ADD CONSTRAINT connection_id_unique UNIQUE (connection_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: login_data_used login_data_used_pkey; Type: CONSTRAINT; Schema: public; Owner: Vir2em_Fabio
--

ALTER TABLE ONLY public.login_data_used
    ADD CONSTRAINT login_data_used_pkey PRIMARY KEY (connection_id);


--
-- Name: tabletest tabletest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tabletest
    ADD CONSTRAINT tabletest_pkey PRIMARY KEY ("Name", "Age");


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: con_id_index; Type: INDEX; Schema: public; Owner: Vir2em_Fabio
--

CREATE UNIQUE INDEX con_id_index ON public.login_attempts USING btree (connection_id);


--
-- Name: INDEX con_id_index; Type: COMMENT; Schema: public; Owner: Vir2em_Fabio
--

COMMENT ON INDEX public.con_id_index IS 'Index su connection ID';


--
-- Name: fki_P; Type: INDEX; Schema: public; Owner: Vir2em_Fabio
--

CREATE INDEX "fki_P" ON public.login_attempts USING btree (connection_id);


--
-- Name: id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX id_index ON public.users USING btree (id);


--
-- Name: users hash_username_password; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER hash_username_password BEFORE INSERT OR UPDATE OF name, password ON public.users FOR EACH ROW EXECUTE FUNCTION public.hash_user_on_insertion();


--
-- Name: login_attempts lockusers; Type: TRIGGER; Schema: public; Owner: Vir2em_Fabio
--

CREATE TRIGGER lockusers AFTER UPDATE ON public.login_attempts FOR EACH STATEMENT EXECUTE FUNCTION public.lock_users_after_max_attempt();


--
-- Name: users tr_repel_admin; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_repel_admin BEFORE INSERT OR UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.tr_maintain_one_admin();

ALTER TABLE public.users DISABLE TRIGGER tr_repel_admin;


--
-- Name: login_attempts con_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: Vir2em_Fabio
--

ALTER TABLE ONLY public.login_attempts
    ADD CONSTRAINT con_id_fk FOREIGN KEY (connection_id) REFERENCES public.login_data_used(connection_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

--
-- Database "users" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4 (Ubuntu 14.4-1.pgdg20.04+1)
-- Dumped by pg_dump version 14.4 (Ubuntu 14.4-1.pgdg20.04+1)

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

--
-- Name: users; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE users WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'it_IT.UTF-8';


ALTER DATABASE users OWNER TO postgres;

\connect users

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

--
-- Name: clean(); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.clean()
    LANGUAGE sql SECURITY DEFINER
    AS $$DELETE FROM LOGIN_ATTEMPTS;
DELETE FROM LOGIN_DATA_USED;
$$;


ALTER PROCEDURE public.clean() OWNER TO postgres;

--
-- Name: get_max_attempts(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_max_attempts() RETURNS integer
    LANGUAGE plpgsql IMMUTABLE LEAKPROOF COST 1 PARALLEL SAFE
    AS $$
BEGIN
    RETURN 5;
END;$$;


ALTER FUNCTION public.get_max_attempts() OWNER TO postgres;

--
-- Name: FUNCTION get_max_attempts(); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public.get_max_attempts() IS 'Funzione di workaround per ottenere il massimo numero di tentativi di login prima di attivare il blocco account';


--
-- Name: hash_user_on_insertion(); Type: FUNCTION; Schema: public; Owner: Vir2em_Fabio
--

CREATE FUNCTION public.hash_user_on_insertion() RETURNS trigger
    LANGUAGE plpgsql STABLE LEAKPROOF
    AS $$DECLARE 
    HASHED_PASSWORD TEXT;
    HASHED_USERNAME TEXT;
    
    BEGIN
        HASHED_PASSWORD := HASHSTRING(NEW.PASSWORD);
        HASHED_USERNAME := HASHSTRING(NEW.NAME);
        NEW.PASSWORD := TRIM(LEADING '\x' FROM HASHED_PASSWORD);
        NEW.NAME := TRIM(LEADING '\x' FROM HASHED_USERNAME);
        RETURN NEW;
    END;
    $$;


ALTER FUNCTION public.hash_user_on_insertion() OWNER TO "Vir2em_Fabio";

--
-- Name: hashstring(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.hashstring(i text) RETURNS text
    LANGUAGE plpgsql IMMUTABLE STRICT LEAKPROOF COST 1 PARALLEL SAFE
    AS $$        DECLARE 
            META BYTEA;
        BEGIN
            META=(sha256(i::bytea))::text;
            
            RETURN TRIM(LEADING '\x' FROM META);
        END;
$$;


ALTER FUNCTION public.hashstring(i text) OWNER TO postgres;

--
-- Name: lock_users(); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.lock_users()
    LANGUAGE plpgsql
    AS $$DECLARE
    MAXATTEMPTS INTEGER;
BEGIN 
    MAXATTEMPTS = GET_MAX_ATTEMPTS();
    
    UPDATE USERS
    SET LOCKED = TRUE
    WHERE NAME =ANY (
        SELECT D.USERNAME 
        FROM LOGIN_ATTEMPTS L JOIN LOGIN_DATA_USED D ON D.CONNECTION_ID = L.CONNECTION_ID
        WHERE L.ATTEMPTS >= MAXATTEMPTS
        GROUP BY D.USERNAME
    );
END;$$;


ALTER PROCEDURE public.lock_users() OWNER TO postgres;

--
-- Name: lock_users_after_max_attempt(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.lock_users_after_max_attempt() RETURNS trigger
    LANGUAGE plpgsql LEAKPROOF
    AS $$BEGIN 
    CALL LOCK_USERS();
    
    DELETE FROM LOGIN_ATTEMPTS 
    WHERE ATTEMPTS > GET_MAX_ATTEMPTS();
    
    RETURN NULL;
END;$$;


ALTER FUNCTION public.lock_users_after_max_attempt() OWNER TO postgres;

--
-- Name: tr_maintain_one_admin(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.tr_maintain_one_admin() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
	
	BEGIN 
		IF NEW.PERMISSION='ADMIN'
		THEN RETURN NULL;
		ELSE RETURN NEW;
		END IF;
	END;

$$;


ALTER FUNCTION public.tr_maintain_one_admin() OWNER TO postgres;

--
-- Name: unique_connection_id(); Type: FUNCTION; Schema: public; Owner: Vir2em_Fabio
--

CREATE FUNCTION public.unique_connection_id() RETURNS trigger
    LANGUAGE plpgsql IMMUTABLE LEAKPROOF
    AS $$
BEGIN 
 
    IF (
        SELECT C.CONNECTION_ID
        FROM LOGIN_ATTEMPTS C
        WHERE C.CONNECTION_ID = NEW.CONNECTION_ID
      ) != NULL
    
    THEN 
        
        UPDATE LOGIN_ATTEMPTS C
        SET C.ATTEMPTS = C.ATTEMPTS + 1
        WHERE C.CONNECTION_ID = NEW.CONNECTION_ID;
        
        RETURN NULL;
    ELSE
    
        RETURN NEW;
    
    END IF;
END;$$;


ALTER FUNCTION public.unique_connection_id() OWNER TO "Vir2em_Fabio";

--
-- Name: FUNCTION unique_connection_id(); Type: COMMENT; Schema: public; Owner: Vir2em_Fabio
--

COMMENT ON FUNCTION public.unique_connection_id() IS 'Trigger per uniqueness nel database in modo da fare silent fail. ';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: login_attempts; Type: TABLE; Schema: public; Owner: Vir2em_Fabio
--

CREATE TABLE public.login_attempts (
    connection_id character varying(70) NOT NULL,
    attempts smallint DEFAULT (0)::smallint NOT NULL
);


ALTER TABLE public.login_attempts OWNER TO "Vir2em_Fabio";

--
-- Name: login_data_used; Type: TABLE; Schema: public; Owner: Vir2em_Fabio
--

CREATE TABLE public.login_data_used (
    connection_id character varying(65) NOT NULL,
    username character varying(65) NOT NULL,
    password character varying(65) NOT NULL
);


ALTER TABLE public.login_data_used OWNER TO "Vir2em_Fabio";

--
-- Name: tabletest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tabletest (
    "Name" character varying(20) NOT NULL,
    "Age" integer NOT NULL
);


ALTER TABLE public.tabletest OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying NOT NULL,
    password character varying NOT NULL,
    permission character varying DEFAULT 'NONE'::character varying NOT NULL,
    locked boolean DEFAULT false NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: TABLE users; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.users IS 'Tabella degli user registrati al sito. Indexata per ottenere migliori performance durante operazioni di lettura.';


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: login_attempts; Type: TABLE DATA; Schema: public; Owner: Vir2em_Fabio
--

COPY public.login_attempts (connection_id, attempts) FROM stdin;
\.


--
-- Data for Name: login_data_used; Type: TABLE DATA; Schema: public; Owner: Vir2em_Fabio
--

COPY public.login_data_used (connection_id, username, password) FROM stdin;
\.


--
-- Data for Name: tabletest; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tabletest ("Name", "Age") FROM stdin;
pain	21
eqe	2221
ffff	2313
rrrrr	3456
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, password, permission, locked) FROM stdin;
1	c91042961c2c888776e14bc58dc5be72f9b4206839287f29e4d40db3021564ca	c91042961c2c888776e14bc58dc5be72f9b4206839287f29e4d40db3021564ca	ADMIN	f
3	27172a8c0d97e70c541e91a7f3e7b337c6f22f370a9f244df3ccee47cb9aee80	27172a8c0d97e70c541e91a7f3e7b337c6f22f370a9f244df3ccee47cb9aee80	READ	f
4	12e33ebe1016aab11a37784c00f7e716bfbcdecc9338a7ad4c1608ddcf706381	12e33ebe1016aab11a37784c00f7e716bfbcdecc9338a7ad4c1608ddcf706381	WRITE	f
2	8f65aa0b044963ddbfde4f3d4dbc29e6494d1aa5754d9f1c001886304fee20f1	772fa128ee814a5a6d35895f55ae1d830efd88faa56b4858cef2f8c6b741aad4	WRITE	f
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: tabletest tabletest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tabletest
    ADD CONSTRAINT tabletest_pkey PRIMARY KEY ("Name", "Age");


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: con_id_index; Type: INDEX; Schema: public; Owner: Vir2em_Fabio
--

CREATE UNIQUE INDEX con_id_index ON public.login_attempts USING btree (connection_id);


--
-- Name: INDEX con_id_index; Type: COMMENT; Schema: public; Owner: Vir2em_Fabio
--

COMMENT ON INDEX public.con_id_index IS 'Index su connection ID';


--
-- Name: fki_P; Type: INDEX; Schema: public; Owner: Vir2em_Fabio
--

CREATE INDEX "fki_P" ON public.login_attempts USING btree (connection_id);


--
-- Name: id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX id_index ON public.users USING btree (id);


--
-- Name: users hash_username_password; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER hash_username_password BEFORE INSERT OR UPDATE OF name, password ON public.users FOR EACH ROW EXECUTE FUNCTION public.hash_user_on_insertion();

ALTER TABLE public.users DISABLE TRIGGER hash_username_password;


--
-- Name: login_attempts lockusers; Type: TRIGGER; Schema: public; Owner: Vir2em_Fabio
--

CREATE TRIGGER lockusers AFTER UPDATE ON public.login_attempts FOR EACH STATEMENT EXECUTE FUNCTION public.lock_users_after_max_attempt();


--
-- Name: users tr_repel_admin; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_repel_admin BEFORE INSERT OR UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.tr_maintain_one_admin();

ALTER TABLE public.users DISABLE TRIGGER tr_repel_admin;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

