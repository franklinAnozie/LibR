-- Create customers table if not exists
CREATE TABLE IF NOT EXISTS customers (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    first_name VARCHAR(256),
    last_name VARCHAR(256),
    email_address VARCHAR(256),
    user_name VARCHAR(256),
    password VARCHAR(256),
    fine INT,
    role VARCHAR(60)
);

-- Insert sample data into customers table
INSERT INTO customers (id, created_at, updated_at, first_name, last_name, email_address, user_name, password, fine, role)
VALUES
    (UUID(), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'John', 'Doe', 'john@example.com', 'john_doe', 'password123', 0, 'customer'),
    (UUID(), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Jane', 'Smith', 'jane@example.com', 'jane_smith', 'password456', 10, 'customer'),
    (UUID(), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Alice', 'Johnson', 'alice@example.com', 'alice_johnson', 'password789', 20, 'customer');

-- Create staff table if not exists
CREATE TABLE IF NOT EXISTS staff (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    first_name VARCHAR(256),
    last_name VARCHAR(256),
    email_address VARCHAR(256),
    user_name VARCHAR(256),
    password VARCHAR(256),
    role VARCHAR(60)
);

-- Insert sample data into staff table
INSERT INTO staff (id, created_at, updated_at, first_name, last_name, email_address, user_name, password, role)
VALUES
    (UUID(), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Admin', 'User', 'admin@example.com', 'admin_user', 'admin123', 'admin'),
    (UUID(), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Manager', 'Smith', 'manager@example.com', 'manager_smith', 'manager456', 'manager');

-- Create books table if not exists
CREATE TABLE IF NOT EXISTS books (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    title VARCHAR(256),
    author VARCHAR(256),
    publisher VARCHAR(256),
    ISBN_Number VARCHAR(256)
);

-- Insert sample data into books table
INSERT INTO books (id, created_at, updated_at, title, author, publisher, ISBN_Number)
VALUES
    (UUID(), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Book1', 'Author1', 'Publisher1', '1234567890'),
    (UUID(), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Book2', 'Author2', 'Publisher2', '2345678901'),
    (UUID(), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Book3', 'Author3', 'Publisher3', '3456789012');
