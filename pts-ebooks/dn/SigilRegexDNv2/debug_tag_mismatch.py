
import re

def check_tags(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Basic parser to find tags
    # Matches </tag> or <tag ...> or <tag />
    tag_pattern = re.compile(r'<(/?)([\w:]+)([^>]*)>')
    
    stack = []
    lines = content.splitlines()
    
    # Self-closing tags in XHTML/HTML (void elements)
    void_tags = {'meta', 'link', 'img', 'br', 'hr', 'input', 'area', 'base', 'col', 'embed', 'param', 'source', 'track', 'wbr'}

    for i, line in enumerate(lines):
        line_num = i + 1
        pos = 0
        while pos < len(line):
            match = tag_pattern.search(line, pos)
            if not match:
                break
            
            full_tag = match.group(0)
            is_closing = match.group(1) == '/'
            tag_name = match.group(2).lower()
            attributes = match.group(3)
            is_self_closing = attributes.strip().endswith('/')
            
            pos = match.end()

            # Skip comments and doctype (simplified)
            if full_tag.startswith('<!--') or full_tag.startswith('<!'):
                continue

            if is_self_closing or tag_name in void_tags:
                continue

            if not is_closing:
                stack.append((tag_name, line_num))
            else:
                if not stack:
                    print(f"Error at line {line_num}: Unexpected closing tag </{tag_name}>. Stack is empty.")
                else:
                    last_tag, last_line = stack[-1]
                    if last_tag == tag_name:
                        stack.pop()
                    else:
                        # Mismatch found
                        print(f"Error at line {line_num}: Closing tag </{tag_name}> does not match opening tag <{last_tag}> from line {last_line}.")
                        # For debugging, print stack context
                        print(f"Current Stack (last 5): {stack[-5:]}")
                        return

    if stack:
        print(f"Error: End of file reached with unclosed tags: {stack}")
    else:
        print("No tag mismatches found.")

if __name__ == "__main__":
    check_tags('src/v2.0/dn.26.rhyt.pts.htm')
