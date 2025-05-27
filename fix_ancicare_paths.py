import os
import re

# Directory containing the AnciCare site
ROOT_DIR = "./vintage-ancicare-website"

def fix_paths_in_file(file_path):
    with open(file_path, "r", encoding="latin-1") as f:
        content = f.read()

    original = content

    # Replace backslashes with slashes
    content = content.replace("\\", "/")

    # Lowercase "IMAGES" paths
    content = re.sub(r'(?i)src="IMAGES/', 'src="images/', content)
    content = re.sub(r'(?i)href="IMAGES/', 'href="images/', content)
    content = re.sub(r'(?i)background="IMAGES/', 'background="images/', content)

    # Replace full Windows file paths with just filenames (e.g., C:/website/whatever/foo.htm → foo.html)
    content = re.sub(r'(?i)value="(?:[A-Z]:)?/?(?:website/)?[^"]*?/?([a-zA-Z0-9_-]+\.(?:htm|html))"', r'value="\1"', content)

    # Normalize all .htm to .html for consistency
    content = re.sub(r'(?i)\.htm(["\'])', r'.html\1', content)

    if content != original:
        with open(file_path, "w", encoding="latin-1") as f:
            f.write(content)
        print(f"✅ Fixed: {file_path}")
    else:
        print(f"— Skipped (no change): {file_path}")

def walk_and_fix_html(root):
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.lower().endswith((".html", ".htm")):
                filepath = os.path.join(dirpath, name)
                fix_paths_in_file(filepath)

if __name__ == "__main__":
    print(f"🔍 Scanning: {ROOT_DIR}")
    walk_and_fix_html(ROOT_DIR)
    print("✅ All done.")
