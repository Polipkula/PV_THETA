create database eshop;
use eshop;

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATETIME NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('new','shipped','closed')),
    paid BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    from_customer_id INT NOT NULL,
    to_customer_id INT NOT NULL,
    amount FLOAT 
    NOT NULL,
    trans_date DATETIME NOT NULL,
    FOREIGN KEY (from_customer_id) REFERENCES customers(id),
    FOREIGN KEY (to_customer_id) REFERENCES customers(id)
);

CREATE VIEW customer_orders_view AS
SELECT 
    o.id AS order_id, 
    c.full_name, 
    c.email, 
    o.order_date, 
    o.status, 
    o.paid
FROM orders o
JOIN customers c ON o.customer_id = c.id;

CREATE VIEW order_summary_view AS
SELECT 
    o.id AS order_id,
    SUM(p.price * oi.quantity) AS total_price,
    COUNT(oi.product_id) AS total_items
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON p.id = oi.product_id
GROUP BY o.id;


INSERT INTO customers (full_name, email, created_at)
VALUES ('Testovací Zákazník', 'test@example.com', NOW());

INSERT INTO customers (full_name, email, created_at)
VALUES ('Testovací Zákazník2', 'test2@example.com', NOW());

INSERT INTO products (name, price, stock)
VALUES
    ('Chytrý telefon XPhone Ultra', 15499.00, 5),
    ('Sluchátka OverEar Q99',       1399.00, 23),
    ('Televize SmartVision 50',     8999.00, 8),
    ('USB Flash 128GB',            249.00, 45),
    ('Herní konzole XPlay',        6999.00, 12),
    ('Externí disk 2TB',           1899.00, 6),
    ('Tablet TabMaster 10',        2999.00, 15),
    ('Bezdrátová myš SpeedMouse',  399.00, 40),
    ('HDMI kabel 2m',              199.00, 50),
    ('LED monitor 24"',            2699.00, 10);






