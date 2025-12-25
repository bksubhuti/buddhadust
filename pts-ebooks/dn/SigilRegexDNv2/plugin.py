#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

def run(bk):
    # Standard header for the clean files
    standard_header = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n'
        '  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n\n'
        '<html lang="en" xmlns="http://www.w3.org/1999/xhtml">\n'
        '<head><title></title>\n</head>\n<body>\n'
    )

    for (id, href) in bk.text_iter():
        if not href.lower().endswith(('.htm', '.html', '.xhtml')):
            continue

        print('Processing %s' % href)
        html = bk.readfile(id)
        if not isinstance(html, str):
            html = str(html, 'utf-8')
        
        html_orig = html

        # 1. Character Replacements
        html = re.sub(r'ɱ', r'ṁ', html)
        html = re.sub(r'ŋ', r'ṅ', html)

        # 2. Extract Content & Reformat Title
        title_pattern = r'<h4 class="ctr"><a[^>]*>(Sutta \d+)</a></h4>(.*?)<h1>(.*?)</h1>'
        match = re.search(title_pattern, html, re.DOTALL)
        
        start_search_pos = 0
        
        if match:
            sutta_full = match.group(1)
            middle_content = match.group(2)
            eng_title = match.group(3)
            
            sutta_num = re.search(r'\d+', sutta_full).group(0)
            
            subtitles = re.findall(r'<h4[^>]*>(.*?)</h4>', middle_content, re.DOTALL)
            
            new_title = f'<div><h1>{sutta_num}. {eng_title}</h1>\n'
            for sub in subtitles:
                new_title += f'<h3 class="sigil_not_in_toc">{sub.strip()}</h3>\n'
            
            start_search_pos = match.end()
            hr_match = re.search(r'<hr\s*/?>', html[start_search_pos:])
            
            if hr_match:
                body_start = start_search_pos + hr_match.start()
                body_content = '<br/>\n' + html[body_start:]
            else:
                body_content = html[start_search_pos:]
            
            html = standard_header + new_title + body_content
        else:
            main_match = re.search(r'<div class="main">', html)
            if main_match:
                html = standard_header + '<div>' + html[main_match.end():]
            else:
                html = re.sub(r'<head>.*?</head>', '<head><title></title></head>', html, flags=re.DOTALL)

        # 3. Clean Note Links (Run BEFORE removing spans to protect notes inside spans)
        # Handle variations:
        # 1. <sup>[<a...>...</a>]</sup>
        # 2. <sup><span ...>[<a...>...</a>]</span></sup>
        # We want to strip the span and the brackets, keeping the <a>
        html = re.sub(r'<sup>\s*(?:<span[^>]*>)?\s*\[?\s*(<a[^>]*?>.*?</a>)\s*\]?\s*(?:</span>)?\s*</sup>', r'<sup>\1</sup>', html, flags=re.DOTALL | re.IGNORECASE)

        # 4. Remove Cross-References / Translation Links
        html = re.sub(r'<span class="f3">\s*(?:\[?\s*<a[^>]*?>.*?</a>\s*\]?.*?)\s*</span>', '', html, flags=re.DOTALL)
        
        # 5. Remove all other <a> tags (Text Links) but protect Note links
        def check_link(match):
            full_tag = match.group(0)
            attributes = match.group(1)
            content = match.group(2)
            
            # Check if it's a note link or editorial note link
            # Matches: #n1, #fn1, #edn1, #edfn1
            if re.search(r'href\s*=\s*["\']#?(?:ed)?(?:fn|n)\d+["\']', attributes, re.IGNORECASE):
                # Remove brackets from inside the link content if they exist: [77] -> 77
                clean_content = re.sub(r'\[(.*?)\]', r'\1', content)
                # Reconstruct tag
                # We need to be careful not to double-close or mess up attributes
                # Simplified reconstruction: <a href=\"...\">clean_content</a>
                # But attributes might be complex. Better to replace content in full_tag.
                # However, regex replacement on string is safer.
                
                # Check if attributes string is clean enough to just reuse
                return f'<a {attributes}>{clean_content}</a>'
            else:
                return content # Return just the text (strip link)

        html = re.sub(r'<a\s+([^>]*)>(.*?)</a>', check_link, html, flags=re.DOTALL | re.IGNORECASE)

        # 6. Reformat Introductions (Specific Fix)
        html = re.sub(r'<h4[^>]*>\s*Introduction.*?</h4>', r'<h2>Introduction</h2>', html, flags=re.DOTALL | re.IGNORECASE)

        # 7. Convert all REMAINING <h4> to <h2>
        html = re.sub(r'<h4([^>]*)>(.*?)</h4>', r'<h2\1>\2</h2>', html, flags=re.DOTALL | re.IGNORECASE)

        # 8. Remove Inline Images / Floats
        html = re.sub(r'<div class="float[lr].*?</div>', '', html, flags=re.DOTALL)

        # 9. Strip Footer
        footer_pattern_contents = r'<hr\s*/?>\s*<p[^>]*>\s*(?:&nbsp;|&#160;|\s)*\[\s*(?:<a[^>]*>)?Contents'
        footer_pattern_contact = r'<hr\s*/?>\s*<p[^>]*>\s*(?:<b>)?Contact:'
        
        footer_match = re.search(footer_pattern_contents, html, re.DOTALL | re.IGNORECASE)
        if not footer_match:
            footer_match = re.search(footer_pattern_contact, html, re.DOTALL | re.IGNORECASE)
        
        if footer_match:
            html = html[:footer_match.start()]
        
        # 10. Balance Tags
        open_divs = len(re.findall(r'<div[^>]*>', html, re.IGNORECASE))
        close_divs = len(re.findall(r'</div>', html, re.IGNORECASE))
        missing_closes = open_divs - close_divs
        if missing_closes > 0:
            html += '\n</div>' * missing_closes
        
        if '</body>' not in html:
            html += '\n</body>'
        if '</html>' not in html:
            html += '\n</html>'

        if html != html_orig:
            bk.writefile(id, html)
            
    return 0

def main():
    print('I reached main when I should not have\n')
    return -1

if __name__ == "__main__":
    sys.exit(main())
