#!/usr/bin/env bash

#set base and scripts directories
SCRIPTDIR=$(dirname "$0")
BASEDIR="$(dirname "$SCRIPTDIR")"

# change to BASEDIR
cd ..

# for every clafer file in clafer_models directory
for f in *.cfr
do
    #set variables and make sure in correct directory
    cd $BASEDIR
    counter=0
    flag=-1

    # Create design space tree images if none exist
    filename="${f%.*}"
    if [ ! -e $filename.dot.png ]; then
        clafer $f -m cvlgraph
        echo 'Creating design space tree image...'
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
    echo "Building clafer instances, this may take some time."
    echo "    Space limited to 1000 instances."
    echo ""
    claferig $f --all=1000 --savedir=$BASEDIR"/"$filename"/""Instances"
    if [ ! "$counter"=0 ]; then
        python $SCRIPTDIR/rename_instances.py $BASEDIR"/"$filename"/""Instances" $counter
    fi

    # clean up clafer instance, rename it, and delete old instance
    python $SCRIPTDIR/cl_abstract.py $f $filename
    cd $BASEDIR"/"$filename
    for csv_file in *.csv
    do
        csv=$csv_file
    done
    echo "Cleaning up clafer instances..."
    echo ""
    python $SCRIPTDIR/clean_clinstance.py $BASEDIR"/"$filename"/""Instances"

    # generate XML from instance
    echo 'Creating .ork files'
    echo ""
    #python $SCRIPTDIR/editXMLXYZ.py $BASEDIR"/"$filename"/""Instances"

done
echo 'Completed execution'
$SHELL
