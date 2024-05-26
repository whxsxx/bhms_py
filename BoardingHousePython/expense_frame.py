import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import mysql.connector
from tkinter import messagebox

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", 
    database="pybh_db"
)
cursor = conn.cursor()

def expense_on_tree_select(event):
    selected_item = expensetree.selection()
    if selected_item:
        values = expensetree.item(selected_item)['values']

        clear_expense_entry_widgets()

        expense_id_entry.insert(0, values[0])
        expenseName_entry.insert(0, values[1])
        expenseAmount_entry.insert(0, values[2])
        expenseDate_entry.insert(0, values[3])

def fetch_expense_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
            database="pybh_db"
        )
        cursor = conn.cursor()

        query = """
        SELECT * FROM expense
        """
        cursor.execute(query)
        expense_data = cursor.fetchall()

        return expense_data

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error fetching expense data: {err}")
        return []

def populate_expense_treeview():
    clear_expense_entry_widgets()
    expense_data = fetch_expense_data()
    for row in expensetree.get_children():
        expensetree.delete(row)
    for row in expense_data:
        expensetree.insert("", "end", values=row)
    pass



def manage_expenses(action):
    try:
        if action == "insert":
            expense_name = expenseName_entry.get()
            expense_date = expenseDate_entry.get()
            expense_amount = expenseAmount_entry.get()

            cursor.execute("INSERT INTO expense (expense_name, expense_date, expense_amount) VALUES (%s, %s, %s)",
                        (expense_name, expense_date, expense_amount))

            # Commit changes
            conn.commit()
            messagebox.showinfo("Success", "Expense created successfully")

        elif action == "update":
            expense_id = expense_id_entry.get()

            expense_name = expenseName_entry.get()
            expense_date = expenseDate_entry.get()
            expense_amount = expenseAmount_entry.get()

            cursor.execute("UPDATE expense SET expense_name=%s, expense_date=%s, expense_amount=%s WHERE expense_id=%s",
                        (expense_name, expense_date, expense_amount, expense_id))

            conn.commit()
            messagebox.showinfo("Success", "Expense updated successfully")

        elif action == "delete":
            if messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?"):
                expense_id = expense_id_entry.get()

                cursor.execute("DELETE FROM expense WHERE expense_id=%s", (expense_id,))

                conn.commit()
                messagebox.showinfo("Success", "Expense deleted successfully")

        populate_expense_treeview()
        clear_expense_entry_widgets()
    except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database error: {err}")

    

def clear_expense_entry_widgets():
    expense_id_entry.delete(0, tk.END)
    expenseName_entry.delete(0, tk.END)
    expenseDate_entry.delete(0, tk.END)
    expenseAmount_entry.delete(0, tk.END)


class ExpenseFrame(ttk.Frame):
    def __init__(self, parent,show_dashboard_frame):
        super().__init__(parent, width=1000, height=800)
        self.pack_propagate(False)

        title_label = ttk.Label(self, text="EXPENSES", foreground="white", font=("", 30, 'bold'))
        title_label.pack(side="top", anchor="nw", padx=(35, 10), pady=(20, 5))

        expense_frame = ttk.Frame(self)
        expense_frame.pack(side="left", fill="both", expand=True, padx=40, pady=(20, 5))

        expense_form = ttk.LabelFrame(expense_frame, text="EXPENSE DETAILS", width=150, height=40)
        expense_form.pack(pady=(0,10))


        expense_form.pack(fill=tk.BOTH, expand=True)

        global expense_id_entry
        expense_id_label = ttk.Label(expense_form, text="#")
        expense_id_label.pack(padx=20, pady=(30, 20))

        expense_id_entry = ttk.Entry(expense_form)
        expense_id_entry.pack(padx=20, pady=20)

        expenseName_label = ttk.Label(expense_form, text="Expense name")
        expenseName_label.pack(padx=20, pady=20)

        global expenseName_entry
        expenseName_entry = ttk.Entry(expense_form)
        expenseName_entry.pack(padx=20, pady=20)

        expenseDate_label = ttk.Label(expense_form, text="Date (YYYY-MM-DD)")
        expenseDate_label.pack(padx=20, pady=20)

        global expenseDate_entry
        expenseDate_entry = ttk.Entry(expense_form)
        expenseDate_entry.pack(padx=20, pady=20)

        expenseAmount_label = ttk.Label(expense_form, text="Expense Amount")
        expenseAmount_label.pack(padx=20, pady=20)

        global expenseAmount_entry
        expenseAmount_entry = ttk.Entry(expense_form)
        expenseAmount_entry.pack(padx=20, pady=(5, 20))





        buttons = ttk.Frame(expense_frame)
        buttons.pack(pady=10)

        add_button = ttk.Button(buttons, text="Create",width=20, command=lambda: manage_expenses("insert"))
        add_button.pack(padx=20, pady=(15,5))

        buttons1 = ttk.Frame(expense_frame)
        buttons1.pack(pady=(10,20))

        upd_button = ttk.Button(buttons1, text="Update",width=20, command=lambda: manage_expenses("update"))
        upd_button.grid(column=0,row=0,padx=10)

        del_button = ttk.Button(buttons1, text="Delete",width=20, command=lambda: manage_expenses("delete"))
        del_button.grid(column=1,row=0,padx=10)

        expenseTable_frame = ttk.Frame(self)
        expenseTable_frame.pack(side="right", fill="both", expand=True, padx=40, pady=(20, 20))

        global expensetree
        columns = ("expense_id","expense_name", "expense_amount","expense_date")
        expensetree = ttk.Treeview(expenseTable_frame, columns=columns, show="headings", height=33)

        for col in columns:
            expensetree.column(col, width=250)

        expensetree.heading("expense_id", text="#")
        expensetree.heading("expense_name", text="Description")
        expensetree.heading("expense_amount", text="Amount")
        expensetree.heading("expense_date", text="Date")
        
        expensetree.grid(row=10, column=0, columnspan=8, padx=(50, 10), pady=10)
        populate_expense_treeview()
        expensetree.bind("<ButtonRelease-1>", expense_on_tree_select)


        refresh_btn = ttk.Button(expenseTable_frame,text="Refresh",width=20,command=populate_expense_treeview)
        refresh_btn.grid(row=11, column=0,padx=100, pady=(10,5))

        back_btn = ttk.Button(expenseTable_frame,text="Back",width=20,command=show_dashboard_frame)
        back_btn.grid(row=11, column=1,padx=100, pady=(10,5))