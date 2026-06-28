import csv
from datetime import datetime

DATABASE_FILE = "data/raw/finanze.csv"

def load_transactions(file_path):
    """Loads transactions from CSV and converts types."""
    transactions = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append({
                    "date": datetime.strptime(row['data'], "%Y-%m-%d"),
                    "description": row['descrizione'],
                    "category": row['categoria'],
                    "amount": float(row['importo'])
                })
        return transactions
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []

def save_report_to_file(expenses, income, start_date, end_date):
    """
    Generates a .txt report file with the summary of the period.
    This is the core of Option 3.
    """
    filename = f"report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.txt"
    total_expenses = sum(t['amount'] for t in expenses)
    total_income = sum(t['amount'] for t in income)
    balance = total_income + total_expenses

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"--- FINANCIAL REPORT ---\n")
            f.write(f"Period: {start_date.date()} to {end_date.date()}\n")
            f.write(f"{'-'*25}\n")
            f.write(f"Total Income:   +{total_income:.2f}€\n")
            f.write(f"Total Expenses:  {total_expenses:.2f}€\n")
            f.write(f"Final Balance:   {balance:.2f}€\n")
            f.write(f"{'-'*25}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"Success! Report saved as: {filename}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

def calculate_daily_average(transaction_list, start_date, end_date):
    """Calculates average daily spending (Option 4)."""
    # Filter only expenses (negative amounts)
    expenses_in_range = [
        t['amount'] for t in transaction_list 
        if start_date <= t['date'] <= end_date and t['amount'] < 0
    ]
    total_spent = sum(expenses_in_range)
    
    delta = end_date - start_date
    days = delta.days + 1
    
    return total_spent / days if days > 0 else 0

def show_menu():
    print("\n--- PERSONAL FINANCE MANAGER 2.0 ---")
    print("1. Add Transaction (Mockup)")
    print("2. Quick Monthly Report")
    print("3. Generate Range Report (.txt file)")
    print("4. Daily Spending Average")
    print("0. Exit")
    return input("Select an option: ")


def add_transaction(transaction_list, file_path):
    """
    Prompts the user for a new transaction and appends it to the CSV file.
    """
    print("\n--- ENTER NEW TRANSACTION ---")
    
    try:
        # 1. Collect and validate data
        date_str = input("Date (YYYY-MM-DD): ")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        description = input("Description: ")
        category = input("Category: ")
        amount = float(input("Amount (use negative for expenses): "))

        # 2. Create the dictionary for the list in memory
        new_entry = {
            "date": date_obj,
            "description": description,
            "category": category,
            "amount": amount
        }
        transaction_list.append(new_entry)

        # 3. Save to CSV using the csv module (safer than manual string writing)
        with open(file_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # We format the date back to string for the CSV
            writer.writerow([
                date_obj.strftime("%Y-%m-%d"), 
                description, 
                category, 
                amount
            ])
            
        print("Transaction saved successfully!")

    except ValueError:
        print("Error: Invalid input. Please check the date format or the amount.")







def main():
    transactions = load_transactions(DATABASE_FILE)
    if not transactions:
        return

    while True:
        choice = show_menu()

        if choice == "1":
            add_transaction(transactions,DATABASE_FILE)

        elif choice == "2":
            year = int(input("Year (YYYY): "))
            month = int(input("Month (MM): "))
            monthly = [t for t in transactions if t['date'].year == year and t['date'].month == month]
            inc = sum(t['amount'] for t in monthly if t['amount'] > 0)
            exp = sum(t['amount'] for t in monthly if t['amount'] < 0)
            print(f"\nBalance: {inc + exp:.2f}€ (Inc: +{inc}, Exp: {exp})")

        elif choice == "3":
            start_str = input("Start Date (YYYY-MM-DD): ")
            end_str = input("End Date (YYYY-MM-DD): ")
            start = datetime.strptime(start_str, "%Y-%m-%d")
            end = datetime.strptime(end_str, "%Y-%m-%d")
            
            in_range = [t for t in transactions if start <= t['date'] <= end]
            expenses = [t for t in in_range if t['amount'] < 0]
            income = [t for t in in_range if t['amount'] > 0]
            
            save_report_to_file(expenses, income, start, end)

        elif choice == "4":
            start_str = input("Start Date (YYYY-MM-DD): ")
            end_str = input("End Date (YYYY-MM-DD): ")
            start = datetime.strptime(start_str, "%Y-%m-%d")
            end = datetime.strptime(end_str, "%Y-%m-%d")
            
            avg = calculate_daily_average(transactions, start, end)
            print(f"\nYour daily average spending for this period was: {avg:.2f}€")

        elif choice == "0":
            break

if __name__ == "__main__":
    main()