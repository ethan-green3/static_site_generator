import os
import shutil

def copy_static(source_dir="static", dest_dir="public"):
    # Delete the destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Removing existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    # Recreate the destination directory
    os.mkdir(dest_dir)

    # Recursively copy contents from source to destination
    def recursive_copy(src, dst):
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)

            if os.path.isfile(src_path):
                print(f"Copying file: {src_path} -> {dst_path}")
                shutil.copy(src_path, dst_path)
            elif os.path.isdir(src_path):
                print(f"Creating directory: {dst_path}")
                os.mkdir(dst_path)
                recursive_copy(src_path, dst_path)

    recursive_copy(source_dir, dest_dir)