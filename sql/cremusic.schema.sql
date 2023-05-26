--
-- PostgreSQL database dump
--

-- Dumped from database version 12.6
-- Dumped by pg_dump version 14.7 (Ubuntu 14.7-0ubuntu0.22.04.1)

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
-- Name: book; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.book (
    id bigint NOT NULL,
    type character varying(32),
    name character varying(256),
    background_image_url character varying(1024),
    background_color_code smallint,
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by character varying(128) DEFAULT 'system'::character varying NOT NULL,
    modified_date timestamp without time zone,
    modified_by character varying(128)
);


ALTER TABLE public.book OWNER TO admin;

--
-- Name: book_code; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.book_code (
    id bigint NOT NULL,
    serial character varying(64) NOT NULL,
    book_id bigint NOT NULL,
    code character varying(64) NOT NULL,
    release_version character varying(64) NOT NULL
);


ALTER TABLE public.book_code OWNER TO admin;

--
-- Name: book_code_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.book_code_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_code_id_seq OWNER TO admin;

--
-- Name: book_code_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.book_code_id_seq OWNED BY public.book_code.id;


--
-- Name: book_episode; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.book_episode (
    id bigint NOT NULL,
    book_id bigint NOT NULL,
    name character varying(256),
    author character varying(256) DEFAULT ''::character varying,
    artist character varying(256) DEFAULT ''::character varying,
    background_image_url character varying(1024),
    background_color_code smallint,
    created_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by character varying(128) DEFAULT 'system'::character varying NOT NULL,
    modified_date timestamp without time zone,
    modified_by character varying(128)
);


ALTER TABLE public.book_episode OWNER TO admin;

--
-- Name: book_episode_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.book_episode_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_episode_id_seq OWNER TO admin;

--
-- Name: book_episode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.book_episode_id_seq OWNED BY public.book_episode.id;


--
-- Name: book_episode_video; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.book_episode_video (
    id bigint NOT NULL,
    book_episode_id bigint NOT NULL,
    name character varying(1024),
    link character varying(1024),
    thumbnail character varying(1024),
    video_id character varying(64) NOT NULL,
    duration bigint DEFAULT 0
);


ALTER TABLE public.book_episode_video OWNER TO admin;

--
-- Name: book_episode_video_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.book_episode_video_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_episode_video_id_seq OWNER TO admin;

--
-- Name: book_episode_video_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.book_episode_video_id_seq OWNED BY public.book_episode_video.id;


--
-- Name: book_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.book_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_id_seq OWNER TO admin;

--
-- Name: book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.book_id_seq OWNED BY public.book.id;


--
-- Name: config; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.config (
    id bigint NOT NULL,
    required_unlock boolean,
    global_code character varying(250),
    secret character varying(250)
);


ALTER TABLE public.config OWNER TO admin;

--
-- Name: config_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.config_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.config_id_seq OWNER TO admin;

--
-- Name: config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.config_id_seq OWNED BY public.config.id;


--
-- Name: flyway_schema_history; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.flyway_schema_history (
    installed_rank integer NOT NULL,
    version character varying(50),
    description character varying(200) NOT NULL,
    type character varying(20) NOT NULL,
    script character varying(1000) NOT NULL,
    checksum integer,
    installed_by character varying(100) NOT NULL,
    installed_on timestamp without time zone DEFAULT now() NOT NULL,
    execution_time integer NOT NULL,
    success boolean NOT NULL
);


ALTER TABLE public.flyway_schema_history OWNER TO admin;

--
-- Name: statistic_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.statistic_log (
    id bigint NOT NULL,
    telephone character varying(16) NOT NULL,
    code character varying(64) NOT NULL,
    name character varying(256) NOT NULL,
    email character varying(256)
);


ALTER TABLE public.statistic_log OWNER TO admin;

--
-- Name: statistic_log_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.statistic_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistic_log_id_seq OWNER TO admin;

--
-- Name: statistic_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.statistic_log_id_seq OWNED BY public.statistic_log.id;


--
-- Name: book id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book ALTER COLUMN id SET DEFAULT nextval('public.book_id_seq'::regclass);


--
-- Name: book_code id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book_code ALTER COLUMN id SET DEFAULT nextval('public.book_code_id_seq'::regclass);


--
-- Name: book_episode id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book_episode ALTER COLUMN id SET DEFAULT nextval('public.book_episode_id_seq'::regclass);


--
-- Name: book_episode_video id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book_episode_video ALTER COLUMN id SET DEFAULT nextval('public.book_episode_video_id_seq'::regclass);


--
-- Name: config id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.config ALTER COLUMN id SET DEFAULT nextval('public.config_id_seq'::regclass);


--
-- Name: statistic_log id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.statistic_log ALTER COLUMN id SET DEFAULT nextval('public.statistic_log_id_seq'::regclass);


--
-- Name: book_code book_code_code_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book_code
    ADD CONSTRAINT book_code_code_key UNIQUE (code);


--
-- Name: book_code book_code_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book_code
    ADD CONSTRAINT book_code_pk PRIMARY KEY (id);


--
-- Name: book_code book_code_serial_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book_code
    ADD CONSTRAINT book_code_serial_key UNIQUE (serial);


--
-- Name: book_episode book_episode_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book_episode
    ADD CONSTRAINT book_episode_pk PRIMARY KEY (id);


--
-- Name: book_episode_video book_episode_video_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book_episode_video
    ADD CONSTRAINT book_episode_video_pk PRIMARY KEY (id);


--
-- Name: book book_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_pk PRIMARY KEY (id);


--
-- Name: config config_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.config
    ADD CONSTRAINT config_pk PRIMARY KEY (id);


--
-- Name: flyway_schema_history flyway_schema_history_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.flyway_schema_history
    ADD CONSTRAINT flyway_schema_history_pk PRIMARY KEY (installed_rank);


--
-- Name: statistic_log statistic_log_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.statistic_log
    ADD CONSTRAINT statistic_log_pk PRIMARY KEY (id);


--
-- Name: statistic_log statistic_log_unique; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.statistic_log
    ADD CONSTRAINT statistic_log_unique UNIQUE (telephone, code);


--
-- Name: flyway_schema_history_s_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX flyway_schema_history_s_idx ON public.flyway_schema_history USING btree (success);


--
-- Name: book_code book_code_book_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book_code
    ADD CONSTRAINT book_code_book_fk FOREIGN KEY (book_id) REFERENCES public.book(id);


--
-- Name: book_episode book_episode_book_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book_episode
    ADD CONSTRAINT book_episode_book_fk FOREIGN KEY (book_id) REFERENCES public.book(id);


--
-- Name: book_episode_video book_episode_video_book_episode_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.book_episode_video
    ADD CONSTRAINT book_episode_video_book_episode_fk FOREIGN KEY (book_episode_id) REFERENCES public.book_episode(id);


--
-- PostgreSQL database dump complete
--

