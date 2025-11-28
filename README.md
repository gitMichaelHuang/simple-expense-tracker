# Simple Expense Tracker v1.0

A CLI application for tracking personal expenses with category-based summaries.

## Features
- Add individual expenses with pre-defined categories: "Bills", "Food", "Savings", "Services", "Other"
- Import CSV data
- View spending summaries and trends

## Design Approach
### 1. Object-Oriented Programming
The application separates data modeling from application logic. The `Expense` class acts as the data transfer object. This provides strict structure for all records passed between the CLI and the file storage.

### 2. Anticipates Ugly Data
I utilized Python's built-in `csv` library rather than manual string manipulation. This provides data integrity even when user inputs contain special characters (like commas), preventing file corruption.

### 3. I/O Performance Consideration
For the **Import Data** feature, I implemented a batch-write strategy. The application buffers valid records in memory and writes them in a single operation (O(1) file operation).

### 4. Persistence
The application features error-handling using try-except blocks.

## Key Files
- `expense_tracker.py` - Main application with CLI interface
- `expense.py` - Expense class definition
- `data.csv` - Primary data storage
- `seed-data.csv` - Pretty data for testing general function, 10 entries
- `test-data.csv` - Ugly data for testing edge cases, 25 entries

## Run
1. Ensure Python 3.x is installed
2. Clone this repository
3. Run: `python expense_tracker.py`

## Use and Test
1. Type "1" and press "Enter" to enter a new expense. You will be prompted with:
   \n-Name
   \n-Amount
   \n-Category (that you will select from a list).
3. Type "2" and press "Enter" to load pre-existing data. There are two files provided: "seed-data.csv" (pretty data, 10 entries) and "test-data.csv" (ugly data, 25 entries).
4. Data stays persist in "data.csv". To remove data, you must manually delete the contents of the file.
5. Type "3" and press "Enter" to see generated summary of the expense data:
    \n-The total expense
    \n-Total expense by category
    \n-Highest and lowest spend category
    \n-Trends: Most frequent category and most frequency recurring purchase

