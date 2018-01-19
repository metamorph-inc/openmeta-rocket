#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
#echo $BASEDIR
cd ..
for datafiles in *.cfr.data
do
    filename="${datafiles%.*}"
    python scripts/data2instances.py $datafiles

    path="$PWD""/""${filename%.*}"
    python scripts/invert_editXML.py $path $BASEDIR/..

done
$SHELL
