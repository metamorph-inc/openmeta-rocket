#!/usr/bin/env bash

for f in *.cfr
do
    filename="${f%.*}"
    clafer $f -m cvlgraph
    python remove_constraints.py $filename.cvl.dot
    dot ${filename}_removed.cvl.dot -Tpng -o ${filename}_removed.dot.png
done
