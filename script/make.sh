#!/bin/bash

# need to input destination file name

path=$(cd "$(dirname "$0")";pwd)
father_path=$(dirname $path)

source_path=$father_path"/data/"
destination_path=$father_path"/qos_policy/"$1"/"

source_file=$father_path"/data/c_read_csv_test.c"
destination_file=$father_path"/qos_policy/"$1"/"$1".out"

source_sh_pir_file=$source_path"sh_pir.csv"
destination_sh_pir_file=$destination_path"sh_pir.csv"

echo "ready to compile..."
echo "finding destination path..."
if [ ! -x "$destination_path" ]; then 
    echo "does not exist, make new path:"
    echo "$destination_path"
    mkdir "$destination_path"  
fi

gcc $source_file -std=c99 -o $destination_file

echo "obtain new file:"
echo "$destination_file"

cp -f "$source_sh_pir_file" "$destination_sh_pir_file"
echo "copy $source_sh_pir_file to $destination_sh_pir_file"

echo "done"
# echo "$source_file"

# echo "$destination_file"
