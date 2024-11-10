import sqlite3
import tkinter as tk
from tkinter import messagebox
from prettytable import PrettyTable
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table

# Initialize colorama
init(autoreset=True)

# Initialize rich console
console = Console()

# Database setup
def setup_database():
    with sqlite3.connect('students.db', timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
        """)
        conn.commit()

def add_student(id, name, age, grade):
    with sqlite3.connect('students.db', timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM students WHERE id = ?", (id,))
        if cursor.fetchone():
            raise ValueError("A student with this ID already exists.")
        cursor.execute("INSERT INTO students (id, name, age, grade) VALUES (?, ?, ?, ?)", (id, name, age, grade))
        conn.commit()

def get_students():
    with sqlite3.connect('students.db', timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        return rows

def update_student(id, name, age, grade):
    with sqlite3.connect('students.db', timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?", (name, age, grade, id))
        conn.commit()

def delete_student(id):
    with sqlite3.connect('students.db', timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (id,))
        conn.commit()

# GUI setup
class StudentManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        
        self.label_id = tk.Label(self, text="ID")
        self.label_id.grid(row=0, column=0)
        self.entry_id = tk.Entry(self)
        self.entry_id.grid(row=0, column=1)
        
        self.label_name = tk.Label(self, text="Name")
        self.label_name.grid(row=1, column=0)
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=1, column=1)
        
        self.label_age = tk.Label(self, text="Age")
        self.label_age.grid(row=2, column=0)
        self.entry_age = tk.Entry(self)
        self.entry_age.grid(row=2, column=1)
        
        self.label_grade = tk.Label(self, text="Grade")
        self.label_grade.grid(row=3, column=0)
        self.entry_grade = tk.Entry(self)
        self.entry_grade.grid(row=3, column=1)
        
        self.button_add = tk.Button(self, text="Add Student", command=self.add_student)
        self.button_add.grid(row=4, column=0, columnspan=2)
        
        self.button_view = tk.Button(self, text="View Students", command=self.view_students)
        self.button_view.grid(row=5, column=0, columnspan=2)
        
        self.button_update = tk.Button(self, text="Update Student", command=self.update_student)
        self.button_update.grid(row=6, column=0, columnspan=2)
        
        self.button_delete = tk.Button(self, text="Delete Student", command=self.delete_student)
        self.button_delete.grid(row=7, column=0, columnspan=2)
        
        self.text_output = tk.Text(self, height=10, width=50)
        self.text_output.grid(row=8, column=0, columnspan=2)

    def add_student(self):
        id = self.entry_id.get()
        name = self.entry_name.get()
        age = self.entry_age.get()
        grade = self.entry_grade.get()
        if id and name and age and grade:
            try:
                add_student(id, name, age, grade)
                messagebox.showinfo("Success", Fore.GREEN + "Student added successfully!")
            except ValueError as ve:
                messagebox.showerror("Error", Fore.RED + str(ve))
        else:
            messagebox.showerror("Error", Fore.RED + "All fields are required.")

    def view_students(self):
        students = get_students()
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Age", "Grade"]

        for student in students:
            table.add_row([student[0], student[1], student[2], student[3]])
        
        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(tk.END, table.get_string())

    def update_student(self):
        id = self.entry_id.get()
        name = self.entry_name.get()
        age = self.entry_age.get()
        grade = self.entry_grade.get()
        if id and name and age and grade:
            update_student(id, name, age, grade)
            messagebox.showinfo("Success", Fore.GREEN + "Student updated successfully!")
        else:
            messagebox.showerror("Error", Fore.RED + "All fields are required.")

    def delete_student(self):
        id = self.entry_id.get()
        if id:
            delete_student(id)
            messagebox.showinfo("Success", Fore.GREEN + "Student deleted successfully!")
        else:
            messagebox.showerror("Error", Fore.RED + "ID is required.")

if __name__ == "__main__":
    setup_database()
    print(Fore.GREEN + Style.BRIGHT + "Starting Student Management System...")
    app = StudentManagementSystem()
    app.mainloop()
