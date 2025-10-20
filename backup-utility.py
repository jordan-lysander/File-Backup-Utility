from pathlib import Path
import shutil
import argparse

parser = argparse.ArgumentParser(description="copy files from one directory to another")
parser.add_argument("src", nargs="?", help="the source directory to copy from")
parser.add_argument("dst", nargs="?", help="the destination directory to copy to")
parser.add_argument("-d", "--dry", action="store_true", help="will print actions to console instead of performing them")
parser.add_argument("-q", "--quiet", action="store_true", help="disables progress console printing")

# copy the source directory, walking from top to bottom
def copy_files(src_dir: Path, dst_dir: Path, dry=False, quiet=False):
    # create the destination directory if it doesn't already exist
    dst_dir.mkdir(parents=True, exist_ok=True)

    # loop through the source directory
    print("- Scanning source directory...")

    for dirpath, dirnames, filenames in src_dir.walk():
        # get the path to the target directory relative to any subdirectories
        relative_dir_path = dirpath.relative_to(src_dir)

        # create all subdirectories in the target directory
        for dirname in dirnames:
            dst_path = dst_dir / relative_dir_path / dirname
            dst_path.mkdir(exist_ok=True)
            print("-- Directory copied:", dirname)

        # copy all files to the target directory
        for filename in filenames:
            src_path = dirpath / filename
            dst_path = dst_dir / relative_dir_path / filename

            # skip unmodified files
            if dst_path.exists() and dst_path.stat().st_mtime >= src_path.stat().st_mtime:
                print("-~- File not copied:", filename, "(unmodified)")
                continue

            shutil.copy2(src_path, dst_path)
            print("--- File copied:", filename)

def instructions():
    return """--- Backup Utility ---
This basic CLI application copies files from one directory to another,
attempting to preserve metadata and ignoring unmodified files.

Paths entered below will be relative to your current directory, unless using absolute paths."""

def get_src_and_dst():
    print(instructions())

    src = Path(input("- Source: "))
    if not src.is_absolute():
        print("Source path not absolute")
        src = Path.cwd() / src
    print("Source path:", src)

    dst = Path(input("- Destination: "))
    if not dst.is_absolute():
        print("Destination path not absolute")
        dst = Path.cwd() / dst
    print("Destination path:", dst)

    return src, dst
        
if __name__ == "__main__":
    args = parser.parse_args()
    if args.src and args.dst:
        src = Path(args.src)
        if not src.is_absolute():
            src = Path.cwd() / src
        dst = Path(args.dst)
        if not dst.is_absolute():
            dst = Path.cwd() / dst
        copy_files(src, dst)
    else:
        src, dst = get_src_and_dst()
        copy_files(src, dst)