CREATE DATABASE crud_app

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    nome_pedido VARCHAR(255),
    id_cliente INT,
    quantidade INT
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    nome_pedido VARCHAR(255),
    id_cliente INT,
    quantidade INT
);