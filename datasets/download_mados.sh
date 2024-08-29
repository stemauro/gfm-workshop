#!/bin/bash

# get directory with data
data_dir="${DATA_DIR:-data}"
mkdir $data_dir
cd $data_dir || exit

# Download data
wget https://zenodo.org/records/10664073/files/MADOS.zip
unzip MADOS.zip

# Remove zip
rm MADOS.zip
