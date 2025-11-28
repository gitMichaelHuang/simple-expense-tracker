# Simple Expense Tracker v1.0

A CLI application for tracking personal expenses with category-based summaries.

## Features
- Add individual expenses with pre-defined categories: Bills, Food, Savings, Services, Other.
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
1. **Add Expense** - Type "1" and enter:
   - Name
   - Amount
   - Category (select from list)

2. **Import Data** - Type "2" to load:
   - `seed-data.csv` (10 clean entries)
   - `test-data.csv` (25 entries with edge cases)

3. **Data Persistence** - All data stored in `data.csv`. Manually delete file contents to reset.

4. **View Summary** - Type "3" to see:
   - Total expenses
   - Spending by category
   - Highest/lowest spend categories
   - Trends: recurring purchases and frequent categories

