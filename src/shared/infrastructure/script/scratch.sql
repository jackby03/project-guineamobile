-- Set the client encoding to UTF8
SET client_encoding = 'UTF8';
SELECT  current_database();

CREATE TABLE public.tb_users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

SELECT * FROM tb_users;

-- Create a new user
INSERT INTO tb_users (user_id,name, email)
VALUES (1,'John Doe', 'jdoe@mail.com');

INSERT INTO tb_users (user_id,name, email)
VALUES (2, 'Maria Lee', 'mlee@mail.com');

SELECT * FROM tb_users WHERE user_id = 1;