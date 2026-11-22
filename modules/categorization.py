import pandas as pd
from pathlib import Path

# MEMBER 2 - CATEGORIZATION MODULE

def categorize_expenses(expenses):
    """Automatically categorize expenses based on description."""

    category_keywords = {
        "Food": ["food", "breakfast", "lunch", "dinner", "restaurant"],
        "Travel": ["bus", "train", "taxi", "travel", "petrol"],
        "Shopping": ["shopping", "clothes", "dress", "shoes"],
        "Entertainment": ["movie", "cinema", "game"],
        "Education": ["book", "college", "course", "education"],
        "Utilities": ["recharge", "electricity", "water", "internet"],
        "Medical": ["medical", "medicine", "hospital"],
    }

    categorized = []

    for expense in expenses:
        description = expense.get("Description", "").lower()
        category = "Others"

        for category_name, keywords in category_keywords.items():
            if any(keyword in description for keyword in keywords):
                category = category_name
                break

        updated_expense = expense.copy()
        updated_expense["Category"] = category
        categorized.append(updated_expense)

    return categorized


def save_categorized_expenses(expenses, output_file):
    """Save categorized expenses into a CSV file."""

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if not expenses:
        raise ValueError("No expense records available.")

    fieldnames = list(expenses[0].keys())

    pd.DataFrame(expenses, columns=fieldnames).to_csv(
        output_file, index=False
    )

    return output_file