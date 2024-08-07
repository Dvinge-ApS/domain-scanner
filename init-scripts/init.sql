-- init-scripts/init.sql
CREATE DATABASE domaindb;

CREATE TABLE IF NOT EXISTS domains (
    id SERIAL PRIMARY KEY,
    domain_name VARCHAR(255) NOT NULL,
    is_available BOOLEAN,
    last_checked TIMESTAMP
);