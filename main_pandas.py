import pandas as pd
import matplotlib.pyplot as plt

DATABASE_PATH = "finanze.csv"

def show_menu():
    """Displays the menu for the Pandas version."""
    print("\n--- PERSONAL FINANCE MANAGER 3.0 (Pandas Edition) ---")
    print("1. Monthly Report & Visualization")
    print("2. Date Range Analysis")
    print("3. Category Statistics")
    print("0. Exit")
    return input("Select an option: ")

def get_category_totals(filtered_df):
    """Returns the sum of amounts grouped by category."""
    return filtered_df.groupby('categoria')['importo'].sum()

def filter_by_month(finance_df, month_year_str):
    """Filters data using a string like 'YYYY-MM'."""
    return finance_df[finance_df['data'].dt.strftime('%Y-%m') == month_year_str]

def filter_by_range(finance_df, start_date, end_date):
    """Filters data between two dates."""
    return finance_df[finance_df['data'].between(start_date, end_date)]

def main():
    # Load data with automatic date parsing
    try:
        finance_df = pd.read_csv(DATABASE_PATH, parse_dates=['data'])
    except FileNotFoundError:
        print(f"Error: {DATABASE_PATH} not found.")
        return

    while True:
        choice = show_menu()

        if choice == "1":
            month_year = input("Enter Year and Month (YYYY-MM): ")
            monthly_data = filter_by_month(finance_df, month_year)
            
            if monthly_data.empty:
                print(f"No data found for: {month_year}")
            else:
                totals = get_category_totals(monthly_data)
                print("\nTotals by Category:")
                print(totals)
                
                # Visualizing the data
                totals.plot(kind='bar', title=f"Expenses/Income for {month_year}", color='skyblue')
                plt.ylabel("Amount (€)")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()

        elif choice == "2":
            start = input("Start Date (YYYY-MM-DD): ")
            end = input("End Date (YYYY-MM-DD): ")
            range_data = filter_by_range(finance_df, start, end)
            
            if range_data.empty:
                print("No data found in this range.")
            else:
                print(f"\nReport from {start} to {end}:")
                print(range_data)
                print(f"\nTotal Balance: {range_data['importo'].sum():.2f}€")

        elif choice == "3":
            # Advanced stats: Percentage of spending by category
            only_expenses = finance_df[finance_df['importo'] < 0]
            if not only_expenses.empty:
                category_distribution = only_expenses.groupby('categoria')['importo'].sum().abs()
                print("\nSpending Distribution:")
                print(category_distribution)
            else:
                print("No expenses found for statistics.")

        elif choice == "0":
            print("Exiting Pandas Edition... Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()