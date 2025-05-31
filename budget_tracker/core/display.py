from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from core.storage import DATA_FILE
from utils import logger
import json


console = Console()

def view_summary():
    console.rule("[bold green]📊 Budget Summary")

    # Load transactions from file
    try:
        with open(DATA_FILE, "r") as f:
            transactions = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        transactions = []

    # Totals
    total_income = sum(t["amount"] for t in transactions if t.get("type") == "income")
    total_expenses = sum(t["amount"] for t in transactions if t.get("type") == "expense")
    balance = total_income - total_expenses

    # Format the output into Rich lines
    summary_text = Text()
    summary_text.append("🟢 Total Income:   ", style="green")
    summary_text.append(f"${total_income:.2f}\n")
    summary_text.append("🔴 Total Expenses: ", style="red")
    summary_text.append(f"${total_expenses:.2f}\n")
    summary_text.append("⚪ Net Balance:     ", style="bold")
    summary_text.append(f"${balance:.2f}", style="bold blue" if balance >= 0 else "bold red")

    # Display in a panel
    console.print(Panel.fit(summary_text, title="Summary", border_style="blue"))

    # Log the summary
    logger.info(f"Summary - Total Income: {total_income}, Total Expenses: {total_expenses}, Balance: {balance}")

    input("\nPress Enter to return to the main menu...")

def view_transactions():
    console.rule("[bold green]📋 Transaction History")

    # Load the transaction list
    try:
        with open(DATA_FILE, "r") as f:
            transactions = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        transactions = []

    if not transactions:
        console.print("[yellow]No transactions found.[/yellow]")
        input("\nPress Enter to return to the main menu...")
        return

    # Create a Rich table
    table = Table(title="Transactions", box=None, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Description", style="white")
    table.add_column("Type", style="bold")
    table.add_column("Category", style="cyan")
    table.add_column("Amount", style="bold", justify="right") 
    table.add_column("Timestamp", style="dim")

    # Populate the table
    for idx, t in enumerate(transactions, 1):
        emoji = "💸" if t["type"] == "expense" else "💰"

        # Format amount as string with 2 decimal places
        amount = f"${t['amount']:.2f}"
        amount_style = "red" if t["type"] == "expense" else "green"

        # Format timestamp (optional: use rich's Date or keep it simple)
        date_time = t["timestamp"].split("T")
        timestamp = f"{date_time[0]} {date_time[1][:8]}"

        table.add_row(
            str(idx),
            t["description"],
            emoji,
            t["category"],
            f"[{amount_style}]{amount}[/{amount_style}]",  # Apply Rich styling to amount
            timestamp
        )

    # log the number of transactions displayed
    logger.info(f"Displayed {len(transactions)} transactions")

    console.print(table)
    input("\nPress Enter to return to the main menu...")
