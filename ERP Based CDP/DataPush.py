import random
import mysql.connector
from faker import Faker

fake = Faker("en_IN")

# DATABASE CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1109_J@in_aman",
    database="erp_cdp_system"
)

# EXCUTING SQL QUERIES
cursor = conn.cursor()

# NUMBER OF RECORDS
NUM_CUSTOMERS = 10000
NUM_SUPPLIERS = 500
NUM_PRODUCTS = 2000
NUM_ORDERS = 10000
NUM_PRODUCTION = 5000

# CDP TABLE
print("Inserting Customers...")

customer_ids = []

for _ in range(NUM_CUSTOMERS):

    registration = fake.date_between(start_date="-5y", end_date="today")
    interaction = fake.date_between(start_date=registration, end_date="today")

    sql = """ INSERT INTO cdp
    (firstName, lastName, gender, dob, email, phone,
    address,city, state, customerSegment,
    registrationDate, lastInteractionDate, loyaltyPoints)

    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        fake.first_name(),
        fake.last_name(),
        random.choice(["Male", "Female"]),
        fake.date_of_birth(minimum_age=18, maximum_age=70),
        fake.unique.email(),
        fake.phone_number()[:15],
        fake.address(),
        fake.city(),
        fake.state(),
        random.choice(["Regular", "Premium", "Gold"]),
        registration,
        interaction,
        random.randint(0, 5000)
    )

    cursor.execute(sql, values)
    customer_ids.append(cursor.lastrowid)

conn.commit()
print("Customers Done")


# SUPPLIER
print("Inserting Suppliers...")

supplier_ids = []

for _ in range(NUM_SUPPLIERS):

    sql = """ INSERT INTO supplier
    (supplierName, contactPerson, phone,
    email, address, city, state)

    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        fake.company(),
        fake.name(),
        fake.phone_number()[:15],
        fake.company_email(),
        fake.address(),
        fake.city(),
        fake.state()
    )

    cursor.execute(sql, values)
    supplier_ids.append(cursor.lastrowid)

conn.commit()
print("Suppliers Done")


# PRODUCT
print("Inserting Products...")

product_ids = []
product_prices = {}
categories = [
    "Electronics",
    "Furniture",
    "Clothing",
    "Food",
    "Sports",
    "Books",
    "Accessories"
]

for _ in range(NUM_PRODUCTS):

    cost = round(random.uniform(100, 5000), 2)
    price = round(cost * random.uniform(1.2, 2.0), 2)

    sql = """ INSERT INTO product
    (supplierID, productName, category,
    description, unitPrice, productionCost,
    unit, status)

    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        random.choice(supplier_ids),
        fake.word().capitalize(),
        random.choice(categories),
        fake.sentence(),
        price,
        cost,
        random.choice(["Piece", "Box", "Kg"]),
        "Available"
    )

    cursor.execute(sql, values)
    product_ids.append(cursor.lastrowid)
    product_prices[cursor.lastrowid] = price

conn.commit()
print("Products Done")


# INVENTORY
print("Inserting Inventory...")

for product in product_ids:

    sql = """ INSERT INTO inventory
    (productID, quantityInStock,
    reorderLevel, warehouseLocation,
    lastUpdated)

    VALUES (%s,%s,%s,%s,%s)
    """

    values = (
        product,
        random.randint(50, 1000),
        random.randint(10, 100),
        random.choice(["Warehouse A", "Warehouse B", "Warehouse C"]),
        fake.date_between(start_date="-1y", end_date="today")
    )

    cursor.execute(sql, values)

conn.commit()
print("Inventory Done")


# SALES ORDER
print("Inserting Orders...")

order_ids = []

for _ in range(NUM_ORDERS):

    order_date = fake.date_between(start_date="-3y", end_date="today")

    sql = """ INSERT INTO salesOrder
    (customerID, orderDate, totalAmount,
    paymentStatus, deliveryStatus, salesPerson)

    VALUES (%s,%s,%s,%s,%s,%s)
    """

    values = (
        random.choice(customer_ids),
        order_date,
        0,
        random.choice(["Paid", "Pending"]),
        random.choice(["Delivered", "Shipped", "Processing"]),
        fake.name()
    )

    cursor.execute(sql, values)

    order_ids.append(cursor.lastrowid)

conn.commit()
print("Orders Done")


# SALES DETAILS
print("Inserting Sales Details...")

delivery_routes = [
    "North Route",
    "South Route",
    "East Route",
    "West Route",
    "Central Route",
    "Express Route",
    "Highway Route",
    "City Route"
]

for order_id in order_ids:
    total_amount = 0

    num_items = random.randint(1, 5)

    for _ in range(num_items):
        product_id = random.choice(product_ids)
        supplier_id = random.choice(supplier_ids)

        quantity = random.randint(1, 10)
        unit_price = product_prices[product_id]
        total_price = quantity * unit_price
        delivery_route = random.choice(delivery_routes)

        total_amount += total_price

        sql = """
        INSERT INTO salesDetails
        (
            orderID,
            productID,
            supplierID,
            quantity,
            unitPrice,
            totalPrice,
            deliveryRoute
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            order_id,
            product_id,
            supplier_id,
            quantity,
            unit_price,
            total_price,
            delivery_route
        )

        cursor.execute(sql, values)

    cursor.execute(
        """
        UPDATE salesOrder
        SET totalAmount = %s
        WHERE orderID = %s
        """,
        (total_amount, order_id)
    )

conn.commit()
print("Sales Details Done")


# PRODUCTION
print("Inserting Production...")

for _ in range(NUM_PRODUCTION):

    product = random.choice(product_ids)

    qty = random.randint(50, 500)

    cost = round(random.uniform(5000, 100000), 2)

    sql = """ INSERT INTO production
    (productID, productionDate, quantityProduced,
    productionCost, supervisor, status)

    VALUES (%s,%s,%s,%s,%s,%s)
    """

    values = (
        product,
        fake.date_between(start_date="-2y", end_date="today"),
        qty,
        cost,
        fake.name(),
        random.choice(["Completed", "In Progress", "Pending"])
    )

    cursor.execute(sql, values)

conn.commit()
print("Production Done")


# FINISH
cursor.close()
conn.close()

print("=" * 50)
print("ERP DATABASE POPULATED SUCCESSFULLY")
print(f"Customers   : {NUM_CUSTOMERS}")
print(f"Suppliers   : {NUM_SUPPLIERS}")
print(f"Products    : {NUM_PRODUCTS}")
print(f"Orders      : {NUM_ORDERS}")
print(f"Production  : {NUM_PRODUCTION}")
print("=" * 50)