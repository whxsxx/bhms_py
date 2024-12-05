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

def manage_rooms(action):
    try:
        if action == "insert":

            room_number = room_num_entry.get()
            room_price = roomPrice_entry.get()

            cursor.execute("INSERT INTO rooms (room_number, room_price) VALUES (%s, %s)",
                        (room_number, room_price))


            conn.commit()
            messagebox.showinfo("Success", "Room created successfully")

        elif action == "update":
            room_id = room_id_entry.get()

            new_room_number = room_num_entry.get()
            room_price = roomPrice_entry.get()

            try:
                conn.start_transaction()

                cursor.execute("UPDATE rooms SET room_number=%s, room_price=%s WHERE room_id=%s",
                            (new_room_number, room_price, room_id))

                cursor.execute("UPDATE tenants SET room_number=%s, room_price=%s WHERE room_number=%s",
                            (new_room_number, room_price, room_id))

                conn.commit()
                messagebox.showinfo("Success", "Room updated successfully")
            except mysql.connector.Error as err:
                conn.rollback()
                messagebox.showerror("Error", f"Failed to update room: {err}")
    



        elif action == "delete":
            if messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?"):
                room_id = room_id_entry.get()

    
                cursor.execute("DELETE FROM rooms WHERE room_id=%s", (room_id,))


                conn.commit()
                messagebox.showinfo("Success", "Room deleted successfully")

        clear_room_entry_widgets()
        populate_rooms_treeview()
    except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")


def room_on_tree_select(event):
    selected_item = roomtree.selection()
    if selected_item:
        values = roomtree.item(selected_item)['values']

        clear_room_entry_widgets()

        room_id_entry.insert(0, values[0])
        room_num_entry.insert(0, values[1])
        roomPrice_entry.insert(0, values[2])

def fetch_rooms_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
            database="pybh_db"
        )
        cursor = conn.cursor()

        query = """
        SELECT * FROM rooms
        """
        cursor.execute(query)
        rooms_data = cursor.fetchall()

        return rooms_data

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error fetching rooms data: {err}")
        return []

def populate_rooms_treeview():
    clear_room_entry_widgets()
    rooms_data = fetch_rooms_data()
    for row in roomtree.get_children():
        roomtree.delete(row)
    for row in rooms_data:
        roomtree.insert("", "end", values=row)
    pass

def clear_room_entry_widgets():
    room_id_entry.delete(0, tk.END)
    room_num_entry.delete(0, tk.END)
    roomPrice_entry.delete(0, tk.END)




class RoomFrame(ttk.Frame):
    def __init__(self, parent,show_dashboard_frame):
        super().__init__(parent)
        self.config(width=1700, height=900)
        self.pack_propagate(False)
        
        title_label = ttk.Label(self, text="ROOMS", foreground="white", font=("", 30, 'bold'))
        title_label.pack(side="top", anchor="nw", padx=(35, 10), pady=(20, 5))

        room_frame = ttk.Frame(self)
        room_frame.pack(side="left", fill="both", expand=True, padx=40, pady=(20, 5))

        room_form = ttk.LabelFrame(room_frame, text="ROOM DETAILS", width=150, height=40)
        room_form.pack(pady=(0,10))


        room_form.pack(fill=tk.BOTH, expand=True)

        global room_id_entry
        room_id_label = ttk.Label(room_form, text="#")
        room_id_label.pack(padx=20, pady=(30, 20))

        room_id_entry = ttk.Entry(room_form)
        room_id_entry.pack(padx=20, pady=20)
        global room_num_entry
        room_num_label = ttk.Label(room_form, text="Room Number")
        room_num_label.pack(padx=20, pady=20)

        room_num_entry = ttk.Entry(room_form)
        room_num_entry.pack(padx=20, pady=20)
        global roomPrice_entry
        roomPrice_label = ttk.Label(room_form, text="Room Price")
        roomPrice_label.pack(padx=20, pady=20)

        roomPrice_entry = ttk.Entry(room_form)
        roomPrice_entry.pack(padx=20, pady=(5, 20))

        buttons = ttk.Frame(room_frame)
        buttons.pack(pady=10)

        add_button = ttk.Button(buttons, text="Create",width=20, command=lambda: manage_rooms("insert"))
        add_button.pack(padx=20, pady=(15,5))

        buttons1 = ttk.Frame(room_frame)
        buttons1.pack(pady=(10,20))

        upd_button = ttk.Button(buttons1, text="Update",width=20, command=lambda: manage_rooms("update"))
        upd_button.grid(column=0,row=0,padx=10)

        del_button = ttk.Button(buttons1, text="Delete",width=20, command=lambda: manage_rooms("delete"))
        del_button.grid(column=1,row=0,padx=10)

        roomTable_frame = ttk.Frame(self)
        roomTable_frame.pack(side="right", fill="both", expand=True, padx=40, pady=(20, 20))

        global roomtree
        columns = ("room_id","room_number", "room_price")
        roomtree = ttk.Treeview(roomTable_frame, columns=columns, show="headings", height=33)

        for col in columns:
            roomtree.column(col, width=350)

        roomtree.heading("room_id", text="#")
        roomtree.heading("room_number", text="Room Number")
        roomtree.heading("room_price", text="Amount")
        

        roomtree.grid(row=10, column=0, columnspan=8, padx=(50, 10), pady=10)
        roomtree.bind("<ButtonRelease-1>", room_on_tree_select)
        populate_rooms_treeview()


        refresh_btn = ttk.Button(roomTable_frame,text="Refresh",width=20,command=populate_rooms_treeview)
        refresh_btn.grid(row=11, column=0,padx=100, pady=(10,5))

        back_btn = ttk.Button(roomTable_frame,text="Back",width=20,command=show_dashboard_frame)
        back_btn.grid(row=11, column=1,padx=100, pady=(10,5))