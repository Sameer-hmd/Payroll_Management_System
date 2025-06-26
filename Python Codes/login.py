import tkinter as tk
from tkinter import ttk, messagebox, StringVar
import sqlite3
import hashlib
import styles

class LoginSystem:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        
        # Set up variables
        self.username = StringVar()
        self.password = StringVar()
        self.user_type = StringVar()
        self.user_type.set("Admin")  # Default selection
        
        # Apply enhanced styles
        styles.configure_styles(root)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Configure the main window
        self.root.title("Payroll Management System - Login")
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Payroll Management System", style="Title.TLabel")
        title_label.pack(pady=20)
        
        # Login Frame
        login_frame = ttk.LabelFrame(main_frame, text="Login")
        login_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True,)
        
        # User Type Selection
        user_type_frame = ttk.Frame(login_frame)
        user_type_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(user_type_frame, text="Login As:").pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            user_type_frame, 
            text="Admin", 
            variable=self.user_type, 
            value="Admin"
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Radiobutton(
            user_type_frame, 
            text="Employee", 
            variable=self.user_type, 
            value="Employee"
        ).pack(side=tk.LEFT, padx=10)
        
        # Add a hint label for users to know login credentials
        hint_frame = ttk.Frame(login_frame)
        hint_frame.pack(fill=tk.X, pady=5)
        ttk.Label(hint_frame, text="Admin: username='admin', password='12345'", foreground="#666666").pack(pady=2)
        ttk.Label(hint_frame, text="Employee: username=Your Employee ID (e.g., 'EMP001', 'EMP002')", foreground="#666666").pack(pady=2)
        ttk.Label(hint_frame, text="Default password for employees is '54321'", foreground="#666666").pack(pady=2)
        
        # Username
        username_frame = ttk.Frame(login_frame)
        username_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(username_frame, text="Username:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(username_frame, textvariable=self.username).pack(side=tk.RIGHT, padx=5, expand=True, fill=tk.X)
        
        # Password
        password_frame = ttk.Frame(login_frame)
        password_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(password_frame, text="Password:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(password_frame, textvariable=self.password, show="*").pack(side=tk.RIGHT, padx=5, expand=True, fill=tk.X)
        
        # Login Button
        button_frame = ttk.Frame(login_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame, 
            text="Login", 
            command=self.login, 
            style="Accent.TButton",
            padding=(20, 10)
        ).pack()
    
    def login(self):
        """Authenticate the user."""
        username = self.username.get().strip()
        password = self.password.get().strip()
        user_type = self.user_type.get()
        
        # Basic validation
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        conn = None
        try:
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            
            if user_type == "Admin":
                # Admin login
                cursor.execute("SELECT username, password FROM admins WHERE LOWER(username) = LOWER(?)", (username,))
                admin = cursor.fetchone()
                
                if admin:
                    stored_password = admin[1]
                    hashed_input_password = hashlib.sha256(password.encode()).hexdigest()
                    
                    if stored_password == hashed_input_password:
                        print(f"Admin login successful: {username}")
                        self.on_login_success(user_type="admin", user_id=None)
                        return
                
                # Fallback for hardcoded admin
                if username.lower() == "admin" and password == "12345":
                    print("Admin login successful with hardcoded credentials")
                    self.on_login_success(user_type="admin", user_id=None)
                    return
                    
                messagebox.showerror("Error", "Invalid admin credentials")
                
            else:  # Employee login
                # Convert employee ID to uppercase for consistency
                emp_id = username.upper()
                
                # Check if employee exists with that ID
                cursor.execute("SELECT emp_id, password FROM employees WHERE emp_id = ?", (emp_id,))
                employee = cursor.fetchone()
                
                if employee:
                    stored_password = employee[1]
                    hashed_input_password = hashlib.sha256(password.encode()).hexdigest()
                    
                    if stored_password == hashed_input_password:
                        print(f"Employee login successful: {emp_id}")
                        self.on_login_success(user_type="employee", user_id=emp_id)
                        return
                
                # Fallback for hardcoded employee
                if emp_id == "EMP001" and password == "54321":
                    print("Employee login successful with hardcoded credentials")
                    self.on_login_success(user_type="employee", user_id=emp_id)
                    return
                
                messagebox.showerror("Error", "Invalid employee credentials")
                
        except Exception as e:
            print(f"Login error: {str(e)}")
            messagebox.showerror("Database Error", f"An error occurred during login: {str(e)}")
        finally:
            if conn:
                conn.close()