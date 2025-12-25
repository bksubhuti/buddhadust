import re

def check_dn2_endnotes(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Find context for Note 77 (short)
    # Search for the string "77" inside sup/a
    m77 = re.search(r'<sup>.*?77.*?</sup>', content)
    if m77:
        print(f"Note 77 Source: {m77.group(0)}")
    else:
        print("Note 77 not found")

    # Find context for ed1
    med1 = re.search(r'<sup>.*?ed1.*?</sup>', content)
    if med1:
        print(f"Ed1 Source: {med1.group(0)}")
    else:
        print("Ed1 not found")

if __name__ == "__main__":
    check_dn2_endnotes('src/v2.0/dn.02.rhyt.pts.htm')