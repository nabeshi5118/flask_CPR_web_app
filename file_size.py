import os

def get_size(path):
    total_size = 0
    if os.path.isfile(path):
        total_size = os.path.getsize(path)
    else:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
    return total_size

def find_largest_items(directory_paths):
    all_items = []
    for directory_path in directory_paths:
        if os.path.exists(directory_path):
            for root, dirs, files in os.walk(directory_path):
                for name in files:
                    file_path = os.path.join(root, name)
                    size = get_size(file_path)
                    all_items.append((file_path, size))
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    size = get_size(dir_path)
                    all_items.append((dir_path, size))
        else:
            print(f"The path {directory_path} does not exist")

    # Sort all items by size in descending order
    all_items.sort(key=lambda x: x[1], reverse=True)
    return all_items

def display_largest_items(all_items, top_n=10):
    print(f"\nTop {top_n} largest items:")
    for i, item in enumerate(all_items[:top_n]):
        print(f"{i+1}. {item[0]} - {item[1] / (1024*1024):.2f} MB")

# 指定したパスの配列を入力してください
directory_paths = [
    "/home/watanabe/research/Docker-composes/flask_CPR_web_app"
    # 他のパスを追加
]

# 最大表示数を設定
top_n = 10

all_items = find_largest_items(directory_paths)
display_largest_items(all_items, top_n)
