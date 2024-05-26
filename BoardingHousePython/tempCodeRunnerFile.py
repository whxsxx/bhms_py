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