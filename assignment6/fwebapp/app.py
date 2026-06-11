import os
import time
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
# from werkzeug.security import check_password_hash, generate_password_hash

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

""" TODO: Delete once program confirmed working well
# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
"""

# Keys to induce vulnerability to sql injection attacks
vuln=1
safe=0

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

    if vuln: # Vulnerability selection flag
        user_id=session["user_id"]
        query="SELECT cash FROM users WHERE id='"+ str(person) +"'"
        cash=(db.execute(query))[0]["cash"]
        query="SELECT symbol, cname, sum(shareno) FROM logs WHERE person_id='" + str(person) + "' GROUP BY symbol HAVING NOT sum(shareno)=0;"
        holdings=db.execute(query)

    else:
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

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if vuln: # In a sense, the checks for both being filled protects against a "dumber" SQL attack bot
            pass
        else:
            # Ensure username was submitted
            if not request.form.get("username"):
                return apology("must provide username", 403)
            # Ensure password was submitted
            elif not request.form.get("password"):
                return apology("must provide password", 403)

        # Query database for username
        if vuln:
            query = "SELECT * FROM users WHERE username = '" + request.form.get("username")+"'"
            rows = db.execute(query)
        else:
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not (rows[0]["hash"]==request.form.get("password")):
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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if vuln:
            pass
        else:
            # Ensure username was submitted
            if not request.form.get("username"):
                return apology("must provide username", 400)
            # Ensure password was submitted
            elif not request.form.get("password") or not request.form.get("confirmation"):
                return apology("must provide password", 400)

        # Ensure password matches confirmation.
        if not (request.form.get("password")==request.form.get("confirmation")):
            return apology("passwords do not match", 400)

        # Ensure username is not duplicated
        usernames=db.execute("SELECT username FROM users;")
        tried_username=request.form.get("username")
        for username in usernames:
            if tried_username==username["username"]:
                return apology("username already taken!", 400)

        # If they reach this far there are (assume) no errors
        username=request.form.get("username")
        password=request.form.get("password")
        # Insert into db
        if vuln:
            query="INSERT INTO users (username, hash) VALUES ('" + username+  "','" + password + "')"
            db.execute(query)
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, password)

        # Feedback message
        flash('You were successfully registered!')

        # Redirect user to login page
        return render_template("register.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

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
