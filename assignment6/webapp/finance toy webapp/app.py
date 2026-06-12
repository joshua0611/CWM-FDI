import os
import time
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# database consists of table consisting of headers: id, username, hash, cash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""
    # Getting this far is only possible with a login
    # Implying also the existence of the session userid

    # Extract relevant data before launching query
    person=session["user_id"]

    # Extract data through SQL queries
    cash=(db.execute("SELECT cash FROM users WHERE id= ? ;", session["user_id"]))[0]["cash"]
    holdings=db.execute("SELECT symbol, cname, sum(shareno) FROM logs WHERE person_id=? GROUP BY symbol HAVING NOT sum(shareno)=0", person)

    # Generate lists of dictionaries of (symbol, current holding, price), db.execute select returns list of dicts
    total_share_value=0
    for entry in holdings:
        entry["price"]=(lookup(entry["symbol"])["price"])
        total_share_value+=(lookup(entry["symbol"])["price"])*(entry["sum(shareno)"])

    # Determine grand total
    grand_total=total_share_value+cash


    # Render template, do the necessary calculations and presentation within the template
    return render_template("index.html", holdings=holdings, cash=cash, grand_total=grand_total)

    # To remove, this is a dummy placeholder
    testno=session["user_id"]
    return apology(f"TODO....your id is: {testno}")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # If method is get, as by redirection (clicked the buy button)
    if request.method=="GET":
        return render_template("buy.html")

    # If method is post, as by submission of buy request
    else:
    # Ensure that a quote was submitted
        if not request.form.get ("symbol"):
            return apology("must provide quote", 400)
        else:
            # Handle lookup result
            try:
                quote=lookup(request.form.get ("symbol"))
                if quote==None:
                    return apology("Invalid symbol", 400)
            except:
                # Deal with invalid quote
                return apology("Invalid symbol", 400)
        try:
            shareno=int(request.form.get("shares"))
        except:
            return apology("Number of shares to be bought must be a positive integer!", 400)
        if shareno<=0:
            return apology("Number of shares to be bought must be a positive integer!", 400)

        person=session["user_id"] # the person's user id as referenced in users
        symbol=request.form.get("symbol")
        cname=quote["name"]

        shareprice=float(quote["price"])
        value=(shareno)*(quote["price"])
        date=datetime.date.today().strftime("%Y/%m/%d")
        time=datetime.datetime.now().strftime("%H:%M:%S")

        # Check if the dude is too broke
        funds=db.execute("SELECT cash FROM users WHERE id= ? ", person)[0]["cash"]
        if (funds<value):
            return apology("You too broke bruh", 400)

        # Execute buying of shares, update shares if it exists, else create new share
        newcash=funds-value
        db.execute("UPDATE users SET cash = ? WHERE id=?", newcash, person)

        # Update purchase logs
        db.execute("INSERT INTO logs (person_id, type, symbol, cname, shareno, shareprice, value, date, time) VALUES (?, 'Buy', ?, ?, ?, ?, ?, ?, ?)", person, symbol, cname, shareno, shareprice, value, date, time) # id for this table does not need to be added, will be automatically added

        # Give success alert
        flash('Share(s) bought successfully!')

        return redirect("/")

    """Buy shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    share_summary=db.execute("SELECT * FROM logs WHERE person_id=? ORDER BY date DESC, time DESC;", session["user_id"])
    return render_template("history.html", share_summary=share_summary)

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
        # Render template for the input of the quote request
        return render_template("quote_request.html")

    if request.method == "POST":
        # Extract the quote to be quoted and render the template
        # Ensure that a quote was submitted
        if not request.form.get ("symbol"):
            return apology("must provide quote", 400)
        else:
            # Handle lookup result
            try:
                lookup_outcome=lookup(request.form.get ("symbol"))
                if lookup_outcome==None:
                    return apology("Invalid symbol", 400)
            except:
                # Deal with invalid quote
                return apology("Invalid symbol", 400)

            # Split the outcome of the lookup
            company_name=lookup_outcome["name"]
            company_price=lookup_outcome["price"]
            company_symbol=lookup_outcome["symbol"]

            # Render template based on the outcomes
            return render_template("quote_outcome.html", cname=company_name, cprice=company_price, csymbol=company_symbol)
    return apology("Not supposed to be here")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password", 400)

        # Ensure password matches confirmation
        elif not (request.form.get("password")==request.form.get("confirmation")):
            return apology("passwords do not match", 400)

        # Ensure username is not duplicated
        usernames=db.execute("SELECT username FROM users;")
        tried_username=request.form.get("username")
        for username in usernames:
            if tried_username==username["username"]:
                return apology("username already taken!", 400)

        # If they reach this far there are (assume) no errors
        username=request.form.get("username")
        hpassword=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        # Insert into db
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, hpassword)

        # Feedback message
        flash('You were successfully registered!')

        # Redirect user to login page
        return render_template("register.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method=="POST":
        # If getting here by way of form submission
        """Sell shares of stock"""
            # extract critical values

    # Ensure that a quote was submitted
        if not request.form.get ("symbol"):
            return apology("must provide quote", 400)
        else:
            # Handle lookup result
            try:
                symbol=lookup(request.form.get ("symbol"))
                if symbol==None:
                    return apology("Invalid symbol", 400)
            except:
                # Deal with invalid quote
                return apology("Invalid symbol", 400)

            # Check if the share valus is a positive integer
        try:
            shareno=-int(request.form.get("shares"))
        except:
            return apology("Number of shares to be bought must be a positive integer!", 403)
        if shareno>=0:
            return apology("Number of shares to be sold must be a positive integer!", 403)

            # Check if the guy has enough shares
                # Extract the guy's share counts
        person=session["user_id"]
        symbol=request.form.get ("symbol")
        share_count=db.execute("SELECT sum(shareno) FROM logs WHERE person_id=? AND symbol=?  GROUP BY symbol;", person, symbol)
                # Compare the number of shares he has with sell request

        if (share_count[0]["sum(shareno)"]<(-shareno)):
            return apology("Not enough shares", 400)
        else: # enough shares, and selected valid share
                # magic the logs
                    # extract the rest of the info
            quote=lookup(symbol)

            cname=quote["name"]
            shareprice=quote["price"]
            value=(shareno)*(shareprice)
            date=datetime.date.today().strftime("%Y/%m/%d")
            time=datetime.datetime.now().strftime("%H:%M:%S")
                    # magic the logs proper
            db.execute("INSERT INTO logs (person_id, type, symbol, cname, shareno, shareprice, value, date, time) VALUES (?, 'Sell', ?, ?, ?, ?, ?, ?, ?)", person, symbol, cname, shareno, shareprice, value, date, time) # id for this table does not need to be added, will be automatically added

                # magic the cash
            funds=db.execute("SELECT cash FROM users WHERE id=?;", person)
            newcash=funds[0]["cash"]-value
            db.execute("UPDATE users SET cash =? WHERE id=?", newcash, person)

                # flash, return the template
            flash("Selling of shares successful!")

            return redirect("/")

    # If getting here by way of redirect
        # Render the unique template
    if request.method == "GET":
        person=session["user_id"]
        share_options=db.execute("SELECT symbol, sum(shareno) FROM logs WHERE person_id=? GROUP BY symbol HAVING NOT sum(shareno)=0 ;", person)
        return render_template("sell.html", share_options=share_options)

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    # if route is reached by way of form submission
    if request.method=="POST":
        added_cash=int(request.form.get("added_cash"))

        # check for input validity
        if added_cash<=0:
            return apology("added cash value must be positive!", 403)

        # add cash
        current_cash=db.execute("SELECT cash FROM users WHERE id=?;", session["user_id"])
        new_cash=current_cash[0]["cash"]+added_cash*1000
        db.execute("UPDATE users SET cash=? WHERE id=?;", new_cash, session["user_id"])

        # flash success message
        flash("Cash added successfully!")

        # return
        return redirect("/")
    if request.method=="GET":
        return render_template("add_cash.html")