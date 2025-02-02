import os

def get_icon_path():
    """Returns the absolute path to the icon file."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "deskmate_logo_removebg.ico"))
