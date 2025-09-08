# SQL CRM Database Project  

This project designs and implements a **Customer Relationship Management (CRM) database** in SQLite. It creates a normalized relational schema with constraints, imports structured data from CSV files, and executes SQL queries for business insights.  

---

## 🚀 Features  
- **Database Schema Design**:  
  - Tables for Customer, Orders, Invoice, Product, Opportunity, Quote, Payment, Shipping/Billing, etc.  
  - Enforced **foreign keys, primary keys, and constraints** (e.g., discounts, quantity limits).  

- **Data Integration**:  
  - Automated import of CSV files into the correct tables.  
  - Error handling and rollback for data consistency.  

- **Analytics & Reporting**:  
  - Quarterly sales by vehicle type.  
  - Revenue by sales stage.  
  - Lost reasons analysis.  
  - Customer and order segmentation.  

- **Python + SQL Integration**:  
  - Used **SQLite3** for database creation and querying.  
  - Loaded data into **Pandas DataFrames** for further exploration.  

---

## ⚙️ Tech Stack  
- Python (sqlite3, pandas, csv, os)  
- SQLite (relational database)  
- CSV (raw data source)  

---

## 📊 Example Query  
```sql
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
JOIN Product p ON p.product_id = q.product_id
JOIN VehicleType vt ON p.vehicle_type_id = vt.vehicle_type_id
JOIN Invoice i ON i.order_id = o.order_id
GROUP BY quarter, vehicle_type_name;
