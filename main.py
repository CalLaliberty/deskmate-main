import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import ttkbootstrap as ttk
import subprocess
import sys

from utils.file_categories import FILE_CATEGORIES

# Ensure the icon path is correct when running the bundled executable
def get_icon_path():
    if getattr(sys, 'frozen', False):
        # When bundled, PyInstaller extracts files to sys._MEIPASS
        return os.path.join(sys._MEIPASS, "deskmate_logo_removebg.ico")
    else:
        # For normal execution, icon file is assumed to be in the same directory as the script
        return "deskmate_logo_removebg.ico"


class CustomMessageBox:
    def __init__(self, parent, title, message):
        self.top = ttk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("400x200")  # Increased dialog size
        self.top.resizable(False, False)

        # Apply ttkbootstrap style
        self.style = ttk.Style()
        self.style.theme_use("darkly")

        # Create a frame for the message
        frame = ttk.Frame(self.top, padding=15)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Message text with word wrapping
        self.message_label = ttk.Label(
            frame, text=message, font=("Arial", 12), wraplength=350  # Set wrap length
        )
        self.message_label.pack(pady=10)

        # Yes and No buttons with larger size
        self.button_frame = ttk.Frame(frame)
        self.button_frame.pack(pady=10)

        self.yes_button = ttk.Button(
            self.button_frame, text="Yes", style="success.TButton", command=self.on_yes
        )
        self.yes_button.pack(side="left", padx=10, ipadx=15, pady=5)

        self.no_button = ttk.Button(
            self.button_frame, text="No", style="danger.TButton", command=self.on_no
        )
        self.no_button.pack(side="right", padx=10, ipadx=15, pady=5)

        self.result = None

    def on_yes(self):
        self.result = True
        self.top.destroy()

    def on_no(self):
        self.result = False
        self.top.destroy()

    def show(self):
        self.top.wait_window()
        return self.result


class DesktopCleanerApp:
    def __init__(self, root):
        """Initialize the Desktop Cleaner application."""
        self.root = root
        self.root.title("DeskMate - Folder Organizer")
        self.root.geometry("920x550")
        self.root.resizable(False, False)

        # Set custom window icon
        self.root.iconbitmap(get_icon_path())

        # Apply ttkbootstrap theme
        self.style = ttk.Style()
        self.style.theme_use("darkly")

        # Create the main frame with padding
        frame = ttk.Frame(root, padding=15, relief="ridge", borderwidth=3)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Label for folder selection (larger font)
        self.label = ttk.Label(frame, text="Select a folder to clean:", font=("Arial", 16, "bold"))
        self.label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Input field for folder path (larger font)
        self.folder_path = tk.StringVar()
        self.folder_entry = ttk.Entry(frame, textvariable=self.folder_path, width=60, font=("Arial", 14))
        self.folder_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Button to browse for a folder (aligned to the right)
        self.browse_button = ttk.Button(frame, text="Browse", command=self.select_folder, style="primary.TButton")
        self.browse_button.grid(row=1, column=1, padx=5, pady=5, sticky="e", ipadx=10)

        # Button to start cleaning (aligned to the right below)
        self.clean_button = ttk.Button(frame, text="Clean", command=self.organize_desktop, style="success.TButton")
        self.clean_button.grid(row=2, column=1, padx=5, pady=10, sticky="e", ipadx=10)

        # Button to show history
        self.history_button = ttk.Button(frame, text="Show History", command=self.show_history, style="info.TButton")
        self.history_button.grid(row=4, column=1, padx=5, pady=10, sticky="e", ipadx=10)

        # Log output box for detailed actions (larger font)
        self.log_text = scrolledtext.ScrolledText(frame, width=85, height=15, wrap="word", font=("Consolas", 12))
        self.log_text.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        # History of actions
        self.history = []

    def select_folder(self):
        """Open a dialog to select a folder."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def organize_desktop(self):
        """Organize files into categorized folders."""
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return

        created_folders = []
        self.log_message("Starting organization...\n")

        # Create categorized folders and move files accordingly
        for category, extensions in FILE_CATEGORIES.items():
            category_folder = os.path.join(folder, category)
            os.makedirs(category_folder, exist_ok=True)
            files_moved_to_category = False

            # Move files to the appropriate category
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isdir(file_path):
                    continue

                file_extension = os.path.splitext(filename)[1].lower()
                if file_extension in extensions:
                    try:
                        shutil.move(file_path, os.path.join(category_folder, filename))
                        action = f"✅ Moved: {filename.ljust(25)} → {category}"
                        self.log_message(action)
                        self.history.append(action)  # Save to history
                        files_moved_to_category = True
                    except Exception as e:
                        self.log_message(f"❌ Error moving {filename}: {e}")

            if files_moved_to_category:
                created_folders.append(category_folder)

        self.delete_empty_folders(folder)
        self.ask_to_rename_folders(created_folders)
        self.prompt_open_folder(folder)
        self.log_message("\n🎉 Organization complete!\n")

    def delete_empty_folders(self, folder):
        """Delete any empty folders that were created."""
        for category in FILE_CATEGORIES.keys():
            category_folder = os.path.join(folder, category)
            if os.path.isdir(category_folder) and not os.listdir(category_folder):
                try:
                    os.rmdir(category_folder)
                    action = f"🗑 Deleted empty folder: {category_folder}"
                    self.log_message(action)
                    self.history.append(action)  # Save to history
                except Exception as e:
                    self.log_message(f"❌ Error deleting {category_folder}: {e}")

    def ask_to_rename_folders(self, created_folders):
        """Ask the user if they want to rename newly created folders."""
        for folder in created_folders:
            new_name = simpledialog.askstring("Rename Folder", f"Rename {os.path.basename(folder)}? (Leave empty to skip)")
            if new_name:
                new_folder_path = os.path.join(os.path.dirname(folder), new_name)
                try:
                    os.rename(folder, new_folder_path)
                    action = f"✏️ Renamed folder: {os.path.basename(folder)} → {new_name}"
                    self.log_message(action)
                    self.history.append(action)  # Save to history
                except Exception as e:
                    self.log_message(f"❌ Error renaming {folder}: {e}")

    def log_message(self, message):
        """Log messages in the output box with formatting."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.yview(tk.END)

    def prompt_open_folder(self, folder):
        """Ask the user if they want to open the organized folder."""
        custom_dialog = CustomMessageBox(self.root, "Open Folder", "Do you want to open the folder and see the updates?")
        open_folder = custom_dialog.show()
        if open_folder:
            self.open_folder(folder)

    def open_folder(self, folder):
        """Open the folder in the system's file explorer."""
        if os.name == 'nt':  # Windows
            os.startfile(folder)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.Popen(["open" if "darwin" in os.sys.platform else "xdg-open", folder])

    def show_history(self):
        """Display the history of actions in a new window."""
        history_window = ttk.Toplevel(self.root)
        history_window.title("History of Actions")
        history_window.geometry("600x400")
        history_window.resizable(False, False)

        history_text = scrolledtext.ScrolledText(history_window, width=70, height=20, wrap="word", font=("Consolas", 12))
        history_text.pack(padx=10, pady=10)

        if self.history:
            history_text.insert(tk.END, "\n".join(self.history))
        else:
            history_text.insert(tk.END, "No actions in history.")

if __name__ == "__main__":
    root = ttk.Window(themename="vapor")
    app = DesktopCleanerApp(root)
    root.mainloop()
