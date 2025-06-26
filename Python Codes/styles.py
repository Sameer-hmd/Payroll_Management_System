"""
Enhanced Styles for the Payroll Management System
"""


# Color scheme (Material Design inspired)
BG_COLOR = "#f5f5f5"  # Light gray background
PRIMARY_COLOR = "#1976d2"  # Blue
SECONDARY_COLOR = "#b0bec5"  # Light blue-gray
SUCCESS_COLOR = "#4caf50"  # Green
WARNING_COLOR = "#ff9800"  # Orange
ERROR_COLOR = "#f44336"  # Red
ACCENT_COLOR = "#9c27b0"  # Purple
INFO_COLOR = "#2196f3"  # Light blue
DARK_BG_COLOR = "#37474f"  # Dark blue-gray
LIGHT_TEXT_COLOR = "#ffffff"  # White
DARK_TEXT_COLOR = "#212121"  # Very dark gray
MEDIUM_GRAY = "#757575"  # Medium gray
BORDER_COLOR = "#e0e0e0"  # Light gray for borders
HIGHLIGHT_COLOR = "#bbdefb"  # Very light blue

# Font definitions - using more modern fonts if available
HEADING_FONT = ("Segoe UI", 14, "bold")  # Windows-friendly modern font
SUBHEADING_FONT = ("Segoe UI", 12, "bold")
NORMAL_FONT = ("Segoe UI", 11)
SMALL_FONT = ("Segoe UI", 9)
BUTTON_FONT = ("Segoe UI", 11, "bold")
TITLE_FONT = ("Segoe UI", 35, "bold")
MONOSPACE_FONT = ("Consolas", 10)  # Better monospace font for receipts

# Button style - improved padding for better touch/click targets
BTN_PADDING = [15, 8]  # [horizontal, vertical]
ENTRY_PADDING = [8, 8]  # Larger entry padding for better visibility

# Common dimensions
TABLE_ROW_HEIGHT = 35  # Slightly taller for better readability

def configure_styles(root):
    """Configure ttk styles for the application."""
    import tkinter as tk
    from tkinter import ttk
    
    style = ttk.Style(root)
    
    # Try to set a modern theme if available
    try:
        style.theme_use('clam')  # 'clam' is generally more customizable
    except tk.TclError:
        pass  # Fall back to default if not available
    
    # Base styles
    style.configure('TFrame', background=BG_COLOR)
    style.configure('TLabel', background=BG_COLOR, font=NORMAL_FONT, foreground=DARK_TEXT_COLOR)
    style.configure('Bold.TLabel', background=BG_COLOR, font=SUBHEADING_FONT, foreground=DARK_TEXT_COLOR)
    style.configure('Title.TLabel', background=BG_COLOR, font=TITLE_FONT, foreground=PRIMARY_COLOR)
    
    # Button styles
    style.configure('TButton', 
                   font=BUTTON_FONT, 
                   background=PRIMARY_COLOR, 
                   foreground=LIGHT_TEXT_COLOR,
                   padding=BTN_PADDING)
    
    style.configure('Accent.TButton', 
                   font=BUTTON_FONT, 
                   background=ACCENT_COLOR, 
                   foreground=LIGHT_TEXT_COLOR,
                   padding=BTN_PADDING)
    
    style.configure('Warning.TButton', 
                   font=BUTTON_FONT, 
                   background=WARNING_COLOR, 
                   foreground=DARK_TEXT_COLOR,
                   padding=BTN_PADDING)
    
    style.configure('Success.TButton', 
                   font=BUTTON_FONT, 
                   background=SUCCESS_COLOR, 
                   foreground=LIGHT_TEXT_COLOR,
                   padding=BTN_PADDING)
    
    style.configure('Danger.TButton', 
                   font=BUTTON_FONT, 
                   background=ERROR_COLOR, 
                   foreground=LIGHT_TEXT_COLOR,
                   padding=BTN_PADDING)
    
    style.configure('Info.TButton', 
                   font=BUTTON_FONT, 
                   background=INFO_COLOR, 
                   foreground=LIGHT_TEXT_COLOR,
                   padding=BTN_PADDING)
    
    # Button hover states
    style.map('TButton', 
             background=[('active', SECONDARY_COLOR)],
             foreground=[('active', DARK_TEXT_COLOR)])
    
    style.map('Accent.TButton', 
             background=[('active', '#1565c0')],
             foreground=[('active', LIGHT_TEXT_COLOR)])
    
    style.map('Warning.TButton', 
             background=[('active', '#e68a00')],
             foreground=[('active', DARK_TEXT_COLOR)])
    
    style.map('Success.TButton', 
             background=[('active', '#3d8b40')],
             foreground=[('active', LIGHT_TEXT_COLOR)])
    
    style.map('Danger.TButton', 
             background=[('active', '#d32f2f')],
             foreground=[('active', LIGHT_TEXT_COLOR)])
    
    style.map('Info.TButton', 
             background=[('active', '#1976d2')],
             foreground=[('active', LIGHT_TEXT_COLOR)])
    
    # Form controls with enhanced styling for a modern look
    style.configure('TEntry', 
                   font=NORMAL_FONT, 
                   padding=ENTRY_PADDING,
                   fieldbackground=LIGHT_TEXT_COLOR,
                   background=LIGHT_TEXT_COLOR,
                   bordercolor=BORDER_COLOR,  # Defined border color
                   relief="solid",  # Consistent relief style
                   borderwidth=1)  # Thinner border for modern look
                   
    # Add focus effect for entry fields 
    style.map('TEntry',
              bordercolor=[('focus', PRIMARY_COLOR)],
              lightcolor=[('focus', PRIMARY_COLOR)], 
              darkcolor=[('focus', PRIMARY_COLOR)],
              borderwidth=[('focus', 1)])  # Keep same thickness on focus
    
    # Enhanced dropdown styling
    style.configure('TCombobox', 
                   font=NORMAL_FONT, 
                   padding=ENTRY_PADDING,
                   fieldbackground=LIGHT_TEXT_COLOR,
                   background=LIGHT_TEXT_COLOR,
                   arrowsize=15,  # Larger dropdown arrow
                   relief="solid",
                   borderwidth=1)
    
    # Improved dropdown selection styling
    style.map('TCombobox', 
             fieldbackground=[('readonly', LIGHT_TEXT_COLOR)],
             selectbackground=[('readonly', PRIMARY_COLOR)],
             selectforeground=[('readonly', LIGHT_TEXT_COLOR)],
             bordercolor=[('focus', PRIMARY_COLOR)],
             lightcolor=[('focus', PRIMARY_COLOR)],
             darkcolor=[('focus', PRIMARY_COLOR)])
    
    # Treeview styles (tables) with enhanced styling
    style.configure('Treeview', 
                   font=NORMAL_FONT, 
                   rowheight=TABLE_ROW_HEIGHT,
                   background=LIGHT_TEXT_COLOR,
                   fieldbackground=LIGHT_TEXT_COLOR,
                   borderwidth=1,
                   relief="solid")
    
    style.configure('Treeview.Heading', 
                   font=SUBHEADING_FONT,
                   background=PRIMARY_COLOR,
                   foreground=LIGHT_TEXT_COLOR,
                   padding=[5, 5],  # Added padding for better appearance
                   relief="raised")  # Add some depth to headings
    
    # Better selection highlighting with alternating row colors
    style.map('Treeview', 
             background=[('selected', HIGHLIGHT_COLOR), ('alternate', '#f9f9f9')],
             foreground=[('selected', DARK_TEXT_COLOR)])
             
    # Add alternating row colors if possible (may not work on all platforms)
    try:
        style.configure('Treeview', rowheight=TABLE_ROW_HEIGHT)
        style.map('Treeview', 
                 foreground=[('selected', DARK_TEXT_COLOR)])
    except:
        pass
    
    # Frames and containers with enhanced styling
    style.configure('TLabelframe', 
                   background=BG_COLOR, 
                   bordercolor=PRIMARY_COLOR,  # Changed to primary color for more distinction
                   borderwidth=1,  # Thinner border for a modern look
                   relief='groove')  # More subtle 3D effect
    
    style.configure('TLabelframe.Label', 
                   background=BG_COLOR, 
                   font=SUBHEADING_FONT,
                   foreground=PRIMARY_COLOR,
                   padding=[5, 3])  # Add padding to frame labels
    
    # Notebook (tabbed interface) with modernized styling
    style.configure('TNotebook', 
                   background=BG_COLOR,
                   borderwidth=0)
    
    # Modernized tabs with more prominent styling
    style.configure('TNotebook.Tab', 
                   font=BUTTON_FONT,  # Using button font for consistency 
                   padding=[15, 10],  # Larger padding for better touch targets
                   background=SECONDARY_COLOR,
                   foreground=DARK_TEXT_COLOR,
                   borderwidth=0)  # Remove borders for cleaner look
    
    # Enhanced tab selection effects
    style.map('TNotebook.Tab', 
             background=[('selected', PRIMARY_COLOR), ('active', HIGHLIGHT_COLOR)],
             foreground=[('selected', LIGHT_TEXT_COLOR), ('active', DARK_TEXT_COLOR)],
             expand=[('selected', [2, 2, 2, 0])],
             # Add bottom border to selected tab
             borderwidth=[('selected', 0), ('active', 0)],
             relief=[('selected', 'flat')])
    
    # Separator
    style.configure('TSeparator', background=BORDER_COLOR)
    
    # Scale (slider)
    style.configure('TScale', background=BG_COLOR, troughcolor=SECONDARY_COLOR)
    
    # Progressbar
    style.configure('TProgressbar', 
                   background=PRIMARY_COLOR,
                   troughcolor=BG_COLOR,
                   bordercolor=BORDER_COLOR)
    
    # Modify text widget styling (not directly possible with ttk)
    root.option_add('*Text.font', NORMAL_FONT)
    root.option_add('*Text.background', LIGHT_TEXT_COLOR)
    root.option_add('*Text.foreground', DARK_TEXT_COLOR)
    root.option_add('*Text.borderwidth', 1)
    root.option_add('*Text.relief', 'solid')


    