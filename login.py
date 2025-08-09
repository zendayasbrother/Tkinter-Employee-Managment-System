import customtkinter
from tkinter import messagebox
from database import connect_database

# DATABASE CONNECTION
sqliteConnection, cursor = connect_database()
if not sqliteConnection or not cursor:
    messagebox.showerror("Database Error", "Failed to connect to database.")
    exit()

# GUI SETUP
root = customtkinter.CTk()
root.title('APPRENTICE EMS LOGIN')
root.geometry("950x650")
root.configure(bg="#025947")

def login():
    username = usernameEntry.get().strip()
    password = passwordEntry.get().strip()

    if username == '' or password == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        try:
            cursor.execute("SELECT * FROM Administrators WHERE username=? AND password=?", (username, password))
            result = cursor.fetchone()
            if result:
                messagebox.showinfo('Success', 'Login is successful')
                root.destroy()
                import ems
                ems.launch_ems(sqliteConnection, cursor)
            else:
                messagebox.showerror('Error', 'Wrong username or password')
        except Exception as e:
            messagebox.showerror('Error', f'Database error: {e}')

def create_label_entry(text, y, show=None):
    label = customtkinter.CTkLabel(root, text=text)
    label.place(x=20, y=y)
    entry = customtkinter.CTkEntry(root, text_color="#000000", fg_color="#FFFFFF", border_color="#FFFFFF", width=200, show=show)
    entry.place(x=140, y=y)
    return entry

def create_button(text, y, command):
    button = customtkinter.CTkButton(root, text=text, command=command, cursor='hand2')
    button.place(x=140, y=y)

usernameEntry = create_label_entry('Username:', y=150)
passwordEntry = create_label_entry('Password:', y=200, show='*')
create_button('Login', y=250, command=login)

root.mainloop()

# CLOSE CONNECTION
if sqliteConnection:
    sqliteConnection.close()
