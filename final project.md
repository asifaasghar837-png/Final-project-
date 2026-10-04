# Personal Finance & Expense Management System

## Project Overview
A beginner-friendly, console-based Python application that helps a user track
income and expenses, view a financial summary, and analyse spending habits.
The whole project lives in a single file (`personal_finance_manager.py`) and
stores its data permanently in a JSON file.

## Features
- **Add Income** – source, amount (validated), date saved automatically
- **Add Expense** – category, amount (validated), date saved automatically
- **View Transactions** – ID, type, category/source, amount and date in a table
- **Search by Category** – case-insensitive search across income and expenses
- **Financial Summary** – total income, total expenses, remaining balance
- **Delete Transaction** – remove a transaction by ID with error handling
- **Expense Analysis** – totals per category and the highest-spending category
- **Permanent Storage** – auto-created `finance_data.json`, auto-saved on every change
- **Input Validation** – empty text, invalid numbers, negative/zero amounts,
  invalid menu choices, invalid IDs, and missing or corrupted JSON files

## Technologies Used
- Python 3
- Standard library only: `json`, `os`, `math`, `datetime`

## How to Install / Run
1. Install Python 3 from https://www.python.org (if not already installed).
2. Put `personal_finance_manager.py` in a folder (and optionally `finance_data.json`).
3. Open the folder in VS Code.
4. Open a terminal and run:
   ```
   python personal_finance_manager.py
   ```
   (On some systems use `python3` instead of `python`.)

No packages need to be installed (see `requirements.txt`).

## How to Use
1. Start the program – the menu appears.
2. Type a number from 1 to 8 and press Enter.
3. Follow the on-screen prompts (category, then amount).
4. Choose **8** to exit. Your data is already saved.

Menu:
```
1. Add Income          5. Financial Summary
2. Add Expense         6. Delete Transaction
3. View Transactions   7. Expense Analysis
4. Search by Category  8. Exit
```

## Data Storage
- All transactions are saved in `finance_data.json` (same folder as the script).
- The file is created automatically if it does not exist.
- If the file is corrupted, it is renamed to `finance_data.json.corrupted.bak`
  and the program starts with fresh data, so nothing is lost silently.

Each transaction looks like this:
```json
{
    "id": 1,
    "type": "Income",
    "category": "Salary",
    "amount": 50000.0,
    "date": "2026-10-03"
}
```

## Learning Outcomes
- Writing modular code with functions
- Reading and writing JSON files
- Using lists, dictionaries and loops
- Validating user input with `try/except` and `while` loops
- Handling file errors and corrupted data
- Working with dates using `datetime`
- Building a menu-driven console application

## Future Improvements
- Edit existing transactions
- Filter by date range or month
- Monthly/yearly reports and budget limits with alerts
- Export reports to CSV or Excel
- Charts for expense analysis
- Password protection and multiple user profiles
- A graphical interface (Tkinter) or web version

## Author
**Asifa Asghar**
