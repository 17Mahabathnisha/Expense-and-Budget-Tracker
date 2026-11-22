import pandas as pd
from pathlib import Path

# MEMBER 3 - BUDGET ANALYSIS MODULE

def analyze_budget(expenses, category_budgets=None):

    if category_budgets is None:
        category_budgets = {
            "Food": 800,
            "Travel": 500,
            "Education": 1600,
            "Utilities": 600,
            "Shopping": 700,
            "Medical": 300,
            "Entertainment": 300
        }

    df = pd.DataFrame(expenses)

    if df.empty:
        raise ValueError("No expense records available.")

    df["Amount"] = pd.to_numeric(df["Amount"], errors="raise")

    actual_expenses = df.groupby("Category")["Amount"].sum()

    report = []

    for category, budget in category_budgets.items():
        actual = float(actual_expenses.get(category, 0))
        remaining = budget - actual

        if remaining > 0:
            status = "Within Budget"
        elif remaining == 0:
            status = "Budget Used"
        else:
            status = "Over Budget"

        report.append({
            "Category": category,
            "Budget": budget,
            "Actual Expense": actual,
            "Remaining": remaining,
            "Status": status
        })

    return pd.DataFrame(report)


def save_budget_report(report, output_file):

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    report.to_csv(output_file, index=False)

    return output_file