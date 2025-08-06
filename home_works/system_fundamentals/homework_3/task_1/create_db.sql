DROP DATABASE IF EXISTS usersdb;

CREATE DATABASE usersdb;

-- Видаляємо таблиці в правильному порядку (спочатку залежні)
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
id SERIAL PRIMARY KEY,
fullname VARCHAR(100),
email VARCHAR(100) UNIQUE
);

CREATE TABLE status (
id SERIAL PRIMARY KEY,
name VARCHAR(50) CHECK (name IN ('new', 'in progress', 'completed'))
);

CREATE TABLE tasks (
id SERIAL PRIMARY KEY,
title VARCHAR(100),
description TEXT,
status_id INTEGER REFERENCES status(id)  ON DELETE CASCADE,
user_id INTEGER REFERENCES users(id)  ON DELETE CASCADE
);