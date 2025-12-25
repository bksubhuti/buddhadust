import os
import re
import sys

def get_toc_ids(file_path):
    ids = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # In AN v1.1, IDs are on H1, H2, H3, H4
        matches = re.findall(r'<h[1234][^>]*id="(sigil_toc_id_\d+)"', content)
        for i, match in enumerate(matches):
            ids[f'h{i+1}'] = match
    except:
        pass
    return ids

def apply_an_v11_styling(body_html, ids):
    # 1. Standardize Pali
    body_html = body_html.replace('ɱ', 'ṁ').replace('ŋ', 'ṅ')

    # 2. Reformat Headers
    body_html = re.sub(r'<h4 class="ctr"><i>(.*?)</i></h4>', r'<h4 class="ctr">\1</h4>', body_html, flags=re.DOTALL)
    body_html = body_html.replace('<br />', '<br/>')
    
    body_html = re.sub(r'<h4 class="ctr">Suttas? (\d+.*?)</h4>', r'<h3 class="ctr">Suttas \1</h3>', body_html)

    def h1_replacer(m):
        text = m.group(1)
        text = text.replace('Part ', '').replace('<br/>', '. ')
        return f'<h1>{text}</h1>'
    body_html = re.sub(r'<h1>(.*?)</h1>', h1_replacer, body_html, flags=re.DOTALL)

    # 3. Clean
    body_html = body_html.replace('<hr />', '<hr/>')
    body_html = body_html.replace('<p>&nbsp;</p>', '<p>&#160;</p>')
    body_html = body_html.replace('<span class="f1"><sup>', '<span class="f3"><sup>')
    
    body_html = re.sub(r'<h4 class="ctr">The Book of the Gradual Sayings.*?</h4>', '', body_html, flags=re.DOTALL)
    body_html = re.sub(r'<p class="ctr"><b><i>Honour to that Exalted One.*?</i></b></p>', '', body_html, flags=re.DOTALL)
    
    body_html = re.sub(r'<span class="f[34]»[[<]ab.*?]]</span> ?', '', body_html)
    body_html = re.sub(r'<span class="f[34]»[[<]ab.*?]]</span> ?', '', body_html)
    body_html = re.sub(r'(<sup>.*?<)a(.*?>.*?<)(/a)(>.*?</sup>)', r'\1aNOTE\2\3NOTE\4', body_html, flags=re.DOTALL)
    body_html = re.sub(r'</?a(?:(?= )[^>]*)?>', '', body_html)
    body_html = body_html.replace('aNOTE', 'a').replace('/aNOTE', '/a')

    body_html = re.sub(r'T?<span class="f2"><b>HUS</b></span>', 'THUS', body_html)
    body_html = re.sub(r'\bTHUS HAVE I HEARD:', 'THUS have I heard:', body_html, flags=re.IGNORECASE)

    body_html = re.sub(r'<div class="float[lr].*?</div>', '', body_html, flags=re.DOTALL)
    body_html = re.sub(r'<p class="fine ctr c">.*?</p>', '', body_html, flags=re.DOTALL)
    body_html = re.sub(r'<p class="(?:ctr|f2)">Copyright.*? </p>', '', body_html, flags=re.DOTALL)
    body_html = re.sub(r'<p class="(?:c|f)[^>]*?>Translated.*?Use.</p>', '', body_html, flags=re.DOTALL)
    body_html = re.sub(r'<sup>\[(.*?)\]</sup>', r'<sup>\1</sup>', body_html)

    # 4. Inject IDs
    found_headers = re.findall(r'<(h[1234])(.*?>)', body_html)
    for i in range(min(len(found_headers), len(ids))):
        key = f'h{i+1}'
        tag = found_headers[i][0]
        pattern = f'<{tag}{found_headers[i][1]}'
        replacement = f'<{tag} id="{ids[key]}" {found_headers[i][1]}'
        body_html = body_html.replace(pattern, replacement, 1)

    # 5. Indentation
    lines = [line.strip() for line in body_html.split('\n') if line.strip()]
    return "\n\n".join(["    " + l for l in lines])

def get_v11_boilerplate(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        header = content.split('<div class="main">')[0] + '<div class="main">'
        tail = "</div>\n\n<hr/>\n</body>\n</html>"
        return header, tail
    except:
        header = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head><title></title></head>
<body>
  <div class="main">"""
        tail = "  </div>\n\n<hr/>\n</body>\n</html>"
        return header, tail

def process_file(filename, v11_dir, v2_dir, out_dir):
    v2_path = os.path.join(v2_dir, filename)
    v11_path = os.path.join(v11_dir, filename)
    if not os.path.exists(v2_path): return
    
    ids = get_toc_ids(v11_path)
    header, tail = get_v11_boilerplate(v11_path)
    with open(v2_path, 'r', encoding='utf-8') as f:
        v2_content = f.read()
        
    main_match = re.search(r'<div class="main">(.*?)</div>', v2_content, re.DOTALL)
    body_to_style = main_match.group(1) if main_match else v2_content
    
    styled_body = apply_an_v11_styling(body_to_style, ids)
    final_output = header + "\n" + styled_body + "\n\n" + tail
    
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, filename), 'w', encoding='utf-8') as f:
        f.write(final_output)
    print(f"Processed {filename}")

if __name__ == "__main__":
    v11_dir = 'an/src/v1.1'
    v2_dir = 'an/src/v2.0'
    out_dir = 'an/src/epub_v2_styled_an'
    
    if not os.path.exists(v11_dir):
        print(f"Error: {v11_dir} not found")
        sys.exit(1)

    v11_files = set(os.listdir(v11_dir))
    v2_files = set(os.listdir(v2_dir))
    common_files = sorted(list(v11_files.intersection(v2_files)))
    
    files = common_files
    if '--all' not in sys.argv:
        files = common_files[:5]
        
    for f in files:
        process_file(f, v11_dir, v2_dir, out_dir)
