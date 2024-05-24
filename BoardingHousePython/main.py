import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import mysql.connector

##FRAMES##
from index_frame import IndexFrame
from dashboard_frame import DashboardFrame
from tenants_frame import TenantsFrame
from room_frame import RoomFrame
from expense_frame import ExpenseFrame

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pybh_db"
    )
    mycursor = mydb.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Error connecting to database: {err}")
    exit(1)

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        self.geometry("800x500")

        self.index_frame = IndexFrame(self, self.user_login)
        self.dashboard_frame = DashboardFrame(self, self.show_index_frame, self.show_tenants_frame,self.show_room_frame,self.show_expense_frame)
        self.tenants_frame = TenantsFrame(self,self.show_dashboard_frame)
        self.room_frame = RoomFrame(self,self.show_dashboard_frame)
        self.expense_frame = ExpenseFrame(self,self.show_dashboard_frame)

        self.show_index_frame()

    def user_login(self):
        username = self.index_frame.get_username()
        password = self.index_frame.get_password()

        mycursor.execute("SELECT * FROM account WHERE username = %s AND password = %s", (username, password))
        result = mycursor.fetchone()

        if result:
            messagebox.showinfo("", "Login Successful!")
            self.show_dashboard_frame()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def show_index_frame(self):
        self.dashboard_frame.pack_forget()
        self.expense_frame.pack_forget()
        self.room_frame.pack_forget()
        self.tenants_frame.pack_forget()

        self.title("Boarding House Monitoring Log in")
        
        self.geometry("800x500")
        self.index_frame.pack(expand=True, fill=tk.BOTH)

    def show_dashboard_frame(self):
        self.index_frame.pack_forget()
        self.tenants_frame.pack_forget()
        self.expense_frame.pack_forget()
        self.room_frame.pack_forget()
        self.title("Dashboard")
        self.geometry("1400x800")
        self.dashboard_frame.pack(expand=True, fill=tk.BOTH)

    def show_tenants_frame(self):
        self.index_frame.pack_forget()
        self.dashboard_frame.pack_forget()
        self.expense_frame.pack_forget()
        self.room_frame.pack_forget()
        self.title("Manage Tenants")
        self.geometry("1700x1000")
        self.tenants_frame.pack(expand=True, fill=tk.BOTH)

    def show_room_frame(self):
        self.index_frame.pack_forget()
        self.tenants_frame.pack_forget()
        self.expense_frame.pack_forget()
        self.dashboard_frame.pack_forget()
        self.title("Manage Room")
        self.geometry("1700x900")
        self.room_frame.pack(expand=True, fill=tk.BOTH)


    def show_expense_frame(self):
        self.index_frame.pack_forget()
        self.dashboard_frame.pack_forget()
        self.room_frame.pack_forget()
        self.tenants_frame.pack_forget()
        self.title("Manage Expense")
        self.geometry("1700x900")
        self.expense_frame.pack(expand=True, fill=tk.BOTH)

if __name__ == "__main__":
    app = App()
    app.mainloop()
