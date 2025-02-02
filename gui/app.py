import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import ttkbootstrap as ttk
import subprocess
import datetime
from gui.custom_message_box import CustomMessageBox
from utils.file_operations import organize_files, delete_empty_folders
from utils.helpers import get_icon_path
from utils.file_categories import FILE_CATEGORIES


class DesktopCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DeskMate - Folder Organizer")
        self.root.geometry("1000x650")
        self.root.resizable(True, True)
        self.root.maxsize(1024, 768)  # Set the maximum window size
        self.root.minsize(512, 384)  # Set the minimum window size
        self.root.iconbitmap(get_icon_path())

        self.style = ttk.Style()
        self.style.theme_use("minty")

        frame = ttk.Frame(root, padding=15, relief="ridge", borderwidth=3)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Set the grid layout with column/row weights for resizing
        frame.grid_rowconfigure(0, weight=0)  # Label row
        frame.grid_rowconfigure(1, weight=0)  # Entry row
        frame.grid_rowconfigure(2, weight=0)  # Button row
        frame.grid_rowconfigure(3, weight=1)  # ScrolledText (this should expand)
        frame.grid_rowconfigure(4, weight=0)  # History button row

        frame.grid_columnconfigure(0, weight=1)  # First column (Entry + ScrolledText)
        frame.grid_columnconfigure(1, weight=0)  # Second column (Buttons)

        self.label = ttk.Label(frame, text="Select a folder to clean:", font=("Arial", 16, "bold"))
        self.label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.folder_path = tk.StringVar()
        self.folder_entry = ttk.Entry(frame, textvariable=self.folder_path, width=60, font=("Arial", 14))
        self.folder_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.browse_button = ttk.Button(frame, text="Browse", command=self.select_folder, style="primary.TButton")
        self.browse_button.grid(row=1, column=1, padx=5, pady=5, sticky="e", ipadx=10)

        self.clean_button = ttk.Button(frame, text="Clean", command=self.organize_desktop, style="success.TButton")
        self.clean_button.grid(row=2, column=1, padx=5, pady=10, sticky="e", ipadx=10)

        self.history_button = ttk.Button(frame, text="Show History", command=self.show_history, style="info.TButton")
        self.history_button.grid(row=4, column=1, padx=5, pady=10, sticky="e", ipadx=10)

        self.log_text = scrolledtext.ScrolledText(frame, width=85, height=15, wrap="word", font=("Consolas", 12))
        self.log_text.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        self.history = []

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def organize_desktop(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return

        self.log_message("📂 Starting organization...\n")
        history, created_folders = organize_files(folder, FILE_CATEGORIES)
        self.history.extend(history)

        delete_empty_folders(folder, self.log_message, self.history)
        self.ask_to_rename_folders(created_folders)
        self.prompt_open_folder(folder)
        self.log_message("\n🎉 Organization complete!\n")

    def ask_to_rename_folders(self, created_folders):
        for folder in created_folders:
            dialog = self.RenameFolderDialog(self.root, folder)
            self.root.wait_window(dialog)  # Wait for the dialog to close
            new_name = dialog.get_result()

            if new_name:
                new_folder_path = os.path.join(os.path.dirname(folder), new_name)
                try:
                    os.rename(folder, new_folder_path)
                    action = f"✏️ Renamed folder: {os.path.basename(folder)} → {new_name}"
                    self.log_message(action)
                    self.history.append(action)
                except Exception as e:
                    self.log_message(f"❌ Error renaming {folder}: {e}")

    def log_message(self, message):
        """Logs messages with timestamps."""
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S] ")
        full_message = timestamp + message
        self.log_text.insert(tk.END, full_message + "\n")
        self.log_text.yview(tk.END)

    def prompt_open_folder(self, folder):
        """Ask user if they want to open the organized folder."""
        custom_dialog = CustomMessageBox(self.root, "Open Folder", "Do you want to open the folder and see the updates?")
        if custom_dialog.show():
            self.open_folder(folder)

    def open_folder(self, folder):
        """Opens the folder in the OS file explorer."""
        if os.name == 'nt':
            os.startfile(folder)
        else:
            subprocess.Popen(["open" if "darwin" in os.sys.platform else "xdg-open", folder])

    def show_history(self):
        """Displays the history of file operations."""
        history_window = tk.Toplevel(self.root)
        history_window.title("History of Actions")
        history_window.geometry("600x400")
        history_window.resizable(False, False)

        history_text = scrolledtext.ScrolledText(history_window, width=70, height=20, wrap="word", font=("Consolas", 12))
        history_text.pack(padx=10, pady=10)

        history_text.insert(tk.END, "\n".join(self.history) if self.history else "No actions in history.")

        # Close window button
        close_button = ttk.Button(history_window, text="Close", command=history_window.destroy, style="danger.TButton")
        close_button.pack(pady=10)

    # Custom dialog class for renaming folders
    class RenameFolderDialog(tk.Toplevel):
        def __init__(self, parent, folder_name):
            super().__init__(parent)
            self.title("Rename Folder (Or Leave Empty to Skip)")
            self.geometry("400x150")  # Adjust the size here
            self.resizable(False, False)

            self.folder_name = folder_name
            self.new_name = tk.StringVar()

            label = ttk.Label(self, text=f"Rename {os.path.basename(self.folder_name)}:", font=("Arial", 12))
            label.pack(pady=10)

            entry = ttk.Entry(self, textvariable=self.new_name, font=("Arial", 12), width=30)
            entry.pack(pady=5)
            entry.focus()

            button_frame = ttk.Frame(self)
            button_frame.pack(pady=10)

            ok_button = ttk.Button(button_frame, text="OK", command=self.on_ok)
            ok_button.pack(side="left", padx=10)

            cancel_button = ttk.Button(button_frame, text="Cancel", command=self.on_cancel)
            cancel_button.pack(side="right", padx=10)

            self.grab_set()  # Makes this window modal (blocks interaction with other windows)

        def on_ok(self):
            new_name = self.new_name.get().strip()
            if new_name:
                self.result = new_name
            else:
                self.result = None
            self.destroy()

        def on_cancel(self):
            self.result = None
            self.destroy()

        def get_result(self):
            return self.result
