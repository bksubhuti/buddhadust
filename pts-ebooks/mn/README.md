## Majjhima Nikaya

-------------------------------

### How to Remove Content Using RegEx in Sigil

This guide assumes you've already added your HTML files into Sigil.

The buddhadust pts-mn files can be found [here](https://github.com/bksubhuti/buddhadust/tree/master/dhamma-vinaya/pts/mn):


1. Double-click into first HTML file
2. Click top line of file
3. Click "Find & Replace"
4. Select "Regex" and "All HTML Files" at the bottom
5. Paste Regex line into "Find" field
6. Select options, if necessary
7. Click "Replace All"
8. Repeat Steps 5-7 for each desired operation

NOTE: Unless otherwise specified, the "Replace" field is always left blank

### Resources for RegEx

* Online RegEx reference and playground: https://regexr.com/
* Excellent text editor that supports RegEx: https://www.sublimetext.com/3

- - -

# MN Reformatting Notes

* Sutta 1 has a non-standard footer (addressed by removing manually)
* Sutta 120's "Thus Have I Heard" is formatted strangely (addressed by fixing manually)
* When a Title has an endnote (16, 48, 51, 83, 95, 102, 109, 119, 120, 130, 136, 139, 152) it appears in the TOC text (addressed by removing manually)

-------------------------------

# MN Reformatting Expressions

These expressions are to be performed in the same order as listed.  For instance, the order of operations is necessary to remove keep the links for the footnotes but to remove all other hyperlinks.



### 1. Change "m" and "n" Style

Find:

a. `ɱ`
b. `ŋ`

Replace:

a. `ṁ`
b. `ṅ`


### 2. Remove Headers + Homepage Line + Nav
DotAll = ON | Wrap = ON

Find:

`<head>.*(?=<div class="main">)`

Replace:

`<head><title></title></head><body>`


### 3. Reformat Titles
DotAll = ON | Minimal Match = OFF | Wrap = ON

Find:

`<h4 class="ctr">.*Sutta (\d+).*>([^>]* Suttaṃ?).*<h1>(.*)<\/h1>`

Replace:

`<h1>\1. \3</h1><h2>\2</h2>`

OR

### 3. Promote Sutta titles to H2 and place underneath (move to after link removal)

Find:

`<h4 class="ctr">[^>]*Sutta (\d+).*>([^>]* Suttaṃ?).*<h1>(.*)<\/h1>`

Replace:

`<h1>\1. \3</h1><h2>\2</h2>`



### 4. Remove Translation Links
DotAll = OFF | Wrap = ON

`<span class="f[34]"><[ab].*\]<\/span> ` (include the space at the end) (267)
or
`<span class="f[34]">\[?<[ab].*\]<\/span> ` (269)

#### Bug to Report

* Sutta 6 is differently formatted at the beginning, missing bracket


### 5a. Rename Note Links
_The purpose of this RegEx is to remove the links but preserve a uniqueness that can be restored back after all global links are removed._

DotAll = OFF | Wrap = ON

Find:

`(<sup>.*<)(a)(.*\/)(a)>(?=.*<\/sup>)`


### 5b. Remove Text Links
_This RegEx will remove any hyperlink or anchor tags_
DotAll = OFF | Minimal Match = ON | Wrap = ON

`<\/?a(?:(?= )[^>]*)?>`


### 5c. Restore Note Links
_This RegEx will restore the hyperlinks for the footnotes that were previously renamed._

DotAll = OFF | Wrap = ON

Find:

`aNOTE`

Replace:

`a`



### 6. Remove Inline Images / Float Boxes
DotAll = ON | Minimal Match = ON | Wrap = ON

`<div class="float[lr](?:pp)?.*?<\/div>` (93)


### 7. Remove Footers
DotAll = ON | Wrap = ON

`<p class="fine ctr c">.*<\/p>` (152)


### 8. Remove Boilerplate
DotAll = ON | Minimal Match = ON | Wrap = ON

`<h4 class="ctr.*<\/h4>` (4?)


### 9. Remove Copyright
DotAll = ON | Wrap = ON

`<p class="ctr">.*(?:Use|permission|Chow|Genaud).<\/p>` (160)


### 10. Remove Brackets on Endnotes
DotAll = OFF | Minimal Match = ON | Wrap = ON

Find:

`<sup>\[(.*)\]<\/sup>` (6700)
	or
`(<sup>.*?)\[(.*?)\](.*?<\/sup>)` (6726) M=0

Replace:

`\1\2\3`


### 11. Fix "Thus Have I Heard" Bolding

Find:

`T<span class="f2"><b>HUS`

Replace:

`<span class="f2"><b>THUS`



- - -

## Deprecated / Unused

### 2. Add Sutta # Before Title
DotAll = ON | Minimal Match = OFF | Wrap = ON

Find:

`(<h4 class="ctr">).*(Sutta \d+)(.*)(<h1>)(.*)<\/h1>`

Replace:

`<h1>\2 - \5</h1>`


### 8a. Fix CC Licence Links
DotAll = OFF | Wrap = ON

Find:

`(<a href="http:\/\/creativecommons.*>)(<img.*)</a>`

Replace:

`\1Creative Commons Licence</a>`


### 8b. Remove License Details Text
DotAll = OFF | Wrap = ON

`For details see.*Use\.`


### 1. Remove Headers
DotAll = ON | Wrap = ON

`<head>.*<\/head>`


### 2. Remove Homepage line
DotAll = OFF | Wrap = ON

`<p class="ctr"><img.*</p>`


### 3. Remove Nav
DotAll = OFF | Wrap = ON

`<p class="ctr f2">.*</p>`


### // 8a? Remove Footers A
DotAll = ON | Wrap = ON

`<p class="ctr"><a href="\.\.\/\.\.\/\.\.\/backmatter.*Statement<\/a><\/p>`


### // 8b? Remove Footers B
DotAll = ON | Wrap = ON

`<p class="fine ctr c">.*Statement<\/p>`


### Fix Most External Links
_(alternative to removal, doesn't work for all though)_

DotAll = OFF | Wrap = ON

Find:

`\.\.\/\.\.\/\.\.\/`

Replace:

`http://www.buddhadust.net/`
