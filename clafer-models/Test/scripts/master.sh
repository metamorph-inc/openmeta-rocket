#!/usr/bin/env bash
cd ..
for datafiles in *.cfr.data
do
    filename="${datafiles%.*}"
    python scripts/data2instances.py $datafiles

    cd ${filename%.*}/Instances
    for instancefiles in *.txt
    do
        python ../../scripts/newInstance2XML.py $instancefiles
    done

done
$SHELL
