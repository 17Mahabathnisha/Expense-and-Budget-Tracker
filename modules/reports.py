import pandas as pd
from pathlib import Path

# MEMBER 4 - REPORTS & VISUALIZATION MODULE

def generate_report(expenses):
    """Generate summary data for dashboard and reports."""

    df = pd.DataFrame(expenses)

    if df.empty:
        return {
            "total_expense": 0,
            "transaction_count": 0,
            "category_count": 0,
            "category_summary": {},
            "payment_summary": {}
        }

    df["Amount"] = pd.to_numeric(df["Amount"], errors="raise")

    return {
        "total_expense": float(df["Amount"].sum()),
        "transaction_count": len(df),
        "category_count": df["Category"].nunique(),
        "category_summary": df.groupby("Category")["Amount"].sum().to_dict(),
        "payment_summary": df.groupby("Payment_mode")["Amount"].sum().to_dict()
    }


def export_report(expenses, output_file):
    """Export expense records as CSV report."""

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(expenses)
    df.to_csv(output_file, index=False)

    return output_file