from pathlib import Path
import shutil

src_dir = Path("C:/2025 Software Dev/Portfolio Projects/File Backup Utility/Copy")
dst_dir = Path("C:/2025 Software Dev/Portfolio Projects/File Backup Utility/Paste")

src_files = src_dir.rglob('*')

for item in src_files:
    old_path = src_dir / item.name
    if item.is_file() and item not in dst_dir.iterdir():
        new_path = dst_dir / item.name
        shutil.copy2(old_path, new_path)
    elif item.is_dir() and item not in dst_dir.iterdir():
        item.mkdir(parents=True, exist_ok=True)
    