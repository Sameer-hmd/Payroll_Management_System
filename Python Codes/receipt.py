import tkinter as tk
from tkinter import ttk, messagebox
import styles
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
from datetime import datetime


class ReceiptGenerator:

    def __init__(self, parent):
        self.parent = parent
        self.current_receipt_data = None
        
        # Apply enhanced styles
        styles.configure_styles(parent.master)
        
        self.setup_ui()

    def setup_ui(self):
        # Create a frame to contain the receipt view
        receipt_frame = ttk.Frame(self.parent, padding=20)
        receipt_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create a frame for the receipt display
        self.display_frame = ttk.LabelFrame(receipt_frame,
                                            text="Salary Receipt Preview")
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a text widget to display the receipt
        self.receipt_text = tk.Text(self.display_frame,
                                    width=80,
                                    height=30,
                                    font=styles.MONOSPACE_FONT,
                                    bg=styles.LIGHT_TEXT_COLOR,
                                    fg=styles.DARK_TEXT_COLOR,
                                    relief="solid",
                                    borderwidth=1)
        self.receipt_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create a frame for buttons
        button_frame = ttk.Frame(receipt_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # Add print and export buttons
        button_container = ttk.Frame(button_frame)
        button_container.pack(side=tk.RIGHT)

        self.export_txt_button = ttk.Button(button_container,
                                            text="Export as TXT",
                                            command=self.export_as_txt,
                                            style="Warning.TButton")
        self.export_txt_button.pack(side=tk.LEFT, padx=5)

        self.print_button = ttk.Button(button_container,
                                       text="Print PDF Receipt",
                                       command=self.print_receipt,
                                       style="Success.TButton")
        self.print_button.pack(side=tk.LEFT, padx=5)

        # Initially disable buttons until a receipt is generated
        self.print_button.config(state=tk.DISABLED)
        self.export_txt_button.config(state=tk.DISABLED)

    def generate_receipt(self, salary_data):
        """Generate a receipt preview from salary data."""
        try:
            # Store the current receipt data for printing
            self.current_receipt_data = salary_data

            # Clear the text widget
            self.receipt_text.delete(1.0, tk.END)

            # Extract data from salary_data tuple
            salary_id = salary_data[0]
            emp_id = salary_data[1]
            name = salary_data[2]
            department = salary_data[3]
            basic_salary = salary_data[4]
            da = salary_data[5]
            hra = salary_data[6]
            ma = salary_data[7]
            pf = salary_data[8]
            insurance = salary_data[9]
            tax = salary_data[10]
            net_salary = salary_data[11]
            date = salary_data[12]
            address = salary_data[13]
            designation = salary_data[14]
            phone = salary_data[15]

            # Format the receipt
            self.receipt_text.insert(tk.END, f"{' '*20}COMPANY NAME\n")
            self.receipt_text.insert(tk.END,
                                     f"{' '*15}EMPLOYEE SALARY RECEIPT\n")
            self.receipt_text.insert(tk.END, f"{'-'*80}\n\n")

            self.receipt_text.insert(
                tk.END, f"Receipt No: {salary_id}{' '*20}Date: {date}\n\n")

            self.receipt_text.insert(tk.END, f"Employee ID: {emp_id}\n")
            self.receipt_text.insert(tk.END, f"Employee Name: {name}\n")
            self.receipt_text.insert(tk.END, f"Department: {department}\n")
            self.receipt_text.insert(tk.END, f"Designation: {designation}\n")
            self.receipt_text.insert(tk.END, f"Address: {address}\n")
            self.receipt_text.insert(tk.END, f"Phone: {phone}\n\n")

            self.receipt_text.insert(tk.END, f"{'-'*80}\n")
            self.receipt_text.insert(
                tk.END,
                f"{'EARNINGS':<30}{'AMOUNT':<15}{'DEDUCTIONS':<20}{'AMOUNT':<15}\n"
            )
            self.receipt_text.insert(tk.END, f"{'-'*80}\n")

            self.receipt_text.insert(
                tk.END,
                f"{'Basic Salary':<30}{basic_salary:<15}{'Provident Fund':<20}{pf:<15}\n"
            )
            self.receipt_text.insert(
                tk.END,
                f"{'Dearness Allowance':<30}{da:<15}{'Insurance':<20}{insurance:<15}\n"
            )
            self.receipt_text.insert(
                tk.END,
                f"{'House Rent Allowance':<30}{hra:<15}{'Tax':<20}{tax:<15}\n")
            self.receipt_text.insert(
                tk.END, f"{'Medical Allowance':<30}{ma:<15}{'':<20}{'':<15}\n")

            self.receipt_text.insert(tk.END, f"{'-'*80}\n")

            total_earnings = basic_salary + da + hra + ma
            total_deductions = pf + insurance + tax

            self.receipt_text.insert(
                tk.END,
                f"{'Total Earnings':<30}{total_earnings:<15}{'Total Deductions':<20}{total_deductions:<15}\n"
            )
            self.receipt_text.insert(tk.END, f"{'-'*80}\n\n")

            self.receipt_text.insert(tk.END, f"Net Salary: {net_salary}\n\n")

            self.receipt_text.insert(tk.END, f"{'-'*80}\n")
            self.receipt_text.insert(
                tk.END,
                f"This is a computer-generated receipt and does not require a signature.\n"
            )

            # Enable the print and export buttons
            self.print_button.config(state=tk.NORMAL)
            self.export_txt_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error",
                                 f"Failed to generate receipt: {str(e)}")

    def export_as_txt(self):
        """Export the receipt as a text file."""
        try:
            if not self.current_receipt_data:
                messagebox.showerror("Error", "No receipt data available")
                return

            # Extract basic data from salary_data tuple
            emp_id = self.current_receipt_data[1]
            name = self.current_receipt_data[2]

            # Create receipts directory if it doesn't exist
            if not os.path.exists('receipts'):
                os.makedirs('receipts')

            # Create text filename
            filename = f"receipts/salary_receipt_{emp_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

            # Get the text content from the text widget
            receipt_content = self.receipt_text.get(1.0, tk.END)

            # Write the content to a text file
            with open(filename, 'w') as file:
                file.write(receipt_content)

            messagebox.showinfo("Success",
                                f"Receipt has been exported to {filename}")

            # Try to open the text file
            try:
                import subprocess
                import platform

                if platform.system() == 'Windows':
                    subprocess.Popen(['start', '', filename], shell=True)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.call(('open', filename))
                else:  # Linux
                    subprocess.call(('xdg-open', filename))
            except Exception as e:
                messagebox.showinfo(
                    "Info",
                    f"Text file saved to {filename}, but could not open automatically."
                )
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to export receipt as text: {str(e)}")

    def print_receipt(self):
        """Generate PDF and open it."""
        try:
            if not self.current_receipt_data:
                messagebox.showerror("Error", "No receipt data available")
                return

            # Extract data from salary_data tuple
            salary_id = self.current_receipt_data[0]
            emp_id = self.current_receipt_data[1]
            name = self.current_receipt_data[2]
            department = self.current_receipt_data[3]
            basic_salary = self.current_receipt_data[4]
            da = self.current_receipt_data[5]
            hra = self.current_receipt_data[6]
            ma = self.current_receipt_data[7]
            pf = self.current_receipt_data[8]
            insurance = self.current_receipt_data[9]
            tax = self.current_receipt_data[10]
            net_salary = self.current_receipt_data[11]
            date = self.current_receipt_data[12]
            address = self.current_receipt_data[13]
            designation = self.current_receipt_data[14]
            phone = self.current_receipt_data[15]

            # Create PDF directory if it doesn't exist
            if not os.path.exists('receipts'):
                os.makedirs('receipts')

            # Create PDF filename
            filename = f"C:/Users/@/OneDrive/Desktop/Replit python/receipts/salary_receipt_{emp_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

            # Create the PDF
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles_sheet = getSampleStyleSheet()

            # Create custom paragraph style
            title_style = ParagraphStyle(
                'Title',
                parent=styles_sheet['Title'],
                alignment=1,  # Center
                fontName='Helvetica-Bold',
                fontSize=16)

            # Create a list to hold the content
            content = []

            # Add company title
            content.append(Paragraph("COMPANY NAME", title_style))
            content.append(Paragraph("EMPLOYEE SALARY RECEIPT", title_style))
            content.append(Spacer(1, 0.25 * inch))

            # Add receipt info
            content.append(
                Paragraph(
                    f"Receipt No: {salary_id}                  Date: {date}",
                    styles_sheet['Normal']))
            content.append(Spacer(1, 0.15 * inch))

            # Add employee info
            content.append(
                Paragraph(f"Employee ID: {emp_id}", styles_sheet['Normal']))
            content.append(
                Paragraph(f"Employee Name: {name}", styles_sheet['Normal']))
            content.append(
                Paragraph(f"Department: {department}", styles_sheet['Normal']))
            content.append(
                Paragraph(f"Designation: {designation}",
                          styles_sheet['Normal']))
            content.append(
                Paragraph(f"Address: {address}", styles_sheet['Normal']))
            content.append(Paragraph(f"Phone: {phone}",
                                     styles_sheet['Normal']))
            content.append(Spacer(1, 0.15 * inch))

            # Create earnings and deductions table
            earnings_data = [
                ["EARNINGS", "AMOUNT", "DEDUCTIONS", "AMOUNT"],
                [
                    "Basic Salary", f"{basic_salary:.2f}", "Provident Fund",
                    f"{pf:.2f}"
                ],
                [
                    "Dearness Allowance", f"{da:.2f}", "Insurance",
                    f"{insurance:.2f}"
                ],
                ["House Rent Allowance", f"{hra:.2f}", "Tax", f"{tax:.2f}"],
                ["Medical Allowance", f"{ma:.2f}", "", ""],
                [
                    "Total Earnings", f"{(basic_salary + da + hra + ma):.2f}",
                    "Total Deductions", f"{(pf + insurance + tax):.2f}"
                ],
            ]

            # Create the table
            table = Table(earnings_data,
                          colWidths=[2 * inch, 1 * inch, 2 * inch, 1 * inch])

            # Style the table
            table.setStyle(
                TableStyle([
                    ('BACKGROUND', (0, 0), (3, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (3, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (3, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (3, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (3, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (3, 0), 12),
                    ('BACKGROUND', (0, -1), (3, -1), colors.beige),
                    ('FONTNAME', (0, -1), (3, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                    ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
                ]))

            content.append(table)
            content.append(Spacer(1, 0.25 * inch))

            # Add net salary
            content.append(
                Paragraph(f"<b>Net Salary: {net_salary:.2f}</b>",
                          styles_sheet['Normal']))
            content.append(Spacer(1, 0.25 * inch))

            # Add footer
            content.append(
                Paragraph(
                    "This is a computer-generated receipt and does not require a signature.",
                    styles_sheet['Italic']))

            # Build the PDF
            doc.build(content)

            messagebox.showinfo("Success",
                                f"Receipt has been saved to {filename}")

            # Try to open the PDF file
            try:
                import subprocess
                import platform

                if platform.system() == 'Windows':
                    subprocess.Popen(['start', '', filename], shell=True)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.call(('open', filename))
                else:  # Linux
                    subprocess.call(('xdg-open', filename))
            except Exception as e:
                messagebox.showinfo(
                    "Info",
                    f"PDF file saved to {filename}, but could not open automatically."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print receipt: {str(e)}")
