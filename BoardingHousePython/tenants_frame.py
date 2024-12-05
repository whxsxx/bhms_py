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

def fetch_rooms():
    cursor = conn.cursor()
    cursor.execute("SELECT room_number, room_price FROM rooms")
    rooms = cursor.fetchall()
    conn.close()
    return rooms

def populate_comboboxes():
    rooms = fetch_rooms()
    print(rooms)
    room_numbers = [room[0] for room in rooms]
    room_prices = [room[1] for room in rooms]

    roomNum_entry['values'] = room_numbers
    roomPrice_entry['values'] = room_prices

    global room_data, price_data
    room_data = {room[0]: room[1] for room in rooms}
    price_data = {room[1]: room[0] for room in rooms}

    if room_numbers:
        roomNum_entry.set(room_numbers[0])
        roomPrice_entry.set(room_data[room_numbers[0]])

def update_room_price(event):
    selected_room_number = roomNum_entry.get()
    if selected_room_number in room_data:
        roomPrice_entry.set(room_data[selected_room_number])

def update_room_number(event):
    selected_room_price = float(roomPrice_entry.get())
    if selected_room_price in price_data:
        roomNum_entry.set(price_data[selected_room_price])


def manage_tenants(action):
    try:   
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
            database="pybh_db"
            )
        cursor = conn.cursor()
        if action == "insert":
            first_name = firstname_entry.get()
            last_name = lastname_entry.get()
            address = address_entry.get()
            date = date_entry.get()
            due = due_entry.get()
            room_number = roomNum_entry.get()
            room_price = roomPrice_entry.get()

            # Check the current number of tenants in the specified room
            cursor.execute("SELECT COUNT(*) FROM tenants WHERE room_number = %s", (room_number,))
            tenant_count = cursor.fetchone()[0]

            if tenant_count >= 5:
                messagebox.showerror("Error", "Cannot add more than 5 tenants to a room")
                return

            cursor.execute("INSERT INTO tenants (first_name, last_name, address, date, due, room_number, room_price) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (first_name, last_name, address, date, due, room_number, room_price))


            conn.commit()
            messagebox.showinfo("Success", "Tenant created successfully")

        elif action == "update":
            tenant_id = tenants_id_entry.get()
            first_name = firstname_entry.get()
            last_name = lastname_entry.get()
            address = address_entry.get()
            date = date_entry.get()
            due = due_entry.get()
            room_number = roomNum_entry.get()
            room_price = roomPrice_entry.get()

            cursor.execute("UPDATE tenants SET first_name=%s, last_name=%s, address=%s, date=%s, due=%s, room_number=%s, room_price=%s WHERE tenant_id=%s",
                        (first_name, last_name, address, date, due, room_number, room_price, tenant_id))

            conn.commit()
            messagebox.showinfo("Success", "Tenant updated successfully")

        elif action == "delete":
            if messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?"):
                tenant_id = tenants_id_entry.get()


                cursor.execute("DELETE FROM tenants WHERE tenant_id=%s", (tenant_id,))

                
                conn.commit()
                messagebox.showinfo("Success", "Tenant deleted successfully")

        clear_entry_widgets()
        populate_tenants_treeview()
    except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")

    


def clear_entry_widgets():
    tenants_id_entry.delete(0, 'end')
    firstname_entry.delete(0, 'end')
    lastname_entry.delete(0, 'end')
    address_entry.delete(0, 'end')
    date_entry.delete(0, 'end')
    due_entry.delete(0, 'end')
    roomNum_entry.delete(0, 'end')
    roomPrice_entry.delete(0, 'end')


def tenants_on_tree_select(event):
    selected_item = tenantsTree.selection()
    if selected_item:
        values = tenantsTree.item(selected_item)['values']
        clear_entry_widgets()
        tenants_id_entry.insert(0, values[0])
        firstname_entry.insert(0, values[1])
        lastname_entry.insert(0, values[2])
        address_entry.insert(0, values[3])
        date_entry.insert(0, values[4])
        due_entry.insert(0, values[5])
        roomNum_entry.set(values[6])
        roomPrice_entry.set(values[7])




def fetch_tenants_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
            database="pybh_db"
        )
        cursor = conn.cursor()
        query = """
        SELECT * FROM tenants
        """
        cursor.execute(query)
        tenants_data = cursor.fetchall()

        return tenants_data

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error fetching tenants data: {err}")
        return []

def populate_tenants_treeview():
    
    clear_entry_widgets()
    tenants_data = fetch_tenants_data()
    for row in tenantsTree.get_children():
        tenantsTree.delete(row)
    for row in tenants_data:
        tenantsTree.insert("", "end", values=row)
    pass



class TenantsFrame(ttk.Frame):
    def __init__(self, parent,show_dashboard_frame):
        super().__init__(parent)


        self.config(width=1700, height=900)
        self.pack_propagate(False)

        title_label = ttk.Label(self, text="TENANTS", foreground="white", font=("", 30, 'bold'))
        title_label.pack(side="top", anchor="nw", padx=(35, 10), pady=(20, 5))

        tenant_frame = ttk.Frame(self)
        tenant_frame.pack(side="left", fill="both", expand=True, padx=40, pady=(20, 5))

        tenant_form = ttk.LabelFrame(tenant_frame, text="TENANT INFORMATION", width=100, height=500)
        tenant_form.pack(pady=(0,10))


        tenant_form.pack(fill=tk.BOTH, expand=True)

        global tenants_id_entry
        tenants_id_label = ttk.Label(tenant_form, text="#")
        tenants_id_label.pack(padx=20, pady=(15, 5))

        tenants_id_entry = ttk.Entry(tenant_form)
        tenants_id_entry.pack(padx=20, pady=5)

        global firstname_entry
        firstname_label = ttk.Label(tenant_form, text="Firstname")
        firstname_label.pack(padx=20, pady=5)

        firstname_entry = ttk.Entry(tenant_form)
        firstname_entry.pack(padx=20, pady=5)

        global lastname_entry
        lastname_label = ttk.Label(tenant_form, text="Lastname")
        lastname_label.pack(padx=20, pady=5)

        lastname_entry = ttk.Entry(tenant_form)
        lastname_entry.pack(padx=20, pady=5)

        global address_entry
        address_label = ttk.Label(tenant_form, text="Address")
        address_label.pack(padx=20, pady=5)

        address_entry = ttk.Entry(tenant_form)
        address_entry.pack(padx=20, pady=5)

        global date_entry
        date_label = ttk.Label(tenant_form, text="Date (YYYY-MM-DD)")
        date_label.pack(padx=20, pady=5)

        date_entry = ttk.Entry(tenant_form)
        date_entry.pack(padx=20, pady=5)

        global due_entry
        due_label = ttk.Label(tenant_form, text="Due (YYYY-MM-DD)")
        due_label.pack(padx=20, pady=5)

        due_entry = ttk.Entry(tenant_form)
        due_entry.pack(padx=20, pady=5)

        roomNum_label = ttk.Label(tenant_form, text="Room Number")
        roomNum_label.pack(padx=20, pady=5)

        global roomNum_entry
        roomNum_entry = ttk.Combobox(tenant_form)
        roomNum_entry.pack(padx=20, pady=5)
        roomNum_entry.bind("<<ComboboxSelected>>", update_room_price)

        roomPrice_label = ttk.Label(tenant_form, text="Room Price")
        roomPrice_label.pack(padx=20, pady=5)

        global roomPrice_entry
        roomPrice_entry = ttk.Combobox(tenant_form)
        roomPrice_entry.pack(padx=20, pady=(5, 20))
        roomPrice_entry.bind("<<ComboboxSelected>>", update_room_number)

        populate_comboboxes()


        
        buttons = ttk.Frame(tenant_frame)
        buttons.pack(pady=10)

        add_button = ttk.Button(buttons, text="Create",width=20, command=lambda: manage_tenants("insert"))
        add_button.pack(padx=20, pady=(15,5))

        buttons1 = ttk.Frame(tenant_frame)
        buttons1.pack(pady=(10,20))

        upd_button = ttk.Button(buttons1, text="Update",width=20, command=lambda: manage_tenants("update"))
        upd_button.grid(column=0,row=0,padx=10)

        del_button = ttk.Button(buttons1, text="Delete", width=20,command=lambda: manage_tenants("delete"))
        del_button.grid(column=1,row=0,padx=10)



        tenantTable_frame = ttk.Frame(self)
        tenantTable_frame.pack(side="right", fill="both", expand=True, padx=40, pady=(20, 20))

        global tenantsTree
        columns = ("tenants_id","firstname", "lastname", "address", "date","due", "room_number", "room_price")
        tenantsTree = ttk.Treeview(tenantTable_frame, columns=columns, show="headings", height=38)

        for col in columns:
            tenantsTree.column(col, width=130)

        tenantsTree.heading("tenants_id", text="#")
        tenantsTree.heading("firstname", text="Firstname")
        tenantsTree.heading("lastname", text="Lastname")
        tenantsTree.heading("address", text="Address")
        tenantsTree.heading("date", text="Date")
        tenantsTree.heading("due", text="Due")
        tenantsTree.heading("room_number", text="Room Number")
        tenantsTree.heading("room_price", text="Amount")
        

        tenantsTree.grid(row=10, column=0, columnspan=8, padx=(50, 10), pady=10)
        populate_tenants_treeview()
        tenantsTree.bind("<<TreeviewSelect>>", tenants_on_tree_select)

        refresh_btn = ttk.Button(tenantTable_frame,text="Refresh",width=20,command=populate_tenants_treeview)
        refresh_btn.grid(row=11, column=0,padx=100, pady=(10,5))

        back_btn = ttk.Button(tenantTable_frame,text="Back",width=20,command=show_dashboard_frame)
        back_btn.grid(row=11, column=1,padx=100, pady=(10,5))