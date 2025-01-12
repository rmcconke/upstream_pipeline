#!/bin/bash

for case in case_0p5 case_0p8 case_1p0 case_1p2 case_1p5
do
    echo $case
    ./phll_RANS_single.sh $case &
    ./phll_DNS_single.sh $case &
    sleep 10
done



