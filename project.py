"""
Project Title:               Simple GUI-IZED (Gooey-Eyes) RegEx Crossword Puzzle
Name:                        Carl Jayvin T. Lee
GitHub and edX usernames:    Longicolnis and CJLee16
City and Country:            Quezon City, Philippines
Date:                        April 30, 2025
"""

import tkinter as tk
from tkinter import messagebox
import re

# Global var: RegEx Patterns, Grid List & Root 
row_regex = [
    r"0?1?0*1+",
    r"[^0]+0?1+0",
    r"[^1]0?1*0+[^1]",
    r"01+01",
    r"1+01+"
]
col_regex = [
    r"1+0+1",
    r"1?0101*0?",
    r"0+1+",
    r"1*0[^1][^0]",
    r"1+0*1*0?"
]
grid_entries = []  # Store entry widgets
root = None        # For Shortcuts

def main():
    # Initialize the main application window
    global root
    root = tk.Tk()
    root.title("Regular Expression Crossword Puzzle")  # Title of the Window
    root.geometry("500x500")
    root.resizable(False, False)

    # Load UI components
    menu(root)
    create_label(root)
    center_frame(root)
    button(root)

    # Set window close protocol and shortcuts (future: Save/Undo/Redo)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.bind("<Control-Return>", shortcut)
    root.mainloop()  # Start the Tkinter main loop

def menu(root):
    # Create a menubar
    menubar = tk.Menu(root)

    # File Menu
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=on_closing)  # Use quit() to exit properly
    filemenu.add_command(label="Force Exit", command=root.quit)
    filemenu.add_separator()
    filemenu.add_command(label="Save Progress")

    # Action Menu
    actionmenu = tk.Menu(menubar, tearoff=0)
    actionmenu.add_command(label="Undo (Ctrl + Z)")
    actionmenu.add_command(label="Redo (Ctrl + Y)")
    actionmenu.add_separator()
    actionmenu.add_command(label="Show Answer (Ctrl + Enter)", command=show_ans)
    
    # Help Menu
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Instructions", command=instructs)

    # Cascade adding
    menubar.add_cascade(menu=filemenu, label="File")
    menubar.add_cascade(menu=actionmenu, label="Action")
    menubar.add_cascade(menu=helpmenu, label="Help")
    root.config(menu=menubar)

def shortcut(event):
    # Trigger answer reveal on Ctrl+Enter
    if event.state == 4 and event.keysym == "Return":  # Ctrl+Enter
        show_ans()

def instructs():
    # Show instruction dialog box
    instructions = (
        "🧩 Instructions: How to Play\n\n"
        "Be sure to familiarize with Regular Expressions"
        "1. Fill the grid with 0s and 1s to match all row and column regex patterns.\n"
        "2. Each cell accepts only 0 or 1; no blanks allowed.\n"
        "3. Syntax:\n"
        "   • n – 100% n\n"
        "   • n* – 0 or more n\n"
        "   • n+ – 1 o more n\n"
        "   • n? – 0 or 1 n\n"
        "   • [^n] – not n\n"
        "4. Buttons:\n"
        "   ✅ Check – Validates your input.\n"
        "   🔄 Reset – Clears the grid.\n"
        "   👁️ Show Answer – Displays the correct answer.\n"
        "5. Match all patterns to win. Good luck!"
    )
    messagebox.showinfo("Instructions", instructions)
    
def on_closing():
    # Confirm quit prompt
    if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
        root.destroy()

def center_frame(root):
    # Frame for horizontal centering
    center_frame = tk.Frame(root)
    center_frame.pack(pady=10)

    # Load column and grid labels
    col_labels(center_frame)
    grid_labels(center_frame)

def create_label(root):
    # Top label with motivational message
    label = tk.Label(root, text="Match the numbers based on the clues.\nGood luck!",
                     font=('Century Gothic', 15))
    label.pack(padx=20,pady=20)

def col_labels(center_frame):
    # Display column regex clues rotated vertically
    for col in range(len(col_regex)):
        # Increased width and height for better spacing
        canvas = tk.Canvas(center_frame, width=60, height=100)
        canvas.grid(row=1, column=col+1, padx=5, pady=5)

        # Adjusted position of the rotated text
        canvas.create_text(30, 50, text=col_regex[col], angle=270, font=('Century Gothic', 11))

def grid_labels(center_frame):
    # Create 5 rows and 5 columns inside the center_frame
    for row in range(len(row_regex)):  # Adjusted for 5 rows
        global grid_entries # Row label
        grid_entries = []
        for row in range(len(row_regex)):
            # Display row regex clues on the left
            row_label = tk.Label(center_frame, text=f"{row_regex[row]}", font=('Century Gothic', 11))
            row_label.grid(row=row+2, column=0, padx=4, pady=5)

            row_entries = []
            for col in range(len(col_regex)):  # Adjusted for 5 columns
                # Validation that it's only 1 Character per Box
                vcmd = center_frame.register(validate_entry)
                entry = tk.Entry(center_frame, width=2, font=('Century Gothic', 16), justify='center',
                validate='key', validatecommand=(vcmd, '%P'))

                entry.grid(row=row+2, column=col+1, padx=5, pady=5)
                row_entries.append(entry)
            grid_entries.append(row_entries)

def check_grid():
    # Validate current grid input against regex patterns
    user_grid = []
    result = ""
    for row in range(len(row_regex)):
        row_data = ""
        for col in range(len(col_regex)):
            value = grid_entries[row][col].get().strip()
            # Check if there are empty boxes
            if value == "":
                messagebox.showwarning("Missing Input", f"Please fill up the box first!")
                return
            # Check if there are non-binary inputs
            elif value not in ('0', '1'):
                messagebox.showwarning("Invalid Input", f"Only 0 or 1 allowed, Error at ({row+1},{col+1})")
                return
            row_data += value
        user_grid.append(row_data)
    
    # Validate each row against its regex
    for i in range(len(row_regex)):
        if not re.fullmatch(row_regex[i], user_grid[i]):
            messagebox.showerror("Row Error", f"Row {i+1} doesn't match the pattern!")
            result="Invalid"
            return
    
    # Validate each column against its regex
    for j in range(len(row_regex)):
        column_data = "".join(user_grid[i][j] for i in range(len(row_regex)))
        if not re.fullmatch(col_regex[j], column_data):
            messagebox.showerror("Column Error", f"Column {j+1} doesn't match the pattern!")
            result="Invalid"
            return
    
    result="Valid"
    messagebox.showinfo("Success!", "Congratulations! All entries are valid.")
    return result

def validate_grid(grid):
    """
    Validates a 2D list of binary strings against row and column regexes.
    Returns 'Valid' or 'Invalid' for PyTest
    """
    # Check for proper grid dimensions
    if len(grid) != len(row_regex) or any(len(row) != len(col_regex) for row in grid):
        return "Invalid"
    
    # Check all entries for validity (only '0' and '1')
    for row in grid:
        if any(char not in ('0', '1') for char in row):
            return "Invalid"
    
    # Validate each row
    for i, pattern in enumerate(row_regex):
        if not re.fullmatch(pattern, grid[i]):
            return "Invalid"

    # Validate each column
    for j, pattern in enumerate(col_regex):
        column_data = ''.join(grid[i][j] for i in range(len(row_regex)))
        if not re.fullmatch(pattern, column_data):
            return "Invalid"
    
    return "Valid"

# Vertification of entry
def validate_entry(text):
    # Allow only 0, 1, or empty input
    return text in ('', '0', '1')

# Button initializations
def button(root):
    # Create and pack Check, Reset, and Show Answer buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    check_button = tk.Button(button_frame, text="Check", font=('Century Gothic', 14), command=check_grid)
    reset_button = tk.Button(button_frame, text="Reset", font=('Century Gothic', 14), command=reset_grid)
    ans_button = tk.Button(button_frame, text="Show Answer", font=('Century Gothic', 14), command=show_ans)
    
    check_button.pack(side="left", padx=10)
    reset_button.pack(side="left", padx=10)
    ans_button.pack(side="left", padx=10)

def reset_grid():
    # Clear all entries in the grid
    for row in grid_entries:
        for entry in row:
            entry.delete(0, tk.END)

def show_ans():
    # Fill grid with the correct answer to be checked
    correct_ans = [
        "10011",
        "11010",
        "00000",
        "01101",
        "10111"
    ]
    # Nested Loop to print through the grid
    for row in range(len(correct_ans)):
        for col in range(len(correct_ans[row])):
            grid_entries[row][col].delete(0, tk.END)                # Clear existing input
            grid_entries[row][col].insert(0, correct_ans[row][col]) # Insert the correct answer

if __name__ == "__main__":
    main()
