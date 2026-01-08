-- =====================================================
-- Database initialization script for EC3 Assessment
-- MariaDB 12.x
-- =====================================================

-- Drop database if it already exists (safe reset)
DROP DATABASE IF EXISTS ec3_leads_db;

-- Create database
CREATE DATABASE ec3_leads_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Use the database
USE ec3_leads_db;

-- =====================================================
-- Leads table
-- =====================================================

CREATE TABLE leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    source VARCHAR(100),
    created_time DATETIME NOT NULL
);

-- =====================================================
-- Verification query
-- =====================================================

SELECT * FROM leads;
