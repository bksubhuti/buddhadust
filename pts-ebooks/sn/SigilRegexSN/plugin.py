#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
 
import sys 
import re  #for regex


text_type = str 
def run(bk):  
    for (id, href) in bk.text_iter():  #For each html file in the 'text' section of the epbu   
        print('Chapter found %s:' % href) #Print the section name   
        html = bk.readfile(id)   #Read the section into html   
        if not isinstance(html, text_type): #If the section is not str    
            html = text_type(html, 'utf-8') #then sets its type to 'utf-8'   

        html_orig = html     #Copy the text to html_orig 
 
        # Expression Template
        # html = re.sub(r'',r'', html, 0, 0)


        # Change "m" and "n" Style
        html = re.sub(r'ɱ',r'ṁ', html, 0, 0)
        html = re.sub(r'ŋ',r'ṅ', html, 0, 0)

        # Remove Headers + Homepage Line + Nav
        html = re.sub(r'<head>.*(?=<div class="main">)',r'<head><title></title></head><body>', html, 0, re.DOTALL)


        # REFORMAT TITLES

        # A. Demote H1s to H3
        # html = re.sub(r'(?:<h1)(.*?)(?:h1>)',r'<h3\1h3>', html, 0, re.DOTALL)

        # B. Promote individual "Sutta(s) headers to H2
        # html = re.sub(r'(?:<h4)(.*Suttas? \d+.*)(?:h4>)',r'<h2\1h2>', html, 0, 0)

        # Remove Translation Links
        html = re.sub(r'<span class="f[34]">\[?<[ab].*\]<\/span> ',r'', html, 0, 0)
        

        # REFORMAT NOTE LINKS

        # A. Rename Note Links
        html = re.sub(r'(<sup>.*<)(a)(.*\/)(a)>(?=.*<\/sup>)',r'\1aNOTE\3aNOTE>', html, 0, 0)
        
        # B. Remove Text Links
        html = re.sub(r'<\/?a(?:(?= )[^>]*)?>',r'', html, 0, 0)

        # C. Restore Note Links
        html = re.sub(r'aNOTE',r'a', html, 0, 0)


        # Remove Float Boxes / Inline Images
        html = re.sub(r'<div class="float[lr](?:pp)?.*?<\/div>',r'', html, 0, re.DOTALL)

        # Remove Footers
        html = re.sub(r'<p class="fine ctr c">.*<\/p>',r'', html, 0, re.DOTALL)
        
        # Remove Copyright
        html = re.sub(r'<p class="(?:c|f)[^>]*?>Translated.*?(?:Use\.|Domain)<\/p>',r'', html, 0, re.DOTALL)

        # Remove Brackets on Endnotes
        html = re.sub(r'(<sup>.*?)\[(.*?)\](.*?<\/sup>)',r'\1\2\3', html, 0, 0)


 
        if not html == html_orig:   #If the text has changed         
            bk.writefile(id, html)   #Write the amended text to the book 
            
    return 0    # 0 - means success, anything else means failure  


def main():
    print('I reached main when I should not have\n')
    return(-1)

if __name__ == "__main__":
    sys.exit(main())