#=============== Personal fitness tracker ==================================

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#File Setup -------

file_name = "expenses.csv"

#create empty file if not exist ------

try:
    df = pd.read_csv(file_name)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Notes("])
    df.to_csv(file_name, index=False)

#-------------------------
#Add new Expenses
#-------------------------

def add_expenses():
    category = input("Enter category (e.g. Food, Travel): ")
    amount = float(input("Enter amount spent: "))
    notes = input("Enter notes (optional): ")

    date = datetime.now().strftime("%Y-%m-%d")
    new_entry = pd.DataFrame([[date, category, amount, notes]],
                             columns=["Date", "Category", "Amount", "Notes"])
    df = pd.read_csv(file_name)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(file_name, index=False)
    print("Expense added successfully!")

#-------------------------
#Generate monthly report
#-------------------------

def monthly_report():
    month = int(input("Enter month number (1-12): "))
    df = pd.read_csv(file_name)
    df["Date"] = pd.to_datetime(df["Date"])  # convert strint --> datetime
    monthly_df = df[df["Date"].dt.month == month]

    if monthly_df.empty:
        print(f"No expenses found for month {month}")
        return
    
    print("\n--- Monthly Report ---")
    print("Total spent:", monthly_df["Amount"].sum())
    print("\nCategory-wise breakdown:")
    print(monthly_df.groupby("Category")["Amount"].sum())

#-------------------------
#Generate Yearly Report
#-------------------------

def yearly_report():
    year = int(input("Enter year (e.g. 2025): "))
    df = pd.read_csv(file_name)
    df["Date"] = pd.to_datetime(df["Date"])
    yearly_df = df[df["Date"].dt.year == year]

    if yearly_df.empty:
        print(f"No expenses found for year {year}")
        return
    
    print("\n--- Yearly Report ---")
    print("Total Spent:", yearly_df["Amount"].sum())
    print("\nCategory-wise breakdown:")
    print(yearly_df.groupby("Category")["Amount"].sum())
    print("\nMonthly Breakdown:")
    print(yearly_df.groupby(yearly_df["Date"].dt.month)["Amount"].sum())

#-------------------------
#Category Breakdown
#-------------------------

def category_breakdown():
    category = input("Enter category name: ")
    df = pd.read_csv(file_name)
    df["Date"] = pd.to_datetime(df["Date"])
    cat_df = df[df["Category"].str.lower() == category.lower()]

    if cat_df.empty:
        print(f"No expenses found for category '{category}'")
        return
    
    print(f"\n--- Breakdown for {category} ---")
    print(cat_df[["Date", "Amount", "Notes"]])
    print("Total spent:", cat_df["Amount"].sum())

#-------------------------
#Charts
#-------------------------

def plot_pie():
    year = int(input("Enter year: "))
    month = int(input("Enter month (1-12): "))
    df = pd.read_csv(file_name)
    df["Date"] = pd.to_datetime(df["Date"])
    monthly_df = df[(df["Date"].dt.year == year) & (df["Date"].dt.month == month)]

    if monthly_df.empty:
        print(f"No expenses to plot for {month}/{year}")
        return

    category_sum = monthly_df.groupby("Category")["Amount"].sum()
    category_sum.plot(kind="pie", autopct="%1.1f%%")
    plt.title(f"Spending Breakdown {month}/{year}")
    plt.ylabel("")
    plt.show()

def plot_trend():
    year = int(input("Enter year: "))
    month = int(input("Enter month (1-12): "))
    df = pd.read_csv(file_name)
    df["Date"] = pd.to_datetime(df["Date"])
    monthly_df = df[(df["Date"].dt.year == year) & (df["Date"].dt.month == month)]

    if monthly_df.empty:
        print(f"No expenses to plot for {month}/{year}")
        return

    daily_sum = monthly_df.groupby(monthly_df["Date"].dt.day)["Amount"].sum()
    daily_sum.plot(kind="line", marker="o")
    plt.title(f"Daily Trend {month}/{year}")
    plt.xlabel("Day")
    plt.ylabel("Amount")
    plt.grid(True)
    plt.show()

#-------------------------
#Budget Alert
#-------------------------

def check_budget():
    year = int(input("Enter year: "))
    month = int(input("Enter month (1-12): "))
    category = input("Enter category: ")
    budget_amount = float(input("Enter your budget for this category: "))

    df = pd.read_csv(file_name)
    df["Date"] = pd.to_datetime(df["Date"])
    monthly_df = df[(df["Date"].dt.year == year) & (df["Date"].dt.month == month)]
    spent = monthly_df[monthly_df["Category"].str.lower() == category.lower()]["Amount"].sum()

    print(f"\n{category} budget for {month}/{year}: {budget_amount}")
    print(f"Amount spent: {spent}")
    if spent > budget_amount:
        print("You have exceeded your budget!")
    else:
        print("You are within your budget.")

#-------------------------
#Menu System
#-------------------------
def main():
    while True:
        print("\n==============================")
        print(" Personal Expense Tracker ")
        print("==============================")
        print("1. Add new expense")
        print("2. View monthly report")
        print("3. View yearly report")
        print("4. View category breakdown")
        print("5. Plot pie chart")
        print("6. Plot trend")
        print("7. Check budget")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ")

        if choice == "1":
            add_expenses()
        elif choice == "2":
            monthly_report()
        elif choice == "3":
            yearly_report()
        elif choice == "4":
            category_breakdown()
        elif choice == "5":
            plot_pie()
        elif choice == "6":
            plot_trend()
        elif choice == "7":
            check_budget()
        elif choice == "8":
            print("Exiting... Have a great day!")
            break
        else:
            print("Invalid choice. Please try again.")

#-------------------------
#Run program
#-------------------------
if __name__ == "__main__":
    main()
