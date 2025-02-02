import os
import shutil

def organize_files(folder, categories):
    """Organizes files into categorized folders."""
    history = []
    created_folders = []

    for category, extensions in categories.items():
        category_folder = os.path.join(folder, category)
        os.makedirs(category_folder, exist_ok=True)
        files_moved = False

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isdir(file_path):
                continue

            if os.path.splitext(filename)[1].lower() in extensions:
                shutil.move(file_path, os.path.join(category_folder, filename))
                history.append(f"✅ Moved: {filename} → {category}")
                files_moved = True

        if files_moved:
            created_folders.append(category_folder)

    return history, created_folders

def delete_empty_folders(folder, log_message, history):
    """Deletes any empty folders that were created."""
    for category in os.listdir(folder):
        category_folder = os.path.join(folder, category)
        if os.path.isdir(category_folder) and not os.listdir(category_folder):
            try:
                os.rmdir(category_folder)
                action = f"🗑 Deleted empty folder: {category_folder}"
                log_message(action)
                history.append(action)
            except Exception as e:
                log_message(f"❌ Error deleting {category_folder}: {e}")
