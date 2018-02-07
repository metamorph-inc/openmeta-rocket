#!/usr/bin/env bash

SCRIPTDIR=$(dirname "$0")
BASEDIR="$(dirname "$SCRIPTDIR")"

cd ..

for f in *.cfr
do
    cd $BASEDIR
    # Create design space tree images if none exist
    filename="${f%.*}"
    if [ ! -e $filename.dot.png ]; then
        clafer $f -m cvlgraph
        python scripts/remove_constraints.py $filename.cvl.dot
        dot ${filename}_removed.cvl.dot -Tpng -o ${filename}.dot.png
        rm -r *.cvl.dot
    fi

    #Create clafer instances from clafer design space
    if [ ! -d $BASEDIR"/"$filename ]; then
        mkdir -p $BASEDIR"/"$filename
        mkdir -p $BASEDIR"/"$filename"/""Instances"
        mkdir -p $BASEDIR"/"$filename"/""XML"
    fi
    claferig $f --all=10000 --savedir=$BASEDIR"/"$filename"/""Instances"

    cd $BASEDIR"/"$filename"/""Instances"
    for datafiles in *.data
    do
        python $SCRIPTDIR/clean_clinstance.py $datafiles
    done
        python $SCRIPTDIR/editXML.py $BASEDIR"/"$filename"/""Instances"


done

$SHELL
