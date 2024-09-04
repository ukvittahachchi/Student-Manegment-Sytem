import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import hashlib

# Function to add student
def add_student():
    name = entry_name.get()
    roll_number = entry_roll.get()
    grade = entry_grade.get()

    if name == "" or roll_number == "" or grade == "":
        messagebox.showerror("Input Error", "All fields are required")
        return
    
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO students (roll_number, name, grade) VALUES (?, ?, ?)", (roll_number, name, grade))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
        entry_name.delete(0, tk.END)
        entry_roll.delete(0, tk.END)
        entry_grade.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Input Error", "Roll number already exists")
    conn.close()

# Function to view students
def view_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    records = c.fetchall()
    conn.close()
    
    view_window = tk.Toplevel()
    view_window.title("View Students")
    view_window.geometry("400x300")
    view_window.configure(bg="#f0f0f0")

    for index, record in enumerate(records):
        tk.Label(view_window, text=f"{record[0]} {record[1]} {record[2]}", bg="#f0f0f0").grid(row=index, column=0, pady=2)

# Function to search student
def search_student():
    roll_number = entry_search.get()
    
    if roll_number == "":
        messagebox.showerror("Input Error", "Roll number is required")
        return

    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE roll_number=?", (roll_number,))
    record = c.fetchone()
    conn.close()

    if record:
        entry_name.delete(0, tk.END)
        entry_roll.delete(0, tk.END)
        entry_grade.delete(0, tk.END)

        entry_roll.insert(0, record[0])
        entry_name.insert(0, record[1])
        entry_grade.insert(0, record[2])
    else:
        messagebox.showerror("Error", "Student not found")

# Function to delete student
def delete_student():
    roll_number = entry_roll.get()
    
    if roll_number == "":
        messagebox.showerror("Input Error", "Roll number is required")
        return

    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE roll_number=?", (roll_number,))
    conn.commit()
    conn.close()

    if c.rowcount > 0:
        messagebox.showinfo("Success", "Student deleted successfully")
        entry_name.delete(0, tk.END)
        entry_roll.delete(0, tk.END)
        entry_grade.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Student not found")

# Function to update student
def update_student():
    name = entry_name.get()
    roll_number = entry_roll.get()
    grade = entry_grade.get()
    
    if name == "" or roll_number == "" or grade == "":
        messagebox.showerror("Input Error", "All fields are required")
        return

    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("UPDATE students SET name=?, grade=? WHERE roll_number=?", (name, grade, roll_number))
    conn.commit()
    conn.close()

    if c.rowcount > 0:
        messagebox.showinfo("Success", "Student updated successfully")
    else:
        messagebox.showerror("Error", "Student not found")

# Signup function
def signup():
    def register_user():
        username = entry_signup_username.get()
        password = entry_signup_password.get()
        confirm_password = entry_confirm_password.get()

        if username == "" or password == "" or confirm_password == "":
            messagebox.showerror("Input Error", "All fields are required")
            return
        
        if password != confirm_password:
            messagebox.showerror("Input Error", "Passwords do not match")
            return
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully")
            signup_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Input Error", "Username already exists")
        conn.close()

    signup_window = tk.Toplevel()
    signup_window.title("Signup")
    signup_window.geometry("300x200")
    signup_window.configure(bg="#f0f0f0")

    frame_signup = tk.Frame(signup_window, bg="#f0f0f0", padx=10, pady=10)
    frame_signup.pack(expand=True)

    tk.Label(frame_signup, text="Username", bg="#f0f0f0").grid(row=0, column=0, pady=5, sticky='w')
    entry_signup_username = tk.Entry(frame_signup)
    entry_signup_username.grid(row=0, column=1, pady=5)

    tk.Label(frame_signup, text="Password", bg="#f0f0f0").grid(row=1, column=0, pady=5, sticky='w')
    entry_signup_password = tk.Entry(frame_signup, show="*")
    entry_signup_password.grid(row=1, column=1, pady=5)

    tk.Label(frame_signup, text="Confirm Password", bg="#f0f0f0").grid(row=2, column=0, pady=5, sticky='w')
    entry_confirm_password = tk.Entry(frame_signup, show="*")
    entry_confirm_password.grid(row=2, column=1, pady=5)

    tk.Button(frame_signup, text="Register", command=register_user, bg="#4caf50", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

# Login function
def login():
    def authenticate_user():
        username = entry_login_username.get()
        password = entry_login_password.get()

        if username == "" or password == "":
            messagebox.showerror("Input Error", "All fields are required")
            return
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        record = c.fetchone()
        conn.close()

        if record:
            messagebox.showinfo("Success", "Login successful")
            login_window.destroy()
            main_window()  # Show the main window
        else:
            messagebox.showerror("Error", "Invalid credentials")

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x150")
    login_window.configure(bg="#f0f0f0")

    frame_login = tk.Frame(login_window, bg="#f0f0f0", padx=10, pady=10)
    frame_login.pack(expand=True)

    tk.Label(frame_login, text="Username", bg="#f0f0f0").grid(row=0, column=0, pady=5, sticky='w')
    entry_login_username = tk.Entry(frame_login)
    entry_login_username.grid(row=0, column=1, pady=5)

    tk.Label(frame_login, text="Password", bg="#f0f0f0").grid(row=1, column=0, pady=5, sticky='w')
    entry_login_password = tk.Entry(frame_login, show="*")
    entry_login_password.grid(row=1, column=1, pady=5)

    tk.Button(frame_login, text="Login", command=authenticate_user, bg="#4caf50", fg="white").grid(row=2, column=0, pady=10)
    tk.Button(frame_login, text="Signup", command=signup, bg="#2196f3", fg="white").grid(row=2, column=1, pady=10)

    login_window.mainloop()

# Main window function
def main_window():
    root = tk.Tk()
    root.title("Student Management System")
    root.geometry("500x400")
    root.configure(bg="#f0f0f0")

    frame_main = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
    frame_main.pack(expand=True, fill='both')

    tk.Label(frame_main, text="Name", bg="#f0f0f0").grid(row=0, column=0, pady=5, sticky='w')
    global entry_name
    entry_name = tk.Entry(frame_main)
    entry_name.grid(row=0, column=1, pady=5)

    tk.Label(frame_main, text="Roll Number", bg="#f0f0f0").grid(row=1, column=0, pady=5, sticky='w')
    global entry_roll
    entry_roll = tk.Entry(frame_main)
    entry_roll.grid(row=1, column=1, pady=5)

    tk.Label(frame_main, text="Grade", bg="#f0f0f0").grid(row=2, column=0, pady=5, sticky='w')
    global entry_grade
    entry_grade = tk.Entry(frame_main)
    entry_grade.grid(row=2, column=1, pady=5)

    tk.Button(frame_main, text="Add", command=add_student, bg="#4caf50", fg="white").grid(row=3, column=0, pady=10)
    tk.Button(frame_main, text="View", command=view_students, bg="#2196f3", fg="white").grid(row=3, column=1, pady=10)

    tk.Label(frame_main, text="Roll Number to Search/Delete", bg="#f0f0f0").grid(row=4, column=0, pady=5, sticky='w')
    global entry_search
    entry_search = tk.Entry(frame_main)
    entry_search.grid(row=4, column=1, pady=5)

    tk.Button(frame_main, text="Search", command=search_student, bg="#ffc107", fg="white").grid(row=5, column=0, pady=10)
    tk.Button(frame_main, text="Delete", command=delete_student, bg="#f44336", fg="white").grid(row=5, column=1, pady=10)

    tk.Button(frame_main, text="Update", command=update_student, bg="#9c27b0", fg="white").grid(row=6, column=0, columnspan=2, pady=10)

    root.mainloop()

# Create the database and tables if they don't exist
def create_database():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database and start with the login window
create_database()
login()