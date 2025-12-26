import re
import difflib
import sys

def clean_html(raw_html):
    # Remove HTML tags
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    # Replace HTML entities
    cleantext = cleantext.replace('&#160;', ' ').replace('&nbsp;', ' ')
    # Normalize whitespace
    return ' '.join(cleantext.split())

def extract_paragraphs(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        sys.exit(1)

    # Find all p tags with class starting with f4
    # We use a non-greedy match for the content
    pattern = re.compile(r'<p class="f4[^\"]*"(?:[^>]*)>(.*?)</p>', re.DOTALL)
    matches = pattern.findall(content)
    
    cleaned_paragraphs = [clean_html(m) for m in matches]
    # Filter out empty paragraphs
    return [p for p in cleaned_paragraphs if p]

def calculate_similarity(text1, text2):
    return difflib.SequenceMatcher(None, text1, text2).ratio() * 100

def get_diff_score(s1, s2):
    # specific heuristic for "majorness" of change
    # combined length * dissimilarity
    matcher = difflib.SequenceMatcher(None, s1, s2)
    return max(len(s1), len(s2)) * (1 - matcher.ratio())

def main(file1, file2):
    paras1 = extract_paragraphs(file1)
    paras2 = extract_paragraphs(file2)

    # 1. Similarity of the full joined text
    full_text1 = "\n".join(paras1)
    full_text2 = "\n".join(paras2)
    overall_sim = calculate_similarity(full_text1, full_text2)
    
    print(f"Text-Only Similarity: {overall_sim:.2f}%")
    print("-" * 40)

    # 2. Paragraph-level comparison
    matcher = difflib.SequenceMatcher(None, paras1, paras2)
    
    changes = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            continue
        
        # We are looking for replacements or significant modifications
        # If it's a huge block insert/delete, we count it as one item
        
        if tag == 'replace':
            # Compare corresponding paragraphs in the block
            # If the block size differs, we might have misaligned/combined paragraphs
            # For simplicity, we pair them up to the min length, then add remaining as insert/delete
            
            p1_slice = paras1[i1:i2]
            p2_slice = paras2[j1:j2]
            
            # For each pair in the replacement block
            for k in range(max(len(p1_slice), len(p2_slice))):
                old_p = p1_slice[k] if k < len(p1_slice) else ""
                new_p = p2_slice[k] if k < len(p2_slice) else ""
                
                score = get_diff_score(old_p, new_p)
                changes.append({
                    'score': score,
                    'type': 'Change',
                    'old': old_p,
                    'new': new_p
                })
        
        elif tag == 'delete':
            for k in range(i1, i2):
                changes.append({
                    'score': len(paras1[k]),
                    'type': 'Deletion',
                    'old': paras1[k],
                    'new': "(Deleted)"
                })
                
        elif tag == 'insert':
            for k in range(j1, j2):
                changes.append({
                    'score': len(paras2[k]),
                    'type': 'Insertion',
                    'old': "(Not in v1.2)",
                    'new': paras2[k]
                })

    # Sort by 'score' (impact) descending
    changes.sort(key=lambda x: x['score'], reverse=True)
    
    print("Top 10 Major Text Changes:")
    for i, change in enumerate(changes[:10], 1):
        print(f"\n{i}. [{change['type']}]")
        print(f"   v1.2: {change['old'][:200]}..." if len(change['old']) > 200 else f"   v1.2: {change['old']}")
        print(f"   v2.0: {change['new'][:200]}..." if len(change['new']) > 200 else f"   v2.0: {change['new']}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 analyze_text_diff.py <file1> <file2>")
