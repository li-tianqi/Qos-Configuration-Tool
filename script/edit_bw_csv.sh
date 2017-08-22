#!/bin/bash

path=$(cd "$(dirname "$0")";pwd)
father_path=$(dirname $path)

file_path=$father_path"/test_data/bandwidth.csv"
#echo $file_path
vim $file_path