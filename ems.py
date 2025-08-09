import sqlite3
import customtkinter
from tkinter import messagebox, END, ttk
from datetime import datetime
from database import connect_database

# DATABASE CONNECTION
def launch_ems(conn, cursor):
    # APP SETTINGS
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.title('EMPLOYEE EMS')
    app.geometry("950x650")
    app.configure(bg='#17043d')

    # FONTS
    font1 = ('Arial', 20, 'bold')
    font2 = ('Arial', 15, 'bold')
    font3 = ('Arial', 12, 'bold')

    # CREATING FRAMES
    frame1 = customtkinter.CTkFrame(app, fg_color="#FFFFFF", width=750, height=650)
    frame1.place(x=375, y=0)

    # LABEL CREATION AND ENTRY
    def create_label_entry(text, y):
        label = customtkinter.CTkLabel(app, text=text, font=font1)
        label.place(x=20, y=y)
        entry = customtkinter.CTkEntry(app, font=font2, text_color="#000000", fg_color="#FFFFFF", border_color="#FFFFFF", width=200)
        entry.place(x=140, y=y)
        return entry

    id_entry = create_label_entry("ID:", 20)
    forename_entry = create_label_entry("Forename:", 66)
    surname_entry = create_label_entry("Surname:", 112)
    sex_entry = create_label_entry("Sex (M/F):", 158)
    dob_entry = create_label_entry("DOB (DD-MM-YYYY):", 204)
    role_entry = create_label_entry("Role:", 250)

    # TREEVIEW SETUP
    style = ttk.Style()
    style.configure("mystyle.Treeview", font=font3, rowheight=70)
    style.configure("mystyle.Treeview.Heading", font=font2)
    style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])

    tv = ttk.Treeview(frame1, columns=(1, 2, 3, 4, 5, 6), show="headings", style="mystyle.Treeview")
    headings = [("ID", 90), ("Forename", 100), ("Surname", 100), ("Sex (M/F)", 100), ("DOB", 90), ("Role", 90)]
    for i, (text, width) in enumerate(headings, start=1):
        tv.heading(str(i), text=text)
        tv.column(str(i), width=width)
    tv.pack(fill="both", expand=True)

    # Utility functions
    def clear():
        for entry in [id_entry, forename_entry, surname_entry, sex_entry, dob_entry, role_entry]:
            entry.delete(0, END)

    def validate_date(date_str):
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    def fetch():
        cursor.execute("SELECT EmployeeID, FirstName, LastName, Sex, DOB, Role FROM Apprentices")
        return cursor.fetchall()

    def display_data():
        tv.delete(*tv.get_children())
        for row in fetch():
            tv.insert("", "end", values=row)

    # CRUD operations
    def insert():
        if any(entry.get().strip() == "" for entry in [id_entry, forename_entry, surname_entry, sex_entry, dob_entry, role_entry]):
            messagebox.showerror("Error", "Please enter all required data.")
        elif not validate_date(dob_entry.get()):
            messagebox.showerror("Error", "Date must be in DD-MM-YYYY format.")
        elif sex_entry.get().upper() not in ["M", "F"]:
            messagebox.showerror("Error", "Sex must be 'M' or 'F'.")
        else:
            try:
                details = (
                    int(id_entry.get()), forename_entry.get(), surname_entry.get(),
                    sex_entry.get().upper(), dob_entry.get(), role_entry.get()
                )
                cursor.execute("""
                    INSERT INTO Employees (EmployeeID, FirstName, LastName, Sex, DOB, Role)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, details)
                conn.commit()
                messagebox.showinfo("Inserted", "Employee has been inserted.")
                display_data()
                clear()
            except ValueError:
                messagebox.showerror("Error", "ID must be a number.")
            except sqlite3.Error as error:
                messagebox.showerror("Error", f"Database error: {error}")

    def update():
        if id_entry.get().strip() == "":
            messagebox.showerror("Error", "Please enter the ID to update.")
            return
        try:
            details = (
                forename_entry.get(), surname_entry.get(), sex_entry.get().upper(),
                dob_entry.get(), role_entry.get(), int(id_entry.get())
            )
            cursor.execute("""
                UPDATE Employees SET FirstName=?, LastName=?, Sex=?, DOB=?, Role=? WHERE ApprenticeID=?
            """, details)
            conn.commit()
            messagebox.showinfo("Updated", "Employee has been updated.")
            display_data()
            clear()
        except ValueError:
            messagebox.showerror("Error", "ID must be a number.")
        except sqlite3.Error as error:
            messagebox.showerror("Error", f"Database error: {error}")

    def delete():
        if id_entry.get().strip() == "":
            messagebox.showerror("Error", "Please enter an ID to delete.")
        else:
            try:
                cursor.execute("DELETE FROM Employees WHERE ApprenticeID=?", (int(id_entry.get()),))
                conn.commit()
                messagebox.showinfo("Deleted", "Employee has been deleted.")
                display_data()
                clear()
            except ValueError:
                messagebox.showerror("Error", "ID must be a number.")
            except sqlite3.Error as error:
                messagebox.showerror("Error", f"Database error: {error}")

    def get_data(event):
        clear()
        selected_row = tv.focus()
        if not selected_row:
            return
        row = tv.item(selected_row)["values"]
        if row:
            id_entry.insert(0, row[0])
            forename_entry.insert(0, row[1])
            surname_entry.insert(0, row[2])
            sex_entry.insert(0, row[3])
            dob_entry.insert(0, row[4])
            role_entry.insert(0, row[5])

    # BUTTONS
    insert_button = customtkinter.CTkButton(app, text="Insert", command=insert, font=font2, width=200)
    insert_button.place(x=140, y=300)

    update_button = customtkinter.CTkButton(app, text="Update", command=update, font=font2, width=200)
    update_button.place(x=140, y=350)

    delete_button = customtkinter.CTkButton(app, text="Delete", command=delete, font=font2, width=200)
    delete_buttn.place(x=140, y=400)

    clear_button = customtkinter.CTkButton(app, text="Clear", command=clear, font=font2, width=200)
    clear_button.place(x=140, y=450)

    refresh_button = customtkinter.CTkButton(app, text="Refresh", command=display_data, font=font2, width=200)
    refresh_button.place(x=140, y=500)

    # BIND TREEVIEW
    tv.bind("<ButtonRelease-1>", get_data)

    # INITIAL DATA LOAD
    display_data()
    app.mainloop()
