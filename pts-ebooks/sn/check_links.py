import os
import re

def check_files(directory):
    print(f"Checking files in {directory}...")
    errors = 0
    for filename in os.listdir(directory):
        if filename.endswith(".htm") or filename.endswith(".xhtml"):
            path = os.path.join(directory, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple check: count of <a vs </a>
            open_a = len(re.findall(r'<a\s', content))
            close_a = len(re.findall(r'</a>', content))
            
            if open_a != close_a:
                print(f"MISMATCH in {filename}: <a ({open_a}) vs </a> ({close_a})")
                errors += 1
                
                # Context check
                matches = re.finditer(r'<a\s[^>]*>', content)
                for m in matches:
                    start = m.end()
                    # Look ahead for closing
                    next_close = content.find('</a>', start)
                    next_open = content.find('<a ', start)
                    
                    if next_close == -1 or (next_open != -1 and next_open < next_close):
                        print(f"  Unclosed tag starting at {m.start()}: {m.group(0)}")
                        # Print snippets
                        snippet = content[m.start():m.start()+100]
                        print(f"  Snippet: {snippet}...")
                        break

    if errors == 0:
        print("All files passed link tag check.")
    else:
        print(f"Found {errors} files with mismatched tags.")

if __name__ == "__main__":
    check_files("sn/src/epub_v2_styled_sn")
