CREATE DATABASE IF NOT EXISTS production_crude_oil;
USE production_crude_oil;
CREATE TABLE production_crude_oil (production_id INT AUTO_INCREMENT PRIMARY KEY, record_year INT, record_month INT, oil_field VARCHAR(255), production_volume INT, unit VARCHAR(255) DEFAULT 'Barrels/day');
INSERT INTO production_crude_oil (record_year, record_month, oil_field, production_volume) VALUES
(1986,1,'Sirikit',20413),
(1986,2,'Sirikit',21231),
(1986,3,'Sirikit',20773),
(1986,4,'Sirikit',15704),
(1986,5,'Sirikit',19808),
(1986,6,'Sirikit',20616),
(1986,7,'Sirikit',21109),
(1986,8,'Sirikit',20038),
(1986,9,'Sirikit',20537),
(1986,10,'Sirikit',19918),
(1986,11,'Sirikit',20311),
(1986,12,'Sirikit',20025),
(1987,1,'Sirikit',19042),
(1987,2,'Sirikit',17860),
(1987,3,'Sirikit',17813),
(1987,4,'Sirikit',16975),
(1987,5,'Sirikit',16511),
(1987,6,'Sirikit',15822),
(1987,7,'Sirikit',15198),
(1987,8,'Sirikit',14879),
(1986,1,'Erawan',15981),
(1986,2,'Erawan',15093),
(1986,3,'Erawan',15993),
(1986,4,'Erawan',15566),
(1986,5,'Erawan',15493),
(1986,6,'Erawan',14316),
(1986,7,'Erawan',12874),
(1986,8,'Erawan',13586),
(1986,9,'Erawan',12615),
(1986,10,'Erawan',13380),
(1986,11,'Erawan',12936),
(1986,12,'Erawan',13381),
(1987,1,'Erawan',14227),
(1987,2,'Erawan',14858),
(1987,3,'Erawan',14445),
(1987,4,'Erawan',14125),
(1987,5,'Erawan',14332),
(1987,6,'Erawan',16245),
(1987,9,'Erawan',16810),
(1987,10,'Erawan',15977);
CREATE TABLE Field (Field_id INT PRIMARY KEY, Field_name VARCHAR(255));
CREATE TABLE Product (Product_id INT PRIMARY KEY, Product_name VARCHAR(255));
CREATE TABLE Field_Product (field_product_id INT PRIMARY KEY, production_id INT, field_id INT, volume INT, `year` INT, `month` INT, unit VARCHAR(255),
  FOREIGN KEY (production_id) REFERENCES Product (Product_id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (field_id) REFERENCES Field (Field_id) ON UPDATE CASCADE ON DELETE CASCADE);
INSERT INTO Field VALUES (1,'Sirikit'),(2,'Erawan'),(3,'Bongkot');
INSERT INTO Product VALUES (1,'Crude oil'),(2,'Condensate');
INSERT INTO Field_Product SELECT p.production_id, 1, f.Field_id, p.production_volume, p.record_year, p.record_month, p.unit FROM production_crude_oil p JOIN Field f ON f.Field_name = p.oil_field;
