import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from werkzeug.security import check_password_hash

from database.db import init_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "dev-secret-key"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("register.html")

    if request.method != "POST":
        abort(405)

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not email or not password or not confirm_password:
        flash("All fields are required.")
        return render_template("register.html", name=name, email=email)

    if password != confirm_password:
        flash("Passwords do not match.")
        return render_template("register.html", name=name, email=email)

    try:
        create_user(name, email, password)
    except sqlite3.IntegrityError:
        flash("Email already registered.")
        return render_template("register.html", name=name, email=email)

    flash("Account created! Please sign in.")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        flash("All fields are required.")
        return render_template("login.html")

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user["password"], password):
        flash("Invalid email or password.")
        return render_template("login.html")

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Ananya Sharma",
        "email": "ananya@example.com",
        "member_since": "January 2024",
        "initials": "AS",
    }
    stats = {
        "total_spent": "₹12,450",
        "transaction_count": 24,
        "top_category": "Food",
    }
    transactions = [
        {"date": "2 May 2026",  "description": "Swiggy Order",     "category": "Food",     "amount": "₹340"},
        {"date": "30 Apr 2026", "description": "Ola Cab",          "category": "Travel",   "amount": "₹220"},
        {"date": "28 Apr 2026", "description": "Electricity Bill", "category": "Bills",    "amount": "₹1,800"},
        {"date": "25 Apr 2026", "description": "Zomato Order",     "category": "Food",     "amount": "₹280"},
        {"date": "22 Apr 2026", "description": "Amazon Purchase",  "category": "Shopping", "amount": "₹1,200"},
    ]
    categories = [
        {"name": "Food",     "total": "₹4,200", "slug": "food"},
        {"name": "Bills",    "total": "₹3,600", "slug": "bills"},
        {"name": "Shopping", "total": "₹2,550", "slug": "shopping"},
        {"name": "Travel",   "total": "₹2,100", "slug": "travel"},
    ]
    return render_template(
        "profile.html",
        user=user, stats=stats, transactions=transactions, categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)
