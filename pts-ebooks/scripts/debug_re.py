import re

content = """<h2 id="sigil_toc_id_2" title="1. The Devas">1. The Devas<span class="f3"><sup><a id="fn1" href="#n1">1</a></sup></span></h2>"""

def protect_notes(match):
    attrs = match.group(1).strip()
    inner = match.group(2)
    print(f"Match found: attrs='{attrs}', inner='{inner}'")
    if re.search(r'(id|href)=["\']#?(fn|n)\d+["\']', attrs):
        return f'###OPEN###{attrs}###INNER###{inner}###CLOSE###'
    return inner

new_content = re.sub(r'<a ([^>]+)>(.*?)</a>', protect_notes, content, flags=re.S)
print("After protect:", new_content)

new_content = re.sub(r'</?a[^>]*>', '', new_content)
print("After strip:", new_content)

new_content = new_content.replace('###OPEN###', '<a ')
new_content = new_content.replace('###INNER###', '>')
new_content = new_content.replace('###CLOSE###', '</a>')
print("After restore:", new_content)

