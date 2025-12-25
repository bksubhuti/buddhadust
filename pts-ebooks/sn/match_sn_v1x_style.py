import os
import re
import json

def process_file(file_path, output_path, harvested_ids):
    filename = os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize newlines
    content = content.replace('\r\n', '\n')

    # 1. Change "m" and "n" Style
    content = content.replace('ɱ', 'ṁ')
    content = content.replace('ŋ', 'ṅ')

    # 2. Remove Headers + Nav
    content = re.sub(r'<!DOCTYPE.*?(?=<div class="main">)', '', content, flags=re.S)
    
    # Remove footer
    content = re.sub(r'<hr />\s*<p class="fine ctr c">.*', '', content, flags=re.S)
    if '</div>' in content:
        content = content.rsplit('</div>', 1)[0] + '</div>'

    # Normalize <br /> to <br/>
    content = content.replace('<br />', '<br/>')

    # Robust Boilerplate Removal (Translated by, Copyright, etc.)
    # We target paragraphs with "ctr" class that contain these keywords.
    # We do this before link protection because these paragraphs often contain links to translators.
    for keyword in ["Translated", "Copyright", "Public Domain", "Terms of Use"]:
        content = re.sub(r'<p[^>]*class="[^"]*ctr[^"]*"[^>]*>.*?' + keyword + r'.*?</p>', '', content, flags=re.S | re.I)

    # Remove Inline Images
    content = re.sub(r'<div class="float[lr](?:pp)?.*?<\/div>', '', content, flags=re.S)
    content = re.sub(r'<p class="ctr"><img src=".*?"></p>', '', content)

    # 4. Remove Translation Links
    # Safe regex that won't eat footnotes (which are f1)
    # The README says f3 or f4.
    content = re.sub(r'<span class="f[34]">\[?<[ab].*?\]</span>\s*', '', content)

    # Convert all f1 to f3
    content = content.replace('class="f1"', 'class="f3"')

    # Step 5: Clean up links - Store and Restore Strategy
    links_to_restore = []
    
    def protect_and_store(match):
        full_tag = match.group(0)
        attrs = match.group(1)
        # Check if it's a footnote link (standard or editorial)
        if re.search(r'(id|href)=["\']#?(?:ed)?(?:fn|n)\d+["\']', attrs):
            placeholder = f'###LINK_{len(links_to_restore)}###'
            links_to_restore.append(full_tag)
            return placeholder
        return match.group(2) # Return inner text (stripping tag)

    # Match full anchor tags
    content = re.sub(r'<a ([^>]+)>(.*?)</a>', protect_and_store, content, flags=re.S)
    
    # Strip any remaining (orphan) a tags
    content = re.sub(r'</?a[^>]*>', '', content)
    
    # Restore valid links
    # Restore in reverse order just in case? No, unique IDs are fine.
    for i, link in enumerate(links_to_restore):
        content = content.replace(f'###LINK_{i}###', link)

    # Remove brackets from sups
    content = content.replace('<sup>[', '<sup>').replace(']</sup>', '</sup>')

    # Fix "THUS HAVE I HEARD" - SN v1.0 style
    content = content.replace('T<span class="f2"><b>HUS</b></span>', '<span class="f2"><b>THUS</b></span>')
    content = content.replace('H<span class="f2"><b>AVE</b></span>', '<span class="f2"><b>HAVE</b></span>')
    content = content.replace('E<span class="f2"><b>ARD:</b></span>', '<span class="f2"><b>EARD:</b></span>')

    # Reformat Headers
    ids_for_file = harvested_ids.get(filename, [])
    h4_blocks = re.findall(r'<h4 class="ctr">(.*?)</h4>', content, re.S)
    
    id_idx = 0
    for h4_inner in h4_blocks:
        if '<i>' in h4_inner: # Pali hierarchy
            content = content.replace(f'<h4 class="ctr">{h4_inner}</h4>', 
                                      f'<h4 class="ctr sigil_not_in_toc">{h4_inner.strip()}</h4>')
        elif 'Kindred Sayings' in h4_inner or 'Suttas' in h4_inner:
            h4_inner_clean = re.sub(r'(?:The )?(?:Book of the)? ?(?:<br/>)? ?Kindred Sayings<br/>\s*', '', h4_inner)
            lines = [l.strip() for l in h4_inner_clean.split('<br/>') if l.strip()]
            
            replacement = []
            for line in lines:
                if id_idx < len(ids_for_file):
                    info = ids_for_file[id_idx]
                    clean_line = re.sub(r'<[^>]+>', '', line).strip()
                    if info['text'] in clean_line or clean_line in info['text']:
                        tag = info['tag']
                        tid = info['id']
                        title = info['title']
                        replacement.append(f'<{tag} id="{tid}" title="{title}">{line}</{tag}>')
                        id_idx += 1
                    else:
                        replacement.append(f'<h4 class="ctr sigil_not_in_toc">{line}</h4>')
                else:
                    replacement.append(f'<h4 class="ctr sigil_not_in_toc">{line}</h4>')
            
            content = content.replace(f'<h4 class="ctr">{h4_inner}</h4>', '\n'.join(replacement))

    # Demote Sutta title H1s to H2 sigil_not_in_toc
    content = re.sub(r'<h1>(.*?)</h1>', r'<h2 class="sigil_not_in_toc">\1</h2>', content)
    content = re.sub(r'<h4 class="ctr">', r'<h4 class="ctr sigil_not_in_toc">', content)

    # Wrap in proper XHTML structure
    xhtml_header = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title></title>
</head>

<body>
'''
    final_content = xhtml_header + content.strip() + '\n</body>\n</html>'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

if __name__ == "__main__":
    v2_dir = "src/v2.0"
    output_dir = "src/epub_v2_styled_sn"
    os.makedirs(output_dir, exist_ok=True)
    
    with open("sn_ids.json", "r", encoding="utf-8") as f:
        harvested_ids = json.load(f)
        
    for filename in os.listdir(v2_dir):
        if filename.endswith(".htm") or filename.endswith(".xhtml"):
            process_file(os.path.join(v2_dir, filename), os.path.join(output_dir, filename), harvested_ids)
    
    print(f"Processed files into {output_dir}")