# How to Run a Batch of Spelling Corrections

* Assuming a directory `dir/` filled with HTML or XML files


#### 1. Prepare a file with each line being one misspelling

`wordlist.txt`

```
accomphshment
acoount
aham
ahns-round
aimsfood
```

#### 2. Prepare another file, with each line being a string replacement

This can be done easily using Sublime Text, Regex, or by merging columns in a spreadsheet editor. A template ODS file is available in this directory.

`sedfile.txt`

```
s/accomphshment/accomplishment/g
s/acoount/account/g
s/aham/ahaṁ/g
s/ahns-round/alms-round/g
s/aimsfood/almsfood/g
```

#### 3. Run Terminal Command

OS X: `grep -rl -Ff wordlist.txt dir/ | xargs sed -f sedfile.txt -i ''`

Linux?: `grep -rl -Ff wordlist.txt dir/ | xargs sed -f sedfile.txt -i`

