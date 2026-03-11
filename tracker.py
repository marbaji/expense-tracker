#!/usr/bin/env python3
"""
Simple Expense Tracker with Rich Formatting
Just run: python3 tracker.py
"""

import json
import sys
import csv
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt
from rich import box
from rich.text import Text

EXPENSE_FILE = "expenses.json"
BUDGET_FILE = "budgets.json"
console = Console()

# Budget thresholds
BUDGET_WARNING_THRESHOLD = 80  # Yellow warning at 80%
BUDGET_OVER_THRESHOLD = 100    # Red alert at 100%

# Color mapping for categories
CATEGORY_COLORS = {
    "food": "bright_yellow",
    "transport": "bright_blue",
    "coffee": "cyan",
    "entertainment": "magenta",
    "shopping": "bright_magenta",
    "utilities": "blue",
    "health": "green",
    "education": "bright_green",
    "rent": "red",
    "groceries": "yellow",
    "other": "white"
}

def get_category_color(category):
    """Get color for a category"""
    return CATEGORY_COLORS.get(category.lower(), "white")


def parse_amount(prompt_text):
    """Parse amount with flexible input ($, commas, spaces)"""
    while True:
        try:
            amount_str = Prompt.ask(prompt_text)
            amount_str = amount_str.strip().replace('$', '').replace(',', '')
            amount = float(amount_str)
            if amount <= 0:
                console.print("[red]❌ Amount must be positive![/red]")
                continue
            return amount
        except ValueError:
            console.print("[red]❌ Please enter a valid number[/red]")


def load_expenses():
    """Load expenses from JSON file"""
    try:
        with open(EXPENSE_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_budgets():
    """Load budgets from JSON file with validation"""
    try:
        with open(BUDGET_FILE, 'r') as f:
            budgets = json.load(f)
            # Validate and normalize: only keep valid positive numbers
            # Normalize keys to lowercase for case-insensitive matching
            validated = {}
            for category, amount in budgets.items():
                if isinstance(amount, (int, float)) and amount > 0:
                    validated[category.lower()] = amount
            return validated
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_budgets(budgets):
    """Save budgets to JSON file"""
    with open(BUDGET_FILE, 'w') as f:
        json.dump(budgets, f, indent=2)


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
    """Add expense with simple prompts"""
    console.print("\n[bold cyan]💸 Add New Expense[/bold cyan]")
    console.print("[dim]" + "─" * 50 + "[/dim]")

    # Get amount using helper function
    amount = parse_amount("\n[yellow]Amount[/yellow] ($)")

    # Get category
    category = Prompt.ask("[green]Category[/green] (e.g., Food, Transport)").strip()
    if not category:
        category = "Other"

    # Get optional description
    description = Prompt.ask("[blue]Description[/blue] (optional)", default="")

    # Save expense
    expenses = load_expenses()
    expense = {
        "id": get_next_id(expenses),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": round(amount, 2),
        "category": category,
        "description": description
    }

    expenses.append(expense)
    save_expenses(expenses)

    # Success message
    success_text = f"✓ Expense saved!\n  ${expense['amount']:.2f} - {expense['category']}"
    if expense['description']:
        success_text += f"\n  ({expense['description']})"

    console.print(f"\n[bold green]{success_text}[/bold green]")


def view_expenses():
    """View all expenses in a beautiful table"""
    expenses = load_expenses()

    if not expenses:
        console.print("\n[yellow]📭 No expenses yet![/yellow]")
        return

    table = Table(
        title="[bold cyan]💰 All Expenses[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )

    table.add_column("ID", justify="right")
    table.add_column("Date")
    table.add_column("Amount", justify="right")
    table.add_column("Category")
    table.add_column("Description")

    for expense in expenses:
        # Get color based on category
        color = get_category_color(expense['category'])

        table.add_row(
            f"[{color}]{expense['id']}[/{color}]",
            f"[{color}]{expense['date']}[/{color}]",
            f"[{color}]${expense['amount']:.2f}[/{color}]",
            f"[bold {color}]{expense['category']}[/bold {color}]",
            f"[{color}]{expense['description']}[/{color}]"
        )

    console.print("\n")
    console.print(table)
    console.print(f"\n[dim]Total expenses: {len(expenses)}[/dim]")


def set_budget():
    """Set monthly budget for a category"""
    console.print("\n[bold cyan]💰 Set Category Budget[/bold cyan]")
    console.print("[dim]" + "─" * 50 + "[/dim]")

    budgets = load_budgets()

    # Show existing budgets
    if budgets:
        console.print("\n[dim]Current budgets:[/dim]")
        for cat, amt in budgets.items():
            console.print(f"  [cyan]{cat.capitalize()}[/cyan]: ${amt:.2f}/month")

    # Get category with validation
    category = Prompt.ask("\n[green]Category[/green]").strip()
    if not category:
        console.print("[red]❌ Category required![/red]")
        return

    # Normalize category to lowercase for consistent matching
    category_key = category.lower()

    # Get budget amount (allow 0 or empty to delete)
    amount_str = Prompt.ask(
        f"[yellow]Monthly budget for {category}[/yellow] ($, 0 to delete)"
    ).strip()

    # Handle deletion
    if amount_str == '0' or not amount_str:
        if category_key in budgets:
            del budgets[category_key]
            save_budgets(budgets)
            console.print(f"\n[bold yellow]✓ Budget removed for {category}[/bold yellow]")
        else:
            console.print(f"\n[yellow]No budget set for {category}[/yellow]")
        return

    # Parse and validate amount
    try:
        amount_str = amount_str.replace('$', '').replace(',', '')
        amount = float(amount_str)
        if amount <= 0:
            console.print("[red]❌ Budget must be positive! Use 0 to delete.[/red]")
            return
    except ValueError:
        console.print("[red]❌ Please enter a valid number[/red]")
        return

    # Save budget with normalized key
    budgets[category_key] = amount
    save_budgets(budgets)

    console.print(f"\n[bold green]✓ Budget set: {category} = ${amount:.2f}/month[/bold green]")


def show_summary():
    """Show spending summary with rich formatting"""
    expenses = load_expenses()

    if not expenses:
        console.print("\n[yellow]📭 No expenses yet![/yellow]")
        return

    total = sum(expense['amount'] for expense in expenses)
    budgets = load_budgets()

    # By category - normalize to handle case variations
    by_category = {}
    category_name_map = {}  # Maps lowercase to first occurrence's original name

    for expense in expenses:
        category_key = expense['category'].lower()

        if category_key not in category_name_map:
            # First time seeing this category (case-insensitive)
            category_name_map[category_key] = expense['category']
            by_category[expense['category']] = expense['amount']
        else:
            # Add to existing category
            original_name = category_name_map[category_key]
            by_category[original_name] += expense['amount']

    # Create summary panel
    summary_text = f"[bold yellow]💰 Total:[/bold yellow] [bold green]${total:.2f}[/bold green]\n"
    summary_text += f"[bold cyan]📊 Entries:[/bold cyan] {len(expenses)}"

    console.print("\n")
    console.print(Panel(summary_text, title="[bold]Spending Summary[/bold]", border_style="cyan"))

    # Create category table
    table = Table(
        title="[bold]📁 Breakdown by Category[/bold]",
        box=box.SIMPLE,
        show_header=True,
        header_style="bold cyan"
    )

    table.add_column("Category", justify="left")
    table.add_column("Spent", justify="right")
    table.add_column("Budget", justify="right")
    table.add_column("Status", justify="right")

    for category in sorted(by_category.keys()):
        amount = by_category[category]
        color = get_category_color(category)
        # Use lowercase for budget lookup to handle case-insensitive matching
        budget = budgets.get(category.lower())

        if budget:
            percentage = (amount / budget) * 100
            # Use threshold constants
            if percentage >= BUDGET_OVER_THRESHOLD:
                status = f"[red]⚠️  {percentage:.0f}% (OVER!)[/red]"
            elif percentage >= BUDGET_WARNING_THRESHOLD:
                status = f"[yellow]⚠️  {percentage:.0f}%[/yellow]"
            else:
                status = f"[green]✓ {percentage:.0f}%[/green]"

            table.add_row(
                f"[bold {color}]{category}[/bold {color}]",
                f"[{color}]${amount:.2f}[/{color}]",
                f"[dim]${budget:.2f}[/dim]",
                status
            )
        else:
            percentage = (amount / total) * 100
            table.add_row(
                f"[bold {color}]{category}[/bold {color}]",
                f"[{color}]${amount:.2f}[/{color}]",
                f"[dim]No budget[/dim]",
                f"[dim]{percentage:.1f}% of total[/dim]"
            )

    console.print("\n")
    console.print(table)


def search_expenses(keyword):
    """Search expenses by category or description keyword"""
    expenses = load_expenses()

    if not expenses:
        console.print("\n[yellow]📭 No expenses yet![/yellow]")
        return

    keyword_lower = keyword.lower()

    # Search in both category and description
    results = [
        exp for exp in expenses
        if keyword_lower in exp['category'].lower() or
           keyword_lower in exp['description'].lower()
    ]

    if not results:
        console.print(f"\n[yellow]🔍 No expenses found matching '{keyword}'[/yellow]")
        return

    # Calculate total for search results
    total = sum(exp['amount'] for exp in results)

    # Create results table
    table = Table(
        title=f"[bold cyan]🔍 Search Results: '{keyword}'[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )

    table.add_column("ID", justify="right")
    table.add_column("Date")
    table.add_column("Amount", justify="right")
    table.add_column("Category")
    table.add_column("Description")

    for expense in results:
        # Get color based on category
        color = get_category_color(expense['category'])

        table.add_row(
            f"[{color}]{expense['id']}[/{color}]",
            f"[{color}]{expense['date']}[/{color}]",
            f"[{color}]${expense['amount']:.2f}[/{color}]",
            f"[bold {color}]{expense['category']}[/bold {color}]",
            f"[{color}]{expense['description']}[/{color}]"
        )

    console.print("\n")
    console.print(table)
    console.print(f"\n[bold]Found:[/bold] [cyan]{len(results)}[/cyan] expenses | [bold]Total:[/bold] [green]${total:.2f}[/green]")


def export_to_csv():
    """Export current month's expenses to CSV"""
    expenses = load_expenses()

    if not expenses:
        console.print("\n[yellow]📭 No expenses to export![/yellow]")
        return

    # Get current year and month
    now = datetime.now()
    current_month = now.strftime("%Y-%m")

    # Filter expenses for current month
    month_expenses = [
        exp for exp in expenses
        if exp['date'].startswith(current_month)
    ]

    if not month_expenses:
        console.print(f"\n[yellow]📭 No expenses found for {now.strftime('%B %Y')}[/yellow]")
        return

    # Generate filename
    filename = f"expenses_{current_month}.csv"

    # Write to CSV
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Date', 'Amount', 'Category', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for exp in month_expenses:
            writer.writerow({
                'ID': exp['id'],
                'Date': exp['date'],
                'Amount': f"${exp['amount']:.2f}",
                'Category': exp['category'],
                'Description': exp['description']
            })

    # Calculate total
    total = sum(exp['amount'] for exp in month_expenses)

    export_text = f"[bold green]✓[/bold green] Exported [cyan]{len(month_expenses)}[/cyan] expenses to [yellow]{filename}[/yellow]\n"
    export_text += f"  Month: [blue]{now.strftime('%B %Y')}[/blue]\n"
    export_text += f"  Total: [green]${total:.2f}[/green]"

    console.print(f"\n{export_text}")


def delete_expense(expense_id):
    """Delete an expense by ID"""
    expenses = load_expenses()
    original_count = len(expenses)
    expenses = [exp for exp in expenses if exp['id'] != expense_id]

    if len(expenses) == original_count:
        console.print(f"\n[red]❌ Expense ID {expense_id} not found![/red]")
    else:
        save_expenses(expenses)
        console.print(f"\n[bold green]✓ Deleted expense ID {expense_id}[/bold green]")


def show_help():
    """Show usage help with rich formatting"""
    help_text = """
[bold cyan]ADD EXPENSE[/bold cyan] (default):
  [yellow]python3 tracker.py[/yellow]
  Just run it and answer the prompts!

[bold cyan]VIEW ALL EXPENSES:[/bold cyan]
  [yellow]python3 tracker.py view[/yellow]

[bold cyan]SHOW SUMMARY:[/bold cyan]
  [yellow]python3 tracker.py summary[/yellow]
  Shows spending vs budgets with warnings!

[bold cyan]SET BUDGET:[/bold cyan]
  [yellow]python3 tracker.py budget[/yellow]
  Set monthly budget limits for categories
  Enter 0 to delete a budget

[bold cyan]SEARCH EXPENSES:[/bold cyan]
  [yellow]python3 tracker.py search <keyword>[/yellow]
  Example: [dim]python3 tracker.py search Food[/dim]
  Example: [dim]python3 tracker.py search lunch[/dim]

  Searches in both category and description!

[bold cyan]EXPORT TO CSV:[/bold cyan]
  [yellow]python3 tracker.py export[/yellow]
  Exports current month's expenses to CSV file

[bold cyan]DELETE EXPENSE:[/bold cyan]
  [yellow]python3 tracker.py delete <ID>[/yellow]
  Example: [dim]python3 tracker.py delete 5[/dim]

[bold cyan]HELP:[/bold cyan]
  [yellow]python3 tracker.py help[/yellow]
"""

    console.print(Panel(
        help_text,
        title="[bold magenta]💸 EXPENSE TRACKER - Quick Reference[/bold magenta]",
        border_style="cyan",
        box=box.DOUBLE
    ))


def main():
    """Main entry point"""
    # Check for command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'view':
            view_expenses()
        elif command == 'summary':
            show_summary()
        elif command == 'budget':
            set_budget()
        elif command == 'search' and len(sys.argv) > 2:
            keyword = ' '.join(sys.argv[2:])  # Join all words after 'search'
            search_expenses(keyword)
        elif command == 'export':
            export_to_csv()
        elif command == 'delete' and len(sys.argv) > 2:
            try:
                expense_id = int(sys.argv[2])
                delete_expense(expense_id)
            except ValueError:
                console.print("[red]❌ Invalid ID. Use: python3 tracker.py delete <ID>[/red]")
        elif command == 'help':
            show_help()
        else:
            console.print(f"[red]❌ Unknown command: {command}[/red]")
            console.print("[yellow]Run: python3 tracker.py help[/yellow]")
    else:
        # Default: add expense
        add_expense()


if __name__ == "__main__":
    main()
