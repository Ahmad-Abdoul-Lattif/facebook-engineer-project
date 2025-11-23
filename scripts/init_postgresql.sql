-- Création de la table des ventes
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    sale_date DATE NOT NULL,
    category VARCHAR(100),
    region VARCHAR(100),
    customer_id INTEGER
);

-- Insertion de données de test
INSERT INTO sales (product_name, quantity, price, sale_date, category, region, customer_id) VALUES
('iPhone 14', 2, 999.99, '2024-01-15', 'Electronics', 'North', 1001),
('MacBook Pro', 1, 2499.99, '2024-01-16', 'Electronics', 'South', 1002),
('AirPods Pro', 5, 249.99, '2024-01-17', 'Electronics', 'East', 1003),
('iPad Air', 3, 599.99, '2024-01-18', 'Electronics', 'West', 1004),
('Samsung Galaxy', 2, 899.99, '2024-01-19', 'Electronics', 'North', 1005),
('Sony Headphones', 4, 199.99, '2024-01-20', 'Electronics', 'South', 1006),
('Nike Shoes', 3, 129.99, '2024-01-21', 'Fashion', 'East', 1007),
('Adidas Jacket', 2, 89.99, '2024-01-22', 'Fashion', 'West', 1008),
('Coffee Maker', 1, 79.99, '2024-01-23', 'Home', 'North', 1009),
('Blender', 2, 49.99, '2024-01-24', 'Home', 'South', 1010),
('Smart Watch', 3, 299.99, '2024-01-25', 'Electronics', 'East', 1011),
('Gaming Console', 1, 499.99, '2024-01-26', 'Electronics', 'West', 1012);

-- Vérification
SELECT 'Initialization completed successfully' AS status;
