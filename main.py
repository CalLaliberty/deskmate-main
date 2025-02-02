import tkinter as tk
import ttkbootstrap as ttk
from gui.app import DesktopCleanerApp


if __name__ == "__main__":
    print("Initializing window...💻")  # Debugging line
    root = tk.Tk()
    print("Creating app instance...🎉")  # Debugging line
    app = DesktopCleanerApp(root)
    print("Entering main loop...👻")  # Debugging line
    root.mainloop()
