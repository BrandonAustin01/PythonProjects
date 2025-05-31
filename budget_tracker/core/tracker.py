from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from datetime import datetime
from core.storage import DATA_FILE
from utils import logger
import json

console = Console()

def add_expense():
    console.rule("[bold green]➕ Add New Expense")

    # Ask the user for a description of the expense
    description = Prompt.ask("Enter a description", default="Unknown expense")

    # Ask the user for the amount and validate it's a number
    while True:
        try:
            amount_str = Prompt.ask("Enter the amount (e.g. 23.50)")
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            break
        except ValueError as e:
            console.print(f"[red]Invalid input[/red]: {e}")
            logger.error(f"Invalid expense amount: {e}")

    # Ask for a category (user-defined or generic)
    category = Prompt.ask("Enter category (e.g. food, rent, misc)", default="uncategorized")

    # Get the current timestamp
    timestamp = datetime.now().isoformat()

    # Create a dictionary representing the transaction
    transaction = {
        "type": "expense",
        "description": description,
        "amount": amount,
        "category": category,
        "timestamp": timestamp
    }

    # Load existing transactions from the JSON file
    try:
        with open(DATA_FILE, "r") as f:
            transactions = json.load(f)
    except json.JSONDecodeError:
        transactions = []

    # Append the new transaction to the list
    transactions.append(transaction)

    # Save the updated transaction list back to the file
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=4)

    # Display success message using Rich
    console.print(Panel.fit(
        f"[bold green]Expense added![/bold green]\n\n"
        f"💬 [cyan]Description:[/cyan] {description}\n"
        f"💰 [cyan]Amount:[/cyan] ${amount:.2f}\n"
        f"📂 [cyan]Category:[/cyan] {category}\n"
        f"🕒 [cyan]Timestamp:[/cyan] {timestamp}",
        title="Success",
        border_style="green"
    ))

    logger.info(f"Added expense: {description}, Amount: {amount}, Category: {category}")

    input("\nPress Enter to return to the main menu...")

def add_income():
    console.rule("[bold green]➕ Add New Income")

    # Ask the user for a description of the income source
    description = Prompt.ask("Enter a description", default="Unknown income")

    # Ask the user for the amount and validate it's a positive number
    while True:
        try:
            amount_str = Prompt.ask("Enter the amount (e.g. 300.00)")
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            break
        except ValueError as e:
            console.print(f"[red]Invalid input[/red]: {e}")
            logger.error(f"Invalid income amount: {e}")

    # Ask for a category (e.g. salary, freelance, gift)
    category = Prompt.ask("Enter category (e.g. salary, gift, bonus)", default="uncategorized")

    # Timestamp when income is added
    timestamp = datetime.now().isoformat()

    # Create the income transaction dictionary
    transaction = {
        "type": "income",
        "description": description,
        "amount": amount,
        "category": category,
        "timestamp": timestamp
    }

    # Load existing transactions from file
    try:
        with open(DATA_FILE, "r") as f:
            transactions = json.load(f)
    except json.JSONDecodeError:
        transactions = []

    # Add new transaction and save
    transactions.append(transaction)
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=4)

    # Success message
    console.print(Panel.fit(
        f"[bold green]Income added![/bold green]\n\n"
        f"💬 [cyan]Source:[/cyan] {description}\n"
        f"💰 [cyan]Amount:[/cyan] ${amount:.2f}\n"
        f"📂 [cyan]Category:[/cyan] {category}\n"
        f"🕒 [cyan]Timestamp:[/cyan] {timestamp}",
        title="Success",
        border_style="cyan"
    ))

    logger.info(f"Added income: {description}, Amount: {amount}, Category: {category}")

    input("\nPress Enter to return to the main menu...")

# core/tracker.py

from core.storage import load_data, save_data
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table

console = Console()

def remove_expense():
    console.rule("[bold red]➖ Remove Expense")

    # Load all transactions
    transactions = load_data()

    # Create a list of indexes for expenses (track actual index in original list)
    expenses = [(i, t) for i, t in enumerate(transactions) if t.get("type") == "expense"]

    if not expenses:
        console.print("[yellow]No expenses found to remove.[/yellow]")
        input("\nPress Enter to return to the main menu...")
        return

    # Display expenses in a table
    table = Table(title="Expenses", box=None, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Description", style="white")
    table.add_column("Amount", style="bold", justify="right")
    table.add_column("Category", style="cyan")
    table.add_column("Timestamp", style="dim")

    for display_index, (_, expense) in enumerate(expenses, 1):
        table.add_row(
            str(display_index),
            expense["description"],
            f"[red]${expense['amount']:.2f}[/red]",
            expense["category"],
            expense["timestamp"].split("T")[0] + " " + expense["timestamp"].split("T")[1][:8]
        )

    console.print(table)

    # Ask user which expense to remove
    while True:
        try:
            choice = int(Prompt.ask("Enter the number of the expense to remove (0 to cancel)"))
            if choice == 0:
                console.print("[yellow]Operation cancelled.[/yellow]")
                return
            if 1 <= choice <= len(expenses):
                break
            else:
                console.print("[red]Invalid number. Please choose from the list.[/red]")
        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]")

    # Get actual index and transaction object from original list
    real_index, removed_expense = expenses[choice - 1]

    # Remove from original transaction list by index
    del transactions[real_index]

    # Save updated data
    save_data(transactions)

    # Show success message
    console.print(Panel.fit(
        f"[bold red]Expense removed successfully![/bold red]\n\n"
        f"💬 [cyan]Description:[/cyan] {removed_expense['description']}\n"
        f"💰 [cyan]Amount:[/cyan] ${removed_expense['amount']:.2f}\n"
        f"📂 [cyan]Category:[/cyan] {removed_expense['category']}\n"
        f"🕒 [cyan]Timestamp:[/cyan] {removed_expense['timestamp']}",
        title="Removed",
        border_style="red"
    ))

    logger.info(f"Removed expense: {removed_expense['description']}, Amount: {removed_expense['amount']}, Category: {removed_expense['category']}")

    input("\nPress Enter to return to the main menu...")
