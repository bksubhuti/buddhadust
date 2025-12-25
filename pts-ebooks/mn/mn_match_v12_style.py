import os
import re
import sys

def get_toc_ids(file_path):
    """Harvests sigil_toc_ids from h1 and h2 tags in the given file."""
    ids = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Find h1 id
        h1_match = re.search(r'id="(sigil_toc_id_\d+)"', content)
        if h1_match:
            ids['h1'] = h1_match.group(1)
        # Find h2 id (usually the 2nd sigil ID in the file)
        h2_matches = re.findall(r'id="(sigil_toc_id_\d+)"', content)
        if len(h2_matches) > 1:
            ids['h2'] = h2_matches[1]
    except:
        pass
    return ids

def apply_v12_styling(body_html, ids):
    # 1. Standardize Pali
    body_html = body_html.replace('ɱ', 'ṁ').replace('ŋ', 'ṅ')

    # 2. Extract components for the header
    h4s = re.findall(r'<h4 class="ctr">.*?</h4>', body_html, re.DOTALL)
    h1_match = re.search(r'<h1>(.*?)</h1>', body_html, re.DOTALL)
    
    # Process top headers
    top_headers = ""
    if len(h4s) >= 2:
        h4_1 = re.sub(r'</?i>', '', h4s[0]).replace('<br />', '<br/>').strip()
        top_headers += "    " + h4_1 + "\n\n"
        h4_2 = re.sub(r'</?i>', '', h4s[1]).replace('<br />', '<br/>').strip()
        top_headers += "    " + h4_2 + "\n\n"

    # Process Sutta Title (H1)
    sutta_title = ""
    sutta_num = ""
    num_match = re.search(r'Sutta (\d+)', body_html)
    if num_match:
        sutta_num = num_match.group(1)
    
    if h1_match:
        title_text = h1_match.group(1).replace('<br />', '<br/>')
        title_text = re.sub(r'<span class="f1">.*?</span>', '', title_text).strip()
        h1_id_attr = f' id="{ids["h1"]}"' if 'h1' in ids else ""
        if sutta_num:
            sutta_title += f"    <h1{h1_id_attr}>{sutta_num}. {title_text}</h1>\n\n"
        else:
            sutta_title += f"    <h1{h1_id_attr}>{title_text}</h1>\n\n"

    # Process Pali Title (H2)
    pali_title_str = ""
    for h4 in h4s:
        if any(x in h4 for x in ['Suttaṃ', 'Sutta']) and all(x not in h4 for x in ['Nikāya', 'Sayings', 'Sutta ']):
            p_title = re.sub(r'</?i>', '', h4)
            p_title = re.sub(r'<h4.*?>', '', p_title).replace('</h4>', '').strip()
            # Remove footnote span
            p_title = re.sub(r'<span class="f1">.*?</span>', '', p_title)
            h2_id_attr = f' id="{ids["h2"]}"' if 'h2' in ids else ""
            pali_title_str = f"    <h2{h2_id_attr}>{p_title}</h2>\n\n"
            break

    # Strip all headers from body
    body_clean = re.sub(r'<h\d.*?>.*?</h\d>', '', body_html, flags=re.DOTALL)
    
    # 3. Clean the rest of the body
    body_clean = body_clean.replace('<br />', '<br/>').replace('<hr />', '<hr/>')
    body_clean = body_clean.replace('<p>&nbsp;</p>', '<p>&#160;</p>')
    body_clean = body_clean.replace('<span class="f1"><sup>', '<span class="f3"><sup>')
    
    # Remove Translation Links / Paragraph Numbers (Hex for robust match)
    body_clean = re.sub(r'<span class="f3">\x5b<a.*?</span> ?', '', body_clean)
    body_clean = re.sub(r'<span class="f[34]">\x5b<[ab].*?\x5d</span> ?', '', body_clean)
    body_clean = re.sub(r'<span class="f[34]">\x5b?<[ab].*?\x5d</span> ?', '', body_clean)
    
    # Link cleaning
    body_clean = re.sub(r'(<sup>.*?<)a(.*?>.*?<)(/a)(>.*?</sup>)', r'\1aNOTE\2\3NOTE\4', body_clean, flags=re.DOTALL)
    body_clean = re.sub(r'</?a(?:(?= )[^>]*)?>', '', body_clean)
    body_clean = body_clean.replace('aNOTE', 'a').replace('/aNOTE', '/a')

    # Drop caps / Opening
    body_clean = re.sub(r'T?<span class="f2"><b>HUS</b></span>\s*(?:HAVE I HEARD|H<span.*?EARD).*?(:)', 
                    r'<span class="f2"><b>THUS</b></span> have I heard\1', body_clean, flags=re.IGNORECASE)

    # General boilerplate removal
    body_clean = re.sub(r'<div class="float[lr].*?</div>', '', body_clean, flags=re.DOTALL)
    body_clean = re.sub(r'<p class="fine ctr c">.*?</p>', '', body_clean, flags=re.DOTALL)
    body_clean = re.sub(r'<p class="f2 ctr">Copyright.*?</p>', '', body_clean, flags=re.DOTALL)
    body_clean = re.sub(r'<p class="ctr">Translated from the Pali.*?</p>', '', body_clean, flags=re.DOTALL)
    body_clean = re.sub(r'<p class="ctr">First Published in 1954.*?</p>', '', body_clean, flags=re.DOTALL)
    body_clean = re.sub(r'<p class="ctr">Associate of Newham.*?</p>', '', body_clean, flags=re.DOTALL)
    body_clean = re.sub(r'<p class="ctr">Scanned, digitized.*?</p>', '', body_clean, flags=re.DOTALL)
    body_clean = re.sub(r'<sup>\x5b(.*?)\x5d</sup>', r'<sup>\1</sup>', body_clean)
    body_clean = re.sub(r'\x5b<a href.*Sutta Search.*\x5d', '', body_clean)

    # 4. Indentation and Spacing
    lines = [line.strip() for line in body_clean.split('\n') if line.strip()]
    indented_body = "\n\n".join(["    " + l for l in lines])
    
    return top_headers + sutta_title + pali_title_str + indented_body

def get_v12_boilerplate(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        header = content.split('<div class="main">')[0] + '<div class="main">'
        tail = "</div>\n\n<hr/>\n</body>\n</html>"
        return header, tail
    except:
        header = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1//EN\"
  \"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html lang=\"en\" xmlns=\"http://www.w3.org/1999/xhtml">
<head><title></title></head>
<body>
  <div class=\"main">
"""
        tail = "  </div>\n\n<hr/>\n</body>\n</html>"
        return header, tail

def process_file(filename, v04_dir, v12_dir, v2_dir, out_dir):
    v2_path = os.path.join(v2_dir, filename)
    v12_path = os.path.join(v12_dir, filename)
    v04_path = os.path.join(v04_dir, filename)
    if not os.path.exists(v2_path): return
    
    ids = get_toc_ids(v04_path)
    header, tail = get_v12_boilerplate(v12_path)
    
    with open(v2_path, 'r', encoding='utf-8') as f:
        v2_content = f.read()
        
    main_match = re.search(r'<div class="main">(.*?)</div>', v2_content, re.DOTALL)
    if not main_match: return
    
    styled_body = apply_v12_styling(main_match.group(1), ids)
    final_output = header + "\n" + styled_body + "\n\n" + tail
    
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, filename), 'w', encoding='utf-8') as f:
        f.write(final_output)
    print(f"Processed {filename}")

if __name__ == "__main__":
    v04_dir = 'mn/src/v0.4'
    v12_dir = 'mn/src/v1.2'
    v2_dir = 'mn/src/v2.0'
    out_dir = 'mn/src/epub_v2_styled'
    
    files = ['mn.001.horn.pts.htm', 'mn.120.horn.pts.htm']
    if '--all' in sys.argv:
        files = sorted([f for f in os.listdir(v2_dir) if f.endswith('.htm')])
        
    for f in files:
        process_file(f, v04_dir, v12_dir, v2_dir, out_dir)