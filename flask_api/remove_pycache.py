import os

def remove_pycache(path):
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_dir = os.path.join(root, dir_name)
                for pyc_file in os.listdir(pycache_dir):
                    pyc_file_path = os.path.join(pycache_dir, pyc_file)
                    os.remove(pyc_file_path)
                os.rmdir(pycache_dir)

if __name__ == "__main__":
    current_directory = os.getcwd()
    remove_pycache(current_directory)
