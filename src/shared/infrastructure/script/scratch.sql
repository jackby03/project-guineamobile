-- Set the client encoding to UTF8
SET client_encoding = 'UTF8';

-- Check the current database
SELECT current_database();

-- Create the table tb_users
CREATE TABLE public.tb_users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

-- Select all users
SELECT * FROM tb_users;

-- Insert a new user (hashed_password is required)
INSERT INTO tb_users (name, email, hashed_password)
VALUES ('John Doe', 'jdoe@mail.com', '$2b$12$examplehashedpassword1');

INSERT INTO tb_users (name, email, hashed_password)
VALUES ('Maria Lee', 'mlee@mail.com', '$2b$12$examplehashedpassword2');

-- Select a specific user by ID
SELECT * FROM tb_users WHERE user_id = 1;