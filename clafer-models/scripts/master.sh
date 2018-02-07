#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
#echo $BASEDIR
cd ..

# Create design space tree images if none exist
for f in *.cfr
do
    filename="${f%.*}"
    if [ ! -e $filename.dot.png ]
    then
        clafer $f -m cvlgraph
        python scripts/remove_constraints.py $filename.cvl.dot
        dot ${filename}_removed.cvl.dot -Tpng -o ${filename}.dot.png
        rm -r *.cvl.dot
    fi
done

# 
for datafiles in *.cfr.data
do
    filename="${datafiles%.*}"
    python scripts/data2instances.py $datafiles

    path="$PWD""/""${filename%.*}"
    python scripts/editXML.py $path $BASEDIR

done
$SHELL
