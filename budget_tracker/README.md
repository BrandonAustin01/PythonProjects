# 💸 Budget Tracker

A terminal-based budget tracker built with Python and Rich. Easily track your income and expenses, view summaries, and manage your finances—all from the command line.

---

## 📦 Features

- ✅ Add Expenses and Income
- 📊 View Total Summary (Income, Expenses, Balance)
- 📋 Display all Transactions in a Styled Table
- 💾 JSON-based Persistent Storage
- 🎨 Rich-powered terminal interface
- 🧱 Modular Codebase (core/, data/)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/BrandonAustin01/budget_tracker.git
cd budget_tracker
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
python main.py
```

---

## 📁 Project Structure

```
budget_tracker/
├── main.py                # Entry point
├── core/
│   ├── tracker.py         # Add income/expense logic
│   ├── display.py         # View summary and table
│   └── storage.py         # Load/save JSON data
├── data/
│   └── transactions.json  # Your transaction history
├── logs/
│   └── chronilog.log      # Optional logging output
├── requirements.txt
└── README.md
```

---

## 📝 Planned Enhancements

- 🔐 Transaction editing and deletion
- 📅 Monthly and category-based filters
- 📤 CSV export
- 📈 Budget limit warnings and suggestions

---

## 🧑‍💻 Author

Brandon McKinney  
Built with Python 3.13, Chronilog, and Rich
