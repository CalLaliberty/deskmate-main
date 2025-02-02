import ttkbootstrap as ttk

class CustomMessageBox:
    def __init__(self, parent, title, message):
        self.top = ttk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("400x200")
        self.top.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("minty")

        frame = ttk.Frame(self.top, padding=15)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.message_label = ttk.Label(frame, text=message, font=("Arial", 12), wraplength=350)
        self.message_label.pack(pady=10)

        self.button_frame = ttk.Frame(frame)
        self.button_frame.pack(pady=10)

        self.yes_button = ttk.Button(self.button_frame, text="Yes", style="success.TButton", command=self.on_yes)
        self.yes_button.pack(side="left", padx=10, ipadx=15, pady=5)

        self.no_button = ttk.Button(self.button_frame, text="No", style="danger.TButton", command=self.on_no)
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
