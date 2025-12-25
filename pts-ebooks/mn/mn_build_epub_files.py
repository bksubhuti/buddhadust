import os
import re
import sys

def get_toc_ids(file_path):
    """Harvests sigil_toc_ids from h1 and h2 tags in the given file."""
    ids = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        h1_match = re.search(r'id="(sigil_toc_id_\d+)"', content)
        if h1_match:
            ids['h1'] = h1_match.group(1)
        h2_matches = re.findall(r'id="(sigil_toc_id_\d+)"', content)
        if len(h2_matches) > 1:
            ids['h2'] = h2_matches[1] # Usually the second one is the h2 ID
    except:
        pass
    return ids

def apply_regex_rules(content):
    # 1. Standardize Pali characters
    content = content.replace('ḱ', 'ṁ') # ɱ -> ṁ
    content = content.replace('ŋ', 'ṅ') # ŋ -> ṅ

    # 2. Clean Header
    content = re.sub(r'<head>.*?(?=<div class="main">)', 
                    '<head><title></title></head>\n<body>\n', 
                    content, flags=re.DOTALL)

    # 3. Reformat Titles (H1 and H2)
    title_pattern = re.compile(
        r'<h4 class="ctr"><a [^>]*>Sutta (\d+)</a></h4>\s*'
        r'<h4 class="ctr"><i>(.*?)</i>.*?</h4>\s*'
        r'<h1>(.*?)</h1>', 
        re.DOTALL
    )
    def title_replacer(m):
        pali = re.sub(r'<.*?>', '', m.group(2)) # Strip nested tags like footnotes
        return f'<h1>{m.group(1)}. {m.group(3)}</h1>\n<h2>{pali}</h2>'
    content = title_pattern.sub(title_replacer, content)

    # 4. Remove Ref Blocks and Paragraph Numbers
    # Using hex \x5b for [ and \x5d for ] to avoid escaping issues
    content = re.sub(r'<span class="f3">\x5b<a.*?</span> ?', '', content)
    content = re.sub(r'<span class="f[34]">\x5b<[ab].*?\x5d</span> ?', '', content)
    content = re.sub(r'<span class="f[34]">\x5b?<[ab].*?\x5d</span> ?', '', content)

    # 5. Clean Links (Keep footnotes)
    content = re.sub(r'(<sup>.*?<)a(.*?>.*?<)(/a)(>.*?</sup>)', r'\1aNOTE\2\3NOTE\4', content, flags=re.DOTALL)
    content = re.sub(r'</?a(?:(?= )[^>]*)?>', '', content)
    content = content.replace('aNOTE', 'a')

    # 6. Remove Floats and Footers
    content = re.sub(r'<div class="float[lr].*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<p class="fine ctr c">.*?</p>', '', content, flags=re.DOTALL)
    content = re.sub(r'<p class="f2 ctr">Copyright.*?</p>', '', content, flags=re.DOTALL)
    content = re.sub(r'<p class="ctr">Translated from the Pali.*?</p>', '', content, flags=re.DOTALL)

    # 7. Clean Endnote Brackets
    content = re.sub(r'<sup>\x5b(.*?)\x5d</sup>', r'<sup>\1</sup>', content)

    # 8. Fix "Thus Have I Heard"
    content = content.replace('T<span class="f2"><b>HUS', '<span class="f2"><b>THUS')
    content = content.replace('H<span class="f2"><b>AVE</b></span><span class="f2"><b>EARD</b></span>', 'HAVE I HEARD')
    content = content.replace('H<span class="f2"><b>AVE</b></span> <span class="f2"><b>HEARD</b></span>', 'HAVE I HEARD')

    # 9. Final Clutter Removal
    content = re.sub(r'\x5b<a href.*Sutta Search.*\x5d', '', content)
    content = content.replace('\r\n', '\n')
    return content

def inject_toc_ids(content, ids):
    if 'h1' in ids:
        content = re.sub(r'<h1>', f'<h1 id="{ids["h1"]}">', content, count=1)
    if 'h2' in ids:
        content = re.sub(r'<h2>', f'<h2 id="{ids["h2"]}">', content, count=1)
    return content

def process_file(filename, v0_4_dir, v2_dir, out_dir):
    v2_path = os.path.join(v2_dir, filename)
    if not os.path.exists(v2_path): return
    
    ids = get_toc_ids(os.path.join(v0_4_dir, filename))
    with open(v2_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    processed = apply_regex_rules(text)
    final = inject_toc_ids(processed, ids)
    
    with open(os.path.join(out_dir, filename), 'w', encoding='utf-8') as f:
        f.write(final)
    print(f"Processed {filename}")

if __name__ == "__main__":
    dirs = {'v0_4': 'mn/src/v0.4', 'v2': 'mn/src/v2.0', 'out': 'mn/src/epub_v2'}
    os.makedirs(dirs['out'], exist_ok=True)
    files = sorted([f for f in os.listdir(dirs['v2']) if f.endswith('.htm')])
    if '--all' not in sys.argv: files = files[:5] + ['mn.120.horn.pts.htm']
    for f in files:
        process_file(f, dirs['v0_4'], dirs['v2'], dirs['out'])