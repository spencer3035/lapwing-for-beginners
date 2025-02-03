#/usr/bin/env bash

dir=$(dirname ${BASH_SOURCE[0]} | xargs realpath)
practice_dir="src/practice/"

cd "$dir/$practice_dir"

for file in *.txt; do 
    # 'sed' removes leading and trailing whitespace, and deletes empty lines
    # 'sort | uniq' both sort and clean up possible duplicate entries
    sorted_string=$(cat $file | sed 's/^ *//; s/ *$//; s/\s*/\t/; /^$/d' | sort | uniq)
    # This needs to be done as a separate step because of how pipes work
    echo "$sorted_string" > $file
done
