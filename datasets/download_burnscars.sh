#!/bin/bash

# get directory with data
data_dir="${DATA_DIR:-data}"
mkdir $data_dir
cd $data_dir || exit

# Download data
mkdir HLSBurnScars
wget https://huggingface.co/datasets/ibm-nasa-geospatial/hls_burn_scars/resolve/main/hls_burn_scars.tar.gz
tar -xvzf hls_burn_scars.tar.gz -C HLSBurnScars
rm hls_burn_scars.tar.gz
