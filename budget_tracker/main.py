from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from core.tracker import add_expense, add_income, remove_expense
from core.display import view_summary, view_transactions
from pathlib import Path
from utils import logger, version

# Initialize Rich console instance
console = Console()

def show_main_menu():
    console.clear()
    console.rule(f"[bold green]💸 Budget Tracker v{version}")
    console.print(Panel.fit("""
    [bold cyan][1][/bold cyan] Add Expense
    [bold cyan][2][/bold cyan] Add Income
    [bold cyan][3][/bold cyan] Remove Expense
    [bold cyan][4][/bold cyan] View Summary
    [bold cyan][5][/bold cyan] View Transactions
    [bold cyan][6][/bold cyan] Exit""",
        title="[green]Main Menu",
        border_style="green"
    ))

    logger.info("[Run] Displayed main menu")

def main():
    while True:
        show_main_menu()
        choice = Prompt.ask("\n[bold white]Choose an option", choices=["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            console.clear()
            add_expense()
            logger.info("[Run] User chose to add an expense")
        elif choice == "2":
            console.clear()
            add_income()
            logger.info("[Run] User chose to add income")
        elif choice == "3":
            console.clear()
            remove_expense()
            logger.info("[Run] User chose to remove an expense")
        elif choice == "4":
            console.clear()
            view_summary()
            logger.info("[Run] User chose to view summary")
        elif choice == "5":
            console.clear()
            view_transactions()
            logger.info("[Run] User chose to view transactions")
        elif choice == "6":
            console.clear()
            console.print("[bold red]Goodbye![/bold red]")
            logger.info("[Run] User chose to exit the application")
            break



if __name__ == "__main__":
    main()