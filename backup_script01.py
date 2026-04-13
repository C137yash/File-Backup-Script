import os
import shutil
import zipfile
import datetime
import logging

# --- SETUP LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backup_log.txt"),
        logging.StreamHandler()  # Also prints to console
    ]
)

def get_folder_path(prompt):
    """Ask user for folder path and validate it exists"""
    while True:
        path = input(prompt).strip()
        if os.path.exists(path) and os.path.isdir(path):
            return path
        else:
            logging.warning(f"❌ Folder not found: {path}")
            print("Please enter a valid existing folder path.")

def create_backup(source, backup_root):
    # Create backup root folder if it doesn't exist
    os.makedirs(backup_root, exist_ok=True)

    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    backup_path = os.path.join(backup_root, backup_name)

    # Copy source to backup folder
    try:
        shutil.copytree(source, backup_path)
        logging.info(f"✅ Copied {source} to {backup_path}")
    except Exception as e:
        logging.error(f"❌ Failed to copy: {e}")
        return

    # Zip the backup
    zip_path = f"{backup_path}.zip"
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_path)
                    zipf.write(file_path, arcname)
        logging.info(f"✅ Zipped to {zip_path}")

        # Optional: Delete the unzipped folder to save space
        shutil.rmtree(backup_path)
        logging.info(f"🗑️ Deleted unzipped folder: {backup_path}")

    except Exception as e:
        logging.error(f"❌ Failed to zip: {e}")

if __name__ == "__main__":
    logging.info("🚀 Starting backup...")

    # Ask user for source and backup folders
    source_folder = get_folder_path("Enter source folder path: ")
    backup_folder = get_folder_path("Enter backup destination folder: ")

    # Run backup
    create_backup(source_folder, backup_folder)

    logging.info("✅ Backup completed.")