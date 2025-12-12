# Mini SQL Database Engine (Python)

A simplified in-memory SQL engine built from scratch using Python.  
This project demonstrates how SQL parsing and execution work internally inside a database system.  
It loads CSV files and executes SQL queries with support for:

- SELECT *
- SELECT column1, column2
- WHERE filtering
- COUNT(*)
- COUNT(column)
- Case-insensitive string matching
- Numeric comparison

---

## 🚀 Features

### 1. Data Loading  
- Load any CSV file as a table.
- Automatically reads column names using `csv.DictReader`.

### 2. SQL Parsing  
Supports a subset of SQL:
SELECT * FROM table;
SELECT col1, col2 FROM table;
SELECT COUNT(*) FROM table;
SELECT COUNT(column) FROM table;
SELECT col FROM table WHERE column = 'value';
SELECT col FROM table WHERE column > number;


### 3. Query Execution  
- Full row projection (`SELECT *`)
- Specific column projection
- WHERE filtering using:
  - `=`, `!=`, `>`, `<`, `>=`, `<=`
- Case-insensitive string comparison
- COUNT aggregates

---

## 📁 Project Structure
## 📁 Project Structure

```text
mini-sql-database-engine/
│
├── parser.py          # SQL parser
├── engine.py          # Query execution engine
├── cli.py             # Command-line interface (REPL)
│
├── sample_data/
│   ├── employees.csv
│   └── orders.csv
│
└── README.md
```


---

## 🧪 Example Queries

### Load CSV
When you run the CLI:
Enter path to CSV file to load: sample_data/orders.csv


### 1. Select All Rows


SELECT * FROM orders;


### 2. Select Specific Columns


SELECT customer, amount FROM orders;


### 3. Filter Rows


SELECT customer FROM orders WHERE status = 'PAID';


### 4. Numeric Filtering
SELECT customer, amount FROM orders WHERE amount > 300;


### 5. Count Rows


SELECT COUNT(*) FROM orders;


---

## ▶️ Running the Application

Use Python 3.10+.

### Run CLI:


python cli.py


The REPL will start:


sql>
---

## 📚 Supported SQL Grammar

### SELECT
SELECT * FROM table;
SELECT col1, col2 FROM table;


### WHERE


WHERE column = value
WHERE column != value
WHERE column > number
WHERE column < number
WHERE column >= number
WHERE column <= number
### COUNT Aggregation
SELECT COUNT(*) FROM table;
SELECT COUNT(column) FROM table;

yaml
Copy code

---

## 🔧 Error Handling

The engine shows meaningful errors:
- Invalid syntax
- Unknown columns
- Table not loaded
- Unsupported operations

---

## 👤 Author
Patnala Kousalya  
Mini SQL Engine Project – Data Engineering Module  