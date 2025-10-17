from pathlib import Path
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("src", help="The source directory to copy from", type=str)
parser.add_argument("dst", help="The destination directory to paste to", type=str)

src_dir = Path("C:/2025 Software Dev/Portfolio Projects/File Backup Utility/Copy")
dst_dir = Path("C:/2025 Software Dev/Portfolio Projects/File Backup Utility/Paste")

# copy the source directory in an arbitrary order
def copy_files_glob():
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

# copy the source directory from top to bottom
def copy_files_walk():
    # create the destination directory if it doesn't already exist
    dst_dir.mkdir(parents=True, exist_ok=True)

    # loop through the source directory
    print("Scanning source directory...")

    for dirpath, dirnames, filenames in src_dir.walk():
        # get the path to the target directory relative to any subdirectories
        relative_dir_path = dirpath.relative_to(src_dir)

        # create all subdirectories in the target directory
        for dirname in dirnames:
            dst_path = dst_dir / relative_dir_path / dirname
            dst_path.mkdir(exist_ok=True)
            print("Directory copied:", dirname)

        # copy all files to the target directory
        for filename in filenames:
            src_path = dirpath / filename
            dst_path = dst_dir / relative_dir_path / filename
            shutil.copy2(src_path, dst_path)
            print("File copied:", filename)
        
if __name__ == "__main__":
    copy_files_walk()