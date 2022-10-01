-- Table: public.reads

-- DROP TABLE IF EXISTS public.reads;

CREATE TABLE IF NOT EXISTS public.reads
(
    "ID" integer NOT NULL DEFAULT nextval('"reads_ID_seq"'::regclass),
    variable text COLLATE pg_catalog."default" NOT NULL,
    value numeric NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT reads_pkey PRIMARY KEY ("ID")
)
