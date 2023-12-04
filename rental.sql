DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS holiday_houses;

CREATE TABLE IF NOT EXISTS customer (
    id INT AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    customer_number VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    address VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    staff_number VARCHAR(50) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    date_joined DATE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS holiday_houses (
    house_id INT AUTO_INCREMENT,
    house_address VARCHAR(255) NOT NULL,
    number_of_bedrooms INT NOT NULL,
    number_of_bathrooms INT NOT NULL,
    maximum_occupancy INT NOT NULL,
    rental_per_night DECIMAL(10, 2) NOT NULL,
    house_image VARCHAR(255), 
    PRIMARY KEY (house_id)
);

INSERT INTO customer (name, customer_number, address, email, phone_number, password, username) VALUES
('John Doe', 'CUST001', '123 Main St', 'johndoe@example.com', '021-456-7890', 'scrypt:32768:8:1$m4QM6tOcxqnUY92t$b87bb8487e328faf42e2fb4dff134fe7fc85e2e69560e96f47c8d2255ba314ae24026bf7d7ad89ad0e95a5e73af3a733cf75a0828fab3dd66dca5e14d57931bd', 'john'),
('Jane A', 'CUST002', '456 Oak St', 'janea@example.com', '021-567-8900', 'scrypt:32768:8:1$m4QM6tOcxqnUY92t$b87bb8487e328faf42e2fb4dff134fe7fc85e2e69560e96f47c8d2255ba314ae24026bf7d7ad89ad0e95a5e73af3a733cf75a0828fab3dd66dca5e14d57931bd', 'a'),
('Jane B', 'CUST003', '451 Oak St', 'janeb@example.com', '021-567-8901', 'scrypt:32768:8:1$m4QM6tOcxqnUY92t$b87bb8487e328faf42e2fb4dff134fe7fc85e2e69560e96f47c8d2255ba314ae24026bf7d7ad89ad0e95a5e73af3a733cf75a0828fab3dd66dca5e14d57931bd', 'b'),
('Jane C', 'CUST004', '453 Oak St', 'janec@example.com', '021-567-8902', 'scrypt:32768:8:1$m4QM6tOcxqnUY92t$b87bb8487e328faf42e2fb4dff134fe7fc85e2e69560e96f47c8d2255ba314ae24026bf7d7ad89ad0e95a5e73af3a733cf75a0828fab3dd66dca5e14d57931bd', 'c'),
('Jane D', 'CUST005', '456 Oak St', 'janed@example.com', '021-567-8903', 'scrypt:32768:8:1$m4QM6tOcxqnUY92t$b87bb8487e328faf42e2fb4dff134fe7fc85e2e69560e96f47c8d2255ba314ae24026bf7d7ad89ad0e95a5e73af3a733cf75a0828fab3dd66dca5e14d57931bd', 'd'),
('Jane E', 'CUST006', '457 Oak St', 'janee@example.com', '021-567-8904', 'scrypt:32768:8:1$m4QM6tOcxqnUY92t$b87bb8487e328faf42e2fb4dff134fe7fc85e2e69560e96f47c8d2255ba314ae24026bf7d7ad89ad0e95a5e73af3a733cf75a0828fab3dd66dca5e14d57931bd', 'e');

INSERT INTO staff (name, staff_number, email, phone_number, date_joined, password, username) VALUES
('Alice Johnson', 'STAFF001', 'alice@example.com', '345-678-9012', '2023-01-10', 'scrypt:32768:8:1$m4QM6tOcxqnUY92t$b87bb8487e328faf42e2fb4dff134fe7fc85e2e69560e96f47c8d2255ba314ae24026bf7d7ad89ad0e95a5e73af3a733cf75a0828fab3dd66dca5e14d57931bd', 'alice'),
('Bob Williams', 'STAFF002', 'bob@example.com', '456-789-0123', '2023-02-15', 'scrypt:32768:8:1$m4QM6tOcxqnUY92t$b87bb8487e328faf42e2fb4dff134fe7fc85e2e69560e96f47c8d2255ba314ae24026bf7d7ad89ad0e95a5e73af3a733cf75a0828fab3dd66dca5e14d57931bd', 'bob'),
('Charlie Brown', 'STAFF003', 'charlie@example.com', '567-890-1234', '2022-03-20', 'scrypt:32768:8:1$m4QM6tOcxqnUY92t$b87bb8487e328faf42e2fb4dff134fe7fc85e2e69560e96f47c8d2255ba314ae24026bf7d7ad89ad0e95a5e73af3a733cf75a0828fab3dd66dca5e14d57931bd', 'charlie');

INSERT INTO admin (name, email, phone_number, password, username) VALUES
('Admin', 'admin@lincoln.com', '021-890-1234', 'scrypt:32768:8:1$m4QM6tOcxqnUY92t$b87bb8487e328faf42e2fb4dff134fe7fc85e2e69560e96f47c8d2255ba314ae24026bf7d7ad89ad0e95a5e73af3a733cf75a0828fab3dd66dca5e14d57931bd', 'adminuser');

INSERT INTO holiday_houses (house_address, number_of_bedrooms, number_of_bathrooms, maximum_occupancy, rental_per_night, house_image) VALUES
('House Address 1', 3, 2, 6, 150.00, '1.jpeg'),
('House Address 2', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 3', 4, 3, 8, 200.00, '2.jpeg'),
('House Address 4', 4, 3, 8, 200.00, '2.jpeg'),
('House Address 5', 4, 3, 8, 200.00, '2.jpeg'),
('House Address 6', 4, 3, 8, 200.00, '2.jpeg'),
('House Address 7', 4, 3, 8, 200.00, '2.jpeg'),
('House Address 8', 4, 3, 8, 200.00, '2.jpeg'),
('House Address 9', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 10', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 11', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 12', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 13', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 14', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 15', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 16', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 17', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 18', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 19', 4, 3, 8, 200.00, '1.jpeg'),
('House Address 20', 4, 3, 8, 200.00, '1.jpeg');



