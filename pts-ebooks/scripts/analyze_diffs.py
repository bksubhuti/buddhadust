import os
import difflib
import sys

def analyze_file_diff(file_path1, file_path2):
    try:
        with open(file_path1, 'r', encoding='utf-8', errors='replace') as f1:
            text1 = f1.read()
        with open(file_path2, 'r', encoding='utf-8', errors='replace') as f2:
            text2 = f2.read()
    except FileNotFoundError:
        return None

    s = difflib.SequenceMatcher(None, text1, text2)
    
    categories = {
        '0-4': 0,
        '4-10': 0,
        '10-100': 0,
        '100+': 0
    }
    
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            continue
            
        # Calculate size of the change
        # For replace, we consider the max of deletion or insertion as the "impact" size
        # For insert, it's the length of inserted text
        # For delete, it's the length of deleted text
        
        len1 = i2 - i1
        len2 = j2 - j1
        
        change_size = max(len1, len2)
        
        if change_size == 0:
            continue
            
        if change_size < 4:
            categories['0-4'] += 1
        elif change_size < 10:
            categories['4-10'] += 1
        elif change_size < 100:
            categories['10-100'] += 1
        else:
            categories['100+'] += 1
            
    return categories

def main():
    dir1 = 'mn/src/v0.4'
    dir2 = 'mn/src/v2.0'
    
    files1 = set(os.listdir(dir1))
    files2 = set(os.listdir(dir2))
    
    common_files = sorted(list(files1.intersection(files2)))
    
    total_stats = {
        '0-4': 0,
        '4-10': 0,
        '10-100': 0,
        '100+': 0
    }
    
    print(f"Analyzing {len(common_files)} common files...")
    
    # Let's process the first file specifically as requested
    first_file = 'mn.001.horn.pts.htm'
    if first_file in common_files:
        stats = analyze_file_diff(os.path.join(dir1, first_file), os.path.join(dir2, first_file))
        print(f"\n--- Analysis for {first_file} ---")
        print(stats)
        print("----------------------------------\n")
        
        # Add to total
        for k, v in stats.items():
            total_stats[k] += v
            
    # Process the rest
    count = 0
    for filename in common_files:
        if filename == first_file:
            continue
            
        # Only process .htm files
        if not filename.endswith('.htm'):
            continue
            
        stats = analyze_file_diff(os.path.join(dir1, filename), os.path.join(dir2, filename))
        if stats:
            for k, v in stats.items():
                total_stats[k] += v
        
        count += 1
        if count % 10 == 0:
            print(f"Processed {count} files...")

    print("\n=== Total Statistics (All Files) ===")
    print(f"0-4 chars:    {total_stats['0-4']}")
    print(f"4-10 chars:   {total_stats['4-10']}")
    print(f"10-100 chars: {total_stats['10-100']}")
    print(f"100+ chars:   {total_stats['100+']}")

if __name__ == "__main__":
    main()
