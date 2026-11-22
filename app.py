from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import add_expense, get_saved_expenses, register_user, get_user, create_table, create_users_table
from pathlib import Path

from modules.expense import load_expenses, calculate_expense_summary
from modules.categorization import categorize_expenses, save_categorized_expenses
from modules.budget_analysis import analyze_budget, save_budget_report
from modules.reports import generate_report, export_report

app = Flask(__name__)
app.secret_key = "expense_tracker_secret_key"
create_table()
create_users_table()

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "input" / "expenses.csv"
OUTPUT_DIR = BASE_DIR / "data" / "output"


def get_expenses():
    user_id = session.get("user_id")

    if not user_id:
        return load_expenses(INPUT_FILE)

    database_expenses = get_saved_expenses(user_id)

    return database_expenses
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        success = register_user(
            full_name,
            username,
            email,
            hashed_password
        )

        if success:
            return redirect(url_for("login"))

        return "Username or Email already exists!"

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = get_user(username)

        if user and check_password_hash(user[4], password):
            session["user_id"] = username
            return redirect(url_for("home"))

        return "Invalid username or password!"

    return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    expenses = get_expenses()
    summary = calculate_expense_summary(expenses)

    return render_template(
        "index.html",
        summary=summary
    )

@app.route("/expense-register")
def expense_register():

    if "user_id" not in session:
        return redirect(url_for("login"))

    expenses = get_expenses()

    return render_template(
        "expense_register.html",
        expenses=expenses
    )


@app.route("/categorization")
def categorization():

    if "user_id" not in session:
        return redirect(url_for("login"))

    expenses = get_expenses()

    categorized_expenses = categorize_expenses(expenses)

    output_file = OUTPUT_DIR / "categorized_expenses.csv"
    save_categorized_expenses(categorized_expenses, output_file)

    return render_template(
        "categorization.html",
        categorized_expenses=categorized_expenses
    )


@app.route("/budget-analysis")
def budget_analysis():

    if "user_id" not in session:
        return redirect(url_for("login"))

    expenses = get_expenses()

    budget_report = analyze_budget(expenses)

    output_file = OUTPUT_DIR / "budget_report.csv"
    save_budget_report(budget_report, output_file)

    budget_records = budget_report.to_dict(orient="records")

    return render_template(
        "budget_analysis.html",
        budget_records=budget_records
    )


@app.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect(url_for("login"))

    expenses = get_expenses()

    report_data = generate_report(expenses)

    output_file = OUTPUT_DIR / "expense_report.csv"
    export_report(expenses, output_file)

    return render_template(
        "reports.html",
        report_data=report_data
    )
@app.route("/add-expense", methods=["GET", "POST"])
def add_expense_page():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        date = request.form["date"]
        description = request.form["description"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        payment_mode = request.form["payment_mode"]

        add_expense(
            session["user_id"],
            date,
            description,
            amount,
            category,
            payment_mode
        )

        return redirect(url_for("add_expense_page"))

    return render_template("add_expense.html")


if __name__ == "__main__":
    app.run(debug=True)