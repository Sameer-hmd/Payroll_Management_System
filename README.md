# Payroll Management System

A comprehensive Python Tkinter-based payroll management system designed for efficient employee data handling and financial processing.

## Features

- User authentication with role-based access (admin/employee)
- Employee data management
- Automated salary calculation
- PDF and TXT receipt generation
- Built-in calculator for quick calculations
- SQLite database integration

## Default Credentials

### Admin Login
- Username: `admin` (case-insensitive)
- Password: `12345`

### Employee Login
- Username: Employee ID (e.g., `EMP001`)
- Password: `54321`

## Main Components

The system consists of four primary frames:

1. **Employee Details**: For managing employee information
2. **Salary Management**: For calculating and processing employee salaries
3. **Calculator**: For quick calculations
4. **Salary Receipt**: For generating printable salary receipts

## Running the System

1. Run the system with: `python payroll_system.py`
2. Login using the default credentials provided above
3. Navigate between the different frames using the tabs

## Admin vs Employee Access

- **Admin**: Full access to add, edit, and delete all employee records and salaries
- **Employee**: Restricted access to view only their personal information and salary details

## File Structure

- `payroll_system.py`: Main application
- `database.py`: Database operations
- `login.py`: Authentication system
- `calculator.py`: Calculator utility
- `receipt.py`: Receipt generation
- `styles.py`: UI styling

Key Files and Their Purposes

1. payroll_system.py - The main application file that:
    Sets up the user interface with four tabs (Employee Details, Salary Management, Calculator, Salary Receipt)
    Handles employee and salary data management
    Integrates all components together

2. login.py - Handles user authentication:
    Provides login screen with admin/employee options
    Authenticates users against the database
    Implements case-insensitive username comparison
    Updates user access level based on credentials

3. database.py - Manages database operations:
    Creates and initializes the SQLite database
    Sets up tables for employees, salaries, and admins
    Creates default admin (username: admin, password: 12345)
    Creates sample employee (ID: EMP001, password: 54321)

4. calculator.py - Simple calculator utility:
    Provides basic arithmetic operations
    Features a clean, responsive interface
    
5. receipt.py - Generates salary receipts:
    Creates formatted text previews of salary receipts
    Exports receipts as TXT files
    Generates professional PDF receipts using ReportLab
    Includes employee details and salary breakdown

6. styles.py - Defines application styling:
    Material Design-inspired color scheme
    Consistent font styles and button appearances
    Responsive layout configurations

7. Login Credentials
    Admin Login: Username: admin, Password: 12345
    Employee Login: Username: EMP001, Password: 54321

Both login types work with the updated credentials, and username comparison is now case-insensitive for admin logins.

The application has a clean, professional appearance with responsive controls and consistent styling throughout all components.
