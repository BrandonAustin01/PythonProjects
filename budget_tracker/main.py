from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from core.tracker import add_expense, add_income
from core.display import view_summary, view_transactions
from pathlib import Path

# Initialize the logger
from utils import logger

# Initialize Rich console instance
console = Console()

# Path to JSON file where transactions will be stored
DATA_FILE = Path("data/transactions.json")

# Ensure the data file exists
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
if not DATA_FILE.exists():
    DATA_FILE.write_text("[]")  # Start with empty list if not found

def show_main_menu():
    console.clear()
    console.rule("[bold green]💸 Budget Tracker")
    console.print(Panel.fit(
        """[bold cyan][1][/bold cyan] Add Expense
[bold cyan][2][/bold cyan] Add Income
[bold cyan][3][/bold cyan] View Summary
[bold cyan][4][/bold cyan] View Transactions
[bold cyan][5][/bold cyan] Exit""",
        title="[green]Main Menu",
        border_style="green"
    ))

    logger.info("[Run] Displayed main menu")

def main():
    while True:
        show_main_menu()
        choice = Prompt.ask("\n[bold white]Choose an option", choices=["1", "2", "3", "4", "5"])

        if choice == "1":
            console.clear()
            add_expense()
        elif choice == "2":
            console.clear()
            add_income()
        elif choice == "3":
            console.clear()
            view_summary()
        elif choice == "4":
            console.clear()
            view_transactions()
        elif choice == "5":
            console.clear()
            console.print("[bold red]Goodbye![/bold red]")
            break

if __name__ == "__main__":
    main()