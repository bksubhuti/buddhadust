## Anguttara Nikaya

-------------------------------

### How to Reformat Content Using RegEx in Sigil

This guide assumes you've already added your HTML files into Sigil.

1. Double-click into first HTML file
2. Click top line of file
3. Click "Find & Replace"
4. Select "Regex" and "All HTML Files" at the bottom
5. Paste Regex line into "Find" field
6. Select options, if necessary
7. Click "Replace All"
8. Repeat Steps 5-7 for each desired operation

NOTE: Unless specified, the "Replace" field is left blank and "Wrap" is always ON

### Resources for RegEx

* Online RegEx reference and playground: https://regexr.com/
* Excellent text editor that supports RegEx: https://www.sublimetext.com/3

-------------------------------

# AN Reformatting Notes

* All operations just take longer, especially generating the HTML TOC and adding the cover


# Build Steps

1. Re-order Suttas
2. Run expressions
3. Build TOC, removing items and endnote numbers
4. Add HTML TOC
5. Add Cover

-------------------------------

# AN Reformatting Expressions


### 1. Change "m" and "n" Style
DotAll = OFF

Find:

a. `ɱ`
b. `ŋ`

Replace:

a. `ṁ`
b. `ṅ`


### 2. Remove Headers + Homepage Line + Nav
DotAll = ON

Find:

`<head>.*?(?=<div class="main">)`

Replace:

`<head><title></title></head><body>`


### 3. Alternate TOC generation

#### Remove "Gradual Sayings" text

##### a. Book 1

Find: `(<h[34][^>]*?>)The Book of the Gradual Sayings.*?Ones<\/h3>` D=1

##### b. Books 2-11
Find: `(<h[34][^>]*?>)The Book of the Gradual Sayings.*?(?=(?:[XVI\. ]+)?The [Bb]ook)` D=1
Replace: `\1` (1327)

##### c. Book 4 Chapters VII and VIII (special fix)
Find: `(Fours)[^<>]*?(Chapter )`
Replace: `\1<br/>`


#### Demote Sutta(s) to H3

Find: `(?:<h2)(.*?Suttas? \d+(?:-\d+)?.*?)(?:h2>)` D=1

Replace: `<h3\1h3>`


#### Promote Book Titles to H1 + Promote Chapter Titles to H2

Find: `(<h4[^>]*?>)([^ṅ]*?(?:Ones|Twos|Threes|Fours|Fives|Sixes|Sevens|Eights|Nines|Tens|Elevens))(<br\/>)(.*?)(<\/h4>)` D=1

Replace: `<h1>\2</h1><h2>\4</h2>`


#### Manual Polish

a. Tell Sigil to include *nothing* in the TOC, which makes it add a "not_in_toc" class to all headers
b. Go in and manually remove that class for the headers we want in the TOC
c. Formatting stays how we like it, and we only get the TOC items we want




### 3a. Reformat Titles

#### Issues

* Part I - Must manually change the first "Part I" title back to H1 before building TOC, then remove the others when building the TOC
* Part II - Sub-sections appear with Roman Numerals instead of as a separate header

#### Solution?

1. Demote all H1 and H2 to H3
2. Promote "Suttas" H4s to H2
	* Leaves large gaps in the TOC, maybe better to include more detailed nav by including the "Sutta" headers?
3. Manually Promote / Add eleven "Part" headers to H1


### 3a. Demote H1s to H3

Find:

a. `(?:<h1)(.*?)(?:h1>)` DA=1 (3315)

Replace:

`<h3\1h3>`



### 3b and 3c COMBINATION
DotAll = OFF

Find: `(?:<h4)(.*Suttas? \d+.*)(?:h4>)`
or
`(?:<h4)(.*?Suttas? \d+(?:-\d+)?.*?)(?:h4>)`

Replace:

`<h2\1h2>`


### 4. Remove Translation Links
DotAll = OFF | Wrap = ON

`<span class="f[34]">\[?<[ab].*\]<\/span> ` (include the space at the end) (4365)



### 5a. Rename Note Links
DotAll = OFF | Minimal Match = ON

Find:

`(<sup>.*<)(a)(.*\/)(a)>(?=.*<\/sup>)` (10835)

Replace:

`\1aNOTE\3aNOTE>`


### 5b. Remove Text Links
DotAll = OFF | Minimal Match = ON | Wrap = ON

`<\/?a(?:(?= )[^>]*)?>` (44466)



### 6c. Restore Note Links
DotAll = OFF | Wrap = ON

Find:

`aNOTE` (21670)

Replace:

`a`


### 7. Remove Inline Images / Float Boxes
DotAll = ON

`<div class="float[lr](?:pp)?.*?<\/div>` M=0 (208)


### 8. Remove Footers
DotAll = ON | Minimal Match = ON | Wrap = ON

Find:

`(?:<p class="ctr"(?: style="margin-top: 4px")?>&#160;\[(?:Contents |Ones).*)?<\/div>\n\n<hr\/>\n?\n?<p class="fine ctr c">.*<\/p>` (46)

Replace:

`</div><hr/>`


or
Find `<p class="fine ctr c">.*<\/p>` (minimal) (1353)



### 10. Remove Copyright
DotAll = ON

`<p class="(?:ctr|f2)">Translated.*?&#160;<\/p>`
	or
`<p class="(?:c|f)[^>]*?>Translated.*?Use.<\/p>` (seems to match the rest)



### 11. Remove Brackets on Endnotes
DotAll = OFF | Minimal Match = ON | Wrap = ON

Find:

`(<sup>.*)\[(.*)\](.*<\/sup>)` (10834)

Replace:

`\1\2\3`



- - -

## Deprecated / Unused


### 12. Fix "Thus Have I Heard" Bolding (remove?)

Find:

`T<span class="f2"><b>HUS`

Replace:

`<span class="f2"><b>THUS`


### 9. Remove Boilerplate before title (do not use?)
DotAll = ON | Minimal Match = ON | Wrap = ON

`<h4.*Aṅguttar.*Suttas.*h2>`

or

Find: `<h4.*Aṅguttar.*Suttas.*([XVI]+)` Replace: `<h4>\1` 
(strips everything before the roman numerals of the Book title)

#### Issues

* Roman numeral use before title is inconsistent


### 3b. Promote Suttas H4s to H2
DotAll = OFF

Find:

`(?:<h4)(.*Suttas.*)(?:h4>)` (Works, but a couple of headers have additional text)

Replace:

`<h2\1h2>`


### 3c. Promote individual Sutta headers to H2
DotAll = OFF

Find: `(?:<h4)(.*Sutta \d+.*)(?:h4>)`
Replace: `<h2\1h2>`