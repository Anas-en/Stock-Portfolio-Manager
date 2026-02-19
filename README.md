
---

# 📈 CS50 Finance – Stock Trading Web Application

A full-stack web application built as part of **CS50's Introduction to Computer Science** by **Harvard University**.

This project simulates a real-world stock trading platform where users can register, log in, buy and sell stocks using real-time market data, track portfolio performance, view transaction history, and securely change their password.

---

# 🚀 Features

* User Registration & Login
* Secure Password Hashing (scrypt)
* Password Change Functionality
* Real-Time Stock Quote Lookup
* Buy Stocks with Virtual Cash
* Sell Owned Stocks
* Portfolio Dashboard
* Transaction History
* Persistent Database Storage
* Flash Messaging for User Feedback

---

# 🛠 Tech Stack

| Layer          | Technology                |
| -------------- | ------------------------- |
| Backend        | Python                    |
| Framework      | Flask                     |
| Database       | SQLite                    |
| ORM            | CS50 SQL Library          |
| Frontend       | HTML, Bootstrap           |
| Templating     | Jinja2                    |
| Authentication | Flask-Session             |
| Security       | Werkzeug (scrypt hashing) |
| API            | IEX Cloud (stock data)    |

---

# 📂 Project Structure

```
finance/
│── app.py
│── helpers.py
│── requirements.txt
│── finance.db
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── quote.html
│   ├── quoted.html
│   ├── buy.html
│   ├── sell.html
│   ├── history.html
│   └── password.html
│
└── static/
    └── styles.css
```

---

# 🗄 Database Schema

## users

| Column   | Type    | Description                     |
| -------- | ------- | ------------------------------- |
| id       | INTEGER | Primary Key                     |
| username | TEXT    | Unique username                 |
| hash     | TEXT    | Hashed password                 |
| cash     | NUMERIC | User balance (default 10000.00) |

---

## transactions

| Column    | Type     | Description                |
| --------- | -------- | -------------------------- |
| id        | INTEGER  | Primary Key                |
| user_id   | INTEGER  | Foreign key → users.id     |
| stock     | TEXT     | Stock symbol               |
| timestamp | DATETIME | Auto timestamp             |
| price     | REAL     | Stock price at transaction |
| shares    | INTEGER  | Number of shares           |
| txn_type  | TEXT     | BUY or SELL                |

---

## shares

| Column    | Type    | Description      |
| --------- | ------- | ---------------- |
| id        | INTEGER | Primary Key      |
| user_id   | INTEGER | Foreign key      |
| stock     | TEXT    | Stock symbol     |
| no_shares | INTEGER | Current holdings |

---

# 🔐 Authentication & Security

* Passwords hashed using `generate_password_hash()` with:

  * Method: `scrypt`
  * Salt length: 16
* Password verification via `check_password_hash()`
* Protected routes using `@login_required`
* Server-side sessions (filesystem-based)
* Password change requires:

  * Correct current password
  * New password confirmation
  * New password different from old

---


---

# 📊 Application Workflow

## Registration

* User creates account
* Password is hashed
* Default cash balance = $10,000

## Buying Stocks

* Validate symbol
* Validate shares (positive integer)
* Check sufficient balance
* Deduct cash
* Insert transaction
* Update shares table

## Selling Stocks

* Validate ownership
* Validate share quantity
* Add cash
* Insert transaction
* Update or delete share record

## Portfolio View

* Fetch current holdings
* Fetch real-time prices
* Calculate total stock value
* Display:

  * Individual stock values
  * Cash balance
  * Total portfolio value

---

# 🧠 Key Concepts Demonstrated

* RESTful Routing
* SQL Queries (SELECT, INSERT, UPDATE, DELETE)
* Foreign Key Relationships
* Session-Based Authentication
* API Integration
* Server-Side Rendering
* Input Validation
* Database Normalization

---

# 📌 Future Improvements

* Portfolio performance charts
* Transaction filtering
* Search & sorting
* Improved UI styling
* Email-based password reset
* Deployment on Render

---

# 👨‍💻 Author

Mohd Anas
CS50 Finance Project
Full Stack Web Development Practice

---
