import re
import sys

def test():
    file_path = 'src/v2.0/dn.01.rhyt.pts.htm'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Extract the end of the file to look at the footer
    footer_section = content[-2000:]
    
    print("\n--- Testing Stricter Regex Pattern ---")
    
    # Strict pattern: HR, P, optional space/nbsp, [, optional link, Contents
    strict_pattern = r'<hr\s*/?>\s*<p[^>]*>\s*(?:&nbsp;|&#160;|\s)*\[\s*(?:<a[^>]*>)?Contents'
    
    m_strict = re.search(strict_pattern, footer_section, re.DOTALL | re.IGNORECASE)
    print(f"Strict Pattern '{strict_pattern}': {bool(m_strict)}")
    if m_strict: print(f"Match: {repr(m_strict.group())}")

if __name__ == "__main__":
    test()