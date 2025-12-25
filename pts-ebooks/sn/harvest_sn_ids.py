import os
import re
import json

def harvest_ids(v1_dir):
    file_to_ids = {}
    for filename in os.listdir(v1_dir):
        if filename.endswith(".htm") or filename.endswith(".xhtml"):
            path = os.path.join(v1_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Find all h1-h4 tags
                header_matches = re.findall(r'<(h[1-4])\s+([^>]+)>(.*?)</\1>', content, re.S)
                
                file_ids = []
                for tag, attrs, inner in header_matches:
                    id_match = re.search(r'id="(sigil_toc_id_\d+)"', attrs)
                    title_match = re.search(r'title="([^"]*)"', attrs)
                    
                    if id_match:
                        tid = id_match.group(1)
                        title = title_match.group(1) if title_match else ""
                        clean_inner = re.sub(r'<[^>]+>', '', inner).strip()
                        file_ids.append({
                            'tag': tag,
                            'id': tid,
                            'title': title,
                            'text': clean_inner
                        })
                
                if file_ids:
                    file_to_ids[filename] = file_ids
                    
    return file_to_ids

if __name__ == "__main__":
    v1_src = "sn/src/v1.0"
    ids = harvest_ids(v1_src)
    with open("sn_ids.json", "w", encoding="utf-8") as f:
        json.dump(ids, f, indent=2)
    print(f"Harvested IDs from {len(ids)} files.")