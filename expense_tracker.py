#!/usr/bin/env python3
"""
Terminal-Based Expense Tracker
Track your expenses with categories, descriptions, and view summaries
"""

import json
import os
from datetime import datetime
from pathlib import Path

# File to store expenses
EXPENSE_FILE = "expenses.json"


def load_expenses():
    """Load expenses from JSON file"""
    if not os.path.exists(EXPENSE_FILE):
        return []

    try:
        with open(EXPENSE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️  Warning: expenses.json is corrupted. Starting fresh.")
        return []


def save_expenses(expenses):
    """Save expenses to JSON file"""
    with open(EXPENSE_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)


def get_next_id(expenses):
    """Get the next available ID"""
    if not expenses:
        return 1
    return max(expense['id'] for expense in expenses) + 1


def add_expense():
    """Add a new expense"""
    print("\n" + "=" * 50)
    print("ADD NEW EXPENSE")
    print("=" * 50)

    # Get amount
    while True:
        try:
            amount_str = input("\nEnter amount: $").strip()
            if not amount_str:
                print("Amount cannot be empty. Try again.")
                continue
            amount = float(amount_str)
            if amount <= 0:
                print("Amount must be positive. Try again.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number (e.g., 45.50)")

    # Get category
    while True:
        category = input("Enter category (e.g., Food, Transport): ").strip()
        if category:
            break
        print("Category cannot be empty. Try again.")

    # Get optional description
    description = input("Enter description (optional, press Enter to skip): ").strip()

    # Create expense entry
    expenses = load_expenses()
    expense = {
        "id": get_next_id(expenses),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": round(amount, 2),
        "category": category,
        "description": description if description else ""
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("\n✓ Expense added successfully!")
    print(f"  ID: {expense['id']}")
    print(f"  Date: {expense['date']}")
    print(f"  Amount: ${expense['amount']:.2f}")
    print(f"  Category: {expense['category']}")
    if expense['description']:
        print(f"  Description: {expense['description']}")


def view_expenses():
    """View all expenses in a formatted table"""
    expenses = load_expenses()

    if not expenses:
        print("\n📭 No expenses recorded yet!")
        return

    print("\n" + "=" * 80)
    print("ALL EXPENSES")
    print("=" * 80)
    print(f"{'ID':<5} {'Date':<12} {'Amount':<12} {'Category':<15} {'Description':<30}")
    print("-" * 80)

    for expense in expenses:
        print(f"{expense['id']:<5} "
              f"{expense['date']:<12} "
              f"${expense['amount']:<11.2f} "
              f"{expense['category']:<15} "
              f"{expense['description']:<30}")

    print("-" * 80)
    print(f"Total expenses: {len(expenses)}")


def view_summary():
    """View spending summary with total and breakdown by category"""
    expenses = load_expenses()

    if not expenses:
        print("\n📭 No expenses recorded yet!")
        return

    # Calculate totals
    total = sum(expense['amount'] for expense in expenses)

    # Calculate by category
    by_category = {}
    for expense in expenses:
        category = expense['category']
        by_category[category] = by_category.get(category, 0) + expense['amount']

    # Display summary
    print("\n" + "=" * 60)
    print("SPENDING SUMMARY")
    print("=" * 60)
    print(f"\n💰 Total Spending: ${total:.2f}")
    print(f"📊 Total Entries: {len(expenses)}")

    print("\n📁 Breakdown by Category:")
    print("-" * 60)
    print(f"{'Category':<20} {'Amount':<15} {'Percentage':<10}")
    print("-" * 60)

    for category in sorted(by_category.keys()):
        amount = by_category[category]
        percentage = (amount / total) * 100
        print(f"{category:<20} ${amount:<14.2f} {percentage:>5.1f}%")

    print("-" * 60)


def edit_expense():
    """Edit an existing expense"""
    expenses = load_expenses()

    if not expenses:
        print("\n📭 No expenses to edit!")
        return

    # Show all expenses first
    view_expenses()

    # Get expense ID to edit
    while True:
        try:
            expense_id = input("\nEnter expense ID to edit (or 'c' to cancel): ").strip()
            if expense_id.lower() == 'c':
                return
            expense_id = int(expense_id)
            break
        except ValueError:
            print("Invalid ID. Please enter a number.")

    # Find expense
    expense = None
    for exp in expenses:
        if exp['id'] == expense_id:
            expense = exp
            break

    if not expense:
        print(f"❌ Expense with ID {expense_id} not found!")
        return

    # Show current values and get new ones
    print(f"\n📝 Editing expense ID {expense_id}")
    print(f"Current: ${expense['amount']:.2f} | {expense['category']} | {expense['description']}")

    # New amount
    new_amount = input(f"\nNew amount (current: ${expense['amount']:.2f}, press Enter to keep): ").strip()
    if new_amount:
        try:
            expense['amount'] = round(float(new_amount), 2)
        except ValueError:
            print("Invalid amount. Keeping original.")

    # New category
    new_category = input(f"New category (current: {expense['category']}, press Enter to keep): ").strip()
    if new_category:
        expense['category'] = new_category

    # New description
    new_description = input(f"New description (current: '{expense['description']}', press Enter to keep): ").strip()
    if new_description:
        expense['description'] = new_description

    save_expenses(expenses)
    print("\n✓ Expense updated successfully!")


def delete_expense():
    """Delete an expense"""
    expenses = load_expenses()

    if not expenses:
        print("\n📭 No expenses to delete!")
        return

    # Show all expenses first
    view_expenses()

    # Get expense ID to delete
    while True:
        try:
            expense_id = input("\nEnter expense ID to delete (or 'c' to cancel): ").strip()
            if expense_id.lower() == 'c':
                return
            expense_id = int(expense_id)
            break
        except ValueError:
            print("Invalid ID. Please enter a number.")

    # Find and remove expense
    original_count = len(expenses)
    expenses = [exp for exp in expenses if exp['id'] != expense_id]

    if len(expenses) == original_count:
        print(f"❌ Expense with ID {expense_id} not found!")
    else:
        save_expenses(expenses)
        print(f"\n✓ Expense ID {expense_id} deleted successfully!")


def show_menu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("💸 EXPENSE TRACKER")
    print("=" * 50)
    print("\n[1] Add Expense")
    print("[2] View All Expenses")
    print("[3] View Summary")
    print("[4] Edit Expense")
    print("[5] Delete Expense")
    print("[6] Exit")
    print("\n" + "=" * 50)


def main():
    """Main program loop"""
    print("\n🎯 Welcome to Expense Tracker!")

    while True:
        show_menu()
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            view_summary()
        elif choice == '4':
            edit_expense()
        elif choice == '5':
            delete_expense()
        elif choice == '6':
            print("\n👋 Thank you for using Expense Tracker. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number between 1 and 6.")

        # Pause before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
