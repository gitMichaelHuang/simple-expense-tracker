from expense import Expense
import sys
import csv
import os
from collections import Counter

DATA_FILE = "data.csv"

def main():
    """
    Simple Expense Tracker v1.0 allows users to:
    1. Add expenses
    2. Import data
    3. View spending summaries organized by category
    """
    # Runs main application loop
    run_cli_user_interface()

def run_cli_user_interface():
    error_msg = ""
    while(True):
        print("\n--- SIMPLE EXPENSE TRACKER v1.0 ---")
        print("1. Add Expense")
        print("2. Import Data")
        print("3. View Summary")
        print("4. Quit Program")
        
        choice = input(f"\n{error_msg}Select Option [1-4]: ")

        if choice == '1':
            # Prompts user to enter data and creates an Expense object
            expense = get_user_expense()
            # Writes the Expense object to the data file as a new row in a csv format
            save_expense_to_file(expense, DATA_FILE)
            print(f"\nExpense entry: [{expense.name}, {expense.amount}, {expense.category}] saved successfully.")
            proceed = input("\nPress enter to return to menu")
            continue

        elif choice == '2':
            print(f"\n --- 2. Import Data: ---")
            new_data_file = input("Type in name of data file to import:\n(e.g. test-data.csv)\n")
            # Returns a list of new data added
            # Writes data from the new csv file into the primary data storage csv file
            new_data = import_new_data(new_data_file)
            if new_data is not None:
                print(f"Imported {len(new_data)} records.")
            else:
                print("Added 0 records.")
            proceed = input("\nPress enter to return to menu")
            continue

        elif choice == '3':
            error_msg = ""
            summarize_expense(DATA_FILE)
            proceed = input("\nPress enter to return to menu")
            continue

        elif choice == '4':
            print("Program closed.")
            sys.exit(0)
            
        else:
            error_msg = "**Invalid option. Please try again.**\n"

def get_user_expense():
    error_msg = ""
    print(f"\n --- 1. Add Expense: ---")
    print(f"For the expense, enter a name, cost, and category")
    print(f"(e.g. Name: Pasta, Cost: 10, Category: Food)")
    expense_name = input("\nName: ")
    expense_amount = None
    while expense_amount is None:
        try:
            expense_amount = float(input(f"{error_msg}*{expense_name}* Cost: "))
        except Exception:
            error_msg = "**Invalid input, please try again.**\n"


    expense_categories = [ "Bills", "Food", "Savings", "Services", "Other"]

    # Since index starts at 0 for enumerate
    offset = 1
    error_msg = ""

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"    {i + offset}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"


        try:
            selected_index = int(input(f"{error_msg}Enter a category number {value_range}: ")) - offset
        except Exception:
            # Error message pattern done like this so its more visible to the user
            error_msg = "**Please enter a valid number!**\n"
            continue

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            error_msg = "**Please enter a valid category!**\n"

def save_expense_to_file(expense: Expense, expense_file_path):
    # Using csv library to safely import data
    with open(expense_file_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([expense.name, expense.amount, expense.category])

def summarize_expense(expense_file_path):
    print(f"\n--- 3. View Summary: ---")
    # Read data from storage file and then conduct analysis
    # First step: reading data
    data: list[Expense] = [] 
    try:
        with open(expense_file_path, "r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3:
                    name, amount, category = row
                    data.append(Expense(name, category, float(amount)))
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Using a dictionary to create key: Categories value: Total cost in category
    amount_by_category = {}
    for expense in data:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    total_spent = sum([x.amount for x in data])
    print(f"Total expense:\n    Total: ${total_spent:.2f}")
    
    print("Total expense by category:")
    for key, amount in amount_by_category.items():
        print(f"    {key}: ${amount:.2f}")

    # Gets the biggest spend category and smallest spend category
    try:
        largest_category = max(amount_by_category, key=amount_by_category.get)
        largest_amount = amount_by_category[largest_category]
        print(f"Largest spend category:\n    {largest_category}: ${largest_amount:.2f}")
    except Exception:
        print("No spending data for largest spend category")

    try:
        smallest_category = min(amount_by_category, key=amount_by_category.get)
        smallest_amount = amount_by_category[smallest_category]
        print(f"Smallest spend category:\n    {smallest_category}: ${smallest_amount:.2f}")

    except Exception:
        print("No spending data for smallest spend category")

    # Finds the most frequent categories by entry count
    try:
        expense_names = [exp.name for exp in data]
        expense_categories = [exp.category for exp in data]
        
        name_counts = Counter(expense_names)
        category_counts = Counter(expense_categories)
        print("Expense trends:")
        most_frequent_name_item = name_counts.most_common(1)[0]
        if most_frequent_name_item[1] > 1:
            most_frequent_name = f"{most_frequent_name_item[0]} ({most_frequent_name_item[1]} times)"
        else:
            most_frequent_name = "None (No purchases recurred)"
        print(f"    Most frequent recurring purchase: {most_frequent_name}")
        most_frequent_category_item = category_counts.most_common(1)[0]
        most_frequent_category = f"{most_frequent_category_item[0]} ({most_frequent_category_item[1]} times)"
        print(f"    Most frequent expense category: {most_frequent_category}")
    except Exception:
        print("No data for analysis")

def import_new_data(new_data_file):
    if not os.path.exists(new_data_file):
        print(f"Error: File not found at path: {new_data_file}")
        return

    # Read all new data into memory first
    new_expenses = []
    try:
        with open(new_data_file, "r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3:
                    try:
                        # Validates if the "Amount" category is a number. If not, then skip row.
                        new_expenses.append([row[0], float(row[1]), row[2]])
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Error reading import file: {e}")
        return None

    if new_expenses:
        # Write using csv library, Advantange: access machine storage once
        with open(DATA_FILE, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(new_expenses)
            
    return new_expenses

if __name__ == "__main__":
    main()