#!/bin/bash

sel=${1-3}

i=0
for fv in $(find /var/www/html/fire/data_furg-fire-dataset -name '*.mp4'); do

    dir=$(dirname "$fv")
    bn=$(basename "$fv" '.mp4')
    xml="$dir/$bn.xml"

    i=$(( i + 1 ))


#    if [ "$i" -ne "$sel" ]; then
#        continue
#    fi

    ./show_furg.py --video "$fv" --xml "$xml"
    sleep 1
done
