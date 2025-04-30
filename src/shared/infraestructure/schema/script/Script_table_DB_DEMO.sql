-- Set the client encoding to UTF8
SET client_encoding = 'UTF8';

CREATE TABLE public.tb_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
);

SELECT * FROM tb_users;