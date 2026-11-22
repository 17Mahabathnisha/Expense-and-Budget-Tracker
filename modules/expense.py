import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# MEMBER 1 - EXPENSE MODULE


def load_expenses(input_file):
    """Read expense records from CSV."""

    input_file = Path(input_file)

    if not input_file.exists():
        raise FileNotFoundError(
            f"Expense file not found: {input_file}"
        )

    expenses = []

    with open(
        input_file,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        required_columns = [
            "Date",
            "Description",
            "Amount",
            "Category",
            "Payment_mode"
        ]

        if not reader.fieldnames:
            raise ValueError("CSV file is empty.")

        missing = [
            col for col in required_columns
            if col not in reader.fieldnames
        ]

        if missing:
            raise ValueError(
                f"Missing CSV columns: {', '.join(missing)}"
            )

        for row in reader:
            row["Amount"] = float(row["Amount"])
            expenses.append(row)

    return expenses


def calculate_expense_summary(expenses, total_budget=5000):
    """Calculate expense and category summaries."""

    total_expense = sum(
        row["Amount"] for row in expenses
    )

    remaining_balance = total_budget - total_expense

    category_totals = defaultdict(float)
    payment_totals = defaultdict(float)
    monthly_totals = defaultdict(float)

    for row in expenses:

        category_totals[row["Category"]] += row["Amount"]

        payment_totals[row["Payment_mode"]] += row["Amount"]

        date_text = row["Date"].strip()
        parsed_date = None

        date_formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%d-%m-%y",
            "%d/%m/%y"
        ]

        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(
                    date_text, date_format
                )
                break
            except ValueError:
                continue

        if parsed_date:
            month = parsed_date.strftime("%B %Y")
            monthly_totals[month] += row["Amount"]

    highest_expense = (
        max(expenses, key=lambda x: x["Amount"])
        if expenses else None
    )

    lowest_expense = (
        min(expenses, key=lambda x: x["Amount"])
        if expenses else None
    )

    return {
        "total_budget": total_budget,
        "total_expense": total_expense,
        "remaining_balance": remaining_balance,
        "category_totals": dict(category_totals),
        "payment_totals": dict(payment_totals),
        "monthly_totals": dict(monthly_totals),
        "highest_expense": highest_expense,
        "lowest_expense": lowest_expense
    }