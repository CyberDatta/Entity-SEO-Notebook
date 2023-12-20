import tkinter as tk
from tkinter import filedialog

def save_as():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Save As"
    )
    if file_path:
        # Perform the save operation with the selected file_path
        print(f"File saved to: {file_path}")

# Create the main window
root = tk.Tk()
root.title("File Save Example")

# Add a button to trigger the "Save As" dialog
save_button = tk.Button(root, text="Save As", command=save_as)
save_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()