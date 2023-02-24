## Samyutta Nikaya

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

# SN Reformatting Notes

* 


# Build Steps

1. Re-order Suttas
2. Run expressions
3. Build TOC, removing items and endnote numbers
4. Add HTML TOC
5. Add Cover

-------------------------------

# SN Reformatting Expressions


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

`<head>.*(?=<div class="main">)`

Replace:

`<head><title></title></head><body>`



### 3. Reformat Titles for TOC generation

#### Remove "Kindred Sayings" text

Find: `(?:The )?(?:Book of the)? ?(?:<br\/>)? ?Kindred Sayings<br\/> `



#### Demote H1s to H2

Find: `(?:<h1)(.*?)(?:h1>)` D=0

Replace: `<h2\1h2>`


#### Promote Vagga Titles to H1 + Promote Samyutta Titles to H2 + Vaggo Titles to H3?

##### Vagga 1.

Find: `(<h4[^>]*?>)([^ṁ]*?)(<br\/>)(.*?)(<br\/>)( [IVX].*?)(<\/h4>)` D=0
or `(<h4[^>]*?>)([^ṁ]*?)(<br\/>)(.*?)(<br\/>)( \d.*?)(<\/h4>)`
or `(<h4[^>]*?>)([^ṁ]*?)(<br\/>)(.*?)(<\/h4>)`


Replace: `<h1>\2</h1><h2>\4</h2><h3>\6</h3>`
or `<h1>\2</h1><h2>\4</h2>`


#### Manual Polish

a. Tell Sigil to include *nothing* in the TOC, which makes it add a "not_in_toc" class to all headers
b. Go in and manually remove that class for the headers we want in the TOC
c. Formatting stays how we like it, and we only get the TOC items we want





### 4. Remove Translation Links
DotAll = OFF | Wrap = ON

`<span class="f[34]">\[?<[ab].*\]<\/span> ` (include the space at the end) (4365)



### 5a. Rename Note Links
DotAll = OFF

Find:

`(<sup>.*<)(a)(.*\/)(a)>(?=.*<\/sup>)`

Replace:

`\1aNOTE\3aNOTE>`


### 5b. Remove Text Links
DotAll = OFF | Minimal Match = ON | Wrap = ON

`<\/?a(?:(?= )[^>]*)?>`



### 6c. Restore Note Links
DotAll = OFF | Wrap = ON

Find:

`aNOTE` (21670)

Replace:

`a`


### 7. Remove Inline Images / Float Boxes
DotAll = ON

`<div class="float[lr](?:pp)?.*?<\/div>`


### 8. Remove Footers
DotAll = ON


Find `<p class="fine ctr c">.*<\/p>`



### 10. Remove Copyright
DotAll = ON

Find:

`<p class="(?:c|f)[^>]*?>Translated.*?(?:Use\.|Domain)<\/p>`



### 11. Remove Brackets on Endnotes
DotAll = OFF

Find:

`<sup>.*?)\[(.*?)\](.*?<\/sup>`

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
