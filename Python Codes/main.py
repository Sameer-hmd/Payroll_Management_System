import tkinter as tk
from tkinter import ttk, messagebox, StringVar, DoubleVar
import sqlite3
import re
import hashlib
from datetime import datetime
import os
import database
import calculator
import receipt
import styles
import login

# Initialize the database first thing to ensure it's ready
database.initialize_db()

class PayrollManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Payroll Management System")
        self.root.geometry("1200x700")
        self.root.config(bg=styles.BG_COLOR)
        # Make the window as large as possible in a cross-platform way
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry(f"{width}x{height}+0+0")
        
        # Apply the enhanced styles
        styles.configure_styles(self.root)
        
        # Database already initialized at the top of the file
        # We don't need to initialize it again here
        
        # User type and ID
        self.user_type = None
        self.user_id = None
        
        # Create variables for employee details
        self.emp_id = StringVar()
        self.name = StringVar()
        self.email = StringVar()
        self.phone = StringVar()
        self.address = StringVar()
        self.gender = StringVar()
        self.department = StringVar()
        self.designation = StringVar()
        self.doj = StringVar()  # Date of joining
        self.password = StringVar()  # For employee password
        
        # Create variables for salary details
        self.basic_salary = DoubleVar()
        self.da = DoubleVar()  # Dearness Allowance
        self.hra = DoubleVar()  # House Rent Allowance
        self.ma = DoubleVar()  # Medical Allowance
        self.pf = DoubleVar()  # Provident Fund
        self.insurance = DoubleVar()
        self.tax = DoubleVar()
        self.net_salary = DoubleVar()
        
        # Search variable
        self.search_by = StringVar()
        self.search_text = StringVar()
        
        # First show the login screen
        self.show_login_screen()
    
    def setup_ui(self):
        # Create a notebook (tabs) for different frames
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Employee Details
        self.employee_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.employee_frame, text="Employee Details")
        self.setup_employee_frame()
        
        # Tab 2: Salary Details
        self.salary_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.salary_frame, text="Salary Management")
        self.setup_salary_frame()
        
        # Tab 3: Calculator
        self.calculator_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.calculator_frame, text="Calculator")
        self.calc = calculator.Calculator(self.calculator_frame)
        
        # Tab 4: Salary Receipt
        self.receipt_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.receipt_frame, text="Salary Receipt")
        self.receipt_generator = receipt.ReceiptGenerator(self.receipt_frame)
    
    def setup_employee_frame(self):
        # Create left and right frames for employee details
        left_frame = ttk.LabelFrame(self.employee_frame, text="Employee Details")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = ttk.LabelFrame(self.employee_frame, text="Employee Database")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Employee details form - each row is a frame
        # Row 1
        row1 = ttk.Frame(left_frame)
        row1.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row1, text="Employee ID:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row1, textvariable=self.emp_id).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Row 2
        row2 = ttk.Frame(left_frame)
        row2.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row2, text="Name:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row2, textvariable=self.name).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Row 3
        row3 = ttk.Frame(left_frame)
        row3.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row3, text="Email:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row3, textvariable=self.email).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Row 4
        row4 = ttk.Frame(left_frame)
        row4.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row4, text="Phone:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row4, textvariable=self.phone).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Row 5
        row5 = ttk.Frame(left_frame)
        row5.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row5, text="Address:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row5, textvariable=self.address).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Row 6
        row6 = ttk.Frame(left_frame)
        row6.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row6, text="Gender:").pack(side=tk.LEFT, padx=5)
        gender_combo = ttk.Combobox(row6, textvariable=self.gender, values=["Male", "Female", "Other"], state="readonly")
        gender_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Row 7
        row7 = ttk.Frame(left_frame)
        row7.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row7, text="Department:").pack(side=tk.LEFT, padx=5)
        dept_combo = ttk.Combobox(row7, textvariable=self.department, 
                                 values=["HR", "Finance", "IT", "Operations", "Marketing", "Sales", "Production"], 
                                 state="readonly")
        dept_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Row 8
        row8 = ttk.Frame(left_frame)
        row8.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row8, text="Designation:").pack(side=tk.LEFT, padx=5)
        desig_combo = ttk.Combobox(row8, textvariable=self.designation, 
                                  values=["Manager", "Developer", "Analyst", "Assistant", "Director", "Engineer", "Specialist"],
                                  state="readonly")
        desig_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Row 9
        row9 = ttk.Frame(left_frame)
        row9.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row9, text="Date of Joining (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row9, textvariable=self.doj).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Row 10 - Password
        row10 = ttk.Frame(left_frame)
        row10.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row10, text="Password:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row10, textvariable=self.password, show="*").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Button Frame
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # CRUD Buttons
        ttk.Button(btn_frame, text="Save", command=self.save_employee, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_employee_fields, style="Warning.TButton").pack(side=tk.LEFT, padx=5)
        
        # Search Frame
        search_frame = ttk.LabelFrame(right_frame, text="Search Employee")
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        search_inner_frame = ttk.Frame(search_frame)
        search_inner_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_inner_frame, text="Search By:").pack(side=tk.LEFT, padx=5)
        search_combo = ttk.Combobox(search_inner_frame, textvariable=self.search_by, 
                                   values=["Employee ID", "Name", "Department", "Designation"],
                                   state="readonly")
        search_combo.pack(side=tk.LEFT, padx=5)
        search_combo.current(0)
        
        ttk.Entry(search_inner_frame, textvariable=self.search_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_inner_frame, text="Search", command=self.search_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_inner_frame, text="Show All", command=self.fetch_employees).pack(side=tk.LEFT, padx=5)
        
        # Employee Table
        table_frame = ttk.Frame(right_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.employee_table = ttk.Treeview(
            table_frame, 
            columns=("emp_id", "name", "email", "phone", "address", "gender", "department", "designation", "doj"),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.config(command=self.employee_table.yview)
        scroll_x.config(command=self.employee_table.xview)
        
        # Set headings
        self.employee_table.heading("emp_id", text="Employee ID")
        self.employee_table.heading("name", text="Name")
        self.employee_table.heading("email", text="Email")
        self.employee_table.heading("phone", text="Phone")
        self.employee_table.heading("address", text="Address")
        self.employee_table.heading("gender", text="Gender")
        self.employee_table.heading("department", text="Department")
        self.employee_table.heading("designation", text="Designation")
        self.employee_table.heading("doj", text="Date of Joining")
        
        # Set column widths
        self.employee_table.column("emp_id", width=80)
        self.employee_table.column("name", width=150)
        self.employee_table.column("email", width=200)
        self.employee_table.column("phone", width=150)
        self.employee_table.column("address", width=200)
        self.employee_table.column("gender", width=80)
        self.employee_table.column("department", width=100)
        self.employee_table.column("designation", width=100)
        self.employee_table.column("doj", width=100)
        
        self.employee_table['show'] = 'headings'
        self.employee_table.pack(fill="both", expand=True)
        
        # Bind the select event
        self.employee_table.bind("<ButtonRelease-1>", self.get_employee_data)
    
    def setup_salary_frame(self):
        # Create left and right frames for salary details
        left_frame = ttk.LabelFrame(self.salary_frame, text="Salary Details")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = ttk.LabelFrame(self.salary_frame, text="Salary Records")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Employee ID selection
        row1 = ttk.Frame(left_frame)
        row1.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row1, text="Employee ID:").pack(side=tk.LEFT, padx=5)
        self.salary_emp_id_combo = ttk.Combobox(row1, textvariable=self.emp_id, state="readonly")
        self.salary_emp_id_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.salary_emp_id_combo.bind("<<ComboboxSelected>>", self.fetch_employee_for_salary)
        
        # Employee info display
        row2 = ttk.Frame(left_frame)
        row2.pack(fill=tk.X, padx=5, pady=5)
        self.emp_info_label = ttk.Label(row2, text="")
        self.emp_info_label.pack(fill=tk.X, expand=True, padx=5)
        
        # Salary details
        row3 = ttk.Frame(left_frame)
        row3.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row3, text="Basic Salary:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row3, textvariable=self.basic_salary).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        row4 = ttk.Frame(left_frame)
        row4.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row4, text="Dearness Allowance:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row4, textvariable=self.da).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        row5 = ttk.Frame(left_frame)
        row5.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row5, text="House Rent Allowance:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row5, textvariable=self.hra).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        row6 = ttk.Frame(left_frame)
        row6.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row6, text="Medical Allowance:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row6, textvariable=self.ma).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        row7 = ttk.Frame(left_frame)
        row7.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row7, text="Provident Fund:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row7, textvariable=self.pf).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        row8 = ttk.Frame(left_frame)
        row8.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row8, text="Insurance:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row8, textvariable=self.insurance).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        row9 = ttk.Frame(left_frame)
        row9.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(row9, text="Tax:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(row9, textvariable=self.tax).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        row10 = ttk.Frame(left_frame)
        row10.pack(fill=tk.X, padx=5)
        ttk.Label(row10, text="Net Salary:").pack(side=tk.LEFT, padx=5)
        ttk.Label(row10, textvariable=self.net_salary, font=styles.HEADING_FONT).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Button frame
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Calculate Net Salary", command=self.calculate_net_salary, style="Accent.TButton").grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Save", command=self.save_salary).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Update", command=self.update_salary).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_salary).grid(row=1, column=0, pady=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_salary_fields, style="Warning.TButton").grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Generate Receipt", command=self.generate_receipt, style="Success.TButton").grid(row=1, column=2, padx=5, pady=5)
        
        # Salary table
        table_frame = ttk.Frame(right_frame)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.salary_table = ttk.Treeview(
            table_frame, 
            columns=("id", "emp_id", "name", "department", "basic", "da", "hra", "ma", "pf", "insurance", "tax", "net_salary", "date"),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.config(command=self.salary_table.yview)
        scroll_x.config(command=self.salary_table.xview)
        
        # Set headings
        self.salary_table.heading("id", text="ID")
        self.salary_table.heading("emp_id", text="Employee ID")
        self.salary_table.heading("name", text="Name")
        self.salary_table.heading("department", text="Department")
        self.salary_table.heading("basic", text="Basic")
        self.salary_table.heading("da", text="DA")
        self.salary_table.heading("hra", text="HRA")
        self.salary_table.heading("ma", text="MA")
        self.salary_table.heading("pf", text="PF")
        self.salary_table.heading("insurance", text="Insurance")
        self.salary_table.heading("tax", text="Tax")
        self.salary_table.heading("net_salary", text="Net Salary")
        self.salary_table.heading("date", text="Date")
        
        # Set column widths
        self.salary_table.column("id", width=40)
        self.salary_table.column("emp_id", width=80)
        self.salary_table.column("name", width=150)
        self.salary_table.column("department", width=100)
        self.salary_table.column("basic", width=80)
        self.salary_table.column("da", width=80)
        self.salary_table.column("hra", width=80)
        self.salary_table.column("ma", width=80)
        self.salary_table.column("pf", width=80)
        self.salary_table.column("insurance", width=80)
        self.salary_table.column("tax", width=80)
        self.salary_table.column("net_salary", width=100)
        self.salary_table.column("date", width=100)
        
        self.salary_table['show'] = 'headings'
        self.salary_table.pack(fill="both", expand=True)
        
        # Bind the select event
        self.salary_table.bind("<ButtonRelease-1>", self.get_salary_data)
        
        # Fetch all employee IDs for the salary tab combobox
        self.fetch_employee_ids()
        # Fetch all salary records
        self.fetch_salaries()
    
    def fetch_employee_ids(self):
        try:
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            cursor.execute("SELECT emp_id FROM employees")
            employee_ids = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            self.salary_emp_id_combo['values'] = employee_ids
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch employee IDs: {str(e)}")
    
    def fetch_employee_for_salary(self, event=None):
        try:
            selected_emp_id = self.emp_id.get()
            if not selected_emp_id:
                return
                
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name, department FROM employees WHERE emp_id=?", (selected_emp_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                name, department = result
                self.emp_info_label.config(text=f"Name: {name} | Department: {department}")
            else:
                self.emp_info_label.config(text="Employee not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch employee details: {str(e)}")
    
    def calculate_net_salary(self):
        try:
            # Get all salary components
            basic = float(self.basic_salary.get())
            da = float(self.da.get())
            hra = float(self.hra.get())
            ma = float(self.ma.get())
            pf = float(self.pf.get())
            insurance = float(self.insurance.get())
            tax = float(self.tax.get())
            
            # Calculate net salary (earnings - deductions)
            earnings = basic + da + hra + ma
            deductions = pf + insurance + tax
            net_salary = earnings - deductions
            
            # Set the net salary
            self.net_salary.set(net_salary)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for all salary fields.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate net salary: {str(e)}")
    
    def show_login_screen(self):
        # Clear all widgets from the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Initialize the login system
        login_system = login.LoginSystem(self.root, self.on_login_success)
    
    def on_login_success(self, user_type, user_id):
        """Called when login is successful"""
        # Store the user type and ID
        self.user_type = user_type
        self.user_id = user_id
        
        # Clear the login screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Set up the main UI
        self.setup_ui()
        
        # Configure access based on user type
        if user_type == "admin":
            # Admin has full access
            self.fetch_employees()
            self.fetch_employee_ids()
            self.fetch_salaries()
        else:
            # Employee has limited access
            self.setup_employee_access()
    
    def setup_employee_access(self):
        """Configure UI for employee access"""
        # Disable access to Employee Details tab for regular employees
        try:
            # First try to hide the tab if the method exists (newer Tkinter versions)
            self.tabs.hide(0)  # Hide the first tab (Employee Details)
        except AttributeError:
            # If hide method doesn't exist, make the tab non-clickable
            for i, tab in enumerate(self.tabs.tabs()):
                if i == 0:  # Employee Details tab
                    self.tabs.tab(tab, state="disabled")
            # Select the Salary tab since employee can't use the first tab
            self.tabs.select(1)
        
        # Modify salary frame to only show employee's own data
        # and disable editing controls
        if self.user_id:
            # Set the employee ID
            self.emp_id.set(self.user_id)
            
            # Disable the employee ID combobox
            self.salary_emp_id_combo.config(state="disabled")
            
            # Fetch only this employee's salary data
            self.fetch_employee_for_salary()
            self.fetch_employee_salaries()
            
            # Disable buttons for employees
            for child in self.salary_frame.winfo_children():
                if isinstance(child, ttk.LabelFrame):
                    for btn in child.winfo_children():
                        if isinstance(btn, ttk.Frame):
                            for button in btn.winfo_children():
                                if isinstance(button, ttk.Button):
                                    if button.cget("text") in ["Save", "Update", "Delete"]:
                                        button.config(state="disabled")
    
    def fetch_employee_salaries(self):
        """Fetch only the logged-in employee's salary records"""
        try:
            if not self.user_id:
                return
                
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM salaries WHERE emp_id=?", (self.user_id,))
            rows = cursor.fetchall()
            conn.close()
            
            # Clear the table
            for item in self.salary_table.get_children():
                self.salary_table.delete(item)
            
            # Add data to the table
            for row in rows:
                self.salary_table.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch salaries: {str(e)}")
    
    def save_employee(self):
        try:
            # Check permission - only admin can save employees
            if self.user_type != "admin":
                messagebox.showerror("Error", "You don't have permission to perform this action")
                return
                
            # Validate fields
            if not self.validate_employee_fields():
                return
            
            # Validate password
            if not self.password.get():
                messagebox.showerror("Error", "Password is required")
                return
            
            # Hash the password
            hashed_password = hashlib.sha256(self.password.get().encode()).hexdigest()
            
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            
            # Check if employee ID already exists
            cursor.execute("SELECT COUNT(*) FROM employees WHERE emp_id=?", (self.emp_id.get(),))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "Employee ID already exists")
                conn.close()
                return
            
            # Insert employee data
            cursor.execute("""
                INSERT INTO employees (emp_id, name, email, phone, address, gender, department, designation, doj, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.emp_id.get(),
                self.name.get(),
                self.email.get(),
                self.phone.get(),
                self.address.get(),
                self.gender.get(),
                self.department.get(),
                self.designation.get(),
                self.doj.get(),
                hashed_password
            ))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Employee has been added successfully")
            self.fetch_employees()
            self.clear_employee_fields()
            self.fetch_employee_ids()  # Update the employee IDs in the salary tab
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save employee: {str(e)}")
    
    def fetch_employees(self):
        try:
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees")
            rows = cursor.fetchall()
            conn.close()
            
            # Clear the table
            for item in self.employee_table.get_children():
                self.employee_table.delete(item)
            
            # Add data to the table
            for row in rows:
                self.employee_table.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch employees: {str(e)}")
    
    def get_employee_data(self, event=None):
        try:
            selected_item = self.employee_table.focus()
            if selected_item:
                values = self.employee_table.item(selected_item, "values")
                self.clear_employee_fields()
                
                self.emp_id.set(values[0])
                self.name.set(values[1])
                self.email.set(values[2])
                self.phone.set(values[3])
                self.address.set(values[4])
                self.gender.set(values[5])
                self.department.set(values[6])
                self.designation.set(values[7])
                self.doj.set(values[8])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get employee data: {str(e)}")
    
    def update_employee(self):
        try:
            # Check permission - only admin can update employees
            if self.user_type != "admin":
                messagebox.showerror("Error", "You don't have permission to perform this action")
                return
                
            # Validate fields
            if not self.validate_employee_fields():
                return
            
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            
            # Check if password is provided for update
            if self.password.get():
                # Hash the new password
                hashed_password = hashlib.sha256(self.password.get().encode()).hexdigest()
                
                # Update employee data with password
                cursor.execute("""
                    UPDATE employees SET 
                    name=?, email=?, phone=?, address=?, gender=?, 
                    department=?, designation=?, doj=?, password=?
                    WHERE emp_id=?
                """, (
                    self.name.get(),
                    self.email.get(),
                    self.phone.get(),
                    self.address.get(),
                    self.gender.get(),
                    self.department.get(),
                    self.designation.get(),
                    self.doj.get(),
                    hashed_password,
                    self.emp_id.get()
                ))
            else:
                # Update employee data without changing password
                cursor.execute("""
                    UPDATE employees SET 
                    name=?, email=?, phone=?, address=?, gender=?, 
                    department=?, designation=?, doj=?
                    WHERE emp_id=?
                """, (
                    self.name.get(),
                    self.email.get(),
                    self.phone.get(),
                    self.address.get(),
                    self.gender.get(),
                    self.department.get(),
                    self.designation.get(),
                    self.doj.get(),
                    self.emp_id.get()
                ))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Employee has been updated successfully")
            self.fetch_employees()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update employee: {str(e)}")
    
    def delete_employee(self):
        try:
            # Check permission - only admin can delete employees
            if self.user_type != "admin":
                messagebox.showerror("Error", "You don't have permission to perform this action")
                return
                
            selected_emp_id = self.emp_id.get()
            if not selected_emp_id:
                messagebox.showerror("Error", "Please select an employee to delete")
                return
            
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
                conn = sqlite3.connect('payroll.db')
                cursor = conn.cursor()
                
                # Delete employee
                cursor.execute("DELETE FROM employees WHERE emp_id=?", (selected_emp_id,))
                
                # Also delete related salary records
                cursor.execute("DELETE FROM salaries WHERE emp_id=?", (selected_emp_id,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Employee has been deleted successfully")
                self.fetch_employees()
                self.fetch_salaries()
                self.clear_employee_fields()
                self.fetch_employee_ids()  # Update the employee IDs in the salary tab
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete employee: {str(e)}")
    
    def clear_employee_fields(self):
        self.emp_id.set("")
        self.name.set("")
        self.email.set("")
        self.phone.set("")
        self.address.set("")
        self.gender.set("")
        self.department.set("")
        self.designation.set("")
        self.doj.set("")
        self.password.set("")
    
    def search_employee(self):
        try:
            search_by = self.search_by.get()
            search_text = self.search_text.get()
            
            if not search_text:
                messagebox.showerror("Error", "Please enter search text")
                return
            
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            
            # Set search column based on selection
            if search_by == "Employee ID":
                column = "emp_id"
            elif search_by == "Name":
                column = "name"
            elif search_by == "Department":
                column = "department"
            elif search_by == "Designation":
                column = "designation"
            else:
                column = "emp_id"
            
            # Execute search query
            cursor.execute(f"SELECT * FROM employees WHERE {column} LIKE ?", (f"%{search_text}%",))
            rows = cursor.fetchall()
            conn.close()
            
            # Clear the table
            for item in self.employee_table.get_children():
                self.employee_table.delete(item)
            
            # Add search results to the table
            for row in rows:
                self.employee_table.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search employees: {str(e)}")
    
    def validate_employee_fields(self):
        # Validate Employee ID
        if not self.emp_id.get():
            messagebox.showerror("Error", "Employee ID is required")
            return False
        
        # Validate Name
        if not self.name.get():
            messagebox.showerror("Error", "Name is required")
            return False
        
        # Validate Email
        email = self.email.get()
        if email and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            messagebox.showerror("Error", "Invalid email format")
            return False
        
        # Validate Phone
        phone = self.phone.get()
        if phone and not re.match(r'^\d{10,15}$', phone):
            messagebox.showerror("Error", "Phone number should be 10-15 digits")
            return False
        
        # Validate Date of Joining
        doj = self.doj.get()
        if doj:
            try:
                datetime.strptime(doj, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Date of Joining should be in YYYY-MM-DD format")
                return False
        
        return True
    
    def save_salary(self):
        try:
            # Check permission - only admin can save salary records
            if self.user_type != "admin":
                messagebox.showerror("Error", "You don't have permission to perform this action")
                return
                
            # Validate fields
            if not self.validate_salary_fields():
                return
            
            # Calculate net salary if not already calculated
            if not self.net_salary.get():
                self.calculate_net_salary()
            
            # Get employee details
            selected_emp_id = self.emp_id.get()
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            
            # Get employee name and department
            cursor.execute("SELECT name, department FROM employees WHERE emp_id=?", (selected_emp_id,))
            emp_data = cursor.fetchone()
            
            if not emp_data:
                messagebox.showerror("Error", "Employee not found")
                conn.close()
                return
                
            name, department = emp_data
            
            # Insert salary data
            cursor.execute("""
                INSERT INTO salaries (emp_id, name, department, basic_salary, da, hra, ma, pf, insurance, tax, net_salary, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                selected_emp_id,
                name,
                department,
                float(self.basic_salary.get()),
                float(self.da.get()),
                float(self.hra.get()),
                float(self.ma.get()),
                float(self.pf.get()),
                float(self.insurance.get()),
                float(self.tax.get()),
                float(self.net_salary.get()),
                datetime.now().strftime('%Y-%m-%d')
            ))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Salary has been saved successfully")
            self.fetch_salaries()
            self.clear_salary_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save salary: {str(e)}")
    
    def fetch_salaries(self):
        try:
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM salaries")
            rows = cursor.fetchall()
            conn.close()
            
            # Clear the table
            for item in self.salary_table.get_children():
                self.salary_table.delete(item)
            
            # Add data to the table
            for row in rows:
                self.salary_table.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch salary records: {str(e)}")
    
    def get_salary_data(self, event=None):
        try:
            selected_item = self.salary_table.focus()
            if selected_item:
                values = self.salary_table.item(selected_item, "values")
                self.clear_salary_fields()
                
                # Set the selected salary data
                self.emp_id.set(values[1])
                self.fetch_employee_for_salary()  # Update employee info label
                
                self.basic_salary.set(float(values[4]))
                self.da.set(float(values[5]))
                self.hra.set(float(values[6]))
                self.ma.set(float(values[7]))
                self.pf.set(float(values[8]))
                self.insurance.set(float(values[9]))
                self.tax.set(float(values[10]))
                self.net_salary.set(float(values[11]))
                
                # Store the salary ID for update/delete operations
                self.selected_salary_id = values[0]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get salary data: {str(e)}")
    
    def update_salary(self):
        try:
            # Check permission - only admin can update salary records
            if self.user_type != "admin":
                messagebox.showerror("Error", "You don't have permission to perform this action")
                return
                
            # Validate fields
            if not self.validate_salary_fields():
                return
            
            # Check if a salary record is selected
            if not hasattr(self, 'selected_salary_id'):
                messagebox.showerror("Error", "Please select a salary record to update")
                return
            
            # Calculate net salary if not already calculated
            if not self.net_salary.get():
                self.calculate_net_salary()
            
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            
            # Update salary data
            cursor.execute("""
                UPDATE salaries SET 
                emp_id=?, basic_salary=?, da=?, hra=?, ma=?, 
                pf=?, insurance=?, tax=?, net_salary=?
                WHERE id=?
            """, (
                self.emp_id.get(),
                float(self.basic_salary.get()),
                float(self.da.get()),
                float(self.hra.get()),
                float(self.ma.get()),
                float(self.pf.get()),
                float(self.insurance.get()),
                float(self.tax.get()),
                float(self.net_salary.get()),
                self.selected_salary_id
            ))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Salary has been updated successfully")
            self.fetch_salaries()
            self.clear_salary_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update salary: {str(e)}")
    
    def delete_salary(self):
        try:
            # Check permission - only admin can delete salary records
            if self.user_type != "admin":
                messagebox.showerror("Error", "You don't have permission to perform this action")
                return
                
            # Check if a salary record is selected
            if not hasattr(self, 'selected_salary_id'):
                messagebox.showerror("Error", "Please select a salary record to delete")
                return
            
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this salary record?"):
                conn = sqlite3.connect('payroll.db')
                cursor = conn.cursor()
                
                # Delete salary record
                cursor.execute("DELETE FROM salaries WHERE id=?", (self.selected_salary_id,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Salary record has been deleted successfully")
                self.fetch_salaries()
                self.clear_salary_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete salary record: {str(e)}")
    
    def clear_salary_fields(self):
        self.basic_salary.set(0)
        self.da.set(0)
        self.hra.set(0)
        self.ma.set(0)
        self.pf.set(0)
        self.insurance.set(0)
        self.tax.set(0)
        self.net_salary.set(0.0)
        self.emp_info_label.config(text="")
        if hasattr(self, 'selected_salary_id'):
            delattr(self, 'selected_salary_id')
    
    def validate_salary_fields(self):
        # Validate Employee ID
        if not self.emp_id.get():
            messagebox.showerror("Error", "Please select an Employee ID")
            return False
        
        # Validate numeric fields
        numeric_fields = [
            ("Basic Salary", self.basic_salary.get()),
            ("Dearness Allowance", self.da.get()),
            ("House Rent Allowance", self.hra.get()),
            ("Medical Allowance", self.ma.get()),
            ("Provident Fund", self.pf.get()),
            ("Insurance", self.insurance.get()),
            ("Tax", self.tax.get())
        ]
        
        for label, value in numeric_fields:
            try:
                float(value)
            except ValueError:
                messagebox.showerror("Error", f"{label} must be a number")
                return False
        
        return True
    
    def generate_receipt(self):
        try:
            # Check if salary data is selected
            if not hasattr(self, 'selected_salary_id'):
                messagebox.showerror("Error", "Please select a salary record to generate receipt")
                return
            
            # Get salary data
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT s.*, e.address, e.designation, e.phone 
                FROM salaries s 
                JOIN employees e ON s.emp_id = e.emp_id 
                WHERE s.id=?
            """, (self.selected_salary_id,))
            
            salary_data = cursor.fetchone()
            conn.close()
            
            if not salary_data:
                messagebox.showerror("Error", "Salary record not found")
                return
            
            # Generate receipt
            self.receipt_generator.generate_receipt(salary_data)
            
            # Switch to the receipt tab
            self.tabs.select(3)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate receipt: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollManagementSystem(root)
    root.mainloop()
