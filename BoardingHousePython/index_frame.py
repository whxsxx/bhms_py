import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class IndexFrame(ttk.Frame):
    def __init__(self, parent, login_command):
        super().__init__(parent, width=700, height=700)
        self.pack(expand=True, fill=tk.BOTH)
        self.pack_propagate(False)

        index_frame = ttk.Frame(self, width=700, height=500)
        index_frame.pack(pady=(50,10))

        Title_label = ttk.Label(index_frame, text="BH MONITORING SYSTEM", font=("Helvetica", 20, 'bold'), foreground="white")
        Title_label.pack(pady=(30, 20))

        usr_label = ttk.Label(index_frame, text="User name",font=("",10,'bold'))
        usr_label.pack(pady=(50,10))

        self.usr_entry = ttk.Entry(index_frame, width=30)
        self.usr_entry.pack(pady=10)

        pwrd_label = ttk.Label(index_frame, text="Password",font=("",10,'bold'))
        pwrd_label.pack(pady=10)

        self.pwrd_entry = ttk.Entry(index_frame, width=30, show='*')
        self.pwrd_entry.pack(pady=(10,50))

        login_btn = ttk.Button(index_frame, text="Log in", width=20, bootstyle=OUTLINE, command=login_command,)
        login_btn.pack()

    def get_username(self):
        return self.usr_entry.get()

    def get_password(self):
        return self.pwrd_entry.get()
