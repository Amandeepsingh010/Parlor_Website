-- Parlor Perfect Database Schema
-- MySQL 8.0+

-- Drop existing tables if they exist
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS festival_discount;
DROP TABLE IF EXISTS users;

-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    is_admin TINYINT(1) DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_is_admin (is_admin)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Services Table
CREATE TABLE services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    base_price DECIMAL(10, 2) NOT NULL,
    discount_percent DECIMAL(5, 2) DEFAULT 0,
    discounted_price DECIMAL(10, 2),
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Festival Discount Table
CREATE TABLE festival_discount (
    id INT AUTO_INCREMENT PRIMARY KEY,
    discount_percent DECIMAL(5, 2) DEFAULT 0,
    description VARCHAR(255),
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bookings Table
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    service_id INT NOT NULL,
    booking_date DATETIME NOT NULL,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_service_id (service_id),
    INDEX idx_booking_date (booking_date),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert Sample Admin User (password: admin123)
INSERT INTO users (name, email, phone, password, is_admin) VALUES 
('Admin User', 'admin@parlor.com', '+919876543210', '0192023a7bbd73250516f069df18b500', 1);

-- Insert Sample Services - Facials
INSERT INTO services (category, service_name, description, base_price, discount_percent, discounted_price) VALUES
('Facials', 'Gold Facial', 'Premium gold facial with anti-aging benefits', 1500, 0, 1500),
('Facials', 'Silver Facial', 'Hydrating silver facial treatment', 1200, 0, 1200),
('Facials', 'Diamond Facial', 'Luxury diamond facial for radiant skin', 2000, 0, 2000);

-- Insert Sample Services - Hydra Facial
INSERT INTO services (category, service_name, description, base_price, discount_percent, discounted_price) VALUES
('Hydra Facial', 'Hydra Facial Machine', 'Advanced hydra facial treatment with extractions', 3000, 0, 3000),
('Hydra Facial', 'Hydra Facial + Serums', 'Hydra facial with premium serums', 3500, 0, 3500);

-- Insert Sample Services - Nails
INSERT INTO services (category, service_name, description, base_price, discount_percent, discounted_price) VALUES
('Nails', 'Basic Manicure', 'Classic manicure with nail paint', 300, 0, 300),
('Nails', 'Gel Manicure', 'Gel manicure with UV curing', 700, 0, 700),
('Nails', 'Nail Art', 'Creative nail art designs', 500, 0, 500),
('Nails', 'Pedicure', 'Full pedicure service', 400, 0, 400);

-- Insert Sample Services - Waxing
INSERT INTO services (category, service_name, description, base_price, discount_percent, discounted_price) VALUES
('Waxing', 'Face Waxing', 'Face hair removal', 250, 0, 250),
('Waxing', 'Arms Waxing', 'Full arms hair removal', 350, 0, 350),
('Waxing', 'Legs Waxing', 'Full legs hair removal', 500, 0, 500),
('Waxing', 'Full Body Waxing', 'Complete body waxing', 1500, 0, 1500);

-- Insert Sample Services - Threading
INSERT INTO services (category, service_name, description, base_price, discount_percent, discounted_price) VALUES
('Threading', 'Eyebrow Threading', 'Precise eyebrow threading', 100, 0, 100),
('Threading', 'Upper Lip Threading', 'Upper lip hair removal', 80, 0, 80),
('Threading', 'Full Face Threading', 'Complete face threading', 300, 0, 300);

-- Insert Sample Services - Bleach
INSERT INTO services (category, service_name, description, base_price, discount_percent, discounted_price) VALUES
('Bleach', 'Standard Bleach', 'Basic hair bleaching', 200, 0, 200),
('Bleach', 'Premium Bleach', 'Organic bleach with conditioner', 350, 0, 350),
('Bleach', 'Face Bleach', 'Facial hair lightening', 150, 0, 150);

-- Insert Sample Services - Hair
INSERT INTO services (category, service_name, description, base_price, discount_percent, discounted_price) VALUES
('Hair', 'Hair Spa', 'Relaxing hair spa treatment', 600, 0, 600),
('Hair', 'Hair Smoothening', 'Hair smoothening treatment', 3000, 0, 3000),
('Hair', 'Hair Coloring', 'Professional hair coloring', 1500, 0, 1500);

-- Insert Sample Services - Makeup
INSERT INTO services (category, service_name, description, base_price, discount_percent, discounted_price) VALUES
('Makeup', 'Bridal Makeup', 'Complete bridal makeup', 2500, 0, 2500),
('Makeup', 'Party Makeup', 'Party and event makeup', 1500, 0, 1500),
('Makeup', 'Everyday Makeup', 'Daily makeup touch-ups', 800, 0, 800);

-- Insert Sample Festival Discount
INSERT INTO festival_discount (discount_percent, description, is_active) VALUES
(15, 'Diwali Special - 15% OFF on all services', 1);

-- Create indexes for better performance
CREATE INDEX idx_services_category_active ON services(category, is_active);
CREATE INDEX idx_bookings_date_status ON bookings(booking_date, status);
CREATE INDEX idx_users_email_admin ON users(email, is_admin);

-- Enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Display confirmation
SELECT 'Database setup completed successfully!' as Status;

-- Check created tables
SHOW TABLES;
