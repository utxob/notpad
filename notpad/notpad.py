import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Create main application window
root = tk.Tk()
root.title("Python Notepad")
root.geometry("600x400")

# Function to create a new file
def new_file():
    text_area.delete(1.0, tk.END)
    root.title("Python Notepad - New File")

# Function to open an existing file
def open_file():
    file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file:
        with open(file, "r") as f:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, f.read())
            root.title(f"Python Notepad - {file}")

# Function to save the current file
def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file:
        with open(file, "w") as f:
            f.write(text_area.get(1.0, tk.END))
            root.title(f"Python Notepad - {file}")

# Function to handle the "Exit" event
def exit_app():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.quit()

# Creating the Text Area for the Notepad
text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 12))
text_area.pack(expand=True, fill=tk.BOTH)

# Creating the Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Adding File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

# Adding Edit Menu (Optional, can add more features)
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

# Start the application
root.mainloop()
