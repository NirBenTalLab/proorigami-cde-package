#!/bin/bash
while read -r line || [[ -n "$line" ]]; do
    uid=`echo $line | awk -F',' '{print $2}'`
    if [ -n "$uid" ]; then
        x_group=`awk -F'\t' "/$uid/ { print \\\$10 }" ~/Downloads/ecod.develop111.domains.txt`
       domain_id=`awk -F'\t' "/$uid/ { print \\\$2 }" ~/Downloads/ecod.develop111.domains.txt`
	echo $domain_id
        echo $x_group
	new_line="${x_group},${domain_id},${line}"
	echo $new_line >> ./tmp.csv
    	echo "Text read from file: ${line}"
	echo $uid
    fi
done < "$1"
