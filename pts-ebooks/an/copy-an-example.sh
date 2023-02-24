#!/bin/bash

# make executable using `chmod +x FILENAME.sh` then run using `./FILENAME.sh`

# modify these to match your particular file system
source_dir=~/buddhadust/dhamma-vinaya/pts/an/
dest_dir=~/buddhadust/pts-ebooks/an/AN-all/

# rm -rf "$dest_dir/*" #Remove the contents of DESTINATION
cp -r "$source_dir"/01_ones/* "$dest_dir" #Copy the contents of SRC into DESTINATION
cp -r "$source_dir"/02_twos/* "$dest_dir" #Copy the contents of SRC into DESTINATION
cp -r "$source_dir"/03_threes/* "$dest_dir" #Copy the contents of SRC into DESTINATION
cp -r "$source_dir"/04_fours/* "$dest_dir" #Copy the contents of SRC into DESTINATION
cp -r "$source_dir"/05_fives/* "$dest_dir" #Copy the contents of SRC into DESTINATION
cp -r "$source_dir"/06_sixes/* "$dest_dir" #Copy the contents of SRC into DESTINATION
cp -r "$source_dir"/07_sevens/* "$dest_dir" #Copy the contents of SRC into DESTINATION
cp -r "$source_dir"/08_eights/* "$dest_dir" #Copy the contents of SRC into DESTINATION
cp -r "$source_dir"/09_nines/* "$dest_dir" #Copy the contents of SRC into DESTINATION
cp -r "$source_dir"/10_tens/* "$dest_dir" #Copy the contents of SRC into DESTINATION
cp -r "$source_dir"/11_elevens/* "$dest_dir" #Copy the contents of SRC into DESTINATION
