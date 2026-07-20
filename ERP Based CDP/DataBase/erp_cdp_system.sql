CREATE DATABASE erp_cdp_system;

USE erp_cdp_system;

CREATE TABLE cdp (
    customerID INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR (50) NOT NULL,
    lastName VARCHAR (50) NOT NULL,
    gender VARCHAR (10),
    dob DATE,
    email VARCHAR (100) UNIQUE,
    phone VARCHAR (15),
    address TEXT,
    city VARCHAR (50),
    state VARCHAR (50),
    customerSegment VARCHAR (30),
    registrationDate DATE,
    lastInteractionDate DATE,
    loyaltyPoints INT DEFAULT 0
);

CREATE TABLE supplier (
    supplierID INT AUTO_INCREMENT PRIMARY KEY,
    supplierName VARCHAR (100) NOT NULL,
    contactPerson VARCHAR (100),
    phone VARCHAR (15),
    email VARCHAR (100),
    address TEXT,
    city VARCHAR (50),
    state VARCHAR (50)
);

CREATE TABLE product (
    productID INT AUTO_INCREMENT PRIMARY KEY,
    supplierID INT NOT NULL 
		REFERENCES suppplier (supplierID) 
		ON DELETE CASCADE 
		ON UPDATE CASCADE,
    productName VARCHAR (100) NOT NULL,
    category VARCHAR (50),
    description TEXT,
    unitPrice DECIMAL (10,2),
    productionCost DECIMAL (10,2),
    unit VARCHAR (20),
    status VARCHAR (20)
);

CREATE TABLE salesOrder (
    orderID INT AUTO_INCREMENT PRIMARY KEY,
    customerID INT NOT NULL
		REFERENCES cdp (customerID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    orderDate DATE,
    totalAmount DECIMAL (10,2),
    paymentStatus VARCHAR (30),
    deliveryStatus VARCHAR (30),
    salesPerson VARCHAR (50)
);

CREATE TABLE salesDetails (
    salesDetailID INT AUTO_INCREMENT PRIMARY KEY,
    orderID INT NOT NULL
		REFERENCES salesOrder (orderID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    productID INT NOT NULL
		REFERENCES product (productID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    quantity INT,
    unitPrice DECIMAL (10,2),
    totalPrice DECIMAL (10,2)
);

CREATE TABLE inventory (
    inventoryID INT AUTO_INCREMENT PRIMARY KEY,
    productID INT NOT NULL
		REFERENCES product (productID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    quantityInStock INT,
    reorderLevel INT,
    warehouseLocation VARCHAR (100),
    lastUpdated DATE
);

CREATE TABLE production (
    productionID INT AUTO_INCREMENT PRIMARY KEY,
    productID INT NOT NULL
		REFERENCES product (productID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    productionDate DATE,
    quantityProduced INT,
    productionCost DECIMAL (10,2),
    supervisor VARCHAR (50),
    status VARCHAR (30)
);

ALTER TABLE salesDetails
ADD COLUMN supplierID INT NOT NULL,
ADD COLUMN deliveryRoute VARCHAR(100);

ALTER TABLE salesDetails
ADD CONSTRAINT fk_salesdetails_supplier
FOREIGN KEY (SupplierID)
REFERENCES Supplier(SupplierID)
ON DELETE CASCADE
ON UPDATE CASCADE;