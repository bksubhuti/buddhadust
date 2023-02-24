## Digha Nikaya

-------------------------------

# How to Reformat Content Using RegEx in Sigil

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

# DN Reformatting Notes

* Sutta 2/3 has an appendix that doesn't seem to fit
* Sutta 33 has several separate files, intro needs to be dragged to beginning, Subtitles need to be manually combined or reformatted


# Build Steps

1. Re-order Suttas
2. Run expressions
3. Build TOC, removing items and endnote numbers
4. Add HTML TOC
5. Add Cover

-------------------------------

# DN Reformatting Expressions


### 1. Change "m" and "n" Style
DotAll = OFF

Find:

a. `ɱ` (539)
b. `ŋ` (171)

Replace:

a. `ṁ`
b. `ṅ`


### 2. Remove Headers + Homepage Line + Nav
DotAll = ON

Find:

`<head>.*Sections<\/a>]<\/p>` (46)

Replace:

`<head><title></title></head><body>`



### 3a. Reformat Titles
DotAll = ON | Minimal Match = ON | Wrap = ON

Find:

`<h4 class="ctr">.*Sutta (\d++).*>([^>]* Suttan?t?a?ṃ?).*<h1>(.*)<\/h1>` (Matches 43)

Replace:

`<h1>\1. \3</h1><h3>\2</h3>`


### 3? Remove Boilerplate

Find: `<body.*?(?=<h4 class="ctr">Sutta)`
Replace: `<body>\n<div>`


### 3b. Reformat 33. Recital Titles
DotAll = ON | Minimal Match = ON

* Do Intro manually
* Omit `<h1>`s here from TOC manually

Find:

`(33.*)(<h4[^>]*>)([\w\s]+)(<\/h4>)` (9)

Replace:

`\1<h2>\3</h2>`



### 3c. Reformat Introductions
DotAll = ON | Minimal Match = ON

Find:

`<h4[^\n]*Introduction.* Sutta?n?t?a?\.?.*<\/h4>` (22)

Replace:

`<h2>Introduction</h2>`



### 3d. Strip roman numerals from Sutta name headers and promote

Find: `<h[34][^<]*>[XVI]+\. (.*Suttan?n?t?a?.*)<\/h[34]>` DA = ON | M = ON (12)
Replace: `<h2>\1</h2>`

#### Issues

* 19, 22 missing 2nd Sutta title after Intro (place manually?)
* 21 has "Chapter" headings instead of Sutta title after Introduction (target w code)
	Find: `<h3 [^>]*>(.*)<\/h3>` Replace: `<h2>\1</h2>` D0 M0
* 23 has a solo "Chapter I." heading (remove from TOC manually?)
* 24 has the 2nd Sutta title in all caps (fix manually before 2d?) Pāṭika Suttanta



##### 3e. Decrement Second Title's Header for TOC

Find: `<h1>([^\.]*)<\/h1>` D0 M0 (27)
Replace: `<h3>\1</h3>`



### 4. Remove Translation Links
DotAll = OFF | Wrap = ON

`<span class="f[34]">\[?<[ab].*\]<\/span> ` (include the space at the end) (579)



### 5a. Rename Note Links
DotAll = OFF | Minimal Match = ON

Find:

`(<sup>.*<)(a)(.*\/)(a)>(?=.*<\/sup>)` (3590)

Replace:

`\1aNOTE\3aNOTE>`


### 5b. Remove Text Links
DotAll = OFF | Minimal Match = ON | Wrap = ON

`<\/?a(?:(?= )[^>]*)?>` (4504)



### 6c. Restore Note Links
DotAll = OFF | Wrap = ON

Find:

`aNOTE` (7180)

Replace:

`a`


### 7. Remove Inline Images / Float Boxes
DotAll = ON | Minimal Match = ON | Wrap = ON

`<div class="float[lr](?:pp)?.*<\/div>` (49)



### 8. Remove Footers
DotAll = ON | Minimal Match = ON | Wrap = ON

Find:

`(?:<p class="ctr"(?: style="margin-top: 4px")?>&#160;\[(?:Contents |Ones).*)?<\/div>\n\n<hr\/>\n?\n?<p class="fine ctr c">.*<\/p>` (46)

Replace:

`</div><hr/>`


## ! Confirmed WORKING Up to Here ! ##



### 10. Remove Copyright
DotAll = ON | Minimal Match = ON | Wrap = ON

`<p class="ctr">.*(?:Oxford|copyright\.")<\/p>` (41)
`<p class="ctr">Translated.*&#160;<\/p>` (46) (misses some text in 6, 33, BREAKS PREFACE)


### 11. Remove Brackets on Endnotes
DotAll = OFF | Minimal Match = ON | Wrap = ON

Find:

`<sup>\[(.*)\]<\/sup>` (3435)
	or
`(<sup>.*)\[(.*)\](.*<\/sup>)`

Replace:

`<sup>\1</sup>`
or
`\1\2\3`



### Remove Translated By

Find: `<p class="ctr">Translated.*?(?:Oxford)<\/p>` D=1



- - -

## Deprecated / Unused


### 12. Fix "Thus Have I Heard" Bolding (remove?)

Find:

`T<span class="f2"><b>HUS`

Replace:

`<span class="f2"><b>THUS`