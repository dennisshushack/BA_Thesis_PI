#!/bin/bash

# Creates random files in the directory /home/electrosense
cd /home/electrosense
mkdir random_data
cd random_data
mkdir random_data_big
mkdir random_data_small
cd random_data_big
seq -w 1 $(shuf -i8-15 -n1)  | xargs -n1 -I% sh -c 'dd if=/dev/urandom of=file.% bs=$(shuf -i10000-60000 -n1) count=1024'
cd ..
cd random_data_small
seq -w 1 $(shuf -i100-500 -n1)  | xargs -n1 -I% sh -c 'dd if=/dev/urandom of=file.% bs=$(shuf -i1-10 -n1) count=1024'
