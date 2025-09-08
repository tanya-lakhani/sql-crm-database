import sqlite3

# Establish a database connection
conn = sqlite3.connect('CRM.db')
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON;")


# Industry Table (Removed UNIQUE from industry_name)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Industry (
    industry_id CHAR(8) PRIMARY KEY,
    industry_name VARCHAR(50)
);
''')

# JobTitle Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS JobTitle (
    job_title_id CHAR(8) PRIMARY KEY,
    job_title_name VARCHAR(50)
);
''')

# LeadSource Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS LeadSource (
    lead_source_id CHAR(8) PRIMARY KEY,
    lead_source VARCHAR(50)
);
''')

# LeadStatus Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS LeadStatus (
    lead_status_id CHAR(8) PRIMARY KEY,
    lead_status VARCHAR(50)
);
''')

# LostReason Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS LostReason (
    lost_reason_id CHAR(8) PRIMARY KEY,
    lost_reason VARCHAR(50)
);
''')

# QuoteStatus Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS QuoteStatus (
    quote_status_id CHAR(8) PRIMARY KEY,
    quote_status VARCHAR(50)
);
''')

# PaymentMethod Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS PaymentMethod (
    payment_method_id CHAR(8) PRIMARY KEY,
    payment_method VARCHAR(50)
);
''')

# PaymentStatus Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS PaymentStatus (
    payment_status_id CHAR(8) PRIMARY KEY,
    payment_status VARCHAR(50)
);
''')

# OrderStatus Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS OrderStatus (
    order_status_id CHAR(8) PRIMARY KEY,
    status_name VARCHAR(50)
);
''')

# Warranty Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Warranty (
    warranty_id CHAR(8) PRIMARY KEY,
    warranty VARCHAR(50)
);
''')

# VehicleType Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS VehicleType (
    vehicle_type_id CHAR(8) PRIMARY KEY,
    vehicle_type VARCHAR(50)
);
''')

# FuelType Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS FuelType (
    fuel_type_id CHAR(8) PRIMARY KEY,
    fuel_type VARCHAR(50)
);
''')

# Role Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Role (
    role_id CHAR(8) PRIMARY KEY,
    role VARCHAR(50)
);
''')

# BillingCity Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS BillingCity(
    billing_city_id CHAR(8) PRIMARY KEY,
    billing_city VARCHAR(50)
);
''')

# BillingAddress Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS BillingAddress(
    billing_address_id CHAR(8) PRIMARY KEY,
    billing_address VARCHAR(50) UNIQUE NOT NULL,
    billing_city_id CHAR(8),
    FOREIGN KEY (billing_city_id) REFERENCES BillingCity(billing_city_id) ON DELETE CASCADE
);
''')

# ShippingCity Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ShippingCity(
    shipping_city_id CHAR(8) PRIMARY KEY,
    shipping_city VARCHAR(50)
);
''')

# ShippingAddress Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ShippingAddress(
    shipping_address_id CHAR(8) PRIMARY KEY,
    shipping_address VARCHAR(50) UNIQUE NOT NULL,
    shipping_city_id CHAR(8),
    FOREIGN KEY (shipping_city_id) REFERENCES ShippingCity(shipping_city_id) ON DELETE CASCADE
);
''')


# Stage Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Stage (
    stage_id CHAR(8) PRIMARY KEY,
    stage VARCHAR(50) 
);
''')


# Users Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    user_id CHAR(8) PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_email_address VARCHAR(100) UNIQUE NOT NULL,
    user_phone_number VARCHAR(15) NOT NULL,
    role_id CHAR(8),
    commission_rate VARCHAR(2),
    FOREIGN KEY (role_id) REFERENCES Role(role_id) ON DELETE CASCADE
);
''')

# Account Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Account (
    account_id CHAR(8) PRIMARY KEY,
    account_name VARCHAR(50) NOT NULL,
    account_email_address VARCHAR(100) NOT NULL,
    account_mobile_number VARCHAR(15) NOT NULL,
    billing_address_id CHAR(8),
    user_id CHAR(8),
    account_status BOOLEAN DEFAULT TRUE,
    annual_revenue INTEGER,
    industry_id CHAR(8),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (billing_address_id) REFERENCES BillingAddress(billing_address_id) ON DELETE CASCADE,
    FOREIGN KEY (industry_id) REFERENCES Industry(industry_id) ON DELETE CASCADE
);
''')

# Customer Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Customer (
    customer_id CHAR(8) PRIMARY KEY,
    customer_name VARCHAR(50) NOT NULL,
    customer_email_address VARCHAR(100) UNIQUE NOT NULL,
    customer_mobile_number VARCHAR(15) NOT NULL,
    account_id CHAR(8),
    job_title_id CHAR(8),
    FOREIGN KEY (job_title_id) REFERENCES JobTitle(job_title_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES Account(account_id) ON DELETE CASCADE
);
''')

# Lead Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Lead (
    lead_id CHAR(8) PRIMARY KEY,
    created_date DATE NOT NULL,
    lead_score INTEGER CHECK (lead_score BETWEEN 1 AND 100),
    account_id CHAR(8),
    lead_source_id CHAR(8),
    lead_status_id CHAR(8),
    user_id CHAR(8),
    customer_id CHAR(8),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (lead_source_id) REFERENCES LeadSource(lead_source_id) ON DELETE CASCADE,
    FOREIGN KEY (lead_status_id) REFERENCES LeadStatus(lead_status_id) ON DELETE CASCADE
);
''')

# Product Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Product (
    product_id CHAR(8) PRIMARY KEY,
    product_name VARCHA(50) NOT NULL,
    vehicle_type_id CHAR(8),
    model_year INTEGER,
    base_price INTEGER NOT NULL,
    inventory_level INTEGER CHECK (inventory_level >= 0),
    fuel_type_id CHAR(8),
    weight_capacity INTEGER CHECK (weight_capacity >= 0),
    dimensions VARCHAR(50),
    FOREIGN KEY (fuel_type_id) REFERENCES FuelType(fuel_type_id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_type_id) REFERENCES VehicleType(vehicle_type_id) ON DELETE CASCADE
);
''')


# Opportunity Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Opportunity (
    opportunity_id CHAR(8) PRIMARY KEY,
    close_date DATE,
    expected_close_date DATE,
    opportunity_amount DECIMAL(10,2) NOT NULL,
    lost_reason_id CHAR(8),
    stage_id CHAR(8),
    product_id CHAR(8),
    user_id CHAR(8),
    lead_id CHAR(8),
    customer_id CHAR(8),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (lead_id) REFERENCES Lead(lead_id) ON DELETE CASCADE,
    FOREIGN KEY (stage_id) REFERENCES Stage(stage_id) ON DELETE CASCADE,
    FOREIGN KEY (lost_reason_id) REFERENCES LostReason(lost_reason_id) ON DELETE CASCADE
);
''')

# Quote Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Quote (
    quote_id CHAR(8) PRIMARY KEY,
    expiration_date DATE NOT NULL,
    discount INTEGER CHECK (discount BETWEEN 0 AND 25),
    total_amount DECIMAL(10,2) NOT NULL,
    created_date DATE NOT NULL,
    revision_number INTEGER DEFAULT 1,
    quote_status_id CHAR(8),
    opportunity_id CHAR(8),
    FOREIGN KEY (quote_status_id) REFERENCES QuoteStatus(quote_status_id) ON DELETE CASCADE,
    FOREIGN KEY (opportunity_id) REFERENCES Opportunity(opportunity_id) ON DELETE CASCADE
);
''')

# Order Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    order_id CHAR(8) PRIMARY KEY,
    order_date DATE NOT NULL,
    order_status_id CHAR(8),

    expected_delivery_date DATE,
    delivery_date DATE,
    quote_id CHAR(8),
    shipping_address_id CHAR(8),
    FOREIGN KEY (shipping_address_id) REFERENCES ShippingAddress(shipping_address_id) ON DELETE CASCADE,
    FOREIGN KEY (quote_id) REFERENCES Quote(quote_id) ON DELETE CASCADE,
    FOREIGN KEY (order_status_id) REFERENCES OrderStatus(order_status_id) ON DELETE CASCADE
);
''')

# Invoice Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Invoice (
    invoice_id CHAR(8) PRIMARY KEY,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    total_amount INTEGER,  -- Add a comma here
    late_fees DECIMAL(10,2) DEFAULT 0,
    discount_applied DECIMAL(10,2) DEFAULT 0,
    order_id CHAR(8),
    payment_status_id CHAR(8),
    payment_method_id CHAR(8),
    payment_date DATE,
    final_amount INTEGER,
    FOREIGN KEY (payment_status_id) REFERENCES PaymentStatus(payment_status_id) ON DELETE CASCADE,
    FOREIGN KEY (payment_method_id) REFERENCES PaymentMethod(payment_method_id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE
);
''')




# Quote Line Item Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS QuoteLineItem (
    line_item_id CHAR(8) PRIMARY KEY,
    quote_id CHAR(8),
    product_id CHAR(8),
    quantity INTEGER CHECK (quantity BETWEEN 1 AND 20),
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    warranty_id CHAR(8),
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    FOREIGN KEY (quote_id) REFERENCES Quote(quote_id) ON DELETE CASCADE,
    FOREIGN KEY (warranty_id) REFERENCES Warranty(warranty_id) ON DELETE CASCADE
);
''')



# Save changes and close the connection
conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table_name in tables:
    print(f"Table: {table_name[0]}")
    cursor.execute(f"PRAGMA table_info({table_name[0]});")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  Column: {col[1]}, Type: {col[2]}, NotNull: {col[3]}, DefaultVal: {col[4]}, PrimaryKey: {col[5]}")
    print("-" * 20)

conn.close()
print("Database and tables created successfully!")


import sqlite3
import os
import csv

os.chdir("/Users/mn./Downloads/Schema 3")




# Establish a database connection
conn = sqlite3.connect('CRM.db')
cursor = conn.cursor()

# Function to import CSV into the database
def import_csv_to_table(csv_file, table_name):
    """Imports a CSV file while ensuring correct column mapping."""
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        columns = next(csv_reader)  # Read header row
        
        # Generate SQL placeholders based on table structure
        placeholders = ', '.join(['?' for _ in columns])
        sql = f"INSERT OR REPLACE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        
        for row in csv_reader:
            cursor.execute(sql, row)  # Insert or replace row into table
            
    print(f"{csv_file} imported successfully into {table_name}.")

# Mapping CSV files to database tables
csv_table_mapping = {
    "Industry.csv": "Industry",
    "JobTitle.csv": "JobTitle",
    "LeadSource.csv": "LeadSource",
    "LeadStatus.csv": "LeadStatus",
    "Stage.csv": "Stage",
    "LostReason.csv": "LostReason",
    "QuoteStatus.csv": "QuoteStatus",
    "PaymentMethod.csv": "PaymentMethod",
    "PaymentStatus.csv": "PaymentStatus",
    "OrderStatus.csv": "OrderStatus",
    "Warranty.csv": "Warranty",
    "VehicleType.csv": "VehicleType",
    "FuelType.csv": "FuelType",
    "Role.csv": "Role",
    "BillingCity.csv": "BillingCity",
    "BillingAddress.csv": "BillingAddress",
    "ShippingCity.csv": "ShippingCity",
    "ShippingAddress.csv": "ShippingAddress",
    "Account.csv": "Account",
    "Customer.csv": "Customer",
    "Lead.csv": "Lead",
    "Opportunity.csv": "Opportunity",
    "Quote.csv": "Quote",
    "QuoteLineItem.csv": "QuoteLineItem",
    "Orders.csv": "Orders",
    "Product.csv": "Product",
    "Users.csv": "Users",
    "Invoice.csv": "Invoice"
}

try:
    for csv_file, table_name in csv_table_mapping.items():
        if os.path.exists(csv_file):  # Check if file exists before importing
            import_csv_to_table(csv_file, table_name)
        else:
            print(f"File not found: {csv_file}")

    conn.commit()  # Commit changes after all imports
    print("\nAll CSV data imported successfully!")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    conn.rollback()  # Rollback on error

finally:
    conn.close()  # Close connection
    print("\nDatabase connection closed.")


import pandas as pd
import sqlite3

# Open the database connection
conn = sqlite3.connect('CRM.db')


# Load all tables into Pandas DataFrames
customer_df = pd.read_sql_query("SELECT * FROM Customer", conn)
orders_df = pd.read_sql_query("SELECT * FROM Orders", conn)
industry_df = pd.read_sql_query("SELECT * FROM Industry", conn)
jobtitle_df = pd.read_sql_query("SELECT * FROM JobTitle", conn)
leadsource_df = pd.read_sql_query("SELECT * FROM LeadSource", conn)
leadstatus_df = pd.read_sql_query("SELECT * FROM LeadStatus", conn)
stage_df = pd.read_sql_query("SELECT * FROM Stage", conn)
lostreason_df = pd.read_sql_query("SELECT * FROM LostReason", conn)
quotestatus_df = pd.read_sql_query("SELECT * FROM QuoteStatus", conn)
paymentmethod_df = pd.read_sql_query("SELECT * FROM PaymentMethod", conn)
paymentstatus_df = pd.read_sql_query("SELECT * FROM PaymentStatus", conn)
orderstatus_df = pd.read_sql_query("SELECT * FROM OrderStatus", conn)
warranty_df = pd.read_sql_query("SELECT * FROM Warranty", conn)
vehicletype_df = pd.read_sql_query("SELECT * FROM VehicleType", conn)
fueltype_df = pd.read_sql_query("SELECT * FROM FuelType", conn)
role_df = pd.read_sql_query("SELECT * FROM Role", conn)
billingcity_df = pd.read_sql_query("SELECT * FROM BillingCity", conn)
billingaddress_df = pd.read_sql_query("SELECT * FROM BillingAddress", conn)
shippingcity_df = pd.read_sql_query("SELECT * FROM ShippingCity", conn)
shippingaddress_df = pd.read_sql_query("SELECT * FROM ShippingAddress", conn)
account_df = pd.read_sql_query("SELECT * FROM Account", conn)
lead_df = pd.read_sql_query("SELECT * FROM Lead", conn)
opportunity_df = pd.read_sql_query("SELECT * FROM Opportunity", conn)
quote_df = pd.read_sql_query("SELECT * FROM Quote", conn)
quotelineitem_df = pd.read_sql_query("SELECT * FROM QuoteLineItem", conn)
invoice_df = pd.read_sql_query("SELECT * FROM Invoice", conn)
product_df = pd.read_sql_query("SELECT * FROM Product", conn)
users_df = pd.read_sql_query("SELECT * FROM Users", conn)




##1. Quarterly Sales by Vehicle Type
#Orders → order_id, order_date
#Product → product_id, vehicle_type_id
#VehicleType → vehicle_type_id, vehicle_type
#Invoice → order_id, total_amount



conn = sqlite3.connect("CRM.db")

query = """
SELECT
    strftime('%Y', o.order_date) || '-Q' ||
    CASE 
        WHEN strftime('%m', o.order_date) BETWEEN '01' AND '03' THEN '1'
        WHEN strftime('%m', o.order_date) BETWEEN '04' AND '06' THEN '2'
        WHEN strftime('%m', o.order_date) BETWEEN '07' AND '09' THEN '3'
        WHEN strftime('%m', o.order_date) BETWEEN '10' AND '12' THEN '4'
    END AS quarter,
    vt.vehicle_type AS vehicle_type_name,
    COUNT(o.order_id) AS total_sales,
    SUM(i.total_amount) AS total_revenue
FROM Orders o
JOIN Quote q ON o.quote_id = q.quote_id  
JOIN QuoteLineItem ql ON q.quote_id = ql.quote_id  
JOIN Product p ON ql.product_id = p.product_id  
JOIN VehicleType vt ON p.vehicle_type_id = vt.vehicle_type_id
JOIN Invoice i ON o.order_id = i.order_id  
GROUP BY quarter, vt.vehicle_type
ORDER BY quarter ASC, total_sales DESC;

"""



df1 = pd.read_sql_query(query, conn)
conn.close()


## 2. Territory Sales Leaderboard 
# Orders: order_id, shipping_address_id
# ShippingAddress: shipping_address_id, shipping_city_id
# ShippingCity: shipping_city_id, shipping_city
# Invoice: order_id, total_amount
# QuoteLineItem: quote_id, product_id, quantity, total_price


conn = sqlite3.connect("CRM.db")


query = """
SELECT
    sc.shipping_city,
    COUNT(o.order_id) AS total_orders,
    SUM(i.total_amount) AS total_sales_revenue
FROM Orders o
LEFT JOIN ShippingAddress sa ON o.shipping_address_id = sa.shipping_address_id
LEFT JOIN ShippingCity sc ON sa.shipping_city_id = sc.shipping_city_id
LEFT JOIN Invoice i ON o.order_id = i.order_id
LEFT JOIN Quote q ON o.quote_id = q.quote_id
LEFT JOIN QuoteLineItem qli ON q.quote_id = qli.quote_id

GROUP BY sc.shipping_city
ORDER BY total_sales_revenue DESC;
"""



df2 = pd.read_sql_query(query, conn)
conn.close()

## 4. Top Lead Sources by City 

# Lead: lead_id, lead_source_id, customer_id
# LeadSource: lead_source_id, lead_source
# Customer: customer_id, account_id
# Account: account_id, billing_address_id
# BillingAddress: billing_address_id, billing_city_id
# BillingCity: billing_city_id, billing_city

conn = sqlite3.connect("CRM.db")
query = """
SELECT
    bc.billing_city AS city,
    ls.lead_source AS lead_source,
    COUNT(l.lead_id) AS total_leads,
    AVG(l.lead_score) AS avg_lead_score 
FROM Lead l
JOIN LeadSource ls ON l.lead_source_id = ls.lead_source_id
JOIN Customer c ON l.customer_id = c.customer_id
JOIN Account a ON c.account_id = a.account_id
JOIN BillingAddress ba ON a.billing_address_id = ba.billing_address_id
JOIN BillingCity bc ON ba.billing_city_id = bc.billing_city_id
GROUP BY city, lead_source
ORDER BY city ASC, total_leads DESC;
"""


df2 = pd.read_sql_query(query, conn)
conn.close()




## 5. WarrantyType
conn = sqlite3.connect("CRM.db")

query = """
SELECT
   w.warranty AS WarrantyType, 
   COUNT(qli.line_item_id) AS TotalQuantitySold
FROM QuoteLineItem qli
JOIN Warranty w ON qli.warranty_id = w.warranty_id
GROUP BY w.warranty
ORDER BY TotalQuantitySold DESC;
"""

df2= pd.read_sql_query(query, conn)
conn.close()








