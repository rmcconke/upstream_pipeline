#!/bin/bash


for case in convdiv12600 convdiv20580
do
    echo $case
    ./RANS_single_cndv.sh $case 
done

for case in h20 h26 h31 h38 h42
do
    echo $case
    ./RANS_single_bump.sh $case 
done

for case in cbfs13700
do
    echo $case
    ./RANS_single_cbfs.sh $case 
done




./raw_to_numpy_and_interpolate.sh
