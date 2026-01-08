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
-- Mock data (required by assessment)
-- =====================================================

INSERT INTO leads (name, email, phone, source, created_time)
VALUES
('John Doe', 'john.doe@example.com', '0123456789', 'Website', NOW()),
('Jane Smith', 'jane.smith@example.com', '0987654321', 'Referral', NOW()),
('Bob Brown', 'bob.brown@example.com', NULL, 'Email Campaign', NOW()),
('Alice Green', 'alice.green@example.com', '0112233445', 'Social Media', NOW()),
('Michael White', 'michael.white@example.com', NULL, 'Cold Call', NOW());

-- =====================================================
-- Verification query
-- =====================================================

SELECT * FROM leads;
