# DeskMate 🧹💻

DeskMate is a simple file organization app built using Python and Tkinter. It helps users clean up their desktop or file folders by organizing files into neatly sorted subfolders. With an intuitive graphical interface, DeskMate makes it easy to tidy up your files with just a few clicks! 🎯

## Features ✨

- Organize files into folders based on file types (images, documents, etc.) 📂
- Clean up your desktop by automatically moving files to designated folders 🧹
- Built with Python and Tkinter for a user-friendly experience 🐍
- Customizable folder sorting (add your own folder types) ⚙️

## Requirements ⚡
- Python 3.x or higher 🖥️
- Tkinter (usually included with Python) 📦
- Install dependencies from requirements.txt:

## Installation 🔧

Clone this repository:

```bash
git clone https://github.com/yourusername/deskmate-main.git
```

Navigate into the project directory:

```bash
cd deskmate-main
```

(Optional) Create a virtual environment:

```bash
python -m venv .venv
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage 🚀

Run the app by executing the following command:

```bash
python main.py
```

## 🖥️ Install as a Desktop App
You can create a standalone Windows executable and install DeskMate as a desktop app:

Build the app using PyInstaller:

```bash
pyinstaller --onefile --windowed --name DeskMate --icon=assets/deskmate_logo_removebg.ico --add-data "assets\\deskmate_logo_removebg.ico;assets" main.py
```
### After the build finishes, go to the dist folder. You will see DeskMate.exe there.

1. Right-click DeskMate.exe and select Create shortcut.

2. Move the shortcut to your Desktop or another desired location.

3. Now you can launch DeskMate like a regular desktop application! 🎉

### The graphical user interface (GUI) will appear. Follow the on-screen prompts to clean and organize your files! 🧑‍💻✨

## Contributing 🤝

Feel free to fork this repository and make improvements! If you have any suggestions or find a bug, open an issue or submit a pull request. 🚀

### To Do List 📋

- [ ] Add more file organization options 🎨
- [ ] Implement a drag-and-drop feature 🖱️
- [x] Fix minor UI bugs 🐞

## License 📜

This project is licensed under the MIT License - see the LICENSE file for details. 🔐
