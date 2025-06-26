import sqlite3
import hashlib
import os

def initialize_db():
    """Initialize the database and create tables if they don't exist."""
    conn = None
    try:
        conn = sqlite3.connect('payroll.db')
        cursor = conn.cursor()
        
        # Create employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                emp_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                gender TEXT,
                department TEXT,
                designation TEXT,
                doj TEXT,
                password TEXT NOT NULL
            )
        ''')
        
        # Create salaries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS salaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id TEXT NOT NULL,
                name TEXT NOT NULL,
                department TEXT,
                basic_salary REAL NOT NULL,
                da REAL NOT NULL,
                hra REAL NOT NULL,
                ma REAL NOT NULL,
                pf REAL NOT NULL,
                insurance REAL NOT NULL,
                tax REAL NOT NULL,
                net_salary REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
            )
        ''')
        
        # Create admin table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # Check if admin account exists, if not create a default one
        cursor.execute("SELECT COUNT(*) FROM admins WHERE username = ?", ("admin",))
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Create default admin account only if it doesn't exist
            admin_password = "12345"
            hashed_admin_password = hashlib.sha256(admin_password.encode()).hexdigest()
            cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", 
                          ("admin", hashed_admin_password))
            print(f"Default admin account created: Username: admin, Password: {admin_password}")
        
        # Check if sample employee exists, if not create one
        cursor.execute("SELECT COUNT(*) FROM employees WHERE emp_id = ?", ("EMP001",))
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Create a sample employee for testing only if it doesn't exist
            emp_id = "EMP001"
            name = "John Doe"
            email = "john.doe@example.com"
            phone = "1234567890"
            address = "123 Main St, City"
            gender = "Male"
            department = "IT"
            designation = "Developer"
            doj = "2023-01-01"
            emp_password = "54321"
            
            # Hash the employee password
            hashed_emp_password = hashlib.sha256(emp_password.encode()).hexdigest()
            
            # Insert sample employee
            cursor.execute('''
                INSERT INTO employees (emp_id, name, email, phone, address, gender, 
                                      department, designation, doj, password) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (emp_id, name, email, phone, address, gender, 
                  department, designation, doj, hashed_emp_password))
            
            print(f"Sample employee account created: ID: {emp_id}, Password: {emp_password}")
            
            # Check if sample salary record exists
            cursor.execute("SELECT COUNT(*) FROM salaries WHERE emp_id = ?", (emp_id,))
            salary_count = cursor.fetchone()[0]
            
            if salary_count == 0:
                # Create a test salary entry for the sample employee
                cursor.execute('''
                    INSERT INTO salaries (emp_id, name, department, basic_salary, da, hra, ma, pf, insurance, tax, net_salary, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (emp_id, name, department, 50000, 5000, 10000, 2000, 3000, 1500, 2500, 60000, "2023-04-19"))
        
        conn.commit()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        if conn:
            conn.close()
    finally:
        if conn:
            conn.close()

def check_connection():
    """Check if the database connection works."""
    conn = None
    try:
        conn = sqlite3.connect('payroll.db')
        cursor = conn.cursor()
        
        # Check admins table
        cursor.execute("SELECT * FROM admins")
        admins = cursor.fetchall()
        print(f"Admins in database: {admins}")
        
        # Check employees table
        cursor.execute("SELECT emp_id, name, password FROM employees")
        employees = cursor.fetchall()
        print(f"Employees in database: {employees}")
        
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()
        conn.close()
        return f"SQLite version: {version[0]}"
    except Exception as e:
        if conn:
            conn.close()
        return f"Error connecting to database: {str(e)}"
