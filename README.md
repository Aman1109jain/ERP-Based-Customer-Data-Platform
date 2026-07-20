# ERP-CDP Integration System

## Overview

The ERP-CDP Integration System is a database-driven business management project that integrates Enterprise Resource Planning (ERP) functionalities with a Customer Data Platform (CDP). The system centralizes customer, supplier, product, inventory, production, and sales information into a single relational database, enabling efficient business operations and customer relationship management.

The project is implemented using **MySQL** for database management, **Python** for data generation, and **Streamlit** for interactive dashboard visualization.

## Features

- Customer Data Platform (CDP)
- Supplier Management
- Product Management
- Inventory Management
- Sales Order Processing
- Sales Details Tracking
- Production Management
- Interactive Dashboard
- Business KPI Monitoring
- Automated Dummy Data Generation

## Technologies Used

| Technology       | Purpose                       |
|------------------|--------------------------------|
| MySQL            | Database Management System     |
| Python           | Data Population                |
| Streamlit        | Dashboard Development           |
| Pandas           | Data Processing                 |
| Plotly           | Data Visualization              |
| Faker            | Dummy Data Generation           |
| MySQL Connector  | Database Connectivity           |

Required Python packages include Streamlit, MySQL Connector, Pandas, and Plotly.

## Database Schema

The project consists of 7 relational tables.

### 1. CDP
Stores customer information.

**Primary Key:** `customerID`

**Important Attributes:**
- First Name
- Last Name
- Gender
- DOB
- Email
- Phone
- Address
- Customer Segment
- Registration Date
- Last Interaction Date
- Loyalty Points

### 2. Supplier
Stores supplier details.

**Primary Key:** `supplierID`

**Important Attributes:**
- Supplier Name
- Contact Person
- Phone
- Email
- Address
- City
- State

### 3. Product
Stores product information.

**Primary Key:** `productID`

**Foreign Key:** `supplierID` → Supplier

**Important Attributes:**
- Product Name
- Category
- Description
- Unit Price
- Production Cost
- Unit
- Status

### 4. Inventory
Stores stock availability.

**Primary Key:** `inventoryID`

**Foreign Key:** `productID` → Product

**Important Attributes:**
- Quantity in Stock
- Reorder Level
- Warehouse Location
- Last Updated

### 5. SalesOrder
Stores customer orders.

**Primary Key:** `orderID`

**Foreign Key:** `customerID` → CDP

**Important Attributes:**
- Order Date
- Total Amount
- Payment Status
- Delivery Status
- Sales Person

### 6. SalesDetails
Stores products sold in each order.

**Primary Key:** `salesDetailID`

**Foreign Keys:**
- `orderID` → SalesOrder
- `productID` → Product

**Important Attributes:**
- Quantity
- Unit Price
- Total Price
- Delivery Route

### 7. Production
Stores manufacturing records.

**Primary Key:** `productionID`

**Foreign Key:** `productID` → Product

**Important Attributes:**
- Production Date
- Quantity Produced
- Production Cost
- Supervisor
- Status

## Entity Relationship Diagram

The ER Diagram illustrates the relationships among all database tables.

- One Customer → Many Sales Orders
- One Sales Order → Many Sales Details
- One Supplier → Many Products
- One Product → Many Inventory Records
- One Product → Many Production Records
- One Product → Many Sales Details

*`ER Diagram.png`*


## Dashboard Features

The Streamlit dashboard provides:

**Business KPIs**
- Total Customers
- Total Revenue
- Total Orders
- Total Products
- Total Suppliers
- Average Order Value
- Pending Payments
- Low Stock Count

**Charts**
- Monthly Revenue Trend
- Sales by Category
- Customer Segment Distribution
- Top Products by Revenue
- Delivery Status
- Production Status

**Tables**
- Low Stock Alerts
- Top Customers
- Recent Orders

The dashboard queries the MySQL database to display live business metrics and visualizations.

## Dummy Data Generation

A Python script automatically populates the database using the Faker library.

**Generated records include:**

| Table         | Records                       |
|---------------|--------------------------------|
| CDP           | 10,000                         |
| Supplier      | 500                             |
| Product       | 2,000                           |
| Sales Order   | 10,000                          |
| Production    | 5,000                            |
| Inventory     | Generated for every product     |
| Sales Details | Random items per order          |

The data generation process creates realistic customer, supplier, product, order, inventory, sales detail, and production records.

## Project Structure

```
ERP-CDP-System
│
├── erp_cdp_system.sql
├── Dashboard.py
├── DataPush.py
├── requirements.txt
├── README.md
│
├── CSV Files
│   ├── cdp.csv
│   ├── supplier.csv
│   ├── product.csv
│   ├── inventory.csv
│   ├── salesorder.csv
│   ├── salesdetails.csv
│   └── production.csv
│
└── ER Diagram(1).png
```

## Future Enhancements

- Authentication and Role-Based Access Control
- Predictive Sales Analytics
- AI-Based Customer Segmentation
- Inventory Demand Forecasting
- Supplier Performance Analysis
- Real-Time Notifications
- REST API Integration
- Cloud Deployment
- Mobile Dashboard

## Learning Outcomes

This project demonstrates practical implementation of:

- Relational Database Design
- Primary and Foreign Key Relationships
- SQL Constraints
- ERP System Design
- Customer Data Platform (CDP)
- Python Database Connectivity
- Data Visualization with Streamlit
- Business Intelligence Dashboards
- Data Generation Using Faker
- Database Normalization

## Author

**Aman Jain**

- **Project Title:** ERP-CDP Integration System
- **Database:** MySQL
- **Frontend Dashboard:** Streamlit
- **Programming Language:** Python
