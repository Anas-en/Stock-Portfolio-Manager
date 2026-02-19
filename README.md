Since you have your schema ready, you can integrate it directly into your documentation. This helps anyone reviewing your code (like a CS50 TA) understand exactly how your data is structured.

Here is the updated, complete **README.md** file for your finance app.

---

# C$50 Finance

### **Project Overview**

**C$50 Finance** is a web-based tool developed as part of **CS50x: Introduction to Computer Science**. The application allows users to manage a virtual stock portfolio by "buying" and "selling" stocks using real-time market data. Each user starts with a virtual balance of $10,000.00 to simulate real-world trading.

---

### **Features**

* **Portfolio Tracking (`/`)**: A dynamic dashboard that displays all currently owned stocks, their quantities, current market prices, and the total value of the user's assets.
* **Stock Lookups (`/quote`)**: Allows users to check the real-time price of any stock by its ticker symbol using the IEX API.
* **Trading (`/buy` & `/sell`)**: Enables users to purchase and liquidate stocks. The app validates sufficient funds/shares before executing and updating the database.
* **Audit History (`/history`)**: Provides a full chronological log of every transaction made by the user, including the execution price and timestamp.
* **Security Enhancement (`/change_password`)**: A custom feature allowing users to update their account credentials securely using `scrypt` hashing.

---

### **Technical Implementation**

* **Backend**: Python (Flask)
* **Database**: SQLite (managed via the `cs50` SQL library)
* **Security**: `werkzeug.security` for hashing passwords and `flask_session` for session management.
* **Frontend**: HTML5, CSS3 (Bootstrap), and Jinja2 templating.

---

### **Database Schema**

The application uses the following relational structure in `finance.db`:

#### **1. Users Table**

Stores authentication details and the current liquid cash balance.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, 
    hash TEXT NOT NULL, 
    cash NUMERIC NOT NULL DEFAULT 10000.00
);
CREATE UNIQUE INDEX username ON users (username);

```

#### **2. Transactions Table**

A ledger recording every trade executed on the platform.

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id TEXT NOT NULL,
    stock TEXT NOT NULL,
    timeStamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    purchasePRICE REAL NOT NULL,
    shares INTEGER NOT NULL, 
    txn_type VARCHAR(20) NOT NULL DEFAULT 'BUY',
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX user_idx ON transactions(user_id);

```

#### **3. Shares Table**

An optimized table tracking current aggregate holdings for each user.

```sql
CREATE TABLE shares (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    user_id TEXT NOT NULL, 
    stock TEXT NOT NULL, 
    no_shares INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX shares_idx ON shares(user_id);

```

---

### **Installation**

1. **Extract the project**:
```bash
cd finance

```


2. **Set up the API Key**:
Obtain a key from [IEX Cloud](https://www.google.com/search?q=https://iexcloud.io/) and export it:
```bash
export API_KEY=your_public_key_here

```


3. **Run the application**:
```bash
flask run

```



---
