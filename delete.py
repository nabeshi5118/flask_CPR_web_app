import os
import shutil

def count_files_and_dirs(path):
    file_count = 0
    dir_count = 0
    for root, dirs, files in os.walk(path):
        file_count += len(files)
        dir_count += len(dirs)
    return file_count, dir_count

def delete_contents_of_directory(path):
    if os.path.exists(path):
        file_count, dir_count = count_files_and_dirs(path)
        print(f"The directory {path} contains {file_count} files and {dir_count} directories.")
        if file_count != 0:
            confirmation = input(f"Do you want to proceed with the deletion of {path}? (yes/no): ")
            if confirmation.lower() == 'yes':
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        file_path = os.path.join(root, name)
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    for name in dirs:
                        dir_path = os.path.join(root, name)
                        shutil.rmtree(dir_path)
                        print(f"Deleted directory: {dir_path}")
                print(f"Deletion completed for {path}.")
            else:
                print(f"Deletion aborted for {path}.")
        else:
            print("This directory is empty.")
    else:
        print(f"The path {path} does not exist")

# 指定したパスの配列を入力してください
directory_paths = [
    "cpr_app/static/result",
    "cpr_app/uploads",
    "cpr_app/outputs/cache",
    "cpr_app/outputs/csv",
    "cpr_app/outputs/json"
    # 他のパスを追加
]

for directory_path in directory_paths:
    delete_contents_of_directory(directory_path)
