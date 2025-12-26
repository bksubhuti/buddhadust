import difflib
import sys

def get_line_number(text, char_index):
    return text[:char_index].count('\n') + 1

def analyze_detailed(file1_path, file2_path):
    try:
        with open(file1_path, 'r', encoding='utf-8', errors='replace') as f1:
            text1 = f1.read()
        with open(file2_path, 'r', encoding='utf-8', errors='replace') as f2:
            text2 = f2.read()
    except Exception as e:
        print(f"Error reading files: {e}")
        return

    matcher = difflib.SequenceMatcher(None, text1, text2)
    similarity = matcher.ratio() * 100

    changes = {
        '0-4': [],
        '4-10': [],
        '10-100': [],
        '100+': []
    }

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            continue

        t1_segment = text1[i1:i2]
        t2_segment = text2[j1:j2]
        
        size = max(len(t1_segment), len(t2_segment))
        
        if size == 0: continue

        # Determine category
        if size < 4: category = '0-4'
        elif size < 10: category = '4-10'
        elif size < 100: category = '10-100'
        else: category = '100+'

        # Get line numbers
        line1 = get_line_number(text1, i1)
        line2 = get_line_number(text2, j1)

        # Format the change snippet
        snippet = ""
        if tag == 'replace':
            snippet = f"v0.4 (Line {line1}): {repr(t1_segment)}\n-> v2.0 (Line {line2}): {repr(t2_segment)}"
        elif tag == 'delete':
            snippet = f"v0.4 (Line {line1}): Deleted {repr(t1_segment)}"
        elif tag == 'insert':
            snippet = f"v2.0 (Line {line2}): Inserted {repr(t2_segment)}"

        changes[category].append(snippet)

    print(f"Similarity: {similarity:.2f}%")
    print("-" * 30)

    for category in ['0-4', '4-10', '10-100', '100+']:
        print(f"\nCategory: {category} characters")
        examples = changes[category][:5]
        for idx, ex in enumerate(examples, 1):
            print(f"  {idx}. {ex}")
            print("  ---")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        analyze_detailed(sys.argv[1], sys.argv[2])
    else:
        analyze_detailed('mn/src/v0.4/mn.001.horn.pts.htm', 'mn/src/v2.0/mn.001.horn.pts.htm')
