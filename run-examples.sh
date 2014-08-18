#!/bin/bash

here=`dirname $0`

set -e # error out of the loop of rat.py dies anywhere

for report in "$here/examples/"*; do
    echo "Evaluating $report..."
    $here/rat.py "$report"
    echo
done
