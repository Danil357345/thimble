# test_commit_files.py
# to run: python3 test_commit_files.py

import os
import subprocess
import json
import random
import string
from datetime import datetime

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def create_test_file(content):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{random_string()}.txt"
    dir_path = os.path.join("message", date_str)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, filename)

    with open(file_path, 'w') as f:
        f.write(content)

    return file_path

def run_commit_files(script):
    subprocess.run(script, shell=True, check=True)

def check_git_log():
    result = subprocess.run(["git", "log", "-1", "--pretty=format:%s"], capture_output=True, text=True)
    return "Auto-commit" in result.stdout

def check_metadata_file(filename):
    metadata_file = os.path.join(os.path.dirname(filename), "metadata", os.path.basename(filename) + ".json")
    if not os.path.exists(metadata_file):
        return False
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    return all(key in metadata for key in ['author', 'title', 'hashtags', 'file_hash'])

def run_tests(script):
    print(f"Testing {script}")

    # Test 1: Commit a single file
    file1 = create_test_file("Author: John Doe\nThe Beauty of Nature\n\nNature's beauty is an awe-inspiring spectacle that never fails to amaze us. From the grandeur of mountains to the delicacy of a flower, it reminds us of the world's magnificence.\n\n#nature #beauty #inspiration")
    run_commit_files(script)
    assert check_git_log(), "Git commit not found"
    assert check_metadata_file(file1), "Metadata file not created or invalid"
    print("Test 1 passed: Single file commit")

    # Test 2: Commit multiple files
    file2 = create_test_file("Author: Jane Smith\nThe Art of Cooking\n\nCooking is not just about sustenance; it's an art form that engages all our senses. The sizzle of a pan, the aroma of spices, and the vibrant colors of fresh ingredients all come together to create culinary masterpieces.\n\n#cooking #art #food")
    file3 = create_test_file("Author: Bob Johnson\nThe Joy of Learning\n\nLearning is a lifelong journey that opens doors to new worlds. Whether it's picking up a new skill or diving deep into a subject, the process of discovery and growth is incredibly rewarding.\n\n#learning #education #growth")
    run_commit_files(script)
    assert check_git_log(), "Git commit not found"
    assert check_metadata_file(file2) and check_metadata_file(file3), "Metadata files not created or invalid"
    print("Test 2 passed: Multiple file commit")

    # Test 3: No changes to commit
    run_commit_files(script)
    print("Test 3 passed: No changes to commit")

    print(f"All tests passed for {script}")

if __name__ == "__main__":
    scripts = [
        "python3 commit_files.py",
        "node commit_files.js",
        "php commit_files.php",
        "perl commit_files.pl"
    ]

    for script in scripts:
        run_tests(script)