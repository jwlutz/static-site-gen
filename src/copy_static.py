import os
import shutil

def copy_static_to_public(src_dir="static", dest_dir="docs"):
    if os.path.exists(dest_dir):
        print(f"Deleting {dest_dir} directory...")
        shutil.rmtree(dest_dir)
    print(f"Creating {dest_dir} directory...")
    os.mkdir(dest_dir)
    _copy_directory_contents(src_dir, dest_dir)

def _copy_directory_contents(src, dest):
    items = os.listdir(src)
    for item in items:
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            _copy_directory_contents(src_path, dest_path)