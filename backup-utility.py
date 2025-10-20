from pathlib import Path
import shutil
import argparse

parser = argparse.ArgumentParser(description="copy files from one directory to another")
parser.add_argument("src", nargs="?", help="the source directory to copy from")
parser.add_argument("dst", nargs="?", help="the destination directory to copy to")
options = parser.add_mutually_exclusive_group()
options.add_argument("-d", "--dry", action="store_true", help="will print actions to console instead of performing them")
options.add_argument("-q", "--quiet", action="store_true", help="disables progress console printing")

# simple global log function to respect the '--quiet' argument
log = lambda *args, **kwargs: print(*args, **kwargs)

def create_path(path: str) -> Path:
    p = Path(path)
    return p if p.is_absolute() else Path.cwd() / p

# copy the source directory, walking from top to bottom
def copy_files(src_dir: Path, dst_dir: Path, dry=False) -> None:
    # create the destination directory if it doesn't already exist
    if dry:
        log(f"[DRY RUN] Would create directory: {dst_dir}")
    else:
        dst_dir.mkdir(parents=True, exist_ok=True)

    # loop through the source directory
    log("- Scanning source directory...")

    for dirpath, dirnames, filenames in src_dir.walk():
        # get the path to the target directory relative to any subdirectories
        relative_dir_path = dirpath.relative_to(src_dir)

        # create all subdirectories in the target directory
        for dirname in dirnames:
            dst_path = dst_dir / relative_dir_path / dirname
            if dry:
                log(f"[DRY RUN] -- Dir copied: {dst_path}")
            else:
                dst_path.mkdir(exist_ok=True)
                log(f"-- Dir copied: {dirname}")

        # copy all files to the target directory
        for filename in filenames:
            src_path = dirpath / filename
            dst_path = dst_dir / relative_dir_path / filename

            # skip unmodified files and account for the '--dry' flag
            if dst_path.exists() and dst_path.stat().st_mtime >= src_path.stat().st_mtime:
                if dry:
                    log(f"[DRY RUN] ->- Skipped: {filename}")
                else:
                    log(f"->- Skipped: {filename}")
                continue
            elif dst_path.exists():
                if dry:
                    log(f"[DRY RUN] -+- Updated: {filename}")
                else:
                    log(f"-+- Updated: {filename}")
                continue
            else:
                if dry:
                    log(f"[DRY RUN] --- Copied:  {filename}")
                else:
                    shutil.copy2(src_path, dst_path)
                    log(f"--- Copied:  {filename}")

def instructions() -> str:
    return """--- Backup Utility ---
This basic CLI application copies files from one directory to another,
attempting to preserve metadata and ignoring unmodified files.

Paths entered below will be relative to your current directory, unless using absolute paths."""

def get_src_and_dst() -> tuple[Path, Path]:      # return the source and destination paths
    print(instructions())

    src = create_path(input("- Source: "))
    log("Source path:", src)

    dst = create_path(input("- Destination: "))
    log("Destination path:", dst)

    return src, dst
        
if __name__ == "__main__":
    args = parser.parse_args()
    
    if args.quiet:  # do not print logs if --quiet is flagged as true
        log = lambda *args, **kwargs: None

    if args.src and args.dst:
        src = create_path(args.src)
        dst = create_path(args.dst)
        copy_files(src, dst, dry=args.dry)
    else:
        src, dst = get_src_and_dst()
        copy_files(src, dst, dry=args.dry)