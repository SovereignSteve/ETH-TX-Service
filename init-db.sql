CREATE ROLE publisher WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
  
CREATE ROLE consumer WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
  
CREATE ROLE grafana WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  ENCRYPTED PASSWORD 'SCRAM-SHA-256$4096:kvOU5bMaDZDE84zl11FvMw==$MIyX8ydqHPU0l8HqvGkn5Jkm4UP+rcnTFAOhzkaQfs0=:YWJXGXigQvbQGscPfIEEyBzAR8L1UVNFtXWpzVfy9uk=';

GRANT consumer TO grafana;

CREATE ROLE pyservice WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  ENCRYPTED PASSWORD 'SCRAM-SHA-256$4096:jvKBURu1yk1n0VHxoDNlSw==$+XsVqLmKa1Ss3fbMcoqBbdPr2z0afDVZYqJoeSw3uks=:svKRyvReLee0YCSM38BxlPU+Pi9UlFTE3a/ISi0AyHg=';

GRANT publisher TO pyservice;

-- Table: public.transactions

-- DROP TABLE public.transactions;

CREATE TABLE IF NOT EXISTS public.transactions
(
    blocknumber bigint NOT NULL,
    tx_time bigint NOT NULL,
    hash text COLLATE pg_catalog."default" NOT NULL,
    tx_from text COLLATE pg_catalog."default" NOT NULL,
    tx_to text COLLATE pg_catalog."default" NOT NULL,
    value numeric,
    contractaddress text COLLATE pg_catalog."default",
    input text COLLATE pg_catalog."default",
    type text COLLATE pg_catalog."default",
    gas bigint,
    gasused bigint,
    traceid text COLLATE pg_catalog."default",
    address text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT transactions_pkey PRIMARY KEY (hash)
)

TABLESPACE pg_default;

ALTER TABLE public.transactions
    OWNER to postgres;

GRANT ALL ON TABLE public.transactions TO postgres;
GRANT SELECT ON TABLE public.transactions TO consumer;
GRANT INSERT, SELECT ON TABLE public.transactions TO publisher;
