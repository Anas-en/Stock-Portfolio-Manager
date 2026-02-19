import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":

        # buy = (request.args.get("buy"))
        # if buy == "1":
        #     new_buy = 1
        # else:
        #     new_buy = 0

        user_id = session["user_id"]
        stocks = db.execute(
            "SELECT stock , no_shares AS TotalQuantity FROM shares  WHERE user_id = ? ", user_id)

        # TODO: to render the stocks from the shares table rather than transactions
        # DONE

        stock_price = []

        cash = db.execute("SELECT cash FROM users WHERE id= ?", session["user_id"])

        for objstock in stocks:
            stock = {}
            stock["current_price"] = (lookup(objstock["stock"]))["price"]
            stock["total_price"] = f"{((stock["current_price"]) * objstock["TotalQuantity"]):.2f}"
            stock["stock"] = objstock["stock"]
            stock["TotalQuantity"] = f"{objstock["TotalQuantity"]:.2f}"
            stock_price.append(stock)

        total_stock = 0
        left_cash = cash[0]["cash"]

        for stock in stock_price:
            total_stock += float(stock["total_price"])

        total_money = total_stock + left_cash
        total_stock = f"{total_stock:.3f}"
        left_cash = f"{left_cash:.2f}"
        total_money = f"{total_money:.2f}"

        return render_template("index.html", stock_price=stock_price, left_cash=left_cash, total_money=total_money)
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_raw = request.form.get("shares")

        if not symbol:
            return apology("MISSING SYMBOL", 400)
        if not shares_raw:
            return apology("MISSING SHARES", 400)
        try:
            shares = float(shares_raw)
        except ValueError:
            # checked for the can it be converted to float
            return apology("ONLY +ve integer", 400)

        # check the shares are +ve and an integer
        if shares <= 0 or not shares.is_integer():
            return apology("ONLY +ve integers", 400)

        shares = int(shares)
        # if shares < 0 :
        #     return apology("ONLY +ve integers",400)

        stock = lookup(symbol)
        if stock == None:
            return apology("INVALID SYMBOL", 400)
        rows = db.execute("SELECT cash FROM users WHERE id =?", session["user_id"])

        if float(rows[0]["cash"]) < float(float(stock["price"]) * shares):
            return apology("insufficient Balance", 404)

        new_balance = rows[0]["cash"]-(shares * (lookup(symbol)["price"]))
        db.execute("SELECT * FROM shares WHERE stock =?", symbol)
        db.execute("UPDATE users SET cash = ? WHERE id =?",
                   f"{new_balance:.2f}", session["user_id"])

        db.execute("INSERT INTO transactions (user_id , stock, purchasePRICE, shares,txn_type) VALUES(?,?,?,?,'BUY')",
                   session["user_id"], stock["symbol"], stock["price"], int(shares))

        # managing the stocks table for buy
        # retreive the list of stocks
        shares_list = db.execute(
            "SELECT * FROM shares WHERE user_id = ? AND stock = ?", session["user_id"], symbol)
        if len(shares_list) == 0:  # stock doesn't exits
            # make entry of the stock
            db.execute("INSERT INTO shares (user_id , stock , no_shares) VALUES(?,?,?)",
                       session["user_id"], symbol, shares)
        # if the user and the particular stock exits
        else:
            user_shares = shares_list[0]["no_shares"]

            user_shares += shares
            db.execute("UPDATE shares SET no_shares = ? WHERE user_id = ? AND stock = ?",
                       user_shares, session["user_id"], symbol)

        flash("Bought!")
        return redirect("/")

    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        txns = db.execute("SELECT * FROM transactions WHERE user_id=?", session["user_id"])

        # TODO : have a -ve sign infront of the shares for txn_type = SELL

        return render_template("history.html", txns=txns)
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("MISSING SYMBOL", 400)

        stock = lookup(symbol)
        if stock == None:
            return apology("INVALID SYMBOL", 400)

        return render_template("quoted.html", name=stock["name"], symbol=stock["symbol"], price=stock["price"])
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        user = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not user:
            return apology("MISSING USERNAME", 400)
        if not password:
            return apology("MISSING PASSWORD", 400)
        if password != confirmation:
            return apology("PASSWORD DOES'NT MATCH", 400)

        try:
            db.execute("INSERT INTO users (username,hash) VALUES (?,?)", user,
                       generate_password_hash(password, method='scrypt', salt_length=16))
        except ValueError:
            return apology("USER already exist", 400)

        rows = db.execute("SELECT * FROM users WHERE username =?", user)
        session["user_id"] = rows[0]["id"]
        flash("Registered!")
        return redirect("/")
    return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        shares_list = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])

        return render_template("sell.html", shares=shares_list)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_raw = request.form.get("shares")

        if not symbol:
            return apology("MISSING SYMBOL", 400)

        if not shares_raw:
            return apology("MISSING SHARES", 400)

        if shares_raw.isdigit():
            shares = int(shares_raw)
        else:
            return apology("Try only +ve integer", 400)

        if shares <= 0:
            return apology("ONLY +ve integers", 400)

        shares_list = db.execute(
            "SELECT * FROM shares WHERE user_id = ? AND stock = ?", session["user_id"], symbol)
        if shares_list == []:
            return apology("NOT HAVE THIS STOCK", 404)

        if shares > int(shares_list[0]["no_shares"]):
            return apology("TOO MANY SHARES", 400)

        # now all checks done sell it
        market = lookup(symbol)
        market_price = market["price"]
        db.execute("INSERT INTO transactions(user_id , stock , purchasePRICE , shares , txn_type) VALUES(?,?,?,?,'SELL')",
                   session["user_id"], symbol, market_price, shares)

        user_list = db.execute("SELECT * From users WHERE id = ?", session["user_id"])
        user_cash = user_list[0]["cash"]
        user_cash += (market_price * shares)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash, session["user_id"])

        no_shares = shares_list[0]["no_shares"]
        no_shares -= shares
        if no_shares == 0:
            db.execute("DELETE FROM shares WHERE user_id = ? AND stock = ?",
                       session["user_id"], symbol)
        else:
            db.execute("UPDATE shares SET no_shares = ? WHERE user_id = ? AND stock = ?",
                       no_shares, session["user_id"], symbol)

        # TODO:add a page that after selling a blue line wrote "sold!"
        # above the index.html page
        # DONE
        flash("Sold!")
        return redirect("/")
    return apology("TODO")


@app.route("/change_password", methods=["POST", "GET"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("password.html")
    if request.method == "POST":
        current_password = request.form.get("old_password")
        new_password = request.form.get("password")
        re_password = request.form.get("verify_password")

        if not current_password:
            return apology("Type Current Password", 400)
        if not new_password:
            return apology("Type new_password", 400)
        if new_password != re_password:
            return apology("New Password Not Match")
        if current_password == new_password:
            return apology("New Password cannot be same as Current")

        user = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])
        pwhash = user[0]["hash"]
        if check_password_hash(pwhash, current_password):
            new_pwhash = generate_password_hash(new_password, method='scrypt', salt_length=16)

            db.execute("UPDATE users SET hash = ? WHERE id =?", new_pwhash, session["user_id"])

            flash("Password Changed!")
            return redirect("/")
        else:
            return apology("Current Password Not Matched !!", 401)

    return apology("TODO")
