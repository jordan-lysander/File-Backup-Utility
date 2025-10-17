from pathlib import Path
import shutil

src_dir = Path("C:/2025 Software Dev/Portfolio Projects/File Backup Utility/Copy")
dst_dir = Path("C:/2025 Software Dev/Portfolio Projects/File Backup Utility/Paste")

# create the destination directory if it doesn't already exist
dst_dir.mkdir(parents=True, exist_ok=True)

# loop through the source directory
print("Scanning source directory...")
for src_item in src_dir.rglob('*'):
    # get the path to the destination item relative to any subdirectories
    dst_item = dst_dir / src_item.relative_to(src_dir)

    if src_item.is_file():
        # copy the file to the destination directory
        dst_item.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_item, dst_item)
        print("File copied:", src_item.name)
    elif src_item.is_dir():
        # create the subdirectory if it does not already exist
        dst_item.mkdir(parents=True, exist_ok=True)
        print("Directory copied:", src_item.name)
    