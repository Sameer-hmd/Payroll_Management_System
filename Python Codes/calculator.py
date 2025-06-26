import tkinter as tk
from tkinter import ttk, StringVar
import styles

class Calculator:
    def __init__(self, parent):
        self.parent = parent
        self.result_var = StringVar()
        self.result_var.set("0")
        self.current_expression = ""
        
        # Apply enhanced styles
        styles.configure_styles(parent.master)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create a frame to contain the calculator
        calc_frame = ttk.Frame(self.parent, padding=20)
        calc_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Display
        display_frame = ttk.Frame(calc_frame)
        display_frame.pack(fill=tk.X, pady=10)
        
        display = ttk.Entry(
            display_frame, 
            textvariable=self.result_var, 
            font=('Arial', 24),
            justify='right',
            state='readonly'
        )
        display.pack(fill=tk.X, ipady=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(calc_frame)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Define button layout
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('C', 3, 2), ('+', 3, 3),
            ('=', 4, 0, 4)  # Span 4 columns
        ]
        
        # Create buttons
        for button_def in buttons:
            text = button_def[0]
            row = button_def[1]
            col = button_def[2]
            
            # Check if button spans multiple columns
            if len(button_def) > 3:
                colspan = button_def[3]
                ttk.Button(
                    buttons_frame, 
                    text=text, 
                    command=lambda t=text: self.button_click(t),
                    style="Accent.TButton" if text == "=" else "TButton",
                    padding=10
                ).grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)
            else:
                ttk.Button(
                    buttons_frame, 
                    text=text, 
                    command=lambda t=text: self.button_click(t),
                    style="Accent.TButton" if text in "+-*/=" else "TButton",
                    padding=10
                ).grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights for responsive sizing
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)
    
    def button_click(self, value):
        try:
            if value == "=":
                # Calculate result
                result = eval(self.current_expression) if self.current_expression else 0
                self.result_var.set(str(result))
                self.current_expression = str(result)
            elif value == "C":
                # Clear display
                self.result_var.set("0")
                self.current_expression = ""
            else:
                # Append digit or operator
                self.current_expression += value
                self.result_var.set(self.current_expression)
        except Exception as e:
            self.result_var.set("Error")
            self.current_expression = ""
