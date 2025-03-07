import csv
import datetime
import tkinter as tk
from tkinter import messagebox, ttk

CSV_FILE = "expenses.csv"

def initialize_csv():
    try:
        with open(CSV_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Type", "Balance"])
    except FileExistsError:
        pass

def get_balance():
    try:
        with open(CSV_FILE, "r") as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:
                return float(reader[-1][4])
            else:
                return 0.0
    except FileNotFoundError:
        return 0.0

def add_transaction(category, amount, trans_type):
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")
        return
    
    balance = get_balance()
    if trans_type == "expense" and amount > balance:
        messagebox.showerror("Error", "Insufficient balance!")
        return

    new_balance = balance + amount if trans_type == "income" else balance - amount
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, trans_type, new_balance])
    
    messagebox.showinfo("Success", f"Transaction added! New balance: ${new_balance:.2f}")
    update_balance_label()
    view_transactions()

def view_transactions():
    for row in tree.get_children():
        tree.delete(row)
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                tree.insert("", "end", values=row)
    except FileNotFoundError:
        pass

def monthly_summary():
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)
            expenses = {}
            for row in reader:
                date, category, amount, trans_type, _ = row
                if trans_type == "expense":
                    expenses[category] = expenses.get(category, 0) + float(amount)

            summary_text = "\nMonthly Expense Summary:\n" + "\n".join(f"{cat}: ${total:.2f}" for cat, total in expenses.items())
            messagebox.showinfo("Monthly Summary", summary_text)
    except FileNotFoundError:
        messagebox.showerror("Error", "No transactions found.")

def update_balance_label():
    balance_label.config(text=f"Current Balance: ${get_balance():.2f}")

initialize_csv()

root = tk.Tk()
root.title("E-Wallet Expense Tracker")
root.geometry("600x400")

tk.Label(root, text="E-Wallet Expense Tracker", font=("Arial", 14, "bold")).pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="Category:").grid(row=0, column=0)
category_entry = tk.Entry(frame)
category_entry.grid(row=0, column=1)

tk.Label(frame, text="Amount:").grid(row=1, column=0)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=1, column=1)

tk.Button(frame, text="Add Income", command=lambda: add_transaction("Income", amount_entry.get(), "income")).grid(row=2, column=0, pady=5)
tk.Button(frame, text="Add Expense", command=lambda: add_transaction(category_entry.get(), amount_entry.get(), "expense")).grid(row=2, column=1, pady=5)

tree = ttk.Treeview(root, columns=("Date", "Category", "Amount", "Type", "Balance"), show="headings")
for col in ("Date", "Category", "Amount", "Type", "Balance"):
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="View Transactions", command=view_transactions).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Monthly Summary", command=monthly_summary).grid(row=0, column=1, padx=5)

balance_label = tk.Label(root, text=f"Current Balance: ${get_balance():.2f}", font=("Arial", 12, "bold"))
balance_label.pack(pady=5)

update_balance_label()
view_transactions()

root.mainloop()
