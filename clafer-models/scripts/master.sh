#!/usr/bin/env bash

SCRIPTDIR=$(dirname "$0")
BASEDIR="$(dirname "$SCRIPTDIR")"

cd ..

for f in *.cfr
do
    cd $BASEDIR
    counter=0
    flag=-1
    # Create design space tree images if none exist
    filename="${f%.*}"
    if [ ! -e $filename.dot.png ]; then
        clafer $f -m cvlgraph
        python scripts/remove_constraints.py $filename.cvl.dot
        dot ${filename}_removed.cvl.dot -Tpng -o ${filename}.dot.png
        rm -r *.cvl.dot
    fi


    #Create clafer instances folders
    orig_filename=$filename
    while [ "$flag" -lt 0 ]; do
        if [ -d $BASEDIR"/"$filename ]; then
            let counter+=1
            filename=$orig_filename$counter
        else
            if [ ! "$counter"=0 ]; then
                filename=$orig_filename$counter
            fi
            mkdir -p $BASEDIR"/"$filename
            mkdir -p $BASEDIR"/"$filename"/""Instances"
            mkdir -p $BASEDIR"/"$filename"/""XML"
            flag=1
        fi
    done
    #Generate clafer instances
    claferig $f --all=10000 --savedir=$BASEDIR"/"$filename"/""Instances"
    if [ ! "$counter"=0 ]; then
        python $SCRIPTDIR/rename_instances.py $BASEDIR"/"$filename"/""Instances" $counter
    fi
    python $SCRIPTDIR/cl_abstract.py $f
    cd $BASEDIR"/"$filename"/""Instances"
    # clean up clafer instance, rename it, and delete old instance
    for datafiles in *.data
    do
        python $SCRIPTDIR/clean_clinstance.py $datafiles $counter $csv
    done
        # generate XML from instance
        #python $SCRIPTDIR/editXMLXYZ.py $BASEDIR"/"$filename"/""Instances"

done
$SHELL
