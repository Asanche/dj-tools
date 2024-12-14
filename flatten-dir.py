import os
import shutil
import argparse

def flatten_directory(top_dir, overwrite=False):
    # Walk through the directory tree and move files to the top level directory
    for root, dirs, files in os.walk(top_dir, topdown=False):
        for name in files:
            source = os.path.join(root, name)
            destination = os.path.join(top_dir, name)

            if os.path.exists(destination) and not overwrite:
                print(f"Skipping {name} because it already exists in {top_dir}")
            else:
                shutil.move(source, destination)

        # Remove empty directories
        for name in dirs:
            dir_path = os.path.join(root, name)
            if not os.listdir(dir_path):  # Check if the directory is empty
                os.rmdir(dir_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flatten a directory structure.")
    parser.add_argument("-path", required=True, help="Path to the top level directory.")
    parser.add_argument("-overwrite", action="store_true", help="Overwrite files if conflicts occur.")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a valid directory.")
        exit(1)

    flatten_directory(args.path, args.overwrite)
    print("Directory structure flattened successfully.")
