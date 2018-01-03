#!/usr/bin/env bash

for f in *.cfr
do
    filename="${f%.*}"
    ./clafer $f -m cvlgraph
    perl -pi -e 's/rankdir=BT/rankdir=RL/g' $filename.cvl.dot
    dot $filename.cvl.dot -Tpng -o $filename.cvl.dot.png
done