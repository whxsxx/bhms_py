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



def get_total_room_price():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pybh_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(room_price) FROM tenants")
        result = cursor.fetchone()
        total_room_price = result[0] if result[0] is not None else 0
        conn.close()
        return total_room_price
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error fetching  data: {err}")
        return []

def get_total_tenants():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pybh_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tenants")
        result = cursor.fetchone()
        total_tenants = result[0] if result[0] is not None else 0
        conn.close()
        return total_tenants
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error fetching  data: {err}")
        return []

def get_total_rooms():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pybh_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM rooms")
        result = cursor.fetchone()
        total_rooms = result[0] if result[0] is not None else 0
        conn.close()
        return total_rooms
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error fetching  data: {err}")
        return []

def update_labels():
    total_room_price = get_total_room_price()
    total_tenants = get_total_tenants()
    total_rooms = get_total_rooms()
    numRevenue_label.config(text=str(total_room_price))
    numTenants_label.config(text=str(total_tenants))
    numRoom_label.config(text=str(total_rooms))

def get_room_status():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pybh_db"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT rooms.room_number, COUNT(tenants.tenant_id) as tenant_count
            FROM rooms
            LEFT JOIN tenants ON rooms.room_number = tenants.room_number
            GROUP BY rooms.room_number
        """)
        result = cursor.fetchall()
        room_status = []
        for room_number, tenant_count in result:
            status = "Room is full / 5 person" if tenant_count >= 5 else "Room is not full yet" + " / " + str(tenant_count) + " person"
            room_status.append((room_number, status))
        conn.close()
        return room_status
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

def update_room_details():
    room_status = get_room_status()
    for item in roomDetails.get_children():
        roomDetails.delete(item)
    for room_number, status in room_status:
        roomDetails.insert("", "end", values=(room_number, status))

def refreshData():
    update_room_details()
    update_labels()




class DashboardFrame(ttk.Frame):
    def __init__(self, parent,show_index_frame,show_tenants_frame,show_room_frame,show_expense_frame):
        super().__init__(parent, width=900, height=800)
        self.pack_propagate(False);
        
        
        title_label = ttk.Label(self, text="DASHBOARD", foreground="white", font=("",30,'bold'))
        title_label.grid(row=0, column=0, padx=70, pady=(50,20))

        numRoom_frame = ttk.LabelFrame(self, text="NO. OF ROOMS", width=350, height=150)
        numRoom_frame.grid(column=0, row=1, padx=100, pady=(50,10))
        global numRoom_label
        numRoom_label = ttk.Label(numRoom_frame, text="100",font=("100",20,'bold'))
        numRoom_label.pack(pady=(30,10), padx=(200,40))

        
        numTenants_frame = ttk.LabelFrame(self, text="NO. OF TENANTS", width=350, height=150)
        numTenants_frame.grid(column=1, row=1, padx=100, pady=(50,10))

        global numTenants_label
        numTenants_label = ttk.Label(numTenants_frame, text="",font=("100",20,'bold'))
        numTenants_label.pack(pady=(30,10), padx=(200,40))


        numRevenue_frame = ttk.LabelFrame(self, text="TOTAL REVENUE", width=350, height=150)
        numRevenue_frame.grid(column=2, row=1, padx=100, pady=(50,10))

        global numRevenue_label
        numRevenue_label = ttk.Label(numRevenue_frame, text="",font=("",20,'bold'))
        numRevenue_label.pack(pady=(30,10), padx=(100,40))
        
        update_labels()


        tenantBtn = ttk.Button(self,text="Manage Rooms",width=30,command=show_room_frame)
        tenantBtn.grid(column=0,row=2,padx=100, pady=(20,10))

        roomBtn = ttk.Button(self,text="Manage Tenants",width=30,command=show_tenants_frame)
        roomBtn.grid(column=1,row=2,padx=100, pady=(20,10))

        expenseBtn = ttk.Button(self,text="Manage Expense",width=30,command=show_expense_frame)
        expenseBtn.grid(column=2,row=2,padx=100, pady=(20,10))

        global roomDetails
        columns = ("room_number", "room_status")
        roomDetails = ttk.Treeview(self, columns=columns, show="headings", height=15)

        for col in columns:
            roomDetails.column(col, width=600)


        roomDetails.heading("room_number", text="ROOM NUMBER")
        roomDetails.heading("room_status", text="ROOM STATUS")

        roomDetails.grid(row=3, column=0, columnspan=8, padx=50, pady=(30, 10))
        update_room_details()


        logout_btn = ttk.Button(self,text="Refresh",width=34, bootstyle=DARK,command=refreshData)
        logout_btn.grid(row=4,column=0,pady=10)

        logout_btn = ttk.Button(self,text="LOG OUT",width=34, bootstyle=DARK,command=show_index_frame)
        logout_btn.grid(row=4,column=2,pady=10)

