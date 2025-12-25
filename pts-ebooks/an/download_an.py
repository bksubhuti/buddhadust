import os
import urllib.request
import re
import time

BASE_URL = "https://buddhadust.net/dhamma-vinaya/pts/an/"
SUBDIRS = [
    "01_ones/", "02_twos/", "03_threes/", "04_fours/", "05_fives/",
    "06_sixes/", "07_sevens/", "08_eights/", "09_nines/", "10_tens/", "11_elevens/"
]
TARGET_DIR = "an/src/v2.0/"

def get_file_links(url):
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        # Look for href="anXX.something.htm"
        links = re.findall(r'href="([^"]*an\d+\.[^"]*\.htm)"', html)
        # Filter out duplicates and internal links
        links = list(set(l for l in links if not l.startswith('http') and 'idx' not in l and 'index' not in l))
        return sorted(links)
    except Exception as e:
        print(f"Error reading {url}: {e}")
        return []

def download_file(url, target_path):
    print(f"Downloading {url}...")
    try:
        urllib.request.urlretrieve(url, target_path)
        time.sleep(0.5) # Be nice to the server
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    total = 0
    for subdir in SUBDIRS:
        subdir_url = BASE_URL + subdir
        print(f"Scanning {subdir_url}...")
        files = get_file_links(subdir_url)
        print(f"Found {len(files)} files.")
        for filename in files:
            file_url = subdir_url + filename
            target_path = os.path.join(TARGET_DIR, filename)
            if not os.path.exists(target_path):
                download_file(file_url, target_path)
                total += 1
            else:
                print(f"Skipping {filename} (already exists)")
    print(f"Done. Downloaded {total} new files.")

if __name__ == "__main__":
    main()
