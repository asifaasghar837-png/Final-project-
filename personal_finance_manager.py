"""
Personal Finance & Expense Management System
Author: Asifa Asghar
Requires: Python 3 (standard library only - no installation needed)
"""

import json
import math
import os
from datetime import datetime

# Save the JSON file in the same folder as this script
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_FOLDER, "finance_data.json")


# ---------------- Data storage ----------------
def save_data(transactions):
    """Write the list of transactions to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)
    except OSError as error:
        print(f"Error: Could not save data ({error}).")


def load_data():
    """Load transactions. Create file if missing; back up if corrupted."""
    if not os.path.exists(DATA_FILE):
        save_data([])
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Data is not a list")

        required = ["id", "type", "category", "amount", "date"]
        for item in data:
            if not isinstance(item, dict) or not all(key in item for key in required):
                raise ValueError("A transaction is missing required fields")

        return data

    except (json.JSONDecodeError, ValueError, OSError):
        print("Warning: finance_data.json is corrupted. Starting with empty data.")
        backup_file = DATA_FILE + ".corrupted.bak"
        try:
            os.replace(DATA_FILE, backup_file)
            print(f"The old file was saved as: {os.path.basename(backup_file)}")
        except OSError:
            pass
        save_data([])
        return []


# ---------------- Helper functions ----------------
def get_category(prompt):
    """Keep asking until the user enters a non-empty category."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("Error: This field cannot be empty. Please try again.")
        else:
            return text.title()  # 'food' and 'FOOD' become 'Food'


def get_amount():
    """Keep asking until the user enters a valid positive number."""
    while True:
        text = input("Enter amount (Rs.): ").strip()
        try:
            amount = float(text)
        except ValueError:
            print("Error: Please enter a valid number (example: 2500 or 99.50).")
            continue

        if math.isnan(amount) or math.isinf(amount):
            print("Error: Please enter a valid number.")
        elif amount <= 0:
            print("Error: Amount must be greater than zero.")
        else:
            return round(amount, 2)


def get_next_id(transactions):
    """Return a new unique ID (highest existing ID + 1)."""
    if len(transactions) == 0:
        return 1
    return max(item["id"] for item in transactions) + 1


def add_transaction(transactions, trans_type, category, amount):
    """Create a transaction, add it to the list and save the file."""
    transaction = {
        "id": get_next_id(transactions),
        "type": trans_type,
        "category": category,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    transactions.append(transaction)
    save_data(transactions)
    return transaction


def print_table(items):
    """Print a list of transactions as a neat table."""
    print()
    print(f"{'ID':<5}{'Type':<10}{'Category/Source':<22}{'Amount (Rs.)':>14}  {'Date':<12}")
    print("-" * 65)
    for item in items:
        print(f"{item['id']:<5}{item['type']:<10}{item['category']:<22}"
              f"{item['amount']:>14,.2f}  {item['date']:<12}")
    print("-" * 65)


# ---------------- Main features ----------------
def add_income(transactions):
    print("\n--- Add Income ---")
    source = get_category("Enter income source (e.g. Salary): ")
    amount = get_amount()
    add_transaction(transactions, "Income", source, amount)
    print(f"Success: Income of Rs. {amount:,.2f} from '{source}' added.")


def add_expense(transactions):
    print("\n--- Add Expense ---")
    category = get_category("Enter expense category (e.g. Food): ")
    amount = get_amount()
    add_transaction(transactions, "Expense", category, amount)
    print(f"Success: Expense of Rs. {amount:,.2f} under '{category}' added.")


def view_transactions(transactions):
    print("\n--- All Transactions ---")
    if len(transactions) == 0:
        print("No transactions found.")
        return
    print_table(transactions)


def search_category(transactions):
    print("\n--- Search by Category ---")
    keyword = input("Enter category to search: ").strip().lower()
    if keyword == "":
        print("Error: Search text cannot be empty.")
        return

    matches = [item for item in transactions if keyword in item["category"].lower()]

    if len(matches) == 0:
        print(f"No transactions found for '{keyword}'.")
    else:
        print(f"Found {len(matches)} matching transaction(s):")
        print_table(matches)


def calculate_totals(transactions):
    total_income = 0
    total_expenses = 0
    for item in transactions:
        if item["type"] == "Income":
            total_income += item["amount"]
        elif item["type"] == "Expense":
            total_expenses += item["amount"]
    return total_income, total_expenses


def financial_summary(transactions):
    print("\n--- Financial Summary ---")
    total_income, total_expenses = calculate_totals(transactions)
    balance = total_income - total_expenses

    print(f"Total Income      : Rs. {total_income:,.2f}")
    print(f"Total Expenses    : Rs. {total_expenses:,.2f}")
    print(f"Remaining Balance : Rs. {balance:,.2f}")
    if balance < 0:
        print("Warning: You are spending more than you earn!")


def delete_transaction(transactions):
    print("\n--- Delete Transaction ---")
    if len(transactions) == 0:
        print("There are no transactions to delete.")
        return

    text = input("Enter the transaction ID to delete: ").strip()
    try:
        transaction_id = int(text)
    except ValueError:
        print("Error: Transaction ID must be a whole number.")
        return

    for item in transactions:
        if item["id"] == transaction_id:
            transactions.remove(item)
            save_data(transactions)
            print(f"Success: Transaction {transaction_id} "
                  f"({item['type']} - {item['category']}) deleted.")
            return

    print(f"Error: No transaction found with ID {transaction_id}.")


def expense_analysis(transactions):
    print("\n--- Expense Analysis ---")

    category_totals = {}
    for item in transactions:
        if item["type"] == "Expense":
            name = item["category"]
            category_totals[name] = category_totals.get(name, 0) + item["amount"]

    if len(category_totals) == 0:
        print("No expenses recorded yet.")
        return

    print("Total expenses by category:")
    for name, total in category_totals.items():
        print(f"  {name:<20} Rs. {total:,.2f}")

    top_category = max(category_totals, key=category_totals.get)
    print(f"\nHighest spending category: {top_category} "
          f"(Rs. {category_totals[top_category]:,.2f})")


# ---------------- Menu and main ----------------
def show_menu():
    print("\n" + "=" * 40)
    print("PERSONAL FINANCE & EXPENSE MANAGER")
    print()
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. Search by Category")
    print("5. Financial Summary")
    print("6. Delete Transaction")
    print("7. Expense Analysis")
    print("8. Exit")
    print("=" * 40)


def main():
    transactions = load_data()

    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_income(transactions)
        elif choice == "2":
            add_expense(transactions)
        elif choice == "3":
            view_transactions(transactions)
        elif choice == "4":
            search_category(transactions)
        elif choice == "5":
            financial_summary(transactions)
        elif choice == "6":
            delete_transaction(transactions)
        elif choice == "7":
            expense_analysis(transactions)
        elif choice == "8":
            print("\nThank you for using the Finance Manager. Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram closed. Goodbye!")