from tkinter import messagebox
import sqlite3
from customtkinter import *
from yahoo_fin import stock_info
import getpass
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


global symbol_entry 
# Your database and functions for managing users SQL

def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            income REAL,
            debts REAL,
            assets REAL
        )
    ''')
    conn.commit()
    conn.close()


def check_login(username, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(username, email, password, income, debts, assets):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, password, income, debts, assets) VALUES (?, ?, ?, ?, ?, ?)', (username, email, password, income, debts, assets))
    conn.commit()
    conn.close()

def create_user(username, email, password, income, debts, assets):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        messagebox.showerror("Error", "Username already exists. Choose a different username.")
    else:
        register_user(username, email, password, income, debts, assets)
        messagebox.showinfo("Registration Successful", "User {} registered successfully.".format(username))

    conn.close()

# Your GUI functions

def login():
    for widget in root.winfo_children():
        widget.destroy()

    name_label = CTkLabel(root, text="Enter your name:")
    name_label.pack(pady=10)

    name_entry = CTkEntry(root)
    name_entry.pack(pady=10)

    password_label = CTkLabel(root, text="Enter your Password:")
    password_label.pack(pady=10)

    password_entry = CTkEntry(root, show = '*')
    password_entry.pack(pady=10)

    submit_button = CTkButton(root, text="Submit", command=lambda: authenticate(name_entry.get(), password_entry.get()))
    submit_button.pack(pady=20)
    btn_exit = CTkButton(root, text="Exit", command=root.destroy)
    btn_exit.pack()

def authenticate(username, password):
    user = check_login(username, password)

    if user:
        nextPhase()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def addInfo():
    root.geometry("1000x800")
    for widget in root.winfo_children():
        widget.destroy()

    # Ask for basic personal information
    name_label = CTkLabel(root, text="Enter your name:")
    name_label.pack(pady=10)

    name_entry = CTkEntry(root)
    name_entry.pack(pady=10)

    email_label = CTkLabel(root, text="Enter your email:")
    email_label.pack(pady=10)

    email_entry = CTkEntry(root)
    email_entry.pack(pady=10)

    password_label = CTkLabel(root, text="Enter your password:")
    password_label.pack(pady=10)

    password_entry = CTkEntry(root, show = "*")
    password_entry.pack(pady=10)

    # Ask for financial information
    income_label = CTkLabel(root, text="Enter your income:")
    income_label.pack(pady=10)

    income_entry = CTkEntry(root)
    income_entry.pack(pady=10)

    debts_label = CTkLabel(root, text="Enter your debts:")
    debts_label.pack(pady=10)

    debts_entry = CTkEntry(root)
    debts_entry.pack(pady=10)

    assets_label = CTkLabel(root, text="Enter your assets:")
    assets_label.pack(pady=10)

    assets_entry = CTkEntry(root)
    assets_entry.pack(pady=10)

    submit_button = CTkButton(root, text="Submit", command=lambda: print_info(name_entry.get(), email_entry.get(), password_entry.get(), income_entry.get(), debts_entry.get(), assets_entry.get()))
    submit_button.pack(pady=20)

    btn_exit = CTkButton(root, text="Exit", command=root.destroy)
    btn_exit.pack()


def print_info(name, email, password, income, debts, assets):
    create_user(name, email, password, income,debts,assets)
    for widget in root.winfo_children():
        widget.destroy()
    print("Name:", name)
    print("Email:", email)
    print("Password:", password)
    print("Income:", income)
    print("Debts:", debts)
    print("Assets:", assets)
    mainmenu()

def mainmenu():
    root.geometry("1000x500")
    for widget in root.winfo_children():
        widget.destroy()

    btn_login = CTkButton(root, text="Login", command=login)
    btn_login.pack(pady=20)

    btn_add_info = CTkButton(root, text="Create User", command=addInfo)
    btn_add_info.pack(pady=20)

    btn_exit = CTkButton(root, text="Exit", command=root.destroy)
    btn_exit.pack()

def stock_performance():
    for widget in root.winfo_children():
        widget.destroy()

    symbol_label = CTkLabel(root, text="Enter Stock Symbol:")
    symbol_label.pack(pady=10)

    symbol_entry = CTkEntry(root)
    symbol_entry.pack(pady=10)

    plot_button = CTkButton(root, text="Plot Stock Performance", command=lambda: plot_stock_performance(symbol_entry.get()))
    plot_button.pack(pady=20)

    btn_exit = CTkButton(root, text="Exit", command=root.destroy)
    btn_exit.pack()

def compound_interest_calculator():
    for widget in root.winfo_children():
        widget.destroy()

    principal_label = CTkLabel(root, text="Enter Principal Amount:")
    principal_label.pack(pady=10)

    principal_entry = CTkEntry(root)
    principal_entry.pack(pady=10)

    rate_label = CTkLabel(root, text="Enter Annual Interest Rate (%):")
    rate_label.pack(pady=10)

    rate_entry = CTkEntry(root)
    rate_entry.pack(pady=10)

    time_label = CTkLabel(root, text="Enter Time Period (years):")
    time_label.pack(pady=10)

    time_entry = CTkEntry(root)
    time_entry.pack(pady=10)

    result_label = CTkLabel(root, text="")
    result_label.pack(pady=20)

    calculate_button = CTkButton(root, text="Calculate Compound Interest", command=lambda: calculate_compound_interest(principal_entry.get(), rate_entry.get(), time_entry.get(), result_label))
    calculate_button.pack(pady=20)

    btn_exit = CTkButton(root, text="Exit", command=root.destroy)
    btn_exit.pack()

def calculate_compound_interest(principal, rate, time, result_label):
    try:
        principal = float(principal)
        rate = float(rate) / 100  # Convert percentage to decimal
        time = float(time)

        compound_interest = principal * (1 + rate)**time - principal

        result_label.configure(text=f"Compound Interest: ${compound_interest:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values for Principal, Rate, and Time.")


def mortgage_calculator():
    for widget in root.winfo_children():
        widget.destroy()

    principal_label = CTkLabel(root, text="Enter Loan Amount:")
    principal_label.pack(pady=10)

    principal_entry = CTkEntry(root)
    principal_entry.pack(pady=10)

    interest_label = CTkLabel(root, text="Enter Annual Interest Rate (%):")
    interest_label.pack(pady=10)

    interest_entry = CTkEntry(root)
    interest_entry.pack(pady=10)

    years_label = CTkLabel(root, text="Enter Loan Term (years):")
    years_label.pack(pady=10)

    years_entry = CTkEntry(root)
    years_entry.pack(pady=10)

    result_label = CTkLabel(root, text="")
    result_label.pack(pady=20)

    calculate_button = CTkButton(root, text="Calculate Mortgage", command=lambda: calculate_mortgage(principal_entry.get(), interest_entry.get(), years_entry.get(), result_label))
    calculate_button.pack(pady=20)

    btn_exit = CTkButton(root, text="Exit", command=root.destroy)
    btn_exit.pack()

def calculate_mortgage(loan_amount, interest_rate, loan_term, result_label):
    try:
        loan_amount = float(loan_amount)
        interest_rate = float(interest_rate) / 100  # Convert percentage to decimal
        loan_term = int(loan_term)

        monthly_interest_rate = interest_rate / 12
        total_payments = loan_term * 12

        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**(-total_payments))

        result_label.configure(text=f"Monthly Payment: ${monthly_payment:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values for Loan Amount, Interest Rate, and Loan Term.")

# ...
def tax_calculator():
    for widget in root.winfo_children():
        widget.destroy()

    income_label = CTkLabel(root, text="Enter Annual Income:")
    income_label.pack(pady=10)

    income_entry = CTkEntry(root)
    income_entry.pack(pady=10)

    result_label = CTkLabel(root, text="")
    result_label.pack(pady=20)

    calculate_button = CTkButton(root, text="Calculate Tax", command=lambda: australian_tax_calculator(income_entry.get(), result_label))
    calculate_button.pack(pady=20)

    btn_exit = CTkButton(root, text="Exit", command=root.destroy)
    btn_exit.pack()
# ...

# Add this function for the Australian Tax Calculator
def australian_tax_calculator(annual_income, result_label):
    try:
        annual_income = float(annual_income)

        # Australian tax brackets and rates for the financial year 2022-2023
        tax_brackets = [18200, 45000, 120000, 180000]
        tax_rates = [0.19, 0.325, 0.37, 0.45]

        tax_amount = 0

        for i in range(len(tax_brackets)):
            if annual_income > tax_brackets[i]:
                if i == len(tax_brackets) - 1:
                    # Last bracket
                    tax_amount += (annual_income - tax_brackets[i]) * tax_rates[i]
                else:
                    tax_amount += (tax_brackets[i + 1] - tax_brackets[i]) * tax_rates[i]

        result_label.configure(text=f"Australian Tax Amount: ${tax_amount:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numerical value for Annual Income.")

# ...

# Update the nextPhase function
def nextPhase():
    for widget in root.winfo_children():
        widget.destroy()

    btn_stock_performance = CTkButton(root, text="Check Stock Performance", command=stock_performance)
    btn_stock_performance.pack(pady=20)

    btn_compound_interest = CTkButton(root, text="Compound Interest Calculator", command=compound_interest_calculator)
    btn_compound_interest.pack(pady=20)

    btn_mortgage_calculator = CTkButton(root, text="Mortgage Calculator", command=mortgage_calculator)
    btn_mortgage_calculator.pack(pady=20)

    btn_australian_tax_calculator = CTkButton(root, text="Australian Tax Calculator", command=tax_calculator)
    btn_australian_tax_calculator.pack(pady=20)

# ...

def plot_stock_performance(stock_name):
    stock_data = yf.Ticker(stock_name).history(period="max")

    # Create a matplotlib figure
    fig, ax = plt.subplots()
    ax.plot(stock_data.index, stock_data["Close"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title(f"{stock_name} Stock Performance")

    # Embed the figure in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(pady=20)

    # Update the tkinter main loop
    root.update_idletasks()
    root.update()

# Update the on_plot_button_click function
def on_plot_button_click():
    symbol = symbol_entry.get()

    if symbol:
        plot_stock_performance(symbol)

# Update the on_plot_button_click function
def on_plot_button_click():
    symbol = symbol_entry.get()

    if symbol:
        canvas = FigureCanvasTkAgg(master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=20)
        canvas.draw()
    
# Your custom Tkinter initialization

root = CTk()
root.title('DECASH FINANCE')
root.geometry("1000x500")

# Run the create_table function to ensure the users table exists
create_table()

# Start the main menu
mainmenu()

root.mainloop()
