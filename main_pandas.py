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
                totals_expanses = monthly_data[monthly_data['importo'] < 0]
                Super_Total = totals_expanses['importo'].abs().sum()
                print(Super_Total)
                category_expanses = totals_expanses.groupby('categoria')['importo'].sum().abs()
                #calculate all the category percentage
                category_percentage = (category_expanses/Super_Total)*100

                print("\nTotals by Category:")
                print(category_percentage)
                
                # Visualizing the data
                category_percentage.plot(kind='pie',autopct='%1.1f%%',startangle=140)
                plt.title(f"Expenses_Percentage for {month_year}", pad=30)
                plt.ylabel('')       
                plt.axis('equal')
                plt.tight_layout()    
                plt.show()

        elif choice == "2":
            start = input("Start Date (YYYY-MM-DD): ")
            end = input("End Date (YYYY-MM-DD): ")
            range_data = filter_by_range(finance_df, start, end)
            
            if range_data.empty:
                print("No data found in this range.")
            else:
                expense_period = range_data[range_data['importo'] < 0]
                expense_period =expense_period['importo'].abs().sum()
                income_period = range_data[range_data['importo'] > 0]
                income_period = income_period['importo'].sum()

                #Data Visualization
                plot_data = pd.Series(
                [expense_period, income_period], 
                index=['Income', 'Expense']
                )
                plot_data.plot(kind='bar', color=['green', 'red'])

                
                plt.title(f"Income vs. Expense Comparison between({start} - {end})", pad=20)
                plt.ylabel("amount (€)")
                plt.xticks(rotation=0) # 
                plt.tight_layout()
                plt.show()
                #print report
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