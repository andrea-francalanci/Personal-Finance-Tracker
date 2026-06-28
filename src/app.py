import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Updated path according to the new project structure
DATABASE_PATH = "data/raw/finanze.csv"

st.set_page_config(page_title="Personal Finance Tracker", layout="centered")

st.title("📊 Personal Finance Manager 3.0")
st.write("Welcome to your interactive personal finance dashboard.")

# Secure data loading
try:
    df = pd.read_csv(DATABASE_PATH, parse_dates=['data'])
    st.success("Database loaded successfully!")
    
   

    st.sidebar.title("Navigation")
    choice = st.sidebar.radio(
        "Select an Option:",
        ["Overview & Recent Transactions", "Monthly Report", "Date Range Analysis", "Category Statistics"]
    )
    if choice == "Overview & Recent Transactions":
        st.subheader("Recent Transactions")
        st.dataframe(df, use_container_width=True)

    # ----------------------------------------------------
    # OPTION 1: Monthly Report & Visualization
    # ----------------------------------------------------
    elif choice == "Monthly Report":
        st.subheader("📅 Monthly Expenses Analysis")
        
        # Get unique available months from data to avoid typos
        available_months = df['data'].dt.strftime('%Y-%m').unique()
        selected_month = st.selectbox("Select Year and Month:", sorted(available_months, reverse=True))
        
        # Filter data by month
        monthly_data = df[df['data'].dt.strftime('%Y-%m') == selected_month]
        
        if monthly_data.empty:
            st.warning(f"No data found for: {selected_month}")
        else:
            # Isolate expenses (negative amounts)
            only_expenses = monthly_data[monthly_data['importo'] < 0]
            
            if only_expenses.empty:
                st.info("No expenses found for this month.")
            else:
                super_total = only_expenses['importo'].abs().sum()
                
                # Display metric card
                st.metric(label="Total Expenses This Month", value=f"{super_total:.2f} €")
                
                # Calculations
                category_expenses = only_expenses.groupby('categoria')['importo'].sum().abs()
                category_percentage = (category_expenses / super_total) * 100
                
                # Layout layout with 2 columns: Table on left, Chart on right
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("### Spending Breakdown (%)")
                    st.dataframe(category_percentage.rename("Percentage (%)"), use_container_width=True)
                
                with col2:
                    st.write("### Expense Distribution Chart")
                    fig, ax = plt.subplots()
                    category_percentage.plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax)
                    ax.set_ylabel('')  # Remove standard pandas ylabel
                    st.pyplot(fig)

    # ----------------------------------------------------
    # OPTION 2: Date Range Analysis
    # ----------------------------------------------------
    elif choice == "Date Range Analysis":
        st.subheader("🔍 Date Range Analysis")
        
        # Date pickers widget (much safer than text input!)
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", df['data'].min())
        with col2:
            end_date = st.date_input("End Date", df['data'].max())
            
        if start_date > end_date:
            st.error("Error: Start Date must be before End Date.")
        else:
            # Filter by range
            range_data = df[df['data'].between(pd.to_datetime(start_date), pd.to_datetime(end_date))]
            
            if range_data.empty:
                st.warning("No data found in this range.")
            else:
                # Calculations
                expense_period = range_data[range_data['importo'] < 0]['importo'].abs().sum()
                income_period = range_data[range_data['importo'] > 0]['importo'].sum()
                total_balance = range_data['importo'].sum()
                
                # Display metrics side by side
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Income", f"+{income_period:.2f} €")
                m2.metric("Total Expenses", f"-{expense_period:.2f} €")
                m3.metric("Net Balance", f"{total_balance:.2f} €", delta=f"{total_balance:.2f} €")
                
                # Visualization
                fig, ax = plt.subplots()
                plot_data = pd.Series([expense_period, income_period], index=['Expenses', 'Income'])
                plot_data.plot(kind='bar', color=['#ff4b4b', '#009688'], ax=ax)
                plt.xticks(rotation=0)
                plt.ylabel("Amount (€)")
                
                st.pyplot(fig)
                
                st.write("### Transactions in this Period")
                st.dataframe(range_data, use_container_width=True)

    # ----------------------------------------------------
    # OPTION 3: Category Statistics
    # ----------------------------------------------------
    elif choice == "Category Statistics":
        st.subheader("📊 Global Category Statistics")
        only_expenses = df[df['importo'] < 0]
        
        if not only_expenses.empty:
            category_distribution = only_expenses.groupby('categoria')['importo'].sum().abs()
            
            fig, ax = plt.subplots()
            category_distribution.sort_values().plot(kind='barh', color='#262730', ax=ax)
            plt.xlabel("Total Amount Spent (€)")
            plt.ylabel("Category")
            
            st.pyplot(fig)
        else:
            st.info("No expenses found to calculate stats.")

            
except FileNotFoundError:
    st.error(f"Error: Database file not found at {DATABASE_PATH}. Please check the path!")